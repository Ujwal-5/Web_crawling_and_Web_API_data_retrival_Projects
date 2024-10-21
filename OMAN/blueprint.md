---
name: OMAN Web Crawling Project
description: A project for automated data extraction from Omani websites, with results stored in HTML format.
author: UJWAL S
tags: [web crawling, data extraction, PHP, automation, Oman, HTML]
---

# OMAN Web Crawling Project

## Overview
The OMAN Web Crawling Project automates the process of extracting data from Omani websites. The extracted data is stored in HTML format, providing a structured way to store and view the results of the crawling process.

## Table of Contents
- [Project Structure](#project-structure)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [Configuration](#configuration)

## Project Structure

    OMAN:
    individual_output.html
    oman_crawling.php
    output.html

## Key Features
- **Automated Data Extraction:**
  - `oman_crawling.php` script performs web crawling and extracts data from Omani websites.
  - Extracted data is saved in HTML format, allowing easy viewing and manual processing.

- **Organized Data Storage:**
  - Data is stored in two formats:
    - `individual_output.html` for detailed records.
    - `output.html` for consolidated results.

## Technologies Used
- **Programming Language:** PHP
- **Libraries & Frameworks:**
  - PHP libraries for web scraping (e.g., `cURL`, `DOMDocument`).
- **Tools:** HTML for storing and displaying extracted data.

## Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/OMAN.git
   cd OMAN

## Usage Guide
 - Start the Crawling Process: Run the PHP script to initiate data extraction

    php oman_crawling.php

 - View Extracted Data: Extracted data will be saved in individual_output.html for detailed view and output.html for a consolidated summary.

## Configuration
 - Crawler Settings: Update the target URLs and parsing logic directly in oman_crawling.php to align with the specific structure of the website you are crawling.
 - Output Format: Modify the PHP script if you wish to change how the data is organized or formatted in the HTML files.