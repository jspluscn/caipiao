# !/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import *
from datetime import datetime

try:
    import psycopg2

    db = MySQLDatabase('caipiao', host='127.0.0.1', user='root', passwd='1', port=3306, autorollback=True)
except ImportError:
    db = SqliteDatabase('cp.sqlite')


class BaseModel(Model):
    class Meta:
        database = db
  
class CpModel(BaseModel):   
    id = IntegerField(primary_key=True, verbose_name='id')
    tic_date = CharField(max_length=8, verbose_name='日期')
    w_wan = IntegerField(verbose_name='1')
    w_qian = IntegerField(verbose_name='2')
    w_bai = IntegerField(verbose_name='3')
    w_shi = IntegerField(verbose_name='4')
    w_ge = IntegerField(verbose_name='5')
    tic_num = IntegerField(verbose_name='all')
    qishu = IntegerField(verbose_name='期数')

    created_time = DateTimeField(default=datetime.now, verbose_name='创建时间')


if __name__ == '__main__':
    try:
        CpModel.create_table()
    except Exception, err:
        print err