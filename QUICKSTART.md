# Quick Start Guide

## Getting Started in 5 Minutes

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set Up API Key (Optional but Recommended)

For AI-powered analysis, you'll need an OpenAI API key:

1. Get an API key from https://platform.openai.com/api-keys
2. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your API key:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

### Step 3: Review Your First PDF

```bash
python rfi_reviewer.py path/to/your/rfi_response.pdf
```

This will:
- Extract text from the PDF
- Analyze themes, actions, and timeframes
- Generate a report at `rfi_review_report.json`
- Display a summary in the console

### Step 4: Review Multiple PDFs

```bash
python rfi_reviewer.py file1.pdf file2.pdf file3.pdf -o consolidated_report.json
```

## Common Use Cases

### 1. Reviewing a Batch of RFI Responses

```bash
# Review all PDFs in a directory
python rfi_reviewer.py rfis/*.pdf -o batch_report.json
```

### 2. Quick Analysis Without AI

If you don't have an OpenAI API key, the tool will use basic keyword matching:

```bash
# No API key needed for basic analysis
python rfi_reviewer.py response.pdf
```

### 3. Programmatic Usage

Create a custom script:

```python
from rfi_reviewer import RFIReviewer

reviewer = RFIReviewer()
result = reviewer.review_pdf("my_response.pdf")

# Extract specific information
for action in result["actions"]:
    if action["priority"] == "high":
        print(f"High priority: {action['action']}")
        print(f"Due: {action['timeframe']}")
```

## Understanding the Output

The tool generates a JSON report with:

- **themes**: Main topics covered (e.g., "Security", "Implementation", "Timeline")
- **actions**: Specific tasks with priority, timeframe, and category
- **summary**: Brief overview of the RFI response
- **consolidated_actions**: All actions from multiple files combined

## Tips for Best Results

1. **Use Clear PDFs**: Text-based PDFs work best. Scanned images need OCR first.
2. **Organize Files**: Keep RFI responses in a dedicated folder.
3. **Review Output**: Always validate the AI-generated analysis.
4. **Batch Processing**: Review multiple related PDFs together for better theme consolidation.

## Troubleshooting

**"Error: pdfplumber is not installed"**
→ Run `pip install -r requirements.txt`

**"Warning: No OpenAI API key provided"**
→ Either set up `.env` file or use `--api-key` parameter
→ Tool will work in fallback mode without AI

**No text extracted from PDF**
→ PDF might be image-based; try using OCR tools first

## Next Steps

- Check `example_usage.py` for more advanced examples
- Read the full `README.md` for detailed documentation
- Customize the analysis prompts in `rfi_reviewer.py` for your specific needs

## Support

For issues or questions:
- Check the README.md troubleshooting section
- Open an issue on GitHub
- Review the example_usage.py file for code samples
