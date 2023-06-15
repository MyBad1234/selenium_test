import os
import sys
import pika
import json
import random
from components import (
    Browser, YandexAuth, YandexPhoto, YandexReviews,
    CompanyException, SearchCompanyYandex, CompanySiteYandex,
    RouteYandex, PhoneYandex, ModeException
)


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


def search_func(browser, my_keywords, my_company):
    """work with search company in yandex maps"""

    search_obj = SearchCompanyYandex(
        browser=browser,
        keyword=my_keywords,
        company=my_company
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


def route_func(browser, my_keywords, my_company):
    """func for making route"""

    route_obj = RouteYandex(browser, my_keywords, my_company)
    route_obj.make_route()
    route_obj.input_text()

    company_btn = route_obj.scroll_results()
    company_btn.click()

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


def callback(ch, method, properties, body):
    # decode body
    data_dict = json.loads(body.decode('utf-8'))

    argument = sys.argv[1]

    browser = Browser(mode=argument)
    browser.driver.get(
        url="https://yandex.ru/maps/193/voronezh/?ll=39.198713%2C51.633190&z=16.06"
    )
    browser.company_found = True

    # get keyword and company
    my_company = data_dict.get('company')
    my_keywords = data_dict.get('keywords')

    # auth
    # data_set[2].get('func')()

    # search
    data_set[3].get('func')(browser, my_keywords, my_company)

    # site
    data_set[4].get('func')(browser)

    # phone
    data_set[5].get('func')(browser)

    # route
    data_set[6].get('func')(browser, my_keywords, my_company)

    # photo and reviews
    data_set[0].get('func')(browser)
    data_set[1].get('func')(browser)

    print('the end')

    browser.driver.close()


def main():
    # set params
    credentials = pika.PlainCredentials(
        username=os.environ.get('RABBITMQ_USERNAME'),
        password=os.environ.get('RABBITMQ_PASSWORD')
    )
    parameters = pika.ConnectionParameters(
        host=os.environ.get('RABBITMQ_HOST', '127.0.0.1'),
        port=8080,
        virtual_host=os.environ.get('RABBITMQ_VHOST'),
        credentials=credentials,
        connection_attempts=10,
        retry_delay=10
    )
    connection = pika.BlockingConnection(parameters)

    # make connection
    channel = connection.channel()
    channel.queue_declare(queue='hello')

    # set func to queue
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    # start
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit()
        except SystemExit:
            sys.exit()

    except IndexError:
        print('error of arguments')
        sys.exit()

    except ModeException:
        print('input correct mode of work for clicker')
        sys.exit()
