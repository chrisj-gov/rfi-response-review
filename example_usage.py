#!/usr/bin/env python3
"""
Example usage of the RFI Reviewer tool.

This script demonstrates how to use the RFI Reviewer programmatically.
"""

from rfi_reviewer import RFIReviewer
import json


def example_single_pdf():
    """Example: Review a single PDF file."""
    print("="*60)
    print("Example 1: Reviewing a single PDF")
    print("="*60)
    
    # Initialize the reviewer
    reviewer = RFIReviewer()
    
    # Review a PDF (replace with actual path)
    pdf_path = "sample_rfi_response.pdf"
    
    print(f"Analyzing: {pdf_path}")
    result = reviewer.review_pdf(pdf_path)
    
    # Display results
    print("\nThemes identified:")
    for theme in result.get("themes", []):
        print(f"  - {theme}")
    
    print("\nActions identified:")
    for action in result.get("actions", [])[:5]:
        print(f"\n  Action: {action.get('action', 'N/A')}")
        print(f"  Timeframe: {action.get('timeframe', 'Not specified')}")
        print(f"  Priority: {action.get('priority', 'N/A')}")
        print(f"  Category: {action.get('category', 'N/A')}")
    
    print("\n" + "="*60 + "\n")


def example_multiple_pdfs():
    """Example: Review multiple PDF files."""
    print("="*60)
    print("Example 2: Reviewing multiple PDFs")
    print("="*60)
    
    # Initialize the reviewer
    reviewer = RFIReviewer()
    
    # List of PDFs to review
    pdf_files = [
        "rfi_response_part1.pdf",
        "rfi_response_part2.pdf",
        "rfi_response_part3.pdf"
    ]
    
    print(f"Analyzing {len(pdf_files)} PDF files...")
    results = reviewer.review_multiple_pdfs(pdf_files)
    
    # Generate comprehensive report
    report = reviewer.generate_report(results, "comprehensive_report.json")
    
    print(f"\nTotal themes across all files: {len(report['consolidated_themes'])}")
    print(f"Total actions identified: {len(report['consolidated_actions'])}")
    
    print("\n" + "="*60 + "\n")


def example_custom_analysis():
    """Example: Custom analysis and filtering."""
    print("="*60)
    print("Example 3: Custom analysis with filtering")
    print("="*60)
    
    reviewer = RFIReviewer()
    
    # Review PDFs
    pdf_files = ["response1.pdf", "response2.pdf"]
    results = reviewer.review_multiple_pdfs(pdf_files)
    
    # Filter high-priority actions
    high_priority_actions = []
    for result in results:
        for action in result.get("actions", []):
            if action.get("priority") == "high":
                high_priority_actions.append({
                    "action": action.get("action"),
                    "timeframe": action.get("timeframe"),
                    "file": result.get("file")
                })
    
    print(f"\nHigh-priority actions found: {len(high_priority_actions)}")
    for i, action in enumerate(high_priority_actions[:5], 1):
        print(f"\n{i}. {action['action']}")
        print(f"   Timeframe: {action['timeframe']}")
        print(f"   Source: {action['file']}")
    
    # Group actions by category
    categories = {}
    for result in results:
        for action in result.get("actions", []):
            category = action.get("category", "Uncategorized")
            if category not in categories:
                categories[category] = []
            categories[category].append(action)
    
    print("\nActions by category:")
    for category, actions in categories.items():
        print(f"  {category}: {len(actions)} actions")
    
    print("\n" + "="*60 + "\n")


def example_text_extraction_only():
    """Example: Extract text from PDF without AI analysis."""
    print("="*60)
    print("Example 4: Text extraction only")
    print("="*60)
    
    reviewer = RFIReviewer()
    
    pdf_path = "sample_rfi_response.pdf"
    text = reviewer.extract_text_from_pdf(pdf_path)
    
    print(f"\nExtracted {len(text)} characters from {pdf_path}")
    print("\nFirst 500 characters:")
    print(text[:500])
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    print("\nRFI Reviewer - Example Usage\n")
    
    # Note: These examples assume PDF files exist
    # Replace with actual file paths or create sample PDFs
    
    print("These examples demonstrate various ways to use the RFI Reviewer.")
    print("Make sure to replace the file paths with actual PDF files.\n")
    
    # Uncomment the examples you want to run:
    
    # example_single_pdf()
    # example_multiple_pdfs()
    # example_custom_analysis()
    # example_text_extraction_only()
    
    print("Edit example_usage.py to uncomment and run specific examples.")
