from undetected_chromedriver import Chrome, ChromeOptions

# Set up ChromeOptions
options = ChromeOptions()

# Set the path to the Chrome binary
options.binary_location = '/usr/bin/google-chrome-stable'  # Adjust this path if needed

# Set any additional options as needed
# options.add_argument('--headless')  # Uncomment this line if you want to run in headless mode

# Set up the Undetected ChromeDriver
driver = Chrome(options=options)

# Perform your web scraping operations
driver.get("https://www.amazon.in")

title = driver.title

st.write(title)

# Close the browser
driver.quit()
