# Data Directory

This directory contains data files and parsed results from various sources.

## Directory Structure

```
data/
├── official_documents/     # Official Word documents from MA
├── parsed_data/           # Parsed data from documents
└── README.md             # This file
```

## Usage

### Adding Official Documents

1. Place your official Word document in `data/official_documents/`
2. Run the document parser: `python document_parser.py`
3. Parsed data will be saved to `data/parsed_data/`

### Supported Document Types

- **Word documents** (.docx)
- **PDF files** (.pdf) - coming soon
- **Excel files** (.xlsx) - coming soon

## File Naming Convention

- Use descriptive names:
  - `ma_community_health_centers_2024.docx`
  - `massachusetts_hospitals_official_list.docx`
  - `health_centers_directory_2024.docx`

## Output Format

Parsed data will be saved as:
- JSON format for easy processing
- CSV format for spreadsheet import
- Structured data with consistent fields
