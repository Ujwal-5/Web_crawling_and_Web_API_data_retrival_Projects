---
name: MAURITIUS Web Crawling Project
description: A project for automated crawling and updating company data from Mauritian websites.
author: UJWAL S
tags: [web crawling, data extraction, Python, automation, Mauritius, company data]
---

# MAURITIUS Web Crawling Project

## Overview
The MAURITIUS Web Crawling Project is designed to automate the extraction and updating of company data from Mauritian websites. It uses Python scripts to crawl and store data, with configurable settings for customized data retrieval.

## Table of Contents
- [Project Structure](#project-structure)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [Configuration](#configuration)

## Project Structure

    MAURITIUS:.
    │   .env
    │   settings.py
    │   start_crawler.bat
    │   start_crawlerX.bat
    │   xsmu.json
    │   xsmucbrdx_update_comp_crawling.py
    │   xsmucbrd_update_comp_crawling.py
    │
    ├───Reports
    └───ReportsX


## Key Features
- **Automated Data Crawling:**
  - Uses Python scripts (`xsmucbrdx_update_comp_crawling.py`, `xsmucbrd_update_comp_crawling.py`) to extract and update company data from Mauritian sources.
  - Scripts are designed for different types of data retrieval and updating needs.

- **Configurable Environment:**
  - `settings.py` allows for easy configuration of the crawler settings.
  - `.env` file stores sensitive data like API keys, ensuring security and flexibility.

- **Batch Automation:**
  - `start_crawler.bat` and `start_crawlerX.bat` provide simple commands to initiate the crawling processes, making automation and scheduling easier.

- **Structured Data Storage:**
  - Outputs and reports are saved in organized directories (`Reports` and `ReportsX`), allowing for easy access and further analysis.

## Technologies Used
- **Programming Language:** Python
- **Libraries & Frameworks:**
  - `requests`, `beautifulsoup4` for HTTP requests and HTML parsing.
  - `dotenv` for handling environment variables.
- **Tools:** Batch scripts for process automation.

## Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/MAURITIUS.git
   cd MAURITIUS

## Usage Guide
 - Start the Crawling Process:
 - Use the batch scripts to start the data crawling:

    start_crawler.bat

 - For alternate crawling methods, use:

    start_crawlerX.bat

- View Extracted Data: Generated reports will be saved in the Reports and ReportsX directories.

## Configuration
 - Crawler Settings: Modify settings.py to adjust the URLs, parameters, and scraping logic.
 - Environment Variables: Use the .env file to store and manage sensitive information like API keys securely.
 - Output Directories: Change the paths in the scripts if you want to store outputs in a different location.