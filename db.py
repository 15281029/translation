# -*- coding: utf-8 -*-

from datetime import datetime

import pymysql

from config import DATABASE
from exec import BaseException, DatabaseError


class Database(object):
    def __init__(self):
        try:
            self.database = pymysql.connect(**DATABASE)
            self.cursor = self.database.cursor()
            self.cursor.close()
        except Exception as e:
            raise DatabaseError(e)

    def get_cursor(self):
        self.cursor = self.database.cursor()

    def close_cursor(self):
        self.cursor.close()

    def execute(self, sql):
        try:
            self.get_cursor()
            self.cursor.execute(sql)
            self.database.commit()
            self.close_cursor()
        except Exception as e:
            raise DatabaseError(e)

    def insert(self, table, dic):
        fields = str(tuple([f for f in dic.keys()]))
        values = str(tuple([v for v in dic.values()]))
        fields = fields.replace("'", "`")

        sql = "INSERT INTO `{TABLE}` {FIELDS} VALUES {VALUES}".format(
            TABLE=table, FIELDS=fields, VALUES=values)
        try:
            self.execute(sql)
        except BaseException as e:
            self.close_cursor()
            raise e

    def delete(self, table, cond):
        sql = "DELETE FROM `{TABLE}` WHERE {COND}".format(
            TABLE=table, COND=cond)
        try:
            self.execute(sql)
        except BaseException as e:
            self.close_cursor()
            raise e

    def update(self, table, new, cond):
        sql = "UPDATE `{TABLE}` SET {NEW} WHERE {COND}".format(
            TABLE=table, NEW=new, COND=cond)
        try:
            self.execute(sql)
        except BaseException as e:
            self.close_cursor()
            raise e

    def select(self, field, table, cond, one=True):
        if cond != '':
            sql = "SELECT {FIELD} FROM `{TABLE}` WHERE {COND}".format(
                FIELD=field, TABLE=table, COND=cond)
        else:
            sql = "SELECT {FIELD} FROM `{TABLE}`".format(
                FIELD=field, TABLE=table)
        try:
            self.execute(sql)
            if one:
                data = self.cursor.fetchone()
            else:
                data = self.cursor.fetchall()
            return list(data) if data else []

        except BaseException as e:
            self.close_cursor()
            raise e


try:
    db = Database()
except BaseException as e:
    raise e
