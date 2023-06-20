import pathlib
import datetime


class Logger:
    """class for logs"""

    @staticmethod
    def write_log(text):
        # make path
        log_path = str(pathlib.Path(__file__).parent.parent)
        log_path += '/'
        log_path += 'actions.log'

        # write log
        with open(log_path, 'a+', encoding='utf-8') as file:
            file.write(
                str(datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")) + ": " + text + "\n"
            )


Logger.write_log('oloerlfoerlfoerlf')
