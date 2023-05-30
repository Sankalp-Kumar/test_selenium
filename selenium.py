from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
                
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


ops =webdriver.ChromeOptions()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=ops)

url = 'https://www.google.com/maps/dir///@12.9568867,77.5861919,15z/data=!4m2!4m1!3e0'

driver.get(url)
