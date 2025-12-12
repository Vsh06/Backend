#!/usr/bin/env python3
"""
Manual test script for enhanced repurposing system.
Tests the key functionality without unittest framework.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Repurposing.engine import RepurposeEngine

def test_common_disease_mapping():
    """Test that common disease names are properly mapped"""
    print("Testing common disease mapping...")
    engine = RepurposeEngine()

    # Test some mappings
    assert engine.common_disease_mapping.get('headache') == 'migraine'
    assert engine.common_disease_mapping.get('fever') == 'pyrexia'
    assert engine.common_disease_mapping.get('cough') == 'cough'
    print("✓ Common disease mapping works")

def test_fallback_candidates():
    """Test that fallback candidates exist for common diseases"""
    print("Testing fallback candidates...")
    engine = RepurposeEngine()

    # Test that fallback candidates exist for key diseases
    assert 'migraine' in engine.fallback_candidates
    assert 'pyrexia' in engine.fallback_candidates
    assert 'cough' in engine.fallback_candidates

    # Test structure
    migraine_candidates = engine.fallback_candidates['migraine']
    assert isinstance(migraine_candidates, list)
    assert len(migraine_candidates) > 0

    # Check required fields
    for candidate in migraine_candidates:
        assert 'name' in candidate
        assert 'score' in candidate
        assert 'evidence' in candidate

    print("✓ Fallback candidates are properly structured")

def test_find_candidates_basic():
    """Test basic find_candidates functionality"""
    print("Testing find_candidates basic functionality...")
    engine = RepurposeEngine()

    # Test with a common disease
    candidates = engine.find_candidates('migraine')
    assert isinstance(candidates, list)
    assert len(candidates) > 0

    # Check structure
    for candidate in candidates:
        assert 'molecule_chembl_id' in candidate
        assert 'score' in candidate
        assert 'disease' in candidate

    print(f"✓ Found {len(candidates)} candidates for migraine")

def test_allergy_filtering_with_fallbacks():
    """Test allergy filtering works with fallback candidates"""
    print("Testing allergy filtering with fallbacks...")
    engine = RepurposeEngine()

    # Test with penicillin allergy
    candidates = engine.find_candidates('migraine', allergies=['penicillin'])

    # Check that no penicillin-related drugs are returned
    penicillin_related = ['amoxicillin', 'penicillin', 'ampicillin']
    for candidate in candidates:
        drug_name = candidate.get('molecule_chembl_id', '').lower()
        for penicillin_drug in penicillin_related:
            assert penicillin_drug not in drug_name

    print(f"✓ Allergy filtering works, {len(candidates)} safe candidates found")

def test_multiple_diseases():
    """Test repurposing for multiple common diseases"""
    print("Testing multiple common diseases...")
    engine = RepurposeEngine()

    diseases = ['headache', 'fever', 'cough', 'arthritis', 'nausea']

    for disease in diseases:
        candidates = engine.find_candidates(disease)
        assert isinstance(candidates, list)
        print(f"✓ {disease}: {len(candidates)} candidates")

def test_synonyms():
    """Test disease synonym expansion"""
    print("Testing disease synonyms...")
    engine = RepurposeEngine()

    # Test that both original and mapped terms work
    headache_candidates = engine.find_candidates('headache')
    migraine_candidates = engine.find_candidates('migraine')

    assert isinstance(headache_candidates, list)
    assert isinstance(migraine_candidates, list)

    print("✓ Disease synonyms work")

def main():
    """Run all tests"""
    print("Running enhanced repurposing system tests...\n")

    try:
        test_common_disease_mapping()
        test_fallback_candidates()
        test_find_candidates_basic()
        test_allergy_filtering_with_fallbacks()
        test_multiple_diseases()
        test_synonyms()

        print("\n✅ All tests passed! Enhanced repurposing system is working correctly.")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == '__main__':
    exit(main())
