# Web Scraper for Container Ship Data

A Python-based web scraper using **Selenium** and **Beautiful Soup** to collect cargo, maintenance, and engine data on over 10,000 container ships. Created for the shipping data analysis company **Linerlytica**, this scraper gathers vessel data from the online **Det Norske Veritas (DNV)** registry.

## Features
- Collects data on cargo, maintenance, and engine specifics of container ships
- Outputs structured data for streamlined analysis

## Setup Instructions

### Prerequisites
- **Python 3.x**
- **Selenium**
- **Beautiful Soup**
- **Pandas**

### Files Needed
- `DNV.xlsx`: a file with a list of DNV IDs

   - Create a `.xlsx` file named `DNV.xlsx`
   - Place the DNV IDs under a column with the header `link1`

### Running the Scraper

1. Ensure `DNV.xlsx` is in the root directory of the project.
2. Run the following command:

   ```bash
   python scraper.py
