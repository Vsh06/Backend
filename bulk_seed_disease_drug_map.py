#!/usr/bin/env python3
"""
Bulk seeding script to populate the disease_drug_map table with real biomedical data.
Fetches data from DrugBank, ChEMBL, PubChem, and DisGeNET APIs to create comprehensive
disease-drug mappings for drug repurposing.

Usage:
    python bulk_seed_disease_drug_map.py [--limit N] [--sources SOURCE1,SOURCE2] [--diseases DISEASE1,DISEASE2]

Arguments:
    --limit: Maximum number of mappings to fetch per source (default: 1000)
    --sources: Comma-separated list of sources to use (default: all)
    --diseases: Comma-separated list of diseases to focus on (default: common diseases)
"""

import sys
import os
import json
import asyncio
import logging
import argparse
from typing import List, Dict, Optional, Set
from dataclasses import dataclass
from datetime import datetime, UTC
import re

sys.path.insert(0, os.path.dirname(__file__))

import aiohttp
import httpx
from models import db, DiseaseDrugMap
from app import app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bulk_seed.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class DrugData:
    """Data structure for drug information."""
    name: str
    chemical_formula: Optional[str] = None
    molecular_weight: Optional[float] = None
    iupac_name: Optional[str] = None
    synonyms: List[str] = None
    protein_targets: List[str] = None
    market_names: List[str] = None
    mechanism_of_action: Optional[str] = None
    source: str = "Unknown"

    def __post_init__(self):
        if self.synonyms is None:
            self.synonyms = []
        if self.protein_targets is None:
            self.protein_targets = []
        if self.market_names is None:
            self.market_names = []

@dataclass
class DiseaseData:
    """Data structure for disease information."""
    name: str
    synonyms: List[str] = None
    mesh_id: Optional[str] = None
    omim_id: Optional[str] = None

    def __post_init__(self):
        if self.synonyms is None:
            self.synonyms = []

class PubChemClient:
    """Client for PubChem REST API."""

    BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def get_compound_by_name(self, name: str) -> Optional[DrugData]:
        """Fetch compound data by name."""
        try:
            # First get CID
            url = f"{self.BASE_URL}/compound/name/{name}/cids/JSON"
            async with self.session.get(url) as response:
                if response.status != 200:
                    return None
                data = await response.json()
                cids = data.get('IdentifierList', {}).get('CID', [])
                if not cids:
                    return None
                cid = cids[0]

            # Get compound properties
            url = f"{self.BASE_URL}/compound/cid/{cid}/property/MolecularFormula,MolecularWeight,IUPACName,Title/JSON"
            async with self.session.get(url) as response:
                if response.status != 200:
                    return None
                data = await response.json()

                properties = data.get('PropertyTable', {}).get('Properties', [{}])[0]

                return DrugData(
                    name=name,
                    chemical_formula=properties.get('MolecularFormula'),
                    molecular_weight=properties.get('MolecularWeight'),
                    iupac_name=properties.get('IUPACName'),
                    synonyms=[properties.get('Title', '')],
                    source="PubChem"
                )
        except Exception as e:
            logger.error(f"Error fetching PubChem data for {name}: {e}")
            return None

class ChEMBLClient:
    """Client for ChEMBL API."""

    BASE_URL = "https://www.ebi.ac.uk/chembl/api/data"

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def get_drug_indications(self, limit: int = 1000) -> List[Dict]:
        """Fetch drug indications from ChEMBL."""
        try:
            url = f"{self.BASE_URL}/drug_indication.json?limit={limit}"
            async with self.session.get(url) as response:
                if response.status != 200:
                    return []
                data = await response.json()
                return data.get('drug_indications', [])
        except Exception as e:
            logger.error(f"Error fetching ChEMBL indications: {e}")
            return []

    async def get_molecule_data(self, chembl_id: str) -> Optional[DrugData]:
        """Fetch molecule data by ChEMBL ID."""
        try:
            url = f"{self.BASE_URL}/molecule/{chembl_id}.json"
            async with self.session.get(url) as response:
                if response.status != 200:
                    return None
                data = await response.json()
                molecule = data.get('molecule')

                if not molecule:
                    return None

                return DrugData(
                    name=molecule.get('pref_name', ''),
                    chemical_formula=molecule.get('full_molformula'),
                    molecular_weight=molecule.get('mw_freebase'),
                    synonyms=[molecule.get('pref_name', '')],
                    source="ChEMBL"
                )
        except Exception as e:
            logger.error(f"Error fetching ChEMBL molecule {chembl_id}: {e}")
            return None

