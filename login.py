import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions

driver = webdriver.Chrome()
driver.get("https://yandex.ru/maps/193/voronezh/?ll=39.198713%2C51.633190&z=16.06")

driver1 = webdriver.Chrome()
driver1.get("https://yandex.ru/maps/193/voronezh/?ll=39.198713%2C51.633190&z=16.06")
driver1.find

# work with auth
class YandexAuth:

    def __init__(self, browser):
        self.browser: webdriver.Chrome = browser

    def get_menu_btn(self):
        """gt burger menu with auth btn"""

        time.sleep(3)

        return self.browser.find_element(by=By.CSS_SELECTOR, value='.user-menu-control')

    def get_enter_btn(self):
        """get enter btn from burger menu"""

        time.sleep(2)

        return self.browser.find_element(by=By.LINK_TEXT, value='Войти')

    def get_input_by_css(self, css_selector):
        """search input by css selector"""

        return self.browser.find_element(
            by=By.CSS_SELECTOR, value=css_selector
        )

    def input_text(self, text, selector='input[type="text"]'):
        """input text to form"""

        time.sleep(3)

        input_form = self.get_input_by_css(selector)
        input_form.send_keys(text)

    def get_push_login_btn(self):
        """get btn for pushing login and input password"""

        time.sleep(4)

        return self.browser \
            .find_element(by=By.CSS_SELECTOR, value='.passp-sign-in-button') \
            .find_element(by=By.CSS_SELECTOR, value='button')


# session 1
auth_class = YandexAuth(driver)
auth_class1 = YandexAuth(driver1)

# go to form
auth_class.get_menu_btn().click()
auth_class.get_enter_btn().click()

auth_class1.get_menu_btn().click()
auth_class1.get_enter_btn().click()

# work with form
auth_class.input_text('y4ndex.genag4448@yandex.ru')
auth_class.get_push_login_btn().click()

auth_class1.input_text('y4ndex.genag4448@yandex.ru')
auth_class1.get_push_login_btn().click()

auth_class.input_text(text='Kkq-MUv-rSw-3zv-!@#', selector='input[type="password"]')
auth_class.get_push_login_btn().click()

auth_class1.input_text(text='Kkq-MUv-rSw-3zv-!@#', selector='input[type="password"]')
auth_class1.get_push_login_btn().click()

# for exit
input()
