#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# File       : target.py
# Author     : chenzhou@goldmine
# Copyright  : ForeSee Fund Pte Ltd
# Description: TODO
# Created    : Thu 16 Feb 2017 09:44:36 AM CST
# Revision   : none
#----------------------------------------------------------------------
import os
import logbook
import numpy as np
import pandas as pd
from commbase.commbase import CommBase

class Target(CommBase):
    def __init__(self):
        super(Target, self).__init__()
        self.logger = logbook.Logger('[Target]')
        self.forbid = ['000686', '600000', '600369', '601939']

    def readSignal(self, date):
        target = None
        for key in self.config:
            if not key.startswith('signal_'): continue
            signal = self.getval(key).replace('%Y%m%d', date).replace('$date',date)
            weight = self.getval(key.replace('signal_', 'weight_'))
            data = {}
            for line in open(signal):
                if line[0] not in ['0', '3', '6']: continue
                items = line.strip().split('|')
                stkid = items[0][0:6]
                if stkid in self.forbid: continue
                data[stkid] = float(items[1])
            data = pd.Series(data)
            data = data / data.sum() * float(weight)
            if target is None: target = data
            else: target = target.add(data, fill_value=0)
        return target

    def work(self, date):
        target = self.readSignal(date)
        target = target / target.sum()
        lastclose  = self.lastclose(date)
        suspending = self.suspending(date)
        for sid in target.index:
            if sid in suspending:          target.ix[sid] = np.nan
            if sid not in lastclose.index: target.ix[sid] = np.nan
        target = target.dropna()
        limit  = float(self.getval('limit'))
        target = target[target>limit]
        univ = pd.read_csv('/13data/moneymaker/product_data/0_getalpha/data/universe_V11',index_col=0)
        univ.index = [s.replace('-','') for s in univ.index]
        univ = univ.loc[date,:]
        target = target[univ]
        target = target / target.sum()
        target.index.name, target.name = 'sid', 'weight'
        outfile = self.getval('outfile').replace("%Y%m%d", date).replace('$date',date)
        if os.path.isfile(outfile): os.system('rm -f '+outfile)
        target.to_csv(outfile, header=True)
        os.chmod(outfile, 0444)

if __name__ == "__main__":
    job = Target()
    job.run()
