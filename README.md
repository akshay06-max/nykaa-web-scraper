# Nykaa E-Commerce Web Scraper

## Task Overview
This project fulfills **(Web Scraping)**. It is a robust Python automation tool designed to extract product names, prices, and customer ratings from Nykaa's e-commerce platform based on user search queries.

## Technical Implementation
To bypass aggressive anti-bot protections (like `403 Forbidden` client blocks), this project utilizes **Selenium WebDriver** instead of basic HTTP request libraries. It drives a headless instance of Google Chrome to properly render dynamic JavaScript components and extract real-time data accurately.

## Files Included
- `selenium_scraper.py`: The core automation and parsing script.
- `nykaa_sunscreen_data.csv`: The final structured data output file.
