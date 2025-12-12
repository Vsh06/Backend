#!/usr/bin/env python3
"""
Test script for the Flask backend endpoints with new data structure.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app

def test_endpoints():
    """Test all the backend endpoints."""
    with app.test_client() as client:
        print("=== Testing Flask Backend Endpoints ===\n")

        # Test health endpoint
        print("1. Testing /health endpoint:")
        response = client.get('/health')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}\n")

        # Test drugs endpoint
        print("2. Testing /drugs endpoint:")
        response = client.get('/drugs')
        drugs_data = response.get_json()
        print(f"   Status: {response.status_code}")
        print(f"   Found {len(drugs_data.get('drugs', []))} drugs")
        if drugs_data.get('drugs'):
            print(f"   Sample drug: {drugs_data['drugs'][0]}")
        print()

        # Test indications endpoint
        print("3. Testing /indications endpoint:")
        response = client.get('/indications')
        indications_data = response.get_json()
        print(f"   Status: {response.status_code}")
        print(f"   Found {len(indications_data.get('indications', []))} indications")
        if indications_data.get('indications'):
            print(f"   Sample indication: {indications_data['indications'][0]}")
        print()

        # Test composition endpoint
        print("4. Testing /composition endpoint (Aspirin):")
        response = client.get('/composition?drug_name=Aspirin')
        composition_data = response.get_json()
        print(f"   Status: {response.status_code}")
        print(f"   Response: {composition_data}")
        print()

        # Test repurpose endpoint
        print("5. Testing /repurpose endpoint (hypertension):")
        response = client.get('/repurpose?disease=hypertension')
        repurpose_data = response.get_json()
        print(f"   Status: {response.status_code}")
        print(f"   Response: {repurpose_data}")
        print()

        # Test formula endpoint
        print("6. Testing /formula endpoint (Aspirin SMILES):")
        response = client.get('/formula?smiles=CC(=O)OC1=CC=CC=C1C(=O)O')
        formula_data = response.get_json()
        print(f"   Status: {response.status_code}")
        print(f"   Response: {formula_data}")
        print()

        # Test specific drug endpoint
        print("7. Testing /drug/Aspirin endpoint:")
        response = client.get('/drug/Aspirin')
        drug_data = response.get_json()
        print(f"   Status: {response.status_code}")
        print(f"   Response: {drug_data}")
        print()

        # Test drug indications endpoint
        print("8. Testing /drug_indications/CHEMBL25 endpoint:")
        response = client.get('/drug_indications/CHEMBL25')
        drug_indications_data = response.get_json()
        print(f"   Status: {response.status_code}")
        print(f"   Response: {drug_indications_data}")
        print()

        print("=== All endpoint tests completed ===")

if __name__ == "__main__":
    test_endpoints()
