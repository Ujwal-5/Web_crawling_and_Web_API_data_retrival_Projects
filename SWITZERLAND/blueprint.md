---
name: SWITZERLAND Web Crawling Project
description: A project for automated data extraction from Swiss websites, with results stored in JSON and HTML formats.
author: UJWAL S
tags: [web crawling, data extraction, Python, automation, Switzerland, JSON, HTML, AWS S3]
---

# SWITZERLAND Web Crawling Project

## Overview
The SWITZERLAND Web Crawling Project automates the process of extracting data from Swiss websites. The extracted data is stored in JSON and HTML formats, providing structured access for further analysis or integration. The project also includes functionality for monitoring and saving data to an S3 bucket.

## Table of Contents
- [Project Structure](#project-structure)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [Configuration](#configuration)

## Project Structure

    SWITZERLAND:.
    │   .env
    │   custom_request.py
    │   data.json
    │   database.py
    │   env_setup.bat
    │   folder.py
    │   moniter.py
    │   requirements.txt
    │   s3_move.py
    │   save_file.py
    │   settings.py
    │   start_crawler.bat
    │   xschregx_crawling.py
    │   xschregx_moniter.json
    │
    └───html
            CHE-156.673.513.html
            CHE-216.194.767.html
            CHE-408.878.014.html
            CHE-439.706.828.html


## Key Features
- **Automated Data Extraction:**
  - `xschregx_crawling.py` is the primary script for extracting data from Swiss websites.
  - Custom HTTP requests are handled by `custom_request.py` for advanced scraping needs.

- **Monitoring and Logging:**
  - `moniter.py` and `xschregx_moniter.json` help keep track of the crawling process and monitor changes in data.

- **Data Storage and Management:**
  - Extracted data is saved in `data.json` for structured access.
  - Raw HTML responses are stored in the `html` folder for reference.

- **AWS S3 Integration:**
  - `s3_move.py` facilitates moving extracted data to an S3 bucket for cloud storage.

## Technologies Used
- **Programming Language:** Python
- **Libraries & Frameworks:** 
  - Requests for HTTP requests
  - BeautifulSoup for HTML parsing
  - Boto3 for AWS S3 interactions
- **Tools:** AWS S3, .env for environment management

## Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/SWITZERLAND.git
   cd SWITZERLAND

## Usage Guide
 - Start the Crawling Process:

    python xschregx_crawling.py

 - Upload Data to S3:

    python s3_move.py

## Configuration
 - Crawling Settings: Adjust target URLs, user agents, and other crawling settings within settings.py and custom_request.py.
 - Environment Variables: Set your AWS credentials and other secrets in the .env file.
 - Output Location: By default, data is saved in data.json and html folder. Modify paths in the scripts if you want to change the output locations.
