import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions

from selenium.webdriver import ActionChains

driver = webdriver.Chrome()
driver.get("https://yandex.ru/maps/193/voronezh/?ll=39.198713%2C51.633190&z=16.06")


def test_write_plus_it():
    text_box_input = driver.find_element(by=By.CSS_SELECTOR, value="input")
    text_box_input.send_keys("Плюс Ай Ти" + Keys.ENTER)


test_write_plus_it()


def get_element_from_carousel(part_name):
    """get tab from carousel by part_name"""

    time.sleep(5)
    cards_menu = driver.find_elements(by=By.CSS_SELECTOR, value='.carousel__content')

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


def go_photo():
    """get photo from card"""

    return get_element_from_carousel('Фото и видео')


# get photos
# photo_elem = go_photo()
# photo_elem.click()


def scroll_content():
    """scroll all photo of company"""

    time.sleep(2)
    driver.execute_script("document.querySelector('.scroll__container').\
            scrollTo(0, document.querySelector('.scroll__container').scrollHeight)")


# scroll_content()


def go_reviews():
    """go to the reviews tab"""

    return get_element_from_carousel('Отзывы')


# get reviews
# reviews_elem = go_reviews()
# reviews_elem.click()
# scroll_content()


# get site
def get_business_menu():
    """find site on card"""
    time.sleep(3)
    try:
        driver.execute_script("document.querySelector('.scroll__container').scrollTo(0, 0)")
        driver.find_element(by=By.CSS_SELECTOR, value='.business-card-title-view__actions') \
            .find_element(by=By.CSS_SELECTOR, value='a').click()
    except exceptions.NoSuchElementException:
        get_business_menu()


# main_page = get_element_from_carousel('Обзор')
# main_page.click()
# get_business_menu()

# time.sleep(10)
# driver.switch_to.window(driver.window_handles[1])
# time.sleep(2)
# driver.close()

# work with bookmarks
def add_bookmarks():
    """find bookmarks and click to this"""

    time.sleep(3)

    # find element
    elems = driver.find_element(by=By.CSS_SELECTOR, value='.business-card-title-view__actions') \
        .find_elements(by=By.CSS_SELECTOR, value='button')

    button = None
    for i in elems:
        if i.accessible_name == 'Закладки':
            button = i

    # if browser not find button
    if button is None:
        raise ValueError()

    return button


def get_close_bookmarks():
    """close window after click to bookmark"""

    return driver.find_element(by=By.CSS_SELECTOR, value='.close-button')


try:
    bookmark = add_bookmarks()
    bookmark.click()

    time.sleep(3)

    # close window
    close_btn = get_close_bookmarks()
    close_btn.click()
except ValueError:
    pass


# work with phone
phone = driver.find_element(by=By.LINK_TEXT,  value='Показать телефон')
phone.


# for exit
input()
