#from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
# Set up ChromeOptions
#options = ChromeOptions()

# Set the path to the Chrome binary
#options.binary_location = '/usr/bin/google-chrome-stable'  # Adjust this path if needed

# Set any additional options as needed
# options.add_argument('--headless')  # Uncomment this line if you want to run in headless mode

# Set up the Undetected ChromeDriver
#driver = Chrome(options=options)

# Perform your web scraping operations
#driver.get("https://www.amazon.in")

#title = driver.title

#st.write(title)

# Close the browser
#driver.quit()

import streamlit as st

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@st.experimental_singleton
def get_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--headless')

driver = get_driver()
driver.get('https://www.amazon.in/')

driver.find_element(By.ID,value='twotabsearchtextbox').send_keys('snacks')
driver.find_element(By.ID,value='nav-search-submit-text').click()
driver.find_element(By.XPATH, value="//span[@class='nav-line-2 nav-progressive-content']").click()
ele = driver.find_elements(By.XPATH,value='//div[@data-component-type="s-search-result"]/descendant::a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]')
for i in ele:
    print(i.text)
#st.write(driver.title)
