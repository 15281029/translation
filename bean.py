# -*- coding: utf-8 -*-

from datetime import datetime

try:
    from db import db
except Exception as e:
    print(e)


def time_():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class Bean(object):

    def getuser(self, token):
        cond = "`token`='{0}'".format(token)
        try:
            user = db.select("`user`,`type`", 'users', cond, one=True)
        except BaseException as e:
            raise e
        return user if user else None

    def adduser(self, user, token, typed):
        dic = dict()
        dic['user'] = user
        dic['token'] = token
        dic['type'] = typed

        try:
            db.insert('users', dic)
            return True
        except BaseException:
            return False

    def writelogs(self, token, ip, message):
        try:
            user = self.getuser(token)
        except BaseException as e:
            raise e
        user = user[0] if user else 'NULL'
        dic = dict()
        dic['time'] = time_()
        dic['user'] = user
        dic['ip'] = ip
        dic['message'] = message

        try:
            db.insert('logs', dic)
            return True
        except BaseException:
            return False

    def getlogs(self, token):
        try:
            user = self.getuser(token)
        except BaseException as e:
            raise e
        if not user:
            return None
        else:
            if user[1] == 0:
                cond = ''
            else:
                cond = "`user`='{0}'".format(user[0])
            try:
                logs = db.select('*', 'logs', cond, one=False)
            except BaseException:
                return None
        return logs


log = Bean()
