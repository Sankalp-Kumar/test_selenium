import streamlit as st
from selenium import webdriver

def scrape_data(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode

    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get(url)
        # Perform web scraping actions using driver

        # Example: Scrape and display the page title
    title = driver.title
    st.write(f"Page Title: {title}")

def main():
    st.title("Web Scraping with Selenium on Streamlit Cloud")

    # Example scraping URL
    url = st.text_input("Enter a URL to scrape:")
    if st.button("Scrape"):
        scrape_data(url)

if __name__ == "__main__":
    main()
