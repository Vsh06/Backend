#!/usr/bin/env python3
"""
Script to seed the DrugBrandNames database with initial brand name data.
Run this script to populate the brand names table with common drug brand names.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask
from models import DrugBrandNames, db
import json

def seed_brand_names():
    """Seed the database with brand names for common drugs."""

    # Sample brand name data
    brand_data = [
        {
            'canonical_drug_name': 'Paracetamol',
            'brand_names': ['Tylenol', 'Panadol', 'Calpol', 'Dolo', 'Crocin', 'Feverall'],
            'regions': ['US', 'UK', 'India', 'Global'],
            'source': 'DrugBank'
        },
        {
            'canonical_drug_name': 'Ibuprofen',
            'brand_names': ['Advil', 'Motrin', 'Nurofen', 'Brufen', 'Ibu', 'Actiprofen'],
            'regions': ['US', 'UK', 'Europe', 'Global'],
            'source': 'DrugBank'
        },
        {
            'canonical_drug_name': 'Aspirin',
            'brand_names': ['Bayer Aspirin', 'Ecotrin', 'Bufferin', 'Anacin', 'Excedrin'],
            'regions': ['US', 'Europe', 'Global'],
            'source': 'DrugBank'
        },
        {
            'canonical_drug_name': 'Amoxicillin',
            'brand_names': ['Amoxil', 'Trimox', 'Moxatag', 'Larotid', 'Dispermox'],
            'regions': ['US', 'Europe', 'Global'],
            'source': 'DrugBank'
        },
        {
            'canonical_drug_name': 'Omeprazole',
            'brand_names': ['Prilosec', 'Losec', 'Zegerid', 'Omez', 'Ultop'],
            'regions': ['US', 'UK', 'Europe', 'India'],
            'source': 'DrugBank'
        },
        {
            'canonical_drug_name': 'Simvastatin',
            'brand_names': ['Zocor', 'Lipex', 'Zocor Heart-Pro', 'Simlup', 'Simvacor'],
            'regions': ['US', 'UK', 'Europe', 'Global'],
            'source': 'DrugBank'
        },
        {
            'canonical_drug_name': 'Amlodipine',
            'brand_names': ['Norvasc', 'Istin', 'Amlor', 'Amlodac', 'Amlong'],
            'regions': ['US', 'UK', 'Europe', 'India'],
            'source': 'DrugBank'
        },
        {
            'canonical_drug_name': 'Metformin',
            'brand_names': ['Glucophage', 'Fortamet', 'Glumetza', 'Riomet', 'Diaformin'],
            'regions': ['US', 'Europe', 'India', 'Global'],
            'source': 'DrugBank'
        },
        {
            'canonical_drug_name': 'Atorvastatin',
            'brand_names': ['Lipitor', 'Sortis', 'Torvast', 'Atorlip', 'Lipvas'],
            'regions': ['US', 'UK', 'Europe', 'India'],
            'source': 'DrugBank'
        },
        {
            'canonical_drug_name': 'Cetirizine',
            'brand_names': ['Zyrtec', 'Reactine', 'Aller-Tec', 'Cetrizet', 'Zyrtec-D'],
            'regions': ['US', 'Canada', 'Europe', 'Global'],
            'source': 'DrugBank'
        },
        {
            'canonical_drug_name': 'Loratadine',
            'brand_names': ['Claritin', 'Alavert', 'Tavist ND', 'Loratad', 'Roletra'],
            'regions': ['US', 'Europe', 'Global'],
            'source': 'DrugBank'
        },
        {
            'canonical_drug_name': 'Diphenhydramine',
            'brand_names': ['Benadryl', 'Nytol', 'Sominex', 'Tylenol PM', 'Advil PM'],
            'regions': ['US', 'UK', 'Global'],
            'source': 'DrugBank'
        },
        {
            'canonical_drug_name': 'Ranitidine',
            'brand_names': ['Zantac', 'Raniplex', 'Rantac', 'Histac', 'Novo-Ranidine'],
            'regions': ['US', 'UK', 'India', 'Global'],
            'source': 'DrugBank'
        },
        {
            'canonical_drug_name': 'Furosemide',
            'brand_names': ['Lasix', 'Frusemide', 'Frusenex', 'Frusid', 'Urex'],
            'regions': ['US', 'UK', 'Europe', 'India'],
            'source': 'DrugBank'
        },
        {
            'canonical_drug_name': 'Prednisone',
            'brand_names': ['Deltasone', 'Rayos', 'Prednisone Intensol', 'Prednicot', 'Prednol'],
            'regions': ['US', 'Europe', 'Global'],
            'source': 'DrugBank'
        }
    ]

    # Create Flask app context
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        # Create tables if they don't exist
        db.create_all()

        # Clear existing data (optional - comment out if you want to keep existing data)
        # DrugBrandNames.query.delete()
        # db.session.commit()

        # Add new brand name entries
        added_count = 0
        for drug_data in brand_data:
            # Check if this drug already exists
            existing = DrugBrandNames.query.filter_by(
                canonical_drug_name=drug_data['canonical_drug_name']
            ).first()

            if existing:
                print(f"Skipping {drug_data['canonical_drug_name']} - already exists")
                continue

            # Create new entry
            brand_entry = DrugBrandNames(
                canonical_drug_name=drug_data['canonical_drug_name'],
                brand_names=json.dumps(drug_data['brand_names']),
                regions=json.dumps(drug_data['regions']),
                source=drug_data['source']
            )

            db.session.add(brand_entry)
            added_count += 1
            print(f"Added brand names for {drug_data['canonical_drug_name']}: {drug_data['brand_names']}")

        # Commit all changes
        db.session.commit()
        print(f"\nSeeding completed! Added {added_count} new drug brand name entries.")

        # Print summary
        total_entries = DrugBrandNames.query.count()
        print(f"Total brand name entries in database: {total_entries}")

if __name__ == '__main__':
    seed_brand_names()
