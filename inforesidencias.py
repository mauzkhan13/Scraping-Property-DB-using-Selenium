# Import Important Libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import datetime
import random
import os
import time
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import (MoveTargetOutOfBoundsException, NoSuchElementException,
                                        StaleElementReferenceException, TimeoutException,
                                        ElementNotInteractableException)
from selenium.webdriver.chrome.options import Options

# Set up Chrome options
options = Options()
# Add arguments to Chrome options

options.add_argument('--log-level=3')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--disable-infobars')
options.add_argument('--mute-audio')
options.add_argument('--disable-popup-blocking')
options.add_argument('--disable-notifications')
options.add_argument('--disable-translate')
options.add_argument('--disable-logging')
options.add_argument('--disable-default-apps')
options.add_argument('--disable-background-timer-throttling')
options.add_argument('--disable-backgrounding-occluded-windows')
options.add_argument('--disable-breakpad')
options.add_argument('--disable-component-extensions-with-background-pages')
options.add_argument('--disable-features=TranslateUI')
options.add_argument('--disable-hang-monitor')
options.add_argument('--disable-ipc-flooding-protection')
options.add_argument('--disable-prompt-on-repost')
options.add_argument('--disable-renderer-backgrounding')
options.add_argument('--disable-sync')
options.add_argument('--disable-web-resources')
options.add_argument('--enable-automation')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--log-level=3')
options.add_argument('--test-type=webdriver')
options.add_argument('--user-data-dir=/tmp/user-data')
options.add_argument('--v=99')
options.add_argument('--incognito')

# options.add_argument('--headless')  # unComment out the headless option to run the code without the browser mode

PROXY = ''
# Set up proxy
prox = Proxy()
prox.proxy_type = ProxyType.MANUAL
prox.http_proxy = PROXY
prox.ssl_proxy = PROXY

# Set up capabilities
capabilities = webdriver.DesiredCapabilities.CHROME
prox.add_to_capabilities(capabilities)

# Set up Chrome options
options = Options()
options.add_argument('--headless')
# Configure the Chrome driver with proxy and options
driver = webdriver.Chrome(options=options, desired_capabilities=capabilities)

# Set URL and navigate to it
try:
    driver = webdriver.Chrome(options=options)
    url = 'https://www.inforesidencias.com/centros/buscador/residencias?page=108'
    driver.get(url)
    driver.maximize_window()
except Exception as e:
    print(f"An error occurred: {e}")

# Initialize empty lists
name = []
name_addresses = []
postcodes = []
cities = []
provinces = []
plazas = []
phone_numbers = []
website_link_list = []

current_page = 0
page_count = 0

while page_count < 561:

    links = set()
    all_links = driver.find_elements(By.XPATH, '//div[@class="col-md-8"]/div/h2/a')

    for link in all_links:
        links.add(link.get_attribute('href'))

    for url in links:
        sleep(1)
        driver.get(url)

        names = driver.find_element(By.XPATH, '//div[@class="col-md-8"]/div')
        name.append(names.text)

        # Locate the element using the given XPath
        element = driver.find_element(By.XPATH, '//div[@class="col-md-8"]/div[2]/address')
        address_text = element.text
        parts = address_text.split(',')

        name_address = parts[0].strip()
        postcode = ''
        city = ''
        province = ''

        if len(parts) > 1:
            last_part = parts[-1].strip()
            if '(' in last_part and ')' in last_part:
                province_start = last_part.index('(') + 1
                province_end = last_part.index(')')
                province = last_part[province_start:province_end]
                postcode_city = last_part[:province_start - 1].strip()
                postcode_parts = postcode_city.split(' ')
                postcode = postcode_parts[0].strip()
                city = ' '.join(postcode_parts[1:]).strip()
                if len(parts) > 2:
                    name_address += ", " + parts[1].strip()
            elif len(parts) == 2:
                province = last_part.strip()
            else:
                postcode = parts[1].strip().split(' ')[0]
                city = parts[1].strip().split(' ')[1]

        if not name_address:
            name_address = ''
        if not postcode:
            postcode = ''
        if not city:
            city = ''
        if not province:
            province = ''

        name_addresses.append(name_address)
        postcodes.append(postcode)
        cities.append(city)
        provinces.append(province)

        try:
            plaza = driver.find_element(By.XPATH, '//div[@class="col-2"]')
            plazas.append(plaza.text.replace('plazas', '').replace('\n', ''))
        except (
        NoSuchElementException, StaleElementReferenceException, TimeoutException, ElementNotInteractableException,
        MoveTargetOutOfBoundsException):
            plazas.append('Not available')

        try:
            cookies_click = driver.find_element(By.XPATH, '//div[@id="cookiescript_accept"]')
            driver.execute_script("arguments[0].click();", cookies_click)

        except (
        NoSuchElementException, StaleElementReferenceException, TimeoutException, ElementNotInteractableException,
        MoveTargetOutOfBoundsException):
            pass

        try:
            contact_click = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.XPATH, '//div[@class="row p-3 mt-3"]/a')))
            driver.execute_script("arguments[0].click();", contact_click)
        except (
        NoSuchElementException, StaleElementReferenceException, TimeoutException, ElementNotInteractableException,
        MoveTargetOutOfBoundsException):
            pass

        sleep(1)
        try:
            phone_click = driver.find_element(By.XPATH, '//span[contains(text(),"Ver teléfono")]')
            driver.execute_script("arguments[0].click();", phone_click)
        except (
        NoSuchElementException, StaleElementReferenceException, TimeoutException, ElementNotInteractableException,
        MoveTargetOutOfBoundsException):
            pass
        sleep(3)
        try:
            phone = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//div[@id="telefono-contacto-centro"]/a')))
            phone_numbers.append(phone.text)
        except (
        NoSuchElementException, StaleElementReferenceException, TimeoutException, ElementNotInteractableException,
        MoveTargetOutOfBoundsException):
            phone_numbers.append('Not available')

        try:
            original_window_handle = driver.current_window_handle

            website_click = driver.find_element(By.XPATH, '//span[contains(text(),"Visitar web")]')
            driver.execute_script("arguments[0].click();", website_click)

            sleep(3)
            for window_handle in driver.window_handles:
                if window_handle != original_window_handle:
                    driver.switch_to.window(window_handle)
                    new_window_url = driver.current_url
                    website_link_list.append(new_window_url)
                    # print('New window URL:', new_window_url)
                    driver.close()
                    driver.switch_to.window(original_window_handle)
        except (
        NoSuchElementException, StaleElementReferenceException, TimeoutException, ElementNotInteractableException,
        MoveTargetOutOfBoundsException):
            website_link_list.append('Not available')

    next_page_url = f'https://www.inforesidencias.com/centros/buscador/residencias?page={current_page}'
    driver.get(next_page_url)
    print(f"Page number: {current_page}")
    current_page += 1
    page_count += 1

import pandas as pd

data = list(zip(name, name_addresses, postcodes, cities, provinces, plazas, phone_numbers, website_link_list))
columns = ['Name', 'Addresses', 'Postcode', 'City', 'Province', 'Plazas', 'Phone Number', 'Website URL']
df = pd.DataFrame(data, columns=columns)

# Print the DataFrame
print(df)

# Save the DataFrame as an Excel file
df.to_excel('Info Residencias Pycharam.xlsx', index=False)