class DrugBankClient:
    """Client for DrugBank (requires API key)."""

    BASE_URL = "https://api.drugbank.com/v1"

    def __init__(self, session: aiohttp.ClientSession, api_key: Optional[str] = None):
        self.session = session
        self.api_key = api_key or os.getenv('DRUGBANK_API_KEY')

    async def get_drug_data(self, drug_name: str) -> Optional[DrugData]:
        """Fetch drug data from DrugBank."""
        if not self.api_key:
            logger.warning("DrugBank API key not provided, skipping")
            return None

        try:
            headers = {'Authorization': f'Bearer {self.api_key}'}
            url = f"{self.BASE_URL}/drugs/search.json?name={drug_name}"

            async with self.session.get(url, headers=headers) as response:
                if response.status != 200:
                    return None
                data = await response.json()
                drugs = data.get('drugs', [])
                if not drugs:
                    return None

                drug = drugs[0]  # Take first match

                return DrugData(
                    name=drug.get('name', ''),
                    chemical_formula=drug.get('formula'),
                    molecular_weight=drug.get('weight', {}).get('average'),
                    synonyms=drug.get('synonyms', []),
                    protein_targets=[t.get('name', '') for t in drug.get('targets', [])],
                    market_names=drug.get('products', []),
                    mechanism_of_action=drug.get('mechanism_of_action'),
                    source="DrugBank"
                )
        except Exception as e:
            logger.error(f"Error fetching DrugBank data for {drug_name}: {e}")
            return None

class DisGeNETClient:
    """Client for DisGeNET API."""

    BASE_URL = "https://www.disgenet.org/api"

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def get_disease_drug_associations(self, limit: int = 1000) -> List[Dict]:
        """Fetch disease-drug associations from DisGeNET."""
        try:
            url = f"{self.BASE_URL}/dda/gene_disease_drug_association.json?limit={limit}"
            async with self.session.get(url) as response:
                if response.status != 200:
                    return []
                data = await response.json()
                return data
        except Exception as e:
            logger.error(f"Error fetching DisGeNET associations: {e}")
            return []

class DataValidator:
    """Validates and normalizes data."""

    @staticmethod
    def normalize_disease_name(name: str) -> str:
        """Normalize disease names."""
        if not name:
            return ""

        # Common normalizations
        normalizations = {
            r'p\.?c\.?o\.?d\.?': 'PCOD',
            r'p\.?c\.?o\.?s\.?': 'PCOS',
            r'polycystic ovarian syndrome': 'PCOS',
            r'polycystic ovary syndrome': 'PCOS',
            r'diabetes mellitus': 'Diabetes',
            r'hypertension': 'Hypertension',
            r'asthma': 'Asthma',
            r'hiv': 'HIV',
            r'aids': 'HIV',
            r'cancer': 'Cancer',
            r'fever': 'Fever',
            r'migraine': 'Migraine',
            r'arthritis': 'Arthritis',
            r'acne': 'Acne',
            r'depression': 'Depression',
            r'anxiety': 'Anxiety'
        }

        name_lower = name.lower().strip()
        for pattern, replacement in normalizations.items():
            if re.search(pattern, name_lower, re.IGNORECASE):
                return replacement

        return name.strip().title()

    @staticmethod
    def validate_confidence_score(score: float) -> float:
        """Ensure confidence score is between 0 and 100."""
        return max(0.0, min(100.0, score))

    @staticmethod
    def clean_list(data: List) -> List:
        """Clean list data."""
        if not data:
            return []
        return [item for item in data if item and str(item).strip()]

