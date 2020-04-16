#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logbook
import numpy as np
import pandas as pd
from xlwt import Workbook
from commbase import df2xls
from commbase.commbase import CommBase

class NewOpen(CommBase):
    def __init__(self, products = []):
        super(NewOpen, self).__init__()
        self.path = "/home/jiangtz/KunPeng/2_newopen"
        self.logger = logbook.Logger('[NewOpen]')
        if len(products):
            self.products = products


    def SignalWork(self, prod, date):
        self.GetTradeDays(os.path.join(self.path, prod))
        book = 1.0 * 1000 * 1000  # 1 million

        csvfile = self.getval('csvfile').replace('%Y%m%d', date)
        target = self.getval('target').replace('%Y%m%d', date)

        newopen = pd.read_csv(target, dtype=str).set_index('sid')
        self.logger.info("succeed reading "+target)

        newopen["weight"] = newopen["weight"].astype(float)
        newopen['lastclose'] = self.lastExclose(date).reindex(index=newopen.index)
        newopen['shares'] = (book * newopen['weight'] / newopen['lastclose'] / 100).apply(np.round) * 100
        newopen['shares'] = newopen['shares'].astype(int)
        newopen["name"] = self.sharename(date).reindex(index=newopen.index)
        newopen["market"] = [1 if s[0]=='6' else 0 for s in newopen.index]
        newopen['sidcode'] = newopen.index
        newopen["buyprice"] = 0.0
        newopen["sellprice"] = 0.0
        newopen["Remark"] = "open"
        newopen = newopen[newopen['shares']!=0]
        newopen = newopen[["sidcode", "name", "shares", "buyprice", "sellprice", "Remark"]]
        newopen.to_csv(csvfile, encoding='gbk', index=False, header = False)

    def work(self, date):
        for prod in self.products:
            try:
                self.SignalWork(prod, date)
            except:
                print("{} Error".format(prod))

if __name__ == "__main__":
    job = NewOpen()
    job.run()

