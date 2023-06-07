import time

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement


class CompanyException(Exception):
    pass


class Browser:
    """class for create webdriver"""

    company_found: bool

    def __init__(self):
        self.driver = webdriver.Chrome()

    def get_element_from_carousel(self, part_name):
        """get tab from carousel by part_name"""

        if self.company_found is not True:
            raise CompanyException()

        time.sleep(5)
        cards_menu = self.driver.find_elements(
            by=By.CSS_SELECTOR, value='.carousel__content'
        )

        # get elements from all carousel
        photo = None
        for_i = 0
        for_j = 0
        for i in cards_menu:
            if for_i != 0:
                break

            for j in i.find_elements(by=By.CSS_SELECTOR, value='div'):
                if for_j != 0:
                    break

                for k in j.find_elements(by=By.CSS_SELECTOR, value='a'):
                    if k.text == part_name:
                        photo = j
                        for_i = 1
                        for_j = 1
                        break

        # if not found element
        if photo is None:
            raise CompanyException()

        return photo

    def back_to_main(self):
        """go to tab with review of company"""

        back_tab = self.get_element_from_carousel('Обзор')
        back_tab.click()


class YandexPhoto:
    """methods for work with photo in Yandex Map"""

    __photo_tab: WebElement

    def __init__(self, browser: Browser):
        self.browser = browser

    def go_to_photo(self) -> dict:
        """go to tab with photo"""

        if self.browser.company_found is not True:
            # control company
            raise CompanyException()

        # go tab
        self.__photo_tab = self.browser.get_element_from_carousel('Фото и видео')
        try:
            self.__photo_tab.click()
        except exceptions.ElementClickInterceptedException:
            return {
                'errors': 1
            }

        return {
            'errors': 0
        }

    def scroll_content(self):
        """scroll all photo of company"""

        time.sleep(2)
        self.browser.driver.execute_script("document.querySelector('.scroll__container').\
            scrollTo(0, document.querySelector('.scroll__container').scrollHeight)")


class YandexReviews:
    """methods for work with review in Yandex Map"""

    __reviews_tab: WebElement

    def __init__(self, browser: Browser):
        self.browser = browser

    def go_to_review(self) -> dict:
        """go to tab with review"""

        if self.browser.company_found is not True:
            # control company
            raise CompanyException()

        # go to tab
        self.__reviews_tab = self.browser.get_element_from_carousel('Отзывы')
        try:
            self.__reviews_tab.click()
        except exceptions.ElementClickInterceptedException:
            return {
                'errors': 1
            }

        return {
            'errors': 0
        }

    def scroll_content(self):
        """scroll tab with reviews"""

        time.sleep(2)
        self.browser.driver.execute_script("document.querySelector('.scroll__container').\
                    scrollTo(0, document.querySelector('.scroll__container').scrollHeight)")


class YandexAuth:

    def __init__(self, browser: Browser):
        self.browser = browser

    def __get_menu_btn(self):
        """gt burger menu with auth btn"""

        time.sleep(3)

        return self.browser.driver.find_element(
            by=By.CSS_SELECTOR, value='.user-menu-control'
        )

    def __get_enter_btn(self):
        """get enter btn from burger menu"""

        time.sleep(5)

        return self.browser.driver.find_element(by=By.LINK_TEXT, value='Войти')

    def __get_input_by_css(self, css_selector):
        """search input by css selector"""

        time.sleep(2)

        return self.browser.driver.find_element(
            by=By.CSS_SELECTOR, value=css_selector
        )

    def __input_text(self, text, selector='input[type="text"]'):
        """input text to form"""

        time.sleep(3)

        input_form = self.__get_input_by_css(selector)
        input_form.send_keys(text)

    def __get_push_login_btn(self):
        """get btn for pushing login and input password"""

        time.sleep(4)

        return self.browser.driver \
            .find_element(by=By.CSS_SELECTOR, value='.passp-sign-in-button') \
            .find_element(by=By.CSS_SELECTOR, value='button')

    def auth(self, login, password):
        """use all methods for auth in yandex maps"""

        self.__get_menu_btn().click()
        self.__get_enter_btn().click()

        # work with opened form
        self.__input_text(login)
        self.__get_push_login_btn().click()

        self.__input_text(text=password, selector='input[type="password"]')
        self.__get_push_login_btn().click()


class SearchCompanyYandex:
    """search company by keywords"""

    def __init__(self, browser: Browser, keyword: str, company: str):
        self.browser = browser
        self.keyword = keyword
        self.company = company

    def input_text(self):
        """input keyword and company to search"""

        time.sleep(1)

        # input text
        for i in range(10):
            text_box_input = self.browser.driver.find_element(by=By.CSS_SELECTOR, value="input")
            try:
                text_box_input.send_keys(
                    self.keyword
                    + "\ue00d"
                    + self.company
                    + "\ue007"
                )
                return

            except exceptions.StaleElementReferenceException:
                time.sleep(3)

        raise exceptions.StaleElementReferenceException()

    def scroll_results(self):
        """view all results and search"""

        # control: open company or list of company
        elements = self.browser.driver.find_elements(by=By.CSS_SELECTOR, value='.search-snippet-view')
        if len(elements) == 0:
            raise CompanyException()

        time.sleep(3)
        self.browser.driver.execute_script("document.querySelector('.scroll__container').scrollTo(0, 10000)")

        # if list of company
        card = None
        for i in elements:
            for j in i.find_elements(by=By.CSS_SELECTOR, value='div'):
                if j.text == self.company:
                    card = j
                    ActionChains(self.browser.driver) \
                        .scroll_to_element(card) \
                        .perform()

        return card
