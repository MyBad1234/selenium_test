# FOR SQL ##############
class TaskMissingException(Exception):
    """if task is not fond"""

    pass


class DataStructException(Exception):
    """if data in db is incorrect (bad struct)"""

    pass


class ProxyNotFoundExceptions(Exception):
    """if there is no proxy"""

    pass


# FOR COMPONENTS
class CompanyException(Exception):
    pass


class ModeException(Exception):
    """error of mode for browser (window, hide or single)"""

    pass


class CoordinatesException(Exception):
    pass


class AuthException(Exception):
    pass


class CompanyNotFound(Exception):
    pass


class ItIsCompanyException(Exception):
    """if clicker open compony(without search)"""

    pass
