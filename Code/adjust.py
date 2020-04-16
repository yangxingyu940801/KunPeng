#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logbook
import numpy as np
import pandas as pd
import datetime
from xlwt import Workbook
from commbase import df2xls
from commbase.commbase import CommBase

class Adjust(CommBase):
    def __init__(self, products = []):
        super(Adjust, self).__init__()
        self.path = "/home/jiangtz/KunPeng/3_adjust"
        self.logger = logbook.Logger('[Adjust]')
        if len(products):
            self.products = products

    def readHolding(self, holdfile, typeid = ""):
        if not os.path.isfile(holdfile):
            raise Exception("invalid file "+holdfile)
        holding = {}
        holding = pd.read_csv(holdfile)
        holding.columns = range(len(holding.columns))
        holding = holding[[2,5]]
        holding.columns = ["sid", "holding"]
        holding = holding.set_index('sid')
        holding.index = [str(i).zfill(6) for i in holding.index]
        return holding["holding"]

    def SingleRun(self, prod, date):
        self.GetTradeDays(os.path.join(self.path, prod))
        lastclose  = self.lastExclose(date)
        suspending = self.suspending(date)
        for sid in lastclose.index:
            if sid in suspending:
                lastclose[sid] = 0

        lastdate = self.lastdate(date)
        lastsusp = self.suspending(lastdate)
        for sid in lastclose.index:
            if sid in lastsusp:
                lastclose[sid] = 0

        lastdate = self.lastdate(date)
        target   = self.getval('target').replace('%Y%m%d', date)
        holdfile = self.getval('holdfile').replace('%Y%m%d', lastdate)
        buyfile = self.getval('buyfile').replace('%Y%m%d', date)
        selfile = self.getval('selfile').replace('%Y%m%d', date)
        targetfile = self.getval('csvfile').replace('%Y%m%d', date)
        holding = self.readHolding(holdfile)
        exratio = self.exratio(date)
        if exratio is not None:
            for sid, row in exratio.iterrows():
                if sid in holding.index:
                    holding[sid] = holding[sid]*row['exright']
        holdclose = lastclose.reindex(index=holding.index)
        ## setting target position ##
        targetValue = (holding * holdclose).sum()
        ## setting target position ##
        weight = pd.read_csv(target, dtype=str).set_index('sid')['weight'].astype(float)
        self.logger.info("succeed reading target weight: "+target)
        targetclose = lastclose.reindex(index=weight.index)

        targetStartValue = targetValue
        print("TargetValue: ", targetStartValue)
        targetNewValue = 0
        count = 1
        while True:
            if targetNewValue == 0:
                targetValue = targetStartValue
            else:
                targetValue = targetStartValue * (2 - targetNewValue / targetStartValue)
            adjustlimit = targetValue * 0.0001
            ## setting target position ##
            targetShare = targetValue * weight / targetclose
            delta = targetShare.sub(holding, fill_value=0)
            deltaPos = delta[delta>0]
            deltaNeg = delta[delta<0]
            deltaPos = (deltaPos / 100.0).apply(np.floor) * 100
            deltaNeg = (deltaNeg / 100.0).apply(np.ceil) * 100

            delta = pd.concat([deltaPos,deltaNeg],axis=0)

            deltaclose = lastclose.reindex(index=delta.index)
            delta_val = (delta * deltaclose).apply(np.fabs)
            for index in delta.index:
                if delta_val[index] > adjustlimit:
                    continue
                if index not in targetShare.index:
                    continue
                delta[index] = 0

            adjust = pd.DataFrame()
            adjust["shares"] = delta.astype(int)
            adjust["name"] = self.sharename(date).reindex(index=adjust.index)
            adjust["alpha"] = 0
            adjust["market"] = [1 if s[0]=='6' else 0 for s in adjust.index]
            adjust["reptype"] = 0
            adjust['sidcode'] = adjust.index

            ############################## conflict check ##########################################
            if "priority" in self.config:
                pfile = self.config["priority"].replace("%Y%m%d", date)
                for line in open(pfile):
                    if line[1] != ',':
                        continue
                    items = line.strip().split(",")
                    stk, share = items[1], int(items[5])
                    if stk not in adjust.index:
                        continue
                    if share * adjust.ix[stk, "shares"] < 0:
                        adjust.ix[stk, "shares"] = 0

            adjust = adjust[["market", "sidcode", "reptype", "name", "alpha", "shares"]]
            buy = adjust[adjust.shares > 0].copy()
            sel = adjust[adjust.shares < 0].copy()
            sel["shares"] = (-1) * sel["shares"]
            s_adjust = adjust["shares"]
            targetNew = s_adjust.add(holding, fill_value = 0)
            targetNew = targetNew.astype(int)
            targetNew = targetNew[targetNew > 0]
            targetNewValue = (targetNew * lastclose.reindex(index=targetNew.index)).sum()

            count += 1
            if count > 10:
                os.system("echo {} Adjust Error|mail -r ProductsBasket 18700857889@163.com".format(prod))
                break
            if targetStartValue == 0:
                break
            if abs(targetNewValue / targetStartValue - 1) <= 0.02:
                break

        print("TargetNewValue: ", targetNewValue)
        s_adjust = s_adjust[s_adjust != 0]
        targetNew = s_adjust.add(holding, fill_value = 0)
        targetNew = targetNew.astype(int)
        Target = pd.DataFrame()
        Target['shares'] = list(targetNew)
        Target['sidcode'] = targetNew.index
        Target["AccountType"] = '0'
        Target["Account"] = '880004826673'
        Target["direction"] = '1'
        Target["Algo"] = 'TWAP'
        self.NowTime = datetime.datetime.now().time()
        if self.NowTime < datetime.time(9, 30, 0):
            Target["Para"] = 'beginTime=093000;endTime=093300;limitPrice=0;participateRate=0.0;tradingStyle=1'
        elif self.NowTime < datetime.time(9, 45, 0):
            Minute = self.NowTime.minute + 5
            Target["Para"] = 'beginTime=09{}00;endTime=09{}00;limitPrice=0;participateRate=0.0;tradingStyle=1'.format(str(Minute), str(Minute + 3))
        else:
            Target["Para"] = 'beginTime=144400;endTime=144700;limitPrice=0;participateRate=0.0;tradingStyle=1'

        Target = Target[["AccountType", "Account", "sidcode", "shares", "direction", "Algo", "Para"]]

        Target.to_csv(targetfile, encoding='gbk', index=False, header = False)
        buy = buy[['sidcode', 'name', 'shares']]
        sel = sel[['sidcode', 'name', 'shares']]

        buy["weight"] = 0.1
        sel["weight"] = 0.1

        buy["direction"] = 0
        sel["direction"] = 1

        buy.to_csv(buyfile, encoding='gbk', index=False)
        sel.to_csv(selfile, encoding='gbk', index=False)

    def SignleWork(self, prod, date):
        try:
            self.SingleRun(prod, date)
        except:
            print("{} Error".format(prod))

    def work(self, date):
        for prod in self.products:
            print(prod)
            self.SignleWork(prod, date)

if __name__ == "__main__":
    job = Adjust()
    job.run()

