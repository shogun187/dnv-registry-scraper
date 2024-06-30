import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from VesselNotFound import VesselNotFoundException


def setup_driver():
    # Set up the Selenium WebDriver (assume chromedriver is in PATH)
    service = Service("F:/projects/vessel-scraper/chromedriver.exe")  # Change to the path where chromedriver is located
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run headless Chrome
    options.add_argument("start-maximized")

    # Set page load strategy
    options.page_load_strategy = 'eager'

    driver = webdriver.Chrome(service=service, options=options)

    print("WebDriver Created")

    driver.delete_all_cookies()

    print("Cookies deleted")

    return driver


def scrape_fields(soup):
    vessel_data = {}
    for row in soup.find_all('div', class_='item-row'):
        field_name = row.find('div', class_='item-title').get_text(strip=True)
        field_value = row.find('div', class_='item-value').get_text(strip=True)
        vessel_data[field_name] = field_value
    return vessel_data


def scrape_vessel_data(url, driver):
    driver.get(url)

    failed_url = "https://vesselregister.dnv.com/vesselregister"

    # Wait for the page to fully load by checking for the presence of the first data element
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, 'item-row'))
    # )

    WebDriverWait(driver, 120).until(
        lambda d: d.current_url == failed_url or d.find_elements(By.CLASS_NAME, 'item-row')
    )

    if driver.current_url == "https://vesselregister.dnv.com/vesselregister":
        raise VesselNotFoundException()

    # Expand all collapsible sections
    collapsible_headers = driver.find_elements(By.CSS_SELECTOR, '.ant-collapse-header')
    for header in collapsible_headers:
        if 'ant-collapse-item-active' not in header.get_attribute('class'):
            driver.execute_script("arguments[0].scrollIntoView(true);", header)
            time.sleep(0.01)
            header.click()
            time.sleep(0.01)

    # Get the page source and parse with BeautifulSoup
    page_content = driver.page_source
    soup = BeautifulSoup(page_content, 'html.parser')

    return scrape_fields(soup)


# Function to scrape all fields
def scrape_fields(soup):
    data = {}

    # Extracts most of the data except tabled stuff
    for row in soup.find_all('div', class_='item-row'):
        field_name = row.find('div', class_='item-title').get_text(strip=True).rstrip(':')
        field_value = row.find('div', class_='item-value').get_text(strip=True)
        data[field_name] = field_value


    # Extract specific span values inside the header to isolate class_notation
    class_notation_spans = soup.select(
        '.ant-collapse-header + .ant-collapse-content .ant-collapse-content-box span')

    # This string will appear as it has the same classes, so manually remove
    class_notation_values = [span.get_text(strip=True) for span in class_notation_spans if
                             span.get_text(strip=True) != 'No overdue conditions found.']

    # Join class notation values using |
    if class_notation_values:
        data['Class Notations'] = ' | '.join(class_notation_values)


    # Extract propulsion engine name and designer from the table
    for row in soup.select('tbody.ant-table-tbody tr.ant-table-row'):
        cells = row.find_all('td')
        if len(cells) >= 3:
            item_name = cells[0].get_text(strip=True)
            item_type = cells[1].get_text(strip=True)
            item_designer = cells[2].get_text(strip=True)

            if 'Propulsion engine' in item_name:
                data['Propulsion Engine Name'] = item_type
                data['Propulsion Engine Designer'] = item_designer

    return data


def main(input_excel, output_excel, failed_urls_csv):
    url_df = pd.read_excel(input_excel)

    # Initialize the WebDriver
    driver = setup_driver()

    all_vessel_data = []
    index = 0
    failed_urls = []

    for url in url_df['link1']:  # Assuming the column containing URLs is named 'link1'
        index += 1
        start_time = time.time()  # Record the start time
        try:
            print(f"{index}. Scraping data for {url}")

            vessel_data = scrape_vessel_data(url, driver)
            all_vessel_data.append(vessel_data)

        except VesselNotFoundException as e:
            print("Vessel not found")
            continue

        except Exception as e:
            print(f"Failed due to {e}")
            failed_urls.append(url)
            continue

        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Done in {time_taken:.2f}s")

    print("______________________")
    print("______________________")
    print("______________________")
    print("Retrying failed urls")
    print("______________________")
    print("______________________")
    print("______________________")
    print("______________________")


    index = 0

    for failed_url in failed_urls:

        index += 1
        start_time = time.time()  # Record the start time
        try:
            print(f"{index}. Scraping data for failed url {url}")

            vessel_data = scrape_vessel_data(url, driver)
            all_vessel_data.append(vessel_data)

        except VesselNotFoundException as e:
            print("Vessel not found")
            continue

        except Exception as e:
            print(f"Failed due to {e}")
            continue

        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Done in {time_taken:.2f}s")
        failed_urls.remove(failed_url)





    # Close the driver
    driver.quit()

    # Create a DataFrame from the list of dictionaries
    combined_df = pd.DataFrame(all_vessel_data)

    # Save the combined DataFrame to an Excel file
    combined_df.to_excel(output_excel, index=False)

    print(f"Vessel data has been saved to {output_excel}")


    # Save the failed URLs to a CSV file
    failed_urls_df = pd.DataFrame(failed_urls, columns=['failed_url'])
    failed_urls_df.to_csv(failed_urls_csv, index=False)
    print(f"Failed URLs have been saved to {failed_urls_csv}")

if __name__ == "__main__":
    input_excel = 'DNV.xlsx'  # Path to the input Excel file containing URLs
    output_excel = 'combined_vessel_data.xlsx'  # Path to the output Excel file
    failed_urls_csv = 'failed_urls.csv'
    main(input_excel, output_excel, failed_urls_csv)

    # BEST TO CLEAR CHROME BROWSER CACHE BEFORE RUNNING
