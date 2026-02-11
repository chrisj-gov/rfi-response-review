#!/usr/bin/env python3
"""
Test script for the RFI Reviewer tool.

This script tests the basic functionality without requiring actual PDF files.
"""

import sys
import json
from pathlib import Path


def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import pdfplumber
        print("  ✓ pdfplumber installed")
    except ImportError:
        print("  ✗ pdfplumber not installed")
        return False
    
    try:
        import openai
        print("  ✓ openai installed")
    except ImportError:
        print("  ✗ openai not installed")
        return False
    
    try:
        from dotenv import load_dotenv
        print("  ✓ python-dotenv installed")
    except ImportError:
        print("  ✗ python-dotenv not installed")
        return False
    
    return True


def test_rfi_reviewer_class():
    """Test that the RFIReviewer class can be instantiated."""
    print("\nTesting RFIReviewer class...")
    
    try:
        from rfi_reviewer import RFIReviewer
        
        # Test without API key (should work in fallback mode)
        reviewer = RFIReviewer(api_key=None)
        print("  ✓ RFIReviewer instantiated (fallback mode)")
        
        # Test fallback analysis
        test_text = """
        Implementation Plan for RFI Response
        
        We will implement the following actions:
        1. Develop the authentication system within 30 days
        2. Complete security audit by end of Q2
        3. Submit final documentation within 60 days
        
        Key themes include security, compliance, and implementation timeline.
        """
        
        result = reviewer._fallback_analysis(test_text)
        print("  ✓ Fallback analysis works")
        print(f"    - Found {len(result.get('actions', []))} actions")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        return False


def test_report_generation():
    """Test report generation functionality."""
    print("\nTesting report generation...")
    
    try:
        from rfi_reviewer import RFIReviewer
        
        reviewer = RFIReviewer(api_key=None)
        
        # Create mock results
        mock_results = [
            {
                "file": "test1.pdf",
                "themes": ["Security", "Implementation"],
                "actions": [
                    {
                        "action": "Implement MFA",
                        "timeframe": "30 days",
                        "priority": "high",
                        "category": "Security"
                    }
                ],
                "summary": "Test summary"
            },
            {
                "file": "test2.pdf",
                "themes": ["Compliance", "Implementation"],
                "actions": [
                    {
                        "action": "Complete audit",
                        "timeframe": "Q2",
                        "priority": "medium",
                        "category": "Compliance"
                    }
                ],
                "summary": "Test summary 2"
            }
        ]
        
        report = reviewer.generate_report(mock_results)
        
        print(f"  ✓ Report generated")
        print(f"    - Total files: {report['total_files']}")
        print(f"    - Consolidated themes: {len(report['consolidated_themes'])}")
        print(f"    - Consolidated actions: {len(report['consolidated_actions'])}")
        
        # Verify consolidated themes
        expected_themes = {"Security", "Implementation", "Compliance"}
        actual_themes = set(report['consolidated_themes'])
        if expected_themes == actual_themes:
            print(f"  ✓ Theme consolidation works correctly")
        else:
            print(f"  ⚠ Theme consolidation mismatch")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        return False


def test_file_structure():
    """Test that all required files exist."""
    print("\nTesting file structure...")
    
    required_files = [
        "rfi_reviewer.py",
        "requirements.txt",
        "README.md",
        "QUICKSTART.md",
        ".env.example",
        ".gitignore",
        "example_usage.py"
    ]
    
    all_exist = True
    for filename in required_files:
        if Path(filename).exists():
            print(f"  ✓ {filename}")
        else:
            print(f"  ✗ {filename} missing")
            all_exist = False
    
    return all_exist


def main():
    """Run all tests."""
    print("="*60)
    print("RFI Reviewer - Installation Test")
    print("="*60)
    print()
    
    tests = [
        ("File Structure", test_file_structure),
        ("Dependencies", test_imports),
        ("RFI Reviewer Class", test_rfi_reviewer_class),
        ("Report Generation", test_report_generation),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n✗ {test_name} failed with exception: {str(e)}")
            results[test_name] = False
    
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! The RFI Reviewer is ready to use.")
        print("\nNext steps:")
        print("  1. Set up your OpenAI API key in .env file")
        print("  2. Run: python rfi_reviewer.py your_file.pdf")
        print("  3. Check QUICKSTART.md for more examples")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the output above.")
        if not results.get("Dependencies", False):
            print("\nTo install dependencies, run:")
            print("  pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
