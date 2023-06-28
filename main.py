import sys
import time

from modules.components import (
    Browser, CompanyNotFound, CoordinatesException,
)
from modules.sql_query import SqlQuery, TaskMissingException
from modules.log import Logger, ScreenLog
from modules.logic.prod_logic import data_set


def main(main_argument):
    try:
        sql_obj = SqlQuery()

        # get new task
        if main_argument == 'single':
            id_queue = input()
            task = sql_obj.get_data_by_id(id_queue)
        else:
            task = sql_obj.get_data()

        print('\n\n\n\n\n\n\n\n')

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
            browser = Browser(mode='window', id_queue=task.get('id_queue'))
        else:
            browser = Browser(mode=main_argument, id_queue=task.get('id_queue'))

        # generate url and open it
        sql_obj.update_stage_task_other(
            queue_id=task.get('id_queue'), stage='coordinates'
        )
        for_error_stage = 'coordinates'
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

    except TaskMissingException:
        time.sleep(30)

    except CompanyNotFound:
        Logger.write_log(
            'error - not found company in search: ' + str(task.get('id_queue'))
        )

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

    except CoordinatesException:
        Logger.write_log(
            'error - coordinates: ' + str(task.get('id_queue'))
        )

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

    """
    except Exception as ex:
        # view error
        for i in ex.args:
            print(i)

        # write logs
        Logger.write_log(
            'error - ' + for_error_stage + ': ' + str(task.get('id_queue'))
        )

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

        print(ex)

        ScreenLog.save_screens(
            browser, task.get('id_queue'),
            for_error_stage
        )
        browser.driver.quit()

        time.sleep(30)
    """


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
