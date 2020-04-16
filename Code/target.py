#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logbook
import numpy as np
import pandas as pd
import datetime
from multiprocessing import Pool
from commbase.commbase import CommBase

class Target(CommBase):
    def __init__(self, products = []):
        super(Target, self).__init__()
        self.path = "/home/jiangtz/KunPeng/1_target"
        self.logger = logbook.Logger('[Target]')
        self.forbid = []
        if len(products):
            self.products = products

    def readSignal(self, date):
        target = None
        for key in self.config:
            if not key.startswith('signal_'):
                continue
            signal = self.getval(key).replace('%Y%m%d', date).replace('$date',date)
            weight = self.getval(key.replace('signal_', 'weight_'))
            data = {}
            for line in open(signal):
                if line[0] not in ['0', '3', '6']:
                    continue
                items = line.strip().split('|')
                stkid = items[0][0:6]
                if stkid in self.forbid:
                    continue
                data[stkid] = float(items[1])
            data = pd.Series(data)
            data = data / data.sum() * float(weight)
            if target is None:
                target = data
            else:
                target = target.add(data, fill_value=0)
        return target

    def SignalWork(self, prod, date):
        self.GetTradeDays(os.path.join(self.path, prod))
        target = self.readSignal(date)
        target = target / target.sum()
        lastclose  = self.lastclose(date)
        suspending = self.suspending(date)
        for sid in target.index:
            if sid in suspending:
                target.ix[sid] = np.nan
            if sid not in lastclose.index:
                target.ix[sid] = np.nan
        target = target.dropna()
        limit  = float(self.getval('limit'))
        target = target[target>limit]
        univ = pd.read_csv('/13data/QuantData/DailyData/Universe/csv/universe_All',index_col=0)
        univ.index = [str(s).replace('-','') for s in univ.index]
        univ = univ.loc[date,:]
        univ[univ == 1] = True
        univ[univ == 0] = False
        target = target[univ]
        target = target / target.sum()
        target.index.name, target.name = 'sid', 'weight'
        outfile = self.getval('outfile').replace("%Y%m%d", date).replace('$date',date)
        if os.path.isfile(outfile):
            os.system('rm -rf '+outfile)
        target.to_csv(outfile, header=True)
        os.chmod(outfile, 0444)

    def work(self, date):
        for prod in self.products:
            try:
                self.SignalWork(prod, date)
            except:
                print("{} Error".format(prod))



if __name__ == "__main__":
    job = Target()
    job.run()
