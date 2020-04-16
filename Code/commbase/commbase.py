#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# File       : commbase.py
# Author     : chenzhou@foreseefund.com
# Copyright  : ForeSee Fund Pte Ltd
# Description: TODO
# Created    : Wed 08 Feb 2017 01:29:32 PM CST
# Revision   : none
#----------------------------------------------------------------------
import os
import abc
import sys
import logbook
import pymssql
import psycopg2
import argparse
import numpy as np
import pandas as pd
from datetime import datetime
from pymongo import MongoClient
logbook.set_datetime_format('local')

class CommBase(object):

    def __init__(self):
        self.parse_args()
        self.pgconn = False
        self.mgconn = False

    def parse_args(self):
        products = pd.read_csv("/home/jiangtz/KunPeng/ProductName.csv", index_col = 0, header = None)
        self.products = list(products[1])
        self.logger = logbook.Logger('[CommBase]')
        today = datetime.now().strftime('%Y%m%d')
        parser = argparse.ArgumentParser()
        parser.add_argument('-s', '--start', help='start date(included)', type=str)
        parser.add_argument('-e', '--end'  , help='end date(included); default: today', default=today, nargs='?')
        parser.add_argument('date', help='the date to be workd', default=today, nargs='?')
        parser.add_argument('--offset', type=int, default=0)
        self.args = parser.parse_args()

    def GetTradeDays(self, path = ""):
        self.readconfig(os.path.join(path, 'config'))
        self.startdate = self.getval("startdate")
        self.wind = pymssql.connect('192.168.2.181', 'sa', 'Nm,.hjkl@foresee', 'wind')
        cursor = self.wind.cursor()
        CMD = "SELECT DISTINCT(TRADE_DAYS) FROM ASHARECALENDAR WHERE TRADE_DAYS>={start}"
        cursor.execute(CMD.format(start=self.startdate))
        self.dates = sorted([u[0] for u in cursor])

        dates = [self.args.date]
        if self.args.start and self.args.end:
            dates = [dt.strftime('%Y%m%d') for dt in pd.date_range(self.args.start, self.args.end)]
        index = [self.dates.index(date) for date in dates if date in self.dates]
        self.trdday = [self.dates[di-self.args.offset] for di in index if di >= self.args.offset]


    def exratio(self, date):
        CMD = """
            SELECT
                LEFT(s_info_windcode, 6),
                ISNULL(bonus_share_ratio, 0),
                ISNULL(conversed_ratio, 0),
                ISNULL(consolidate_split_ratio, 1),
                ISNULL(cash_dividend_ratio, 0)
            FROM
                AshareExRightDividendRecord
            WHERE
                EX_DATE={date} AND (LEFT(s_info_windcode, 1) in ('0', '3', '6'))
        """
        columns = ['sid', 'bonus', 'conver', 'consol', 'cash']

        cursor = self.wind.cursor()
        cursor.execute(CMD.format(date=date))
        data = pd.DataFrame(list(cursor))
        if len(data) < 1:
            return None
        data.columns = columns
        data = data.set_index('sid')
        data['exright'] = (1 + data['bonus'] + data['conver']) * data['consol']
        data['cashdiv'] = data['cash']
        return data[['exright', 'cashdiv']].astype(float)

    def connPgSql(self):
        self.pgsql = psycopg2.connect(database="freiburg", user="dany", password="KhalDrogo", host="192.168.1.183",port="5432")
        self.pgconn = True

    def connMongo(self):
        self.mongo = MongoClient('192.168.2.183')
        self.mgdb = self.mongo.stocks_dev
        self.mgdb.authenticate('stocks_dev','stocks_dev')
        self.mgconn = True

    def __del__(self):
        self.wind.close()
        if self.pgconn is True:
            self.pgsql.close()
        if self.mgconn is True:
            self.mongo.close()

    def readconfig(self, configPath):
        self.config = {}
        self.config['startdate'] = '20100101'
        if not os.path.isfile(configPath):
            return
        for line in open(configPath):
            if len(line) < 3 :
                continue
            line = line.replace(' ', '').replace('\t', '')
            if line[0] == '#':
                continue
            if line[0] == '[':
                continue
            if line.find("=") > 0:
                key, val = line.strip().split("=")
                self.config[key] = val
            elif line.find(":") > 0:
                key, val = line.strip().split(":")
                val = val.split("|")
                self.config[key] = val
            else:
                raise Exception("invalid line: "+line)

    def getval(self, key, checkfile=False):
        if key not in self.config:
            raise Exception("invalid key " %key)
        if checkfile and (not os.path.exists(self.config[key])):
            raise Exception("can not found file: "+self.config[key])
        return self.config[key]

    def getdate(self, date, back):
        if date not in self.dates:
            raise Exception("date %s is not a tradable day" %date)
        di = self.dates.index(date)
        if di < back:
            raise Exception("%s back %s days exceeds the first day %s" %(date, back, self.startdate))
        lastdate = self.dates[di-back]
        return lastdate

    def lastdate(self, date):
        return self.getdate(date, back=1)

    def getIndexClose(self, date):
        cursor = self.wind.cursor()
        CMD = "SELECT S_INFO_WINDCODE, S_DQ_CLOSE FROM AINDEXEODPRICES WHERE TRADE_DT={date}"
        cursor.execute(CMD.format(date=date))
        data = pd.DataFrame(list(cursor))
        if len(data) < 5:
            raise Exception("too few records are found")
        self.logger.info('there are {} sids found for index close on {}', len(data), date)
        data.columns = ['sid', 'close']
        data = data.set_index('sid')
        return data['close'].astype(float)

    def lastIndexClose(self, date):
        lastdate = self.lastdate(date)
        return self.getIndexClose(lastdate)

    def currIndexClose(self, date):
        return self.getIndexClose(date)

    def getclose(self, date):
        cursor = self.wind.cursor()
        CMD = "SELECT LEFT(S_INFO_WINDCODE, 6), S_DQ_CLOSE FROM ASHAREEODPRICES WHERE TRADE_DT={date}"
        cursor.execute(CMD.format(date=date))
        data = pd.DataFrame(list(cursor))
        if len(data) < 5:
            raise Exception("too few records are found")
        self.logger.info('there are {} sids found for close on {}', len(data), date)
        data.columns = ['sid', 'close']
        data = data.set_index('sid')
        return data['close'].astype(float)

    def lastclose(self, date):
        lastdate = self.lastdate(date)
        return self.getclose(lastdate)

    def currclose(self, date):
        return self.getclose(date)

    def lastExclose(self, date):
        lastclose = self.lastclose(date)
        exratio   = self.exratio(date)
        if exratio is not None:
            for sid, row in exratio.iterrows():
                if sid not in lastclose.index: continue
                lastclose[sid] = (lastclose[sid]-row['cashdiv']) / row['exright']
        return lastclose

    def suspending(self, date):
        cursor = self.wind.cursor()
        CMD = "SELECT LEFT(S_INFO_WINDCODE, 6) FROM ASHARETRADINGSUSPENSION WHERE S_DQ_SUSPENDDATE={date}"
        cursor.execute(CMD.format(date=date))
        data = map(str, [u[0] for u in list(cursor)])
        self.logger.info('there are {} sids found in suspension on {}', len(data), date)
        return data

    def sharename(self, date):
        cursor = self.wind.cursor()
        CMD = "SELECT LEFT(S_INFO_WINDCODE, 6), S_INFO_NAME FROM ASHAREDESCRIPTION"
        cursor.execute(CMD)
        data = pd.Series({u[0]:u[1] for u in list(cursor)})
        data.index.name, data.name = 'sid', 'name'
        self.logger.info('there are {} sids found for sharename on {}', len(data), date)
        return data

    def bef_work(self):
        self.GetTradeDays()

    @abc.abstractmethod
    def work(self, date):
        raise NotImplementedError

    def aft_work(self):
        pass


    def run(self):
        with logbook.NestedSetup([logbook.NullHandler(), logbook.StreamHandler(sys.stdout, bubble=True)]):
            self.bef_work()
            for date in self.trdday:
                if int(date) < int(self.startdate):
                    continue
                self.logger.info('--------------------------')
                self.logger.info('START  Working on '+date)
                self.work(date)
                self.logger.info('FINISH Working on '+date)
            self.aft_work()
