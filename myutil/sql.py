# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: zbertj

import sqlite3


class SqlHelper(object):
    def __init__(self, url, pwd = None, size = None):
        tmp = url.split(":")
        if len(tmp) == 3:
            self.__type = tmp[0]
            self.__host = tmp[1][2:]
            self.__port = tmp[2]
        elif len(tmp) == 2:
            self.__type = tmp[0]
            self.__host = tmp[1][2:]
            self.__port = 0

        self.conn = sqlite3.connect(self.__host, check_same_thread=False)
        self.cursor = self.conn.cursor()


    def is_table_exist(self, table_name):
        sql_str = "select count() from sqlite_master where type='table' and name = '%s'" % table_name
        res = self.cursor.execute(sql_str).fetchone()
        if res[0] == 0:
            return False
        else:
            return True

    def cale_table_rows(self, table_name):
        sql_str = "select count() from %s " % table_name
        res = self.cursor.execute(sql_str).fetchone()
        return res[0]

    def is_table_have_k_v(self, table_name, key, value):
        sql_str = "select count() from %s where %s = '%s'" % (table_name, key, value)
        # print(sql_str)
        res = self.cursor.execute(sql_str).fetchone()
        # print(res)
        if res[0] == 0:
            return False
        else:
            return True



    def create_a_table(self, sql_str):
        # print(sql_str)
        self.cursor.execute(sql_str)






