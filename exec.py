# -*- coding: utf-8 -*-


class BaseException(Exception):
    def __init__(self, ErrorInfo):
        self.eInfo = ErrorInfo

    def __str__(self):
        return '<{0}>: {1}'.format(self.__class__.__name__, self.eInfo)

    __repr__ = __str__


class ConnectError(BaseException):
    def __init__(self, ErrorInfo='Remote Connection Error'):
        super(ConnectError, self).__init__(ErrorInfo)


class ServerError(BaseException):
    def __init__(self, ErrorInfo='Server Error'):
        super(ServerError, self).__init__(ErrorInfo)


class DatabaseError(BaseException):
    def __init__(self, ErrorInfo='Database Error'):
        super(DatabaseError, self).__init__(ErrorInfo)
