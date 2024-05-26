from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.options import PageLoadStrategy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Set up the Selenium WebDriver (assume chromedriver is in PATH)
service = Service("F:/projects/vessel-scraper/chromedriver.exe")  # Change to the path where chromedriver is located
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run headless Chrome

# Set page load strategy
options.page_load_strategy = 'eager'

driver = webdriver.Chrome(service=service, options=options)


# URL to scrape
# url = "https://vesselregister.dnv.com/vesselregister/details/G12916"
# url = "https://vesselregister.dnv.com/vesselregister/details/G31223"
url = "https://vesselregister.dnv.com/vesselregister/imo/9929247"



# Request the page with Selenium
driver.get(url)
print("driver.get completed")

# Wait for the page to fully load by checking for the presence of the first data element
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'item-row'))
)

# Expand all collapsible sections
collapsible_headers = driver.find_elements(By.CSS_SELECTOR, '.ant-collapse-header')
for header in collapsible_headers:
    header.click()

# Get the page source and parse with BeautifulSoup
page_content = driver.page_source
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
