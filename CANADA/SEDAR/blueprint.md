---
name: SEDAR Web Crawling and Data Extraction
description: A project for extracting and analyzing data from SEDAR filings, storing results in HTML format for efficient data management and analysis.
author: UJWAL S
tags: [web crawling, data extraction, Python, automation, SEDAR, HTML]
---

# SEDAR Web Crawling and Data Extraction

## Overview
The SEDAR Web Crawling and Data Extraction project automates the process of gathering data from SEDAR filings. It uses a Jupyter Notebook for data extraction, storing the results in HTML format for easy analysis and further processing.

## Table of Contents
- [Project Structure](#project-structure)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [Configuration](#configuration)

## Project Structure
SEDAR:.
    0373849_B.C._Ltd._000004771.html
    0694758_B.C._Ltd._000021020.html
    0730004_B.C._Ltd._formerly_Diamond_Hawk_Mining_Corp._000021787.html
    sedar1.ipynb


## Key Features
- **Web Crawling:**
  - `sedar1.ipynb` automates data extraction from SEDAR filings, enabling efficient retrieval of company data.
  - Captures and stores extracted filing data in HTML format, making it easy to inspect and validate the information.

- **Data Storage:**
  - **HTML Files:** Each HTML file stores the extracted filing data for individual companies, suitable for manual inspection and validation.

- **Automation:**
  - The project can be integrated with scheduling tools for regular data extraction and updates.

## Technologies Used
- **Programming Languages:** Python  
- **Libraries & Frameworks:**
  - `requests`, `beautifulsoup4` for web crawling and parsing HTML content.

## Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/SEDAR.git
   cd SEDAR

## Usage Guide
 - Run the Web Crawler:

   jupyter notebook sedar1.ipynb

## Configuration
 - Adjust Target URLs: Modify the URLs and extraction logic within sedar1.ipynb to customize the data sources.
 - Output Settings: Update paths for output HTML files as needed directly in the notebook.