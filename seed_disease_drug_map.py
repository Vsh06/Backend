#!/usr/bin/env python3
"""
Seed script to populate the disease_drug_map table with evidence-based mappings.
This creates the disease-drug relationships needed for proper repurposing functionality.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from models import db, DiseaseDrugMap
from app import app
import json

def seed_disease_drug_mappings():
    """Seed the database with disease-drug mappings."""

    # Evidence-based disease-drug mappings
    mappings = [
        # Diabetes
        {
            'disease_name': 'Diabetes',
            'drug_name': 'Metformin',
            'confidence_score': 95.0,
            'mechanism_of_action': 'Activates AMP-activated protein kinase (AMPK), reduces hepatic glucose production, improves insulin sensitivity',
            'protein_targets': json.dumps(['AMPK', 'mTOR', 'Organic cation transporter 1 (OCT1)']),
            'market_names': json.dumps(['Glucophage', 'Fortamet', 'Riomet', 'Glumetza']),
            'source': 'FDA Approved'
        },
        {
            'disease_name': 'Diabetes',
            'drug_name': 'Glipizide',
            'confidence_score': 90.0,
            'mechanism_of_action': 'Stimulates insulin release from pancreatic beta cells by binding to sulfonylurea receptors',
            'protein_targets': json.dumps(['ATP-sensitive potassium channel', 'Sulfonylurea receptor 1']),
            'market_names': json.dumps(['Glucotrol', 'Glucotrol XL']),
            'source': 'FDA Approved'
        },
        {
            'disease_name': 'Diabetes',
            'drug_name': 'Sitagliptin',
            'confidence_score': 88.0,
            'mechanism_of_action': 'Inhibits dipeptidyl peptidase-4 (DPP-4), increases incretin hormones GLP-1 and GIP',
            'protein_targets': json.dumps(['DPP-4', 'GLP-1 receptor', 'GIP receptor']),
            'market_names': json.dumps(['Januvia', 'Janumet']),
            'source': 'FDA Approved'
        },

        # PCOD/PCOS
        {
            'disease_name': 'PCOD',
            'drug_name': 'Metformin',
            'confidence_score': 85.0,
            'mechanism_of_action': 'Improves insulin sensitivity, reduces ovarian androgen production, restores ovulatory function',
            'protein_targets': json.dumps(['AMPK', 'mTOR', 'Insulin receptor']),
            'market_names': json.dumps(['Glucophage', 'Fortamet', 'Riomet']),
            'source': 'Clinical Evidence'
        },
        {
            'disease_name': 'PCOD',
            'drug_name': 'Clomiphene',
            'confidence_score': 90.0,
            'mechanism_of_action': 'Selective estrogen receptor modulator that stimulates ovulation by increasing GnRH and FSH secretion',
            'protein_targets': json.dumps(['Estrogen receptor alpha', 'Estrogen receptor beta', 'GnRH receptor']),
            'market_names': json.dumps(['Clomid', 'Serophene', 'Milophene']),
            'source': 'FDA Approved'
        },
        {
            'disease_name': 'PCOD',
            'drug_name': 'Letrozole',
            'confidence_score': 82.0,
            'mechanism_of_action': 'Aromatase inhibitor that reduces estrogen production, leading to increased FSH secretion and ovulation',
            'protein_targets': json.dumps(['Aromatase', 'FSH receptor', 'LH receptor']),
            'market_names': json.dumps(['Femara']),
            'source': 'Clinical Evidence'
        },
        {
            'disease_name': 'PCOS',
            'drug_name': 'Metformin',
            'confidence_score': 85.0,
            'mechanism_of_action': 'Improves insulin sensitivity, reduces ovarian androgen production, restores ovulatory function',
            'protein_targets': json.dumps(['AMPK', 'mTOR', 'Insulin receptor']),
            'market_names': json.dumps(['Glucophage', 'Fortamet', 'Riomet']),
            'source': 'Clinical Evidence'
        },
        {
            'disease_name': 'PCOS',
            'drug_name': 'Clomiphene',
            'confidence_score': 90.0,
            'mechanism_of_action': 'Selective estrogen receptor modulator that stimulates ovulation by increasing GnRH and FSH secretion',
            'protein_targets': json.dumps(['Estrogen receptor alpha', 'Estrogen receptor beta', 'GnRH receptor']),
            'market_names': json.dumps(['Clomid', 'Serophene', 'Milophene']),
            'source': 'FDA Approved'
        },

        # Hypertension
        {
            'disease_name': 'Hypertension',
            'drug_name': 'Lisinopril',
            'confidence_score': 92.0,
            'mechanism_of_action': 'ACE inhibitor that prevents conversion of angiotensin I to angiotensin II, reducing vasoconstriction',
            'protein_targets': json.dumps(['Angiotensin-converting enzyme (ACE)', 'Bradykinin receptor']),
            'market_names': json.dumps(['Prinivil', 'Zestril', 'Qbrelis']),
            'source': 'FDA Approved'
        },
        {
            'disease_name': 'Hypertension',
            'drug_name': 'Amlodipine',
            'confidence_score': 90.0,
            'mechanism_of_action': 'Calcium channel blocker that inhibits calcium influx into vascular smooth muscle cells',
            'protein_targets': json.dumps(['Voltage-gated calcium channel', 'L-type calcium channel']),
            'market_names': json.dumps(['Norvasc', 'Katerzia']),
            'source': 'FDA Approved'
        },
        {
            'disease_name': 'Hypertension',
            'drug_name': 'Hydrochlorothiazide',
            'confidence_score': 88.0,
            'mechanism_of_action': 'Thiazide diuretic that inhibits sodium reabsorption in the distal convoluted tubule',
            'protein_targets': json.dumps(['Na-Cl cotransporter (NCC)', 'Sodium-potassium ATPase']),
            'market_names': json.dumps(['Microzide', 'Oretic']),
            'source': 'FDA Approved'
        },

        # Asthma
        {
            'disease_name': 'Asthma',
            'drug_name': 'Albuterol',
            'confidence_score': 95.0,
            'mechanism_of_action': 'Beta-2 adrenergic receptor agonist that causes bronchodilation by relaxing airway smooth muscle',
            'protein_targets': json.dumps(['Beta-2 adrenergic receptor', 'G-protein coupled receptor']),
            'market_names': json.dumps(['Ventolin', 'ProAir', 'Proventil']),
            'source': 'FDA Approved'
        },
        {
            'disease_name': 'Asthma',
            'drug_name': 'Fluticasone',
            'confidence_score': 90.0,
            'mechanism_of_action': 'Corticosteroid that binds to glucocorticoid receptors, reducing inflammation in airways',
            'protein_targets': json.dumps(['Glucocorticoid receptor', 'Histone deacetylase']),
            'market_names': json.dumps(['Flovent', 'Flonase']),
            'source': 'FDA Approved'
        },
        {
            'disease_name': 'Asthma',
            'drug_name': 'Montelukast',
            'confidence_score': 85.0,
            'mechanism_of_action': 'Leukotriene receptor antagonist that blocks cysteinyl leukotriene receptors',
            'protein_targets': json.dumps(['Cysteinyl leukotriene receptor 1', 'Cysteinyl leukotriene receptor 2']),
            'market_names': json.dumps(['Singulair']),
            'source': 'FDA Approved'
        },

        # HIV
        {
            'disease_name': 'HIV',
            'drug_name': 'Efavirenz',
            'confidence_score': 88.0,
            'mechanism_of_action': 'Non-nucleoside reverse transcriptase inhibitor that binds to HIV-1 reverse transcriptase',
            'protein_targets': json.dumps(['HIV-1 reverse transcriptase', 'NNRTI binding pocket']),
            'market_names': json.dumps(['Sustiva', 'Atripla']),
            'source': 'FDA Approved'
        },
        {
            'disease_name': 'HIV',
            'drug_name': 'Tenofovir',
            'confidence_score': 90.0,
            'mechanism_of_action': 'Nucleotide reverse transcriptase inhibitor that competes with natural nucleotides for incorporation',
            'protein_targets': json.dumps(['HIV reverse transcriptase', 'DNA polymerase']),
            'market_names': json.dumps(['Viread', 'Truvada', 'Atripla']),
            'source': 'FDA Approved'
        },

        # Cancer (general)
        {
            'disease_name': 'Cancer',
            'drug_name': 'Doxorubicin',
            'confidence_score': 85.0,
            'mechanism_of_action': 'Anthracycline antibiotic that intercalates DNA and inhibits topoisomerase II',
            'protein_targets': json.dumps(['DNA topoisomerase II', 'DNA intercalation sites']),
            'market_names': json.dumps(['Adriamycin', 'Rubex']),
            'source': 'FDA Approved'
        },
        {
            'disease_name': 'Cancer',
            'drug_name': 'Paclitaxel',
            'confidence_score': 82.0,
            'mechanism_of_action': 'Taxane that stabilizes microtubules, preventing cell division during mitosis',
            'protein_targets': json.dumps(['Beta-tubulin', 'Microtubule assembly']),
            'market_names': json.dumps(['Taxol', 'Abraxane']),
            'source': 'FDA Approved'
        },

        # COVID-19
        {
            'disease_name': 'COVID-19',
            'drug_name': 'Remdesivir',
            'confidence_score': 75.0,
            'mechanism_of_action': 'Nucleotide analog that inhibits viral RNA polymerase, terminating RNA synthesis',
            'protein_targets': json.dumps(['SARS-CoV-2 RNA-dependent RNA polymerase']),
            'market_names': json.dumps(['Veklury']),
            'source': 'Emergency Use Authorization'
        },
        {
            'disease_name': 'COVID-19',
            'drug_name': 'Dexamethasone',
            'confidence_score': 78.0,
            'mechanism_of_action': 'Corticosteroid that reduces inflammation and cytokine storm in severe COVID-19',
            'protein_targets': json.dumps(['Glucocorticoid receptor', 'NF-kappaB pathway']),
            'market_names': json.dumps(['Decadron', 'DexPak']),
            'source': 'Clinical Evidence'
        },

        # Pain and Fever (common conditions)
        {
            'disease_name': 'Fever',
            'drug_name': 'Acetaminophen',
            'confidence_score': 95.0,
            'mechanism_of_action': 'Inhibits cyclooxygenase in the brain, reducing prostaglandin synthesis and fever',
            'protein_targets': json.dumps(['COX-1', 'COX-2', 'COX-3']),
            'market_names': json.dumps(['Tylenol', 'Panadol', 'Calpol']),
            'source': 'FDA Approved'
        },
        {
            'disease_name': 'Fever',
            'drug_name': 'Ibuprofen',
            'confidence_score': 90.0,
            'mechanism_of_action': 'NSAID that inhibits cyclooxygenase enzymes, reducing inflammation and fever',
            'protein_targets': json.dumps(['COX-1', 'COX-2', 'Prostaglandin synthesis']),
            'market_names': json.dumps(['Advil', 'Motrin', 'Nurofen']),
            'source': 'FDA Approved'
        },

        # Migraine
        {
            'disease_name': 'Migraine',
            'drug_name': 'Sumatriptan',
            'confidence_score': 88.0,
            'mechanism_of_action': 'Serotonin receptor agonist that constricts cranial blood vessels and reduces neurogenic inflammation',
            'protein_targets': json.dumps(['5-HT1B receptor', '5-HT1D receptor', '5-HT1F receptor']),
            'market_names': json.dumps(['Imitrex', 'Sumavel', 'Alsuma']),
            'source': 'FDA Approved'
        },

        # Arthritis
        {
            'disease_name': 'Arthritis',
            'drug_name': 'Ibuprofen',
            'confidence_score': 92.0,
            'mechanism_of_action': 'NSAID that inhibits cyclooxygenase, reducing prostaglandin-mediated inflammation and pain',
            'protein_targets': json.dumps(['COX-1', 'COX-2', 'Arachidonic acid pathway']),
            'market_names': json.dumps(['Advil', 'Motrin', 'Nurofen']),
            'source': 'FDA Approved'
        },
        {
            'disease_name': 'Arthritis',
            'drug_name': 'Naproxen',
            'confidence_score': 88.0,
            'mechanism_of_action': 'NSAID with longer half-life that inhibits cyclooxygenase enzymes',
            'protein_targets': json.dumps(['COX-1', 'COX-2', 'Prostaglandin E2 synthesis']),
            'market_names': json.dumps(['Aleve', 'Naprosyn', 'Anaprox']),
            'source': 'FDA Approved'
        },

        # Acne
        {
            'disease_name': 'Acne',
            'drug_name': 'Isotretinoin',
            'confidence_score': 90.0,
            'mechanism_of_action': 'Retinoid that reduces sebum production, prevents comedone formation, and has anti-inflammatory effects',
            'protein_targets': json.dumps(['Retinoic acid receptor', 'Sebaceous gland differentiation']),
            'market_names': json.dumps(['Accutane', 'Claravis', 'Amnesteem']),
            'source': 'FDA Approved'
        },

        # Depression
        {
            'disease_name': 'Depression',
            'drug_name': 'Sertraline',
            'confidence_score': 85.0,
            'mechanism_of_action': 'Selective serotonin reuptake inhibitor that increases serotonin levels in the synaptic cleft',
            'protein_targets': json.dumps(['Serotonin transporter (SERT)', '5-HT receptors']),
            'market_names': json.dumps(['Zoloft', 'Lustral']),
            'source': 'FDA Approved'
        },

        # Anxiety
        {
            'disease_name': 'Anxiety',
            'drug_name': 'Alprazolam',
            'confidence_score': 82.0,
            'mechanism_of_action': 'Benzodiazepine that enhances GABAergic neurotransmission by binding to GABA-A receptors',
            'protein_targets': json.dumps(['GABA-A receptor', 'Benzodiazepine binding site']),
            'market_names': json.dumps(['Xanax', 'Niravam']),
            'source': 'FDA Approved'
        }
    ]

    with app.app_context():
        # Clear existing mappings
        DiseaseDrugMap.query.delete()
        db.session.commit()

        # Add new mappings
        for mapping in mappings:
            disease_drug_map = DiseaseDrugMap(**mapping)
            db.session.add(disease_drug_map)

        db.session.commit()
        print(f"Successfully seeded {len(mappings)} disease-drug mappings")

if __name__ == '__main__':
    seed_disease_drug_mappings()
