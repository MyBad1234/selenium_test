import os
import sys
import time
import mysql
import datetime

from components import (
    Browser, YandexAuth, YandexPhoto, YandexReviews,
    CompanyException, SearchCompanyYandex, CompanySiteYandex,
    RouteYandex, PhoneYandex, ModeException, CompanyNotFound,
    CoordinatesException
)
from sql_query import SqlQuery, TaskMissingException


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


def main():
    try:
        sql_obj = SqlQuery()

        # get new task
        task = sql_obj.get_data()

        # set new status for this task (in work)
        sql_obj.update_status_task(
            task_id=task.get('id_queue'), status='2',
        )

        sql_obj.update_status_task_other(
            queue_id=task.get('id_queue'), status='1'
        )

        # decode body
        argument = sys.argv[1]

        browser = Browser(mode=argument)

        # generate url and open it
        sql_obj.update_stage_task_other(
            queue_id=task.get('id_queue'), stage='coordinates'
        )
        url: str = "https://yandex.ru/maps/?ll="
        url += task.get('x')
        url += '%2C'
        url += task.get('y')
        url += '&z=16.06'

        browser.driver.get(url=url)
        browser.company_found = True

        # get keyword and company
        my_company = task.get('company')
        my_keywords = task.get('keywords')

        # auth
        # data_set[2].get('func')()

        # search
        sql_obj.update_stage_task_other(
            queue_id=task.get('id_queue'), stage='search'
        )
        data_set[3].get('func')(browser, my_keywords, my_company)

        # site
        sql_obj.update_stage_task_other(
            queue_id=task.get('id_queue'), stage='site'
        )
        data_set[4].get('func')(browser)

        # phone
        sql_obj.update_stage_task_other(
            queue_id=task.get('id_queue'), stage='phone'
        )
        data_set[5].get('func')(browser)

        # route
        sql_obj.update_stage_task_other(
            queue_id=task.get('id_queue'), stage='route'
        )
        data_set[6].get('func')(browser, my_keywords, my_company)

        # photo and reviews
        sql_obj.update_stage_task_other(
            queue_id=task.get('id_queue'), stage='photo'
        )
        data_set[0].get('func')(browser)

        sql_obj.update_stage_task_other(
            queue_id=task.get('id_queue'), stage='reviews'
        )
        data_set[1].get('func')(browser)

        print('the end')

        browser.driver.quit()

        # close task with good result
        sql_obj.update_status_task(
            task_id=task.get('id_queue'), status='3',
        )

        sql_obj.update_status_task_other(
            queue_id=task.get('id_queue'), status='2'
        )

        time.sleep(30)

    except TaskMissingException:
        print('not found - sleep')
        time.sleep(30)

    except CompanyNotFound:
        sql_obj.update_status_task(
            task_id=task.get('id_queue'), status='4'
        )

        sql_obj.update_status_task_other(
            queue_id=task.get('id_queue'), status=3,
        )

    except CoordinatesException:
        sql_obj.update_status_task(
            task_id=task.get('id_queue'), status='4'
        )

        sql_obj.update_stage_task_other(
            queue_id=task.get('id_queue'), stage='coordinates',
            status=False
        )


if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        sys.exit()
