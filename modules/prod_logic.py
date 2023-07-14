import os
import time
from modules.components import (
    YandexPhoto, YandexReviews, YandexAuth, SearchCompanyYandex,
    CompanySiteYandex, PhoneYandex, RouteYandex
)

from modules.utils import exceptions


def photo_func(browser):
    """work with photo"""

    photo_obj = YandexPhoto(browser)

    # get tab or error of click
    errors = photo_obj.go_to_photo().get('errors')
    if errors != 0:
        return {
            'error': 1
        }

    photo_obj.scroll_content()
    time.sleep(2)
    photo_obj.browser.back_to_main()

    print('photo_func')
    return {
        'error': 0
    }


def review_func(browser):
    """work with review"""

    review_obj = YandexReviews(browser)

    errors = review_obj.go_to_review().get('errors')
    if errors != 0:
        return {
            'error': 1
        }

    review_obj.scroll_content()
    time.sleep(2)
    review_obj.browser.back_to_main()

    print('review_func')
    return {
        'error': 0
    }


def auth_func(browser):
    """work with auth"""

    auth_obj = YandexAuth(browser)
    auth_obj.auth(
        login=os.environ.get('SELENIUM_USERNAME'),
        password=os.environ.get('SELENIUM_PASSWORD')
    )

    print('auth_func')
    return {
        'error': 0
    }


def search_func(browser, my_keywords, my_company, filial):
    """work with search company in yandex maps"""

    search_obj = SearchCompanyYandex(
        browser=browser,
        keyword=my_keywords,
        company=my_company,
        filial=filial
    )
    try:
        # input text and search
        search_obj.input_text()

        # find company and click to card
        company_btn = search_obj.scroll_results()
        company_btn.click()

    except exceptions.CompanyException:
        pass

    except exceptions.ItIsCompanyException:
        pass

    print('search_func')
    return {
        'error': 0
    }


def site_func(browser):
    """func for visit site"""

    site_obj = CompanySiteYandex(browser=browser)
    site_obj.go_site()
    site_obj.close_site()

    print('site_func')
    return {
        'error': 0
    }


def phone_func(browser):
    """func for see phone"""

    phone_obj = PhoneYandex(browser)
    phone_obj.see_phone()
    phone_obj.return_to_start_card()

    print('phone_func')
    return {
        'error': 0
    }


def route_func(browser, my_keywords, my_company, filial):
    """func for making route"""

    try:
        route_obj = RouteYandex(browser, my_keywords,
                                my_company, filial)
        route_obj.make_route()
        # route_obj.input_text()

        # company_btn = route_obj.scroll_results()
        # company_btn.click()
        route_obj.browser.driver.back()

    except exceptions.ItIsCompanyException:
        pass

    print('route_func')
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
    },
    {
        'name': 'site',
        'func': site_func,
        'link': False
    },
    {
        'name': 'phone',
        'func': phone_func,
        'link': False
    },
    {
        'name': 'route',
        'func': route_func,
        'link': False
    }
]
