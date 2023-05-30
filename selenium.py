import streamlit as st
from undetected_chromedriver.v2 import ChromeDriverManager
from selenium import webdriver

def scrape_data(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    with webdriver.Chrome(ChromeDriverManager().install(), options=options) as driver:
        driver.get(url)
        # Perform web scraping actions using driver

        # Example: Scrape and display the page title
        title = driver.title
        st.write(f"Page Title: {title}")

def main():
    st.title("Web Scraping with Streamlit and Undetected Chrome Driver")

    # Example scraping URL
    url = st.text_input("Enter a URL to scrape:")
    if st.button("Scrape"):
        scrape_data(url)

if __name__ == "__main__":
    main()
