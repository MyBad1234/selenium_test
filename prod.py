import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions

from selenium.webdriver import ActionChains

driver = webdriver.Chrome()
driver.get("https://yandex.ru/maps/193/voronezh/?ll=39.206649%2C51.657446&z=13.63")


def write__main_words():
    """write Voronezh and advertising agency to search"""

    time.sleep(1)
    text_box_input = driver.find_element(by=By.CSS_SELECTOR, value="input")
    text_box_input.send_keys("Воронеж" + Keys.ENTER)
    time.sleep(4)
    text_box_input.send_keys(
        "\ue003"
        + "\ue003"
        + "\ue003"
        + "\ue003"
        + "\ue003"
        + "\ue003"
        + "\ue003"
        + "Рекламное агентство"
        + Keys.ENTER
    )

    return text_box_input


text_box = write__main_words()


def get_scroll_results():
    time.sleep(3)
    driver.execute_script("document.querySelector('.scroll__container').scrollTo(0, 10000)")

    time.sleep(3)
    driver.execute_script("document.querySelector('.scroll__container').scrollTo(0, 20000)")

    time.sleep(3)
    driver.execute_script("document.querySelector('.scroll__container').scrollTo(0, 30000)")

    time.sleep(3)
    driver.execute_script("document.querySelector('.scroll__container').scrollTo(0, 40000)")

    time.sleep(3)
    driver.execute_script("document.querySelector('.scroll__container').scrollTo(0, 50000)")

    lol = None
    for i in driver.find_elements(by=By.CSS_SELECTOR, value='.search-snippet-view'):
        for j in i.find_elements(by=By.CSS_SELECTOR, value='div'):
            if j.text == 'Плюс Ай Ти':
                # print('wow')
                # print(j)
                # print(j.text)
                # print(j.get_attribute('innerHTML'))
                # print('\n\n\n\n')

                lol = j
                ActionChains(driver) \
                    .scroll_to_element(lol) \
                    .perform()

    # print(lol.get_attribute('class'))
    return lol


elem = get_scroll_results()
elem.click()


def go_photo():
    """get photo from card"""

    time.sleep(3)
    card_menu = driver.find_element(by=By.CSS_SELECTOR, value='.carousel__content')

    for i in card_menu.find_elements(by=By.CSS_SELECTOR, value='a'):
        if i.text == 'Фото и видео':
            photo = i
            break

    return photo


photo_elem = go_photo()
photo_elem.click()


def get_business_menu():
    """find site on card"""
    time.sleep(3)
    try:
        driver.find_element(by=By.CSS_SELECTOR, value='.business-card-title-view__actions') \
            .find_element(by=By.CSS_SELECTOR, value='a').click()
    except exceptions.NoSuchElementException:
        get_business_menu()


# get_business_menu()
input()
