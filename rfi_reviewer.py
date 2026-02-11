#!/usr/bin/env python3
"""
RFI Response Review Tool

This script analyzes PDF files containing RFI (Request for Information) responses and:
- Extracts text content from PDFs
- Categorizes themes
- Identifies specific actions
- Identifies reasonable timeframes for actions
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

try:
    import pdfplumber
except ImportError:
    print("Error: pdfplumber is not installed. Please run: pip install -r requirements.txt")
    sys.exit(1)

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai is not installed. Please run: pip install -r requirements.txt")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: python-dotenv is not installed. Please run: pip install -r requirements.txt")
    sys.exit(1)


class RFIReviewer:
    """Analyzes RFI response PDF files and extracts structured information."""
    
    def __init__(self, api_key: str = None):
        """Initialize the RFI Reviewer.
        
        Args:
            api_key: OpenAI API key. If not provided, will try to load from environment.
        """
        load_dotenv()
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            print("Warning: No OpenAI API key provided. AI-powered analysis will not be available.")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
                return text
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {str(e)}")
            return ""
    
    def analyze_with_ai(self, text: str) -> Dict[str, Any]:
        """Use AI to analyze the text and extract themes, actions, and timeframes.
        
        Args:
            text: Text content to analyze
            
        Returns:
            Dictionary containing themes, actions, and timeframes
        """
        if not self.client:
            return self._fallback_analysis(text)
        
        try:
            prompt = f"""Analyze the following RFI (Request for Information) response and provide:
1. Main themes and categories (list the key topics covered)
2. Specific actions mentioned (what needs to be done)
3. Timeframes for each action (when things should be completed)

Format your response as JSON with this structure:
{{
    "themes": ["theme1", "theme2", ...],
    "actions": [
        {{
            "action": "description of action",
            "timeframe": "expected timeframe",
            "priority": "high/medium/low",
            "category": "relevant theme"
        }}
    ],
    "summary": "brief summary of the RFI response"
}}

RFI Response Text:
{text[:8000]}
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing RFI responses and extracting structured information."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"Error during AI analysis: {str(e)}")
            return self._fallback_analysis(text)
    
    def _fallback_analysis(self, text: str) -> Dict[str, Any]:
        """Provide basic analysis when AI is not available.
        
        Args:
            text: Text content to analyze
            
        Returns:
            Dictionary with basic analysis
        """
        # Simple keyword-based analysis
        keywords = {
            "themes": [],
            "actions": [],
            "timeframes": []
        }
        
        lines = text.lower().split('\n')
        
        # Look for common action words
        action_words = ['implement', 'develop', 'create', 'establish', 'complete', 
                       'deliver', 'submit', 'provide', 'ensure', 'review']
        
        # Look for timeframe indicators
        timeframe_words = ['days', 'weeks', 'months', 'quarter', 'deadline', 
                          'by', 'within', 'before', 'after']
        
        for line in lines:
            if any(word in line for word in action_words):
                if len(line.strip()) > 10:
                    keywords["actions"].append(line.strip()[:100])
            
            if any(word in line for word in timeframe_words):
                if len(line.strip()) > 5:
                    keywords["timeframes"].append(line.strip()[:100])
        
        return {
            "themes": ["General RFI Response"],
            "actions": [{"action": action, "timeframe": "Not specified", "priority": "medium", "category": "General"} 
                       for action in keywords["actions"][:10]],
            "summary": "Basic analysis completed. Install OpenAI API for detailed analysis."
        }
    
    def review_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Review a single PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Analysis results
        """
        print(f"Reviewing: {pdf_path}")
        
        # Extract text
        text = self.extract_text_from_pdf(pdf_path)
        
        if not text:
            return {
                "file": pdf_path,
                "error": "Could not extract text from PDF",
                "themes": [],
                "actions": [],
                "summary": ""
            }
        
        # Analyze with AI
        analysis = self.analyze_with_ai(text)
        analysis["file"] = pdf_path
        analysis["text_length"] = len(text)
        analysis["analyzed_at"] = datetime.now().isoformat()
        
        return analysis
    
    def review_multiple_pdfs(self, pdf_paths: List[str]) -> List[Dict[str, Any]]:
        """Review multiple PDF files.
        
        Args:
            pdf_paths: List of paths to PDF files
            
        Returns:
            List of analysis results
        """
        results = []
        for pdf_path in pdf_paths:
            result = self.review_pdf(pdf_path)
            results.append(result)
        
        return results
    
    def generate_report(self, results: List[Dict[str, Any]], output_path: str = None):
        """Generate a comprehensive report from analysis results.
        
        Args:
            results: List of analysis results
            output_path: Optional path to save the report
        """
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_files": len(results),
            "files_analyzed": results,
            "consolidated_themes": self._consolidate_themes(results),
            "consolidated_actions": self._consolidate_actions(results)
        }
        
        if output_path:
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"Report saved to: {output_path}")
        
        return report
    
    def _consolidate_themes(self, results: List[Dict[str, Any]]) -> List[str]:
        """Consolidate themes from multiple analyses."""
        all_themes = []
        for result in results:
            if "themes" in result:
                all_themes.extend(result["themes"])
        return list(set(all_themes))
    
    def _consolidate_actions(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Consolidate actions from multiple analyses."""
        all_actions = []
        for result in results:
            if "actions" in result:
                for action in result["actions"]:
                    action_copy = action.copy()
                    action_copy["source_file"] = result.get("file", "unknown")
                    all_actions.append(action_copy)
        return all_actions


