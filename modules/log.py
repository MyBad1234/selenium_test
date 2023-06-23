import os
import pathlib
import datetime

from modules.components import Browser


class Logger:
    """class for logs"""

    @staticmethod
    def write_log(text):
        # make path
        log_path = str(pathlib.Path(__file__).parent.parent)
        log_path += '/screens/'
        log_path += 'actions.log'

        # write log
        try:
            with open(log_path, 'a+', encoding='utf-8') as file:
                file.write(
                    str(datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")) + ": " + text + "\n"
                )

        # if the folder is missing
        except FileNotFoundError:
            os.mkdir(
                str(pathlib.Path(__file__).parent.parent) + '/screens/'
            )

            with open(log_path, 'a+', encoding='utf-8') as file:
                file.write(
                    str(datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")) + ": " + text + "\n"
                )


class ScreenLog:
    """functions for saving screen"""

    @staticmethod
    def save_screens(browser: Browser, id_queue, stage):
        screen_path = str(pathlib.Path(__file__).parent.parent)
        screen_path += '/screens/'

        # create folder
        try:
            os.mkdir(screen_path)
        except FileExistsError:
            pass

        # create folder for this queue
        screen_path += str(id_queue)
        screen_path += '/'

        try:
            os.mkdir(screen_path)
        except FileExistsError:
            pass

        screen_path += stage
        screen_path += '.png'
        browser.driver.save_screenshot(screen_path)
