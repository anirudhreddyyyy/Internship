# Markdown File Analyzer

## Overview

The **Markdown File Analyzer** is a simple command-line tool that analyzes `.md` (Markdown) files and generates a structured summary report. It helps developers and writers understand the structure, content, and quality of their Markdown documents.

This project is ideal for beginners and interns to practice **file handling**, **text parsing**, and **basic validation logic** using a real-world documentation use case.

<!-- Project Overview / Workflow -->
![Project Overview](![alt text](image-2.png))

---

## Features

### Markdown Parsing
- Reads and processes `.md` files
- Uses a Markdown parsing library instead of plain text scanning

### Content Analysis
The tool extracts the following information:
- **Word count**
- **Number of headings** (H1–H6)
- **Number of links**
- **Number of images**

### Link Validation
- Checks whether external links are reachable
- Skips local anchor links
- Flags broken or unreachable links

### Summary Report
- Displays a clear analysis report
- Can be printed to the console or saved to a file

<!-- Sample Output / Report -->
![Markdown Analysis Report](![alt text](image-3.png))


---

## Technology Stack

- **Python** (using `markdown` library)  
  or  
- **JavaScript** (using `marked.js`)

---

## Learning Outcomes

By completing this project, you will learn:
- How to read and parse Markdown files
- How to use third-party libraries
- How to analyze structured text
- How to validate URLs programmatically
- How to generate readable summary reports

---

## Use Cases

- Documentation quality checks
- README validation
- Pre-commit documentation analysis
- Internship or beginner-level learning project
