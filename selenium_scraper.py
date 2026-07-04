from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

def scrape_nykaa_with_selenium(search_query, max_pages=1):
    # Set up Chrome options
    chrome_options = Options()
    # Comment out the next line if you want to visibly see the browser open and click through pages!
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

    # Initialize the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    scraped_data = []

    try:
        for page in range(1, max_pages + 1):
            url = f"https://www.nykaa.com/search/result/?q={search_query}&page_no={page}"
            print(f"Loading page {page}: {url}")
            
            driver.get(url)
            
            # Wait for the JavaScript to render the page content (adjust time if your internet is slow)
            time.sleep(5) 
            
            # NOTE: These class names are placeholders. You will need to inspect the Nykaa 
            # website and replace 'css-d5z3ro', etc., with the current live class names.
            
            # Find all product cards on the page
            product_cards = driver.find_elements(By.CLASS_NAME, "css-d5z3ro") # Placeholder wrapper class
            
            print(f"Found {len(product_cards)} products on page {page}.")
            
            for card in product_cards:
                try:
                    # 1. Product Name
                    name_element = card.find_element(By.CLASS_NAME, "css-xrzmfa") # Placeholder class
                    name = name_element.text
                    
                    # 2. Price
                    price_element = card.find_element(By.CLASS_NAME, "css-111z9ua") # Placeholder class
                    price = price_element.text
                    
                    # 3. Rating (Wrap in try/except because some products might not have ratings yet)
                    try:
                        rating_element = card.find_element(By.CLASS_NAME, "css-mco2vc") # Placeholder class
                        rating = rating_element.text
                    except:
                        rating = "No Rating"
                        
                    if name:
                        scraped_data.append({
                            "Product Name": name,
                            "Price": price,
                            "Rating": rating
                        })
                except Exception as e:
                    # Skip products that don't load properly
                    continue
                    
    finally:
        # Always close the browser when done
        driver.quit()
        
    return scraped_data

def save_to_csv(data, filename="nykaa_products.csv"):
    if not data:
        print("No data extracted. Please check the CSS Class names in the script!")
        return

    fieldnames = ["Product Name", "Price", "Rating"]
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        
    print(f"Success! Saved {len(data)} products to '{filename}'.")

if __name__ == "__main__":
    query = "sunscreen" 
    print(f"Starting Selenium scraping task for: {query.capitalize()}")
    
    product_data = scrape_nykaa_with_selenium(search_query=query, max_pages=1)
    save_to_csv(product_data, filename=f"nykaa_{query}_data.csv")