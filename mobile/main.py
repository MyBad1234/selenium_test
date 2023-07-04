import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


# Create an instance of ChromeOptions
chrome_options = Options()

# Set the user agent string
chrome_options.add_argument("--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) "
                            "AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/114.0.5735.124 Mobile/15E148 Safari/604.1")

# Instantiate the WebDriver with the ChromeOptions
driver = webdriver.Chrome(options=chrome_options)

# Now you can use the driver to navigate to websites and perform actions
driver.get("https://yandex.ru/maps/")

# close window with application
time.sleep(3)
btn_class = driver.find_element(by=By.PARTIAL_LINK_TEXT, value='Установить Яндекс Карты').get_attribute('class')
btn_class = btn_class.split()[0]

close_class = driver.execute_script("return document.querySelector('." + btn_class + "').parentElement"
                                    ".parentElement.parentElement.querySelector('span').className")

close_class = close_class.split()[0]

close_btn = driver.find_element(by=By.CSS_SELECTOR, value='.' + close_class)
close_btn.click()



input()
driver.quit()