class BulkSeeder:
    """Main bulk seeding class."""

    def __init__(self, sources: List[str] = None):
        self.sources = sources or ['pubchem', 'chembl', 'drugbank', 'disgenet']
        self.processed_mappings: Set[str] = set()
        self.stats = {
            'total_processed': 0,
            'successful_inserts': 0,
            'duplicates_skipped': 0,
            'errors': 0
        }

    async def run(self, limit: int = 1000, diseases: List[str] = None) -> None:
        """Run the bulk seeding process."""
        logger.info(f"Starting bulk seeding with sources: {self.sources}")

        async with aiohttp.ClientSession() as session:
            clients = {
                'pubchem': PubChemClient(session),
                'chembl': ChEMBLClient(session),
                'drugbank': DrugBankClient(session),
                'disgenet': DisGeNETClient(session)
            }

            # Collect data from all sources
            all_mappings = []

            if 'chembl' in self.sources:
                logger.info("Fetching data from ChEMBL...")
                chembl_data = await clients['chembl'].get_drug_indications(limit)
                all_mappings.extend(self._process_chembl_data(chembl_data))

            if 'disgenet' in self.sources:
                logger.info("Fetching data from DisGeNET...")
                disgenet_data = await clients['disgenet'].get_disease_drug_associations(limit)
                all_mappings.extend(self._process_disgenet_data(disgenet_data))

            # Filter by diseases if specified
            if diseases:
                diseases_normalized = [DataValidator.normalize_disease_name(d) for d in diseases]
                all_mappings = [m for m in all_mappings if m['disease_name'] in diseases_normalized]

            # Remove duplicates and validate
            unique_mappings = self._deduplicate_mappings(all_mappings)

            # Enrich with additional drug data
            enriched_mappings = await self._enrich_drug_data(unique_mappings, clients)

            # Insert into database
            await self._insert_mappings(enriched_mappings)

            logger.info(f"Bulk seeding completed. Stats: {self.stats}")

    def _process_chembl_data(self, data: List[Dict]) -> List[Dict]:
        """Process ChEMBL drug indication data."""
        mappings = []
        for item in data:
            try:
                disease_name = DataValidator.normalize_disease_name(item.get('mesh_heading', ''))
                if not disease_name:
                    continue

                drug_name = item.get('molecule_chembl_id', '')
                if not drug_name:
                    continue

                # Determine confidence based on max_phase_for_ind
                max_phase = item.get('max_phase_for_ind', 0)
                confidence_map = {0: 10, 1: 30, 2: 60, 3: 80, 4: 95}
                confidence = confidence_map.get(max_phase, 50)

                mappings.append({
                    'disease_name': disease_name,
                    'drug_name': drug_name,
                    'confidence_score': confidence,
                    'mechanism_of_action': item.get('indication_refs', [{}])[0].get('ref_type', ''),
                    'source': 'ChEMBL'
                })
            except Exception as e:
                logger.error(f"Error processing ChEMBL item: {e}")
                continue

        return mappings

    def _process_disgenet_data(self, data: List[Dict]) -> List[Dict]:
        """Process DisGeNET disease-drug association data."""
        mappings = []
        for item in data:
            try:
                disease_name = DataValidator.normalize_disease_name(item.get('disease_name', ''))
                if not disease_name:
                    continue

                drug_name = item.get('drug_name', '')
                if not drug_name:
                    continue

                # Use score as confidence
                score = float(item.get('score', 0))
                confidence = DataValidator.validate_confidence_score(score * 100)

                mappings.append({
                    'disease_name': disease_name,
                    'drug_name': drug_name,
                    'confidence_score': confidence,
                    'source': 'DisGeNET'
                })
            except Exception as e:
                logger.error(f"Error processing DisGeNET item: {e}")
                continue

        return mappings

    def _deduplicate_mappings(self, mappings: List[Dict]) -> List[Dict]:
        """Remove duplicate mappings."""
        seen = set()
        unique = []

        for mapping in mappings:
            key = (mapping['disease_name'], mapping['drug_name'])
            if key not in seen:
                seen.add(key)
                unique.append(mapping)

        logger.info(f"Removed {len(mappings) - len(unique)} duplicate mappings")
        return unique

    async def _enrich_drug_data(self, mappings: List[Dict], clients: Dict) -> List[Dict]:
        """Enrich mappings with additional drug data."""
        logger.info("Enriching drug data...")

        enriched = []
        for mapping in mappings:
            drug_name = mapping['drug_name']

            # Try to get drug data from various sources
            drug_data = None

            if 'pubchem' in self.sources:
                drug_data = await clients['pubchem'].get_compound_by_name(drug_name)
                if drug_data:
                    mapping.update({
                        'chemical_composition': drug_data.chemical_formula,
                        'molecular_weight': drug_data.molecular_weight,
                        'iupac_name': drug_data.iupac_name,
                        'synonyms': json.dumps(drug_data.synonyms)
                    })

            if not drug_data and 'chembl' in self.sources and drug_name.startswith('CHEMBL'):
                drug_data = await clients['chembl'].get_molecule_data(drug_name)

            if not drug_data and 'drugbank' in self.sources:
                drug_data = await clients['drugbank'].get_drug_data(drug_name)
                if drug_data:
                    mapping.update({
                        'protein_targets': json.dumps(drug_data.protein_targets),
                        'market_names': json.dumps(drug_data.market_names),
                        'mechanism_of_action': drug_data.mechanism_of_action
                    })

            enriched.append(mapping)

        return enriched

    async def _insert_mappings(self, mappings: List[Dict]) -> None:
        """Insert mappings into database."""
        logger.info(f"Inserting {len(mappings)} mappings into database...")

        with app.app_context():
            for mapping in mappings:
                try:
                    self.stats['total_processed'] += 1

                    # Check for existing mapping
                    existing = DiseaseDrugMap.query.filter_by(
                        disease_name=mapping['disease_name'],
                        drug_name=mapping['drug_name']
                    ).first()

                    if existing:
                        self.stats['duplicates_skipped'] += 1
                        continue

                    # Create new mapping
                    disease_drug_map = DiseaseDrugMap(**mapping)
                    db.session.add(disease_drug_map)
                    self.stats['successful_inserts'] += 1

                    # Commit in batches
                    if self.stats['successful_inserts'] % 100 == 0:
                        db.session.commit()
                        logger.info(f"Committed {self.stats['successful_inserts']} mappings")

                except Exception as e:
                    self.stats['errors'] += 1
                    logger.error(f"Error inserting mapping {mapping}: {e}")
                    continue

            # Final commit
            db.session.commit()
            logger.info(f"Final commit completed. Total successful inserts: {self.stats['successful_inserts']}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Bulk seed disease-drug mappings')
    parser.add_argument('--limit', type=int, default=1000,
                       help='Maximum number of mappings to fetch per source')
    parser.add_argument('--sources', type=str,
                       help='Comma-separated list of sources (pubchem,chembl,drugbank,disgenet)')
    parser.add_argument('--diseases', type=str,
                       help='Comma-separated list of diseases to focus on')

    args = parser.parse_args()

    sources = args.sources.split(',') if args.sources else None
    diseases = args.diseases.split(',') if args.diseases else None

    seeder = BulkSeeder(sources)
    asyncio.run(seeder.run(args.limit, diseases))

if __name__ == '__main__':
    main()
