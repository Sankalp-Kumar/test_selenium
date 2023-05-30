import streamlit as st
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_data(url):
    options = ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    with Chrome(options=options) as driver:
        driver.get(url)
        # Perform web scraping actions using driver

        # Example: Scrape and display the page title
        title = driver.title
        st.write(f"Page Title: {title}")

        # Example: Scrape and display a specific element
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))
        st.write(f"Element Text: {element.text}")

def main():
    st.title("Web Scraping with Streamlit and Undetected Chrome Driver")

    # Example scraping URL
    url = st.text_input("Enter a URL to scrape:")
    if st.button("Scrape"):
        scrape_data(url)

if __name__ == "__main__":
    main()
