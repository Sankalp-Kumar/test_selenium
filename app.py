import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def scrape_data(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode

    # Specify the path to the ChromeDriver binary
    chromedriver_path = '/home/appuser/.wdm/drivers/chromedriver/linux64/113.0.5672.63/chromedriver'

    # Set up the webdriver with the executable_path parameter
    driver = webdriver.Chrome(executable_path=chromedriver_path)

    #driver = webdriver.Chrome(ChromeDriverManager().install())

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
