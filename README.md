# RFI Response Review Tool

A comprehensive Python tool for analyzing RFI (Request for Information) response PDF files. This tool extracts text from PDFs and uses AI to:

- **Categorize themes** - Identify and group the main topics covered in the responses
- **Identify specific actions** - Extract actionable items that need to be completed
- **Determine timeframes** - Identify reasonable timeframes and deadlines for each action
- **Generate reports** - Create structured JSON reports with all findings

## Features

- 📄 PDF text extraction using pdfplumber
- 🤖 AI-powered analysis using OpenAI's GPT models
- 📊 Theme categorization and consolidation
- ✅ Action identification with priority levels
- ⏰ Timeframe extraction and analysis
- 📈 Comprehensive JSON reporting
- 🔄 Batch processing of multiple PDF files
- 💡 Fallback analysis when AI is not available

## Installation

1. Clone this repository:
```bash
git clone https://github.com/chrisj-gov/rfi-response-review.git
cd rfi-response-review
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Usage

### Basic Usage

Review a single PDF file:
```bash
python rfi_reviewer.py path/to/response.pdf
```

Review multiple PDF files:
```bash
python rfi_reviewer.py file1.pdf file2.pdf file3.pdf
```

### Advanced Options

Specify output file:
```bash
python rfi_reviewer.py response.pdf -o custom_report.json
```

Provide API key directly:
```bash
python rfi_reviewer.py response.pdf --api-key sk-your-key-here
```

### Using as a Python Module

```python
from rfi_reviewer import RFIReviewer

# Initialize the reviewer
reviewer = RFIReviewer(api_key="your-api-key")

# Review a single PDF
result = reviewer.review_pdf("response.pdf")

# Review multiple PDFs
results = reviewer.review_multiple_pdfs(["file1.pdf", "file2.pdf"])

# Generate a comprehensive report
report = reviewer.generate_report(results, "report.json")
```

## Output Format

The tool generates a JSON report with the following structure:

```json
{
  "generated_at": "2026-02-11T18:00:00",
  "total_files": 2,
  "files_analyzed": [
    {
      "file": "response.pdf",
      "themes": ["Technical Implementation", "Security", "Timeline"],
      "actions": [
        {
          "action": "Implement multi-factor authentication",
          "timeframe": "Within 30 days",
          "priority": "high",
          "category": "Security"
        }
      ],
      "summary": "Brief summary of the response",
      "analyzed_at": "2026-02-11T18:00:00"
    }
  ],
  "consolidated_themes": ["Technical Implementation", "Security", "Timeline"],
  "consolidated_actions": [
    {
      "action": "Implement multi-factor authentication",
      "timeframe": "Within 30 days",
      "priority": "high",
      "category": "Security",
      "source_file": "response.pdf"
    }
  ]
}
```

## Requirements

- Python 3.7+
- OpenAI API key (for AI-powered analysis)
- PDF files to analyze

## Dependencies

- `pdfplumber` - PDF text extraction
- `openai` - AI-powered analysis
- `python-dotenv` - Environment variable management

## How It Works

1. **PDF Text Extraction**: The tool uses pdfplumber to extract text content from PDF files
2. **AI Analysis**: Extracted text is sent to OpenAI's GPT model with a structured prompt
3. **Theme Categorization**: The AI identifies and categorizes main themes in the response
4. **Action Identification**: Specific actions are extracted with priority levels and categories
5. **Timeframe Analysis**: Timeframes and deadlines are identified for each action
6. **Report Generation**: All findings are consolidated into a structured JSON report

## Fallback Mode

If no OpenAI API key is provided, the tool will run in fallback mode using basic keyword matching. While not as sophisticated as AI analysis, it can still identify:
- Common action words (implement, develop, create, etc.)
- Timeframe indicators (days, weeks, months, deadlines, etc.)

## Best Practices

1. **Organize PDFs**: Keep RFI response PDFs in a dedicated folder
2. **Use descriptive filenames**: Name PDFs clearly (e.g., `rfi_2026_q1_technical_response.pdf`)
3. **Review the output**: Always review the generated report for accuracy
4. **Iterate**: Use the insights to refine your understanding of the RFI responses

## Troubleshooting

**PDF text extraction fails:**
- Ensure the PDF contains actual text (not scanned images)
- Try using OCR tools first if PDFs are image-based

**AI analysis not working:**
- Check that your OpenAI API key is set correctly
- Verify you have sufficient API credits
- Check your internet connection

**Import errors:**
- Run `pip install -r requirements.txt` to install all dependencies

## Security Notes

- Never commit your `.env` file or API keys to version control
- The `.gitignore` file is configured to exclude sensitive files
- PDF files are not committed by default

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue on GitHub.