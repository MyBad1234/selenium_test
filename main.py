import sys
import time
import traceback
import datetime
from mysql.connector import errors

from modules.components import Browser
from modules.sql_query import SqlQuery
from modules.prod_logic import data_set
from modules.utils import exceptions


def make_url(task_data: dict):
    """make url for yandex map"""

    url: str = "https://yandex.ru/maps/?ll="
    url += task_data.get('x')
    url += '%2C'
    url += task_data.get('y')
    url += '&z=16.06'

    return url


def get_proxy(get_proxy_obj: SqlQuery):
    """get data for using proxy"""

    # get data and set last time update
    data = get_proxy_obj.get_proxy()
    get_proxy_obj.update_proxy(data.get('id'))

    return data


def write_error(error: str) -> str:
    """write error to console with time"""

    now = datetime.datetime.now()

    # get data for write
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    date_str = day + "." + month + "." + year

    hour = str(now.hour)
    minute = str(now.minute)
    second = str(now.second)
    time_str = hour + ":" + minute + ":" + second

    return date_str + " " + time_str + " error: " + error


def write_log(log: str) -> str:
    """write log to console with time"""

    now = datetime.datetime.now()

    # get data for write
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    date_str = day + "." + month + "." + year

    hour = str(now.hour)
    minute = str(now.minute)
    second = str(now.second)
    time_str = hour + ":" + minute + ":" + second

    return date_str + " " + time_str + " log: " + log


def main(main_argument):
    try:
        for_error_stage = 'before'
        sql_obj = SqlQuery()

        # get new task
        if main_argument == 'single':
            id_queue = input()
            task = sql_obj.get_data_by_id(id_queue)
        else:
            task = sql_obj.get_data()

        print('\n\n\n\n\n\n\n\n')
        print(write_log('task: ' + str(task.get('id_queue'))))

        # set new status for this task (in work)
        sql_obj.update_status_task(
            task_id=task.get('id_queue'), status='2',
        )

        sql_obj.update_status_task_other(
            queue_id=task.get('id_queue'), status='1'
        )
        for_error_stage = 'browser'

        # make browser
        if main_argument == 'single':
            browser = Browser(mode='window', id_queue=task.get('id_queue'), proxy=get_proxy(sql_obj))
        else:
            browser = Browser(mode=main_argument, id_queue=task.get('id_queue'), proxy=get_proxy(sql_obj))

        # generate url and open it
        sql_obj.update_stage_task_other(
            queue_id=task.get('id_queue'), stage='coordinates'
        )
        for_error_stage = 'coordinates'

        browser.driver.get(url=make_url(task))
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
        for_error_stage = 'search'
        data_set[3].get('func')(
            browser, my_keywords,
            my_company, task.get('yandex_id')
        )

        # site
        # sql_obj.update_stage_task_other(
        #     queue_id=task.get('id_queue'), stage='site'
        # )
        # for_error_stage = 'site'
        # data_set[4].get('func')(browser)

        # phone
        sql_obj.update_stage_task_other(
            queue_id=task.get('id_queue'), stage='phone'
        )
        for_error_stage = 'phone'
        data_set[5].get('func')(browser)

        # route
        sql_obj.update_stage_task_other(
            queue_id=task.get('id_queue'), stage='route'
        )
        for_error_stage = 'route'
        data_set[6].get('func')(browser, my_keywords,
                                my_company, task.get('yandex_id'))

        # photo and reviews
        sql_obj.update_stage_task_other(
            queue_id=task.get('id_queue'), stage='photo'
        )
        for_error_stage = 'photo'
        data_set[0].get('func')(browser)

        sql_obj.update_stage_task_other(
            queue_id=task.get('id_queue'), stage='reviews'
        )
        for_error_stage = 'reviews'
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

    except errors.ProgrammingError:
        print(write_error('incorrect data for connection to db'))

    except exceptions.TaskMissingException:
        time.sleep(30)

    except exceptions.CompanyNotFound:
        # write error in db
        sql_obj.update_status_task(
            task_id=task.get('id_queue'), status='4'
        )
        sql_obj.update_status_task_other(
            queue_id=task.get('id_queue'), status=3,
        )
        sql_obj.update_stage_task_other(
            task.get('id_queue'), stage='search',
            status=False
        )

        browser.driver.quit()
        time.sleep(30)

    except exceptions.CoordinatesException:
        # write error in db
        sql_obj.update_status_task(
            task_id=task.get('id_queue'), status='4'
        )
        sql_obj.update_status_task_other(
            queue_id=task.get('id_queue'), status=3,
        )
        sql_obj.update_stage_task_other(
            queue_id=task.get('id_queue'), stage='coordinates',
            status=False
        )

        time.sleep(30)

    except Exception:
        # view error
        print(traceback.format_exc())

        # write logs
        sql_obj.update_status_task(
            task_id=task.get('id_queue'), status='4'
        )
        sql_obj.update_status_task_other(
            queue_id=task.get('id_queue'), status=3,
        )
        sql_obj.update_stage_task_other(
            queue_id=task.get('id_queue'), stage=for_error_stage,
            status=False
        )

        browser.driver.quit()

        time.sleep(30)


if __name__ == '__main__':
    try:
        console_argv = sys.argv[1]

        if console_argv == 'window':
            while True:
                main('window')

        elif console_argv == 'docker':
            while True:
                main('docker')

        elif console_argv == 'single':
            main(console_argv)

        else:
            raise IndexError()

    except KeyboardInterrupt:
        sys.exit()

    except IndexError:
        sys.exit()
