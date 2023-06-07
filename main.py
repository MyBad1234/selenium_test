import random
from components import (
    Browser, YandexAuth, YandexPhoto, YandexReviews,
    CompanyException, SearchCompanyYandex, CompanySiteYandex,
    RouteYandex, PhoneYandex
)


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

    print('photo_func')
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

    print('review_func')
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

    print('auth_func')
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

    print('search_func')
    return {
        'error': 0
    }


def site_func():
    """func for visit site"""

    site_obj = CompanySiteYandex(browser=browser)
    site_obj.go_site()
    site_obj.close_site()

    print('site_func')
    return {
        'error': 0
    }


def phone_func():
    """func for see phone"""

    phone_obj = PhoneYandex(browser)
    phone_obj.see_phone()
    phone_obj.return_to_start_card()

    print('phone_func')
    return {
        'error': 0
    }


def route_func():
    """func for making route"""

    route_obj = RouteYandex(browser, 'Воронеж', 'Плюс Ай Ти')
    route_obj.make_route()
    route_obj.input_text()

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
                    browser.back_to_main()

            # work with error's elements
            for i in error_data_set:
                i.get('func')()

        else:
            data_set.pop(rand_int).get('number')

    # control length of a_a
    if len(data_set) == 0:
        logic = False


print('the end')
input()
