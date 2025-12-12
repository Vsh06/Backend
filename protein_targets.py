"""
Protein targets database for common drugs.
Contains known drug-target interactions with confidence scores and explanations.
"""

PROTEIN_TARGETS = {
    "Aspirin": [
        {
            "name": "COX-1",
            "confidence": 95,
            "mechanism": "Irreversible inhibition",
            "explanation": "COX-1 produces prostaglandins that protect the stomach lining and support blood clotting. Aspirin permanently blocks this enzyme, reducing pain and inflammation but may cause stomach irritation."
        },
        {
            "name": "COX-2",
            "confidence": 90,
            "mechanism": "Irreversible inhibition",
            "explanation": "COX-2 is activated during inflammation and produces prostaglandins that cause pain and swelling. Aspirin blocks this enzyme to reduce fever, pain, and inflammation."
        },
        {
            "name": "TXA2 synthase",
            "confidence": 85,
            "mechanism": "Inhibition",
            "explanation": "This enzyme produces thromboxane A2, which promotes blood clot formation. Aspirin reduces heart attack risk by inhibiting this pathway."
        }
    ],
    "Ibuprofen": [
        {
            "name": "COX-1",
            "confidence": 88,
            "mechanism": "Reversible inhibition",
            "explanation": "COX-1 produces protective prostaglandins for stomach lining. Ibuprofen temporarily blocks this enzyme, reducing pain but with less stomach risk than aspirin."
        },
        {
            "name": "COX-2",
            "confidence": 92,
            "mechanism": "Reversible inhibition",
            "explanation": "COX-2 causes inflammation and pain during injury. Ibuprofen preferentially blocks this enzyme to reduce swelling, pain, and fever."
        },
        {
            "name": "NF-κB",
            "confidence": 75,
            "mechanism": "Inhibition",
            "explanation": "NF-κB is a protein that activates inflammation genes. Ibuprofen reduces inflammation by interfering with this signaling pathway."
        }
    ],
    "Acetaminophen": [
        {
            "name": "COX-1",
            "confidence": 70,
            "mechanism": "Weak inhibition",
            "explanation": "COX-1 produces prostaglandins in the brain. Acetaminophen weakly blocks this enzyme to reduce fever and pain without much stomach irritation."
        },
        {
            "name": "COX-2",
            "confidence": 65,
            "mechanism": "Weak inhibition",
            "explanation": "COX-2 contributes to pain and fever. Acetaminophen has minimal effect on this enzyme compared to NSAIDs."
        },
        {
            "name": "COX-3",
            "confidence": 80,
            "mechanism": "Selective inhibition",
            "explanation": "COX-3 is a brain-specific enzyme involved in pain and fever. Acetaminophen selectively targets this enzyme for pain relief."
        }
    ],
    "Paracetamol": [
        {
            "name": "COX-1",
            "confidence": 70,
            "mechanism": "Weak inhibition",
            "explanation": "COX-1 produces prostaglandins in the brain. Paracetamol weakly blocks this enzyme to reduce fever and pain without much stomach irritation."
        },
        {
            "name": "COX-2",
            "confidence": 65,
            "mechanism": "Weak inhibition",
            "explanation": "COX-2 contributes to pain and fever. Paracetamol has minimal effect on this enzyme compared to NSAIDs."
        },
        {
            "name": "COX-3",
            "confidence": 80,
            "mechanism": "Selective inhibition",
            "explanation": "COX-3 is a brain-specific enzyme involved in pain and fever. Paracetamol selectively targets this enzyme for pain relief."
        }
    ],
    "Amoxicillin": [
        {
            "name": "PBP1A",
            "confidence": 90,
            "mechanism": "Inhibition",
            "explanation": "Penicillin-binding protein 1A is essential for bacterial cell wall synthesis. Amoxicillin binds to this protein, weakening bacterial cell walls."
        },
        {
            "name": "PBP1B",
            "confidence": 85,
            "mechanism": "Inhibition",
            "explanation": "PBP1B helps bacteria build strong cell walls. Amoxicillin inhibits this protein, making bacteria vulnerable to immune system attack."
        },
        {
            "name": "PBP2",
            "confidence": 80,
            "mechanism": "Inhibition",
            "explanation": "This penicillin-binding protein maintains bacterial cell wall integrity. Amoxicillin disrupts this protein's function to kill bacteria."
        }
    ],
    "Omeprazole": [
        {
            "name": "H+/K+ ATPase",
            "confidence": 95,
            "mechanism": "Irreversible inhibition",
            "explanation": "This proton pump moves acid into the stomach. Omeprazole permanently blocks it, reducing stomach acid production for heartburn relief."
        },
        {
            "name": "CYP2C19",
            "confidence": 75,
            "mechanism": "Metabolism",
            "explanation": "CYP2C19 is an enzyme that breaks down omeprazole. Genetic variations affect how well the drug works."
        }
    ],
    "Simvastatin": [
        {
            "name": "HMGCS1",
            "confidence": 90,
            "mechanism": "Inhibition",
            "explanation": "HMGCS1 starts cholesterol production in the liver. Simvastatin blocks this enzyme to lower cholesterol levels."
        },
        {
            "name": "HMGCS2",
            "confidence": 85,
            "mechanism": "Inhibition",
            "explanation": "HMGCS2 regulates ketone body production. Simvastatin inhibits this enzyme as part of its cholesterol-lowering mechanism."
        },
        {
            "name": "LDL receptor",
            "confidence": 80,
            "mechanism": "Upregulation",
            "explanation": "LDL receptors remove cholesterol from blood. Simvastatin increases these receptors to improve cholesterol clearance."
        }
    ],
    "Amlodipine": [
        {
            "name": "CACNA1C",
            "confidence": 90,
            "mechanism": "Blockade",
            "explanation": "CACNA1C forms calcium channels in heart and blood vessels. Amlodipine blocks these channels to relax blood vessels and lower blood pressure."
        },
        {
            "name": "CACNA1D",
            "confidence": 85,
            "mechanism": "Blockade",
            "explanation": "This calcium channel subtype is important in vascular smooth muscle. Amlodipine inhibits it to reduce blood pressure."
        }
    ],
    "Metformin": [
        {
            "name": "AMPK",
            "confidence": 85,
            "mechanism": "Activation",
            "explanation": "AMPK is an energy sensor that regulates metabolism. Metformin activates this protein to improve insulin sensitivity and blood sugar control."
        },
        {
            "name": "mTOR",
            "confidence": 75,
            "mechanism": "Inhibition",
            "explanation": "mTOR controls cell growth and metabolism. Metformin inhibits this pathway to reduce blood sugar and support weight management."
        },
        {
            "name": "Complex I",
            "confidence": 80,
            "mechanism": "Inhibition",
            "explanation": "Complex I is part of the mitochondrial electron transport chain. Metformin mildly inhibits it, affecting energy production and metabolism."
        }
    ]
}

def get_protein_targets(drug_name: str) -> list:
    """
    Get protein targets for a given drug name.

    Args:
        drug_name (str): Name of the drug

    Returns:
        list: List of protein target dictionaries, or empty list if not found
    """
    drug_name_lower = drug_name.lower().strip()

    # Direct match
    if drug_name in PROTEIN_TARGETS:
        return PROTEIN_TARGETS[drug_name]

    # Case-insensitive match
    for key in PROTEIN_TARGETS:
        if key.lower() == drug_name_lower:
            return PROTEIN_TARGETS[key]

    # Fuzzy match for common variations
    if drug_name_lower in ['paracetamol', 'acetaminophen']:
        return PROTEIN_TARGETS.get('Acetaminophen', [])
    elif drug_name_lower in ['aspirin']:
        return PROTEIN_TARGETS.get('Aspirin', [])
    elif drug_name_lower in ['ibuprofen']:
        return PROTEIN_TARGETS.get('Ibuprofen', [])

    return []
