import sys

class CommandLineUtils:
    """utils for work with app params"""

    params = {
        '--platform': ['desktop', 'mobile'],
        '-p': ['desktop', 'mobile'],
        '--window': 'next',
        '-w': 'next',
        '--mode': ['background', 'single'],
        '-m': ['background', 'single'],
        '--task': 'value',
        '-t': 'value',
    }
    next_elem = None

    def __init__(self, arr: list):
        self.user_params = arr
        self.data_is_valid = False

    def is_valid(self):
        """control command line"""

        param = 1
        for_while = True

        while for_while:
            

            if param > len(self.user_params):
                for_while = False


print(sys.argv)
