from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Set up the Chrome webdriver using webdriver_manager
driver = webdriver.Chrome(ChromeDriverManager().install())

# Open the webpage
driver.get('https://www.amazon.com')

# Scrape the title of the webpage
title = driver.title
st.write(title)

# Close the browser
driver.quit()

