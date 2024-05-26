from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Set up the Selenium WebDriver (assume chromedriver is in PATH)
service = Service("F:/projects/vessel-scraper/chromedriver.exe")  # Change to the path where chromedriver is located
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run headless Chrome
driver = webdriver.Chrome(service=service, options=options)

# URL to scrape
url = "https://vesselregister.dnv.com/vesselregister/details/G12916"

# Request the page with Selenium
driver.get(url)

# Wait for the specific data field elements to be loaded
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'item-row'))  # Adjust the class name as needed
)

# Get the page source and parse with BeautifulSoup
page_content = driver.page_source
print(page_content)
soup = BeautifulSoup(page_content, 'html.parser')

# Function to scrape all fields
def scrape_fields(soup):
    data = {}
    for row in soup.find_all('div', class_='item-row'):
        field_name = row.find('div', class_='item-title').get_text(strip=True)
        field_value = row.find('div', class_='item-value').get_text(strip=True)
        data[field_name] = field_value
    return data

# Call the function to scrape fields
vessel_data = scrape_fields(soup)
print(vessel_data)

# Close the driver
driver.quit()
