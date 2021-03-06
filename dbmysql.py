#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: xiaoL-pkav
@version: 2015.1.8 bate 1.0
"""
import MySQLdb
import logging

class DbMysql():
    def __init__(self, db_host, db_port, db_user, db_pwd, db_name):
        self.DB_QUERY = None
        self.DB_CONNECT = None
        self.DB_CURSOR = None
        self.DB_ARGS = None
        self.DB_PORT = db_port
        try:
            self.DB_CONNECT = MySQLdb.connect(db_host, db_user, db_pwd, db_name, charset='utf8')
            self.DB_CURSOR = self.DB_CONNECT.cursor(MySQLdb.cursors.DictCursor)
        except Exception, e:
            logging.debug("数据库连接错误：%s " % e)

    def query(self, query, value):
        self.DB_QUERY = query
        self.DB_ARGS = value
        return self

    def execute_query(self):
        if self.DB_QUERY is None:
            logging.debug("请输入SQL语句")
        try:
            self.DB_CURSOR.execute(self.DB_QUERY, self.DB_ARGS)
        except Exception, e:
            self.DB_CONNECT.rollback()
            logging.debug("数据库执行错误 %s" % e)

    def format_data(self):
        results = self.DB_CURSOR.fetchall()
        return results

    def run(self):
        self.execute_query()
        try:
            self.DB_CONNECT.commit()
            return self.DB_CURSOR.rowcount
        except Exception, e:
            logging.debug("CURD 错误：%s" % e)

    def select(self):
        self.execute_query()
        return self.format_data()

    def reinitialize(self):
        self.DB_QUERY = None

    def release(self):
        self.DB_CONNECT.close()
        
#使用样例 Prepared statements执行查询
db = DbMysql('localhost', '3306', 'root', 'root', 'reg110')
#sql = "select Id,weburl from interface where Id = %s limit 10"
sql = "update interface set whois ='xiaoL' where Id = %s "
params = ['2']
db.query(sql, params).run()