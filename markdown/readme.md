# Markdown File Analyzer

A Python command-line tool for analyzing Markdown files. The tool provides statistics on word count, heading structure, links, images, and validates external URLs.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Output Format](#output-format)

## Features

- Word count analysis (excluding code blocks)
- Heading detection and categorization (H1-H6)
- Link extraction and validation
- Image detection with alt text
- HTTP/HTTPS URL validation
- Formatted analysis reports

## Requirements

- Python 3.6 or higher
- pip (Python package installer)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/anirudhreddyyyy/Internship.git
cd markdown
```

### 2. Setup Virtual Environment 

**On Windows:**
```bash
python -m venv mini_project_1
mini_project_1\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv mini_project_1
source mini_project_1/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

Run the analyzer:

```bash
python Mini_Project_1.py
```

When prompted, enter the path to your Markdown file:

```
Enter markdown file path: your_file.md
```

The tool will analyze the file and display a comprehensive report.

## Project Structure

```
markdown/
├── Mini_Project_1.py       # Main analyzer script
├── requirements.txt        # Python dependencies
├── workflow.png            # flow of code
├── output.png              # sample output structure
└── README.md              # Project documentation

```

## Output Format

The analyzer generates a formatted report containing:

- **Word Count**: Total words in the document (excluding code blocks)
- **Headings**: Count of each heading level (H1-H6)
- **Links**: Total links found and broken link details
- **Images**: List of images with alt text and URLs

## Core Functions

### `count_words(content)`
Counts words in markdown content while excluding code blocks and markdown syntax.

### `count_headings(content)`
Returns a dictionary with heading counts categorized by level (h1-h6).

### `extract_links(content)`
Extracts all markdown links and returns a list with link text and URLs.

### `extract_images(content)`
Identifies all images and returns their alt text and URLs.

### `validate_links(links)`
Validates HTTP/HTTPS links by making requests and returns broken links with error details.

### `generate_report(word_count, headings, links, images, broken_links)`
Formats and displays a comprehensive analysis report.