def main():
    """Main entry point for the RFI Reviewer CLI."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Review RFI response PDF files and extract themes, actions, and timeframes"
    )
    parser.add_argument(
        "pdf_files",
        nargs="+",
        help="Path(s) to PDF file(s) to review"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output path for the JSON report",
        default="rfi_review_report.json"
    )
    parser.add_argument(
        "--api-key",
        help="OpenAI API key (or set OPENAI_API_KEY environment variable)",
        default=None
    )
    
    args = parser.parse_args()
    
    # Validate PDF files exist
    pdf_files = []
    for pdf_path in args.pdf_files:
        if not os.path.exists(pdf_path):
            print(f"Error: File not found: {pdf_path}")
            continue
        if not pdf_path.lower().endswith('.pdf'):
            print(f"Warning: {pdf_path} does not appear to be a PDF file")
        pdf_files.append(pdf_path)
    
    if not pdf_files:
        print("Error: No valid PDF files provided")
        sys.exit(1)
    
    # Create reviewer
    reviewer = RFIReviewer(api_key=args.api_key)
    
    # Review PDFs
    print(f"Reviewing {len(pdf_files)} PDF file(s)...")
    results = reviewer.review_multiple_pdfs(pdf_files)
    
    # Generate report
    report = reviewer.generate_report(results, args.output)
    
    # Print summary
    print("\n" + "="*60)
    print("RFI REVIEW SUMMARY")
    print("="*60)
    print(f"Files analyzed: {len(results)}")
    print(f"\nConsolidated Themes ({len(report['consolidated_themes'])}):")
    for theme in report['consolidated_themes']:
        print(f"  - {theme}")
    
    print(f"\nTotal Actions Identified: {len(report['consolidated_actions'])}")
    
    # Group actions by priority
    high_priority = [a for a in report['consolidated_actions'] if a.get('priority') == 'high']
    medium_priority = [a for a in report['consolidated_actions'] if a.get('priority') == 'medium']
    low_priority = [a for a in report['consolidated_actions'] if a.get('priority') == 'low']
    
    if high_priority:
        print(f"\nHigh Priority Actions ({len(high_priority)}):")
        for action in high_priority[:5]:
            print(f"  - {action.get('action', 'N/A')[:80]}")
            print(f"    Timeframe: {action.get('timeframe', 'Not specified')}")
    
    if medium_priority:
        print(f"\nMedium Priority Actions ({len(medium_priority)}):")
        for action in medium_priority[:5]:
            print(f"  - {action.get('action', 'N/A')[:80]}")
            print(f"    Timeframe: {action.get('timeframe', 'Not specified')}")
    
    print("\n" + "="*60)
    print(f"Full report saved to: {args.output}")
    print("="*60)


if __name__ == "__main__":
    main()
