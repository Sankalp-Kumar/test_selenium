#from undetected_chromedriver import Chrome, ChromeOptions

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

@st.cache_resource
def get_driver():
    #return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return webdriver.Chrome(service=Service(ChromeDriverManager(version="114.0.5735.90").install()), options=options)
options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--headless')

driver = get_driver()
driver.get("http://www.amazon.com")

st.write(driver.title)
