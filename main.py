import time
import random

import selenium.webdriver.remote.webelement
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions

from selenium.webdriver import ActionChains


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

        return photo

    def back_to_main(self):
        """go to tab with review of company"""

        back_tab = self.get_element_from_carousel('Обзор')
        back_tab.click()


# get photos
class YandexPhoto:
    """methods for work with photo in Yandex Map"""

    __photo_tab: selenium.webdriver.remote.webelement.WebElement

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


class YandexReviews:
    """methods for work with review in Yandex Map"""

    __reviews_tab: selenium.webdriver.remote.webelement.WebElement

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


# photo_elem = go_photo()
# photo_elem.click()


# def scroll_content():
    """scroll all photo of company"""

#    time.sleep(2)
#    driver.execute_script("document.querySelector('.scroll__container').\
#            scrollTo(0, document.querySelector('.scroll__container').scrollHeight)")


# scroll_content()


# def go_reviews():
    """go to the reviews tab"""

#    return get_element_from_carousel('Отзывы')


# get reviews
"""
reviews_elem = go_reviews()
reviews_elem.click()
scroll_content()
"""


# get site
"""
def get_business_menu():
    '''find site on card'''
    time.sleep(3)
    try:
        driver.execute_script("document.querySelector('.scroll__container').scrollTo(0, 0)")
        driver.find_element(by=By.CSS_SELECTOR, value='.business-card-title-view__actions') \
            .find_element(by=By.CSS_SELECTOR, value='a').click()
    except exceptions.NoSuchElementException:
        get_business_menu()
"""


# main_page = get_element_from_carousel('Обзор')
# main_page.click()
# get_business_menu()

# time.sleep(10)
# window = driver.current_window_handle
# driver.switch_to_window(window)
# driver.close()


# get_business_menu()

browser = Browser()
browser.driver.get(
    url="https://yandex.ru/maps/193/voronezh/?ll=39.198713%2C51.633190&z=16.06"
)
browser.company_found = True


def photo_func():
    """work with photo"""

    photo_obj = YandexPhoto(browser)

    # get tab or error of click
    errors = photo_obj.go_to_photo().get('errors')
    if errors != 0:
        return {
            'error': 1
        }

    photo_obj.scroll_content()

    return {
        'error': 0
    }


def review_func():
    """work with review"""

    review_obj = YandexReviews(browser)

    errors = review_obj.go_to_review().get('errors')
    if errors != 0:
        return {
            'error': 1
        }

    review_obj.scroll_content()

    return {
        'error': 0
    }


def auth_func():
    """work with auth"""

    auth_obj = YandexAuth(browser)
    auth_obj.auth(
        login='y4ndex.genag4448@yandex.ru',
        password='Kkq-MUv-rSw-3zv-!@#'
    )

    return {
        'error': 0
    }


def search_func():
    """work with search company in yandex maps"""

    search_obj = SearchCompanyYandex(
        browser=browser,
        keyword='Воронеж',
        company='Плюс Ай Ти'
    )
    search_obj.input_text()

    # find company and click to card
    try:
        company_btn = search_obj.scroll_results()
        company_btn.click()

    except CompanyException:
        pass

    return {
        'error': 0
    }


data_set = [
    {
        'name': 'photo',
        'func': photo_func,
        'link': True
    },
    {
        'name': 'reviews',
        'func': review_func,
        'link': True
    },
    {
        'name': 'auth',
        'func': auth_func,
        'link': False
    },
    {
        'name': 'search',
        'func': search_func,
        'link': False
    }
]
error_data_set = []

logic = True
first = 0
while logic:
    # get random elem
    if first == 0:
        rand_int = 2
        first = 1
    elif first == 1:
        rand_int = 2
        first = 2
    else:
        rand_int = random.randint(0, len(data_set) - 1)

    # control on error
    if data_set[rand_int].get('func')().get('error') == 1:
        error_data_set.append(
            data_set.pop(rand_int)
        )
    else:
        if data_set[rand_int].get('link'):
            data_set.pop(rand_int)

            # work with linked elements
            while_pass = True
            while while_pass:
                for_while_pass = 0
                for i in range(len(data_set)):
                    if data_set[i].get('link'):
                        for_while_pass += 1
                        data_set.pop(i).get('func')()
                        break

                if for_while_pass == 0:
                    while_pass = False

            # work with error's elements
            for i in error_data_set:
                i.get('func')()

        else:
            data_set.pop(rand_int).get('number')

    # control length of a_a
    if len(data_set) == 0:
        logic = False


input()
