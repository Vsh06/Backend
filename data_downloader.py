import os
import requests
import io
import pandas as pd
import time
import logging
from typing import List, Dict
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PubChemAPI:
    """Handler for PubChem API interactions."""

    BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

    @staticmethod
    def get_compound_properties(cids: List[int], properties: List[str] = None) -> pd.DataFrame:
        """
        Get compound properties from PubChem.

        Args:
            cids: List of compound IDs
            properties: List of properties to fetch (default: basic properties)

        Returns:
            DataFrame with compound properties
        """
        if properties is None:
            properties = ['MolecularFormula', 'MolecularWeight', 'CanonicalSMILES', 'IUPACName']

        property_string = ','.join(properties)
        url = f"{PubChemAPI.BASE_URL}/compound/cid/{','.join(map(str, cids))}/property/{property_string}/CSV"

        try:
            response = requests.get(url)
            response.raise_for_status()
            return pd.read_csv(io.StringIO(response.text))
        except requests.RequestException as e:
            logger.error(f"Error fetching PubChem data: {e}")
            return pd.DataFrame()

    @staticmethod
    def search_compounds_by_name(drug_names: List[str]) -> Dict[str, int]:
        """
        Search for compound CIDs by drug names.

        Args:
            drug_names: List of drug names to search

        Returns:
            Dictionary mapping drug names to CIDs
        """
        name_to_cid = {}
        max_retries = 5
        base_retry_delay = 1  # in seconds

        for name in tqdm(drug_names, desc="Searching PubChem for drug CIDs"):
            for attempt in range(max_retries):
                try:
                    url = f"{PubChemAPI.BASE_URL}/compound/name/{name}/cids/JSON"
                    response = requests.get(url)
                    response.raise_for_status()
                    data = response.json()
                    if 'IdentifierList' in data and 'CID' in data['IdentifierList']:
                        cid = data['IdentifierList']['CID'][0]
                        name_to_cid[name] = cid
                        logger.info(f"Found CID {cid} for {name}")
                    else:
                        logger.warning(f"No CID found for {name}")
                    break  # Success, exit retry loop
                except requests.RequestException as e:
                    if isinstance(e, requests.HTTPError) and e.response.status_code == 503:
                        delay = base_retry_delay * (2 ** attempt)
                        logger.warning(f"Server busy. Retrying for {name} in {delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                        time.sleep(delay)
                    else:
                        logger.error(f"Error searching for {name}: {e}")
                        break # Non-retryable error, exit retry loop
            else: # This else belongs to the for loop, executed if the loop completes without break
                logger.error(f"Failed to retrieve data for {name} after {max_retries} attempts.")

            # Rate limiting after each drug search
            time.sleep(0.2)

        return name_to_cid

class ChEMBLAPI:
    """Handler for ChEMBL API interactions."""

    BASE_URL = "https://www.ebi.ac.uk/chembl/api/data"

    @staticmethod
    def get_drug_indications(limit: int = 1000) -> pd.DataFrame:
        """
        Get drug indications from ChEMBL.

        Args:
            limit: Maximum number of records to fetch

        Returns:
            DataFrame with drug indications
        """
        all_indications = []
        offset = 0
        batch_size = 100

        with tqdm(total=limit, desc="Downloading ChEMBL indications") as pbar:
            while len(all_indications) < limit:
                url = f"{ChEMBLAPI.BASE_URL}/drug_indication.json"
                params = {
                    'limit': min(batch_size, limit - len(all_indications)),
                    'offset': offset
                }

                try:
                    response = requests.get(url, params=params)
                    response.raise_for_status()
                    data = response.json()

                    if not data.get('drug_indications'):
                        break

                    batch_count = len(data['drug_indications'])
                    all_indications.extend(data['drug_indications'])
                    offset += batch_size
                    pbar.update(batch_count)
                    logger.info(f"Fetched {len(all_indications)} drug indications...")

                except requests.RequestException as e:
                    logger.error(f"Error fetching ChEMBL data: {e}")
                    break

                time.sleep(0.1)  # Rate limiting
        return pd.DataFrame(all_indications)

def download_and_integrate_pubchem_data(drug_names: List[str], save_path: str):
    """
    Download and integrate PubChem data for given drug names.

    Args:
        drug_names: List of drug names to fetch data for
        save_path: Path to save the integrated data
    """
    logger.info("Searching for drug CIDs in PubChem...")
    name_to_cid = PubChemAPI.search_compounds_by_name(drug_names)

    if not name_to_cid:
        logger.warning("No compounds found in PubChem")
        return

    cids = list(name_to_cid.values())
    logger.info(f"Fetching properties for {len(cids)} compounds...")

    properties_df = PubChemAPI.get_compound_properties(cids)

    if not properties_df.empty:
        # Add drug names back to the dataframe
        cid_to_name = {v: k for k, v in name_to_cid.items()}
        properties_df['DrugName'] = properties_df['CID'].map(cid_to_name)

        # Reorder columns
        cols = ['DrugName'] + [col for col in properties_df.columns if col != 'DrugName']
        properties_df = properties_df[cols]

        properties_df.to_csv(save_path, index=False)
        logger.info(f"PubChem data saved to {save_path}")
        logger.info(f"Downloaded data for: {', '.join(name_to_cid.keys())}")
    else:
        logger.warning("No property data retrieved from PubChem")

def download_and_integrate_chembl_data(save_path: str):
    """
    Download and integrate ChEMBL drug indication data.

    Args:
        save_path: Path to save the drug indication data
    """
    logger.info("Downloading drug indications from ChEMBL...")
    indications_df = ChEMBLAPI.get_drug_indications(limit=500)

    if not indications_df.empty:
        indications_df.to_csv(save_path, index=False)
        logger.info(f"ChEMBL drug indications saved to {save_path}")
        logger.info(f"Downloaded {len(indications_df)} drug indications")
    else:
        logger.warning("No drug indication data retrieved from ChEMBL")

def create_drug_composition_from_pubchem(pubchem_data_path: str, output_path: str):
    """
    Create drug composition data from PubChem molecular formulas.

    Args:
        pubchem_data_path: Path to PubChem compound data
        output_path: Path to save the composition data
    """
    try:
        # Check if the file is empty or does not exist
        if not os.path.exists(pubchem_data_path) or os.path.getsize(pubchem_data_path) == 0:
            logger.warning(f"PubChem data file is empty or not found: {pubchem_data_path}")
            return

        df = pd.read_csv(pubchem_data_path)

        if df.empty:
            logger.warning("PubChem data file is empty. No composition data to create.")
            return

        composition_data = []
        for _, row in tqdm(df.iterrows(), total=len(df), desc="Processing drug compositions"):
            drug_name = row.get('DrugName', 'Unknown')
            formula = row.get('MolecularFormula', '')

            if formula:
                # Use RDKit to parse molecular formula
                try:
                    mol = Chem.MolFromSmiles(row.get('ConnectivitySMILES', ''))
                    if mol:
                        formula_rdkit = rdMolDescriptors.CalcMolFormula(mol)
                        # Parse formula_rdkit to elements and counts
                        from collections import Counter
                        import re
                        element_pattern = r'([A-Z][a-z]?)(\d*)'
                        elements = re.findall(element_pattern, formula_rdkit)
                        element_counts = Counter()
                        for element, count in elements:
                            count = int(count) if count else 1
                            element_counts[element] += count

                        for element, count in element_counts.items():
                            composition_data.append({
                                'Drug': drug_name,
                                'Component': element,
                                'Amount(mg)': count  # Using count as a proxy for amount
                            })
                    else:
                        logger.warning(f"RDKit failed to parse SMILES for {drug_name}")
                except Exception as e:
                    logger.error(f"Error parsing molecular formula for {drug_name}: {e}")

        if composition_data:
            composition_df = pd.DataFrame(composition_data)
            composition_df.to_csv(output_path, index=False)
            logger.info(f"Drug composition data created at {output_path}")
        else:
            logger.warning("No composition data could be extracted")

    except Exception as e:
        logger.error(f"Error creating composition data: {e}")

def process_custom_drug_list(drug_names: List[str], pubchem_path: str = None, composition_path: str = None, chembl_path: str = None):
    """
    Process a custom list of drug names: download data and create composition.

    Args:
        drug_names: List of drug names to process
        pubchem_path: Path to save PubChem data (optional, defaults to standard path)
        composition_path: Path to save composition data (optional, defaults to standard path)
        chembl_path: Path to save ChEMBL data (optional, defaults to standard path)
    """
    if pubchem_path is None:
        pubchem_path = "Backend/Repurposing/Data/pubchem_compounds.csv"
    if composition_path is None:
        composition_path = "Backend/composition/Data/drug_composition.csv"
    if chembl_path is None:
        chembl_path = "Backend/Repurposing/Data/chembl_indications.csv"

    # Create data directories
    os.makedirs(os.path.dirname(pubchem_path), exist_ok=True)
    os.makedirs(os.path.dirname(composition_path), exist_ok=True)
    os.makedirs(os.path.dirname(chembl_path), exist_ok=True)

    # Download PubChem data for custom drugs
    download_and_integrate_pubchem_data(drug_names, pubchem_path)

    # Create composition data from PubChem
    create_drug_composition_from_pubchem(pubchem_path, composition_path)

    # Note: ChEMBL data is general and not drug-specific, so we don't re-download it for custom lists
    # But we can optionally update it if needed
    # download_and_integrate_chembl_data(chembl_path)

    return {
        "pubchem_path": pubchem_path,
        "composition_path": composition_path,
        "processed_drugs": drug_names
    }

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download and process drug data from PubChem and ChEMBL.")
    parser.add_argument('--drugs', nargs='+', default=[
        'Aspirin', 'Paracetamol', 'Ibuprofen', 'Amoxicillin',
        'Omeprazole', 'Simvastatin', 'Amlodipine', 'Metformin'
    ], help='List of drug names to fetch data for')
    parser.add_argument('--pubchem_path', default="Backend/Repurposing/Data/pubchem_compounds.csv", help='Path to save PubChem data')
    parser.add_argument('--composition_path', default="Backend/composition/Data/drug_composition.csv", help='Path to save drug composition data')
    parser.add_argument('--chembl_path', default="Backend/Repurposing/Data/chembl_indications.csv", help='Path to save ChEMBL drug indications')

    args = parser.parse_args()

    # Use the new function for consistency
    result = process_custom_drug_list(args.drugs, args.pubchem_path, args.composition_path, args.chembl_path)
    logger.info(f"Processing completed: {result}")
