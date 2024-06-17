from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

service = Service(executable_path=CM().install)

driver = webdriver.Chrome()
driver.get('https://x.com/GordonRamsay')
time.sleep(5)

for i in range(10):
    driver.execute_script("window.scrollBy(0, 2000)")
    time.sleep(2)
    tweets = driver.find_elements(By.CLASS_NAME, 'css-175oi2r')
    for tweet in tweets:
        print('------------------------------------------------------------------')
        content = tweet.find_element(By.CSS_SELECTOR, 'article > span')
        print(content.text)
        break