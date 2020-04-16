#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# File       : newopen.py
# Author     : chenzhou@goldmine
# Copyright  : ForeSee Fund Pte Ltd
# Description: TODO
# Created    : Thu 16 Feb 2017 01:10:34 PM CST
# Revision   : none
#----------------------------------------------------------------------
import os
import logbook
import numpy as np
import pandas as pd
from xlwt import Workbook
from commbase import df2xls
from commbase.commbase import CommBase

class NewOpen(CommBase):
    def __init__(self):
        super(NewOpen, self).__init__()
        self.logger = logbook.Logger('[NewOpen]')

    def work(self, date):
        book = 1.0 * 1000 * 1000  # 1 million

        pbgj_file = self.getval('pbgj_file').replace('%Y%m%d', date)
        pbgf_file = self.getval('pbgf_file').replace('%Y%m%d', date)
        xtfs_file = self.getval('xtfs_file').replace('%Y%m%d', date)
        try: hspb_file = self.getval('hspb_file').replace('%Y%m%d', date)
        except: hspb_file = None
        try: ztpb_file = self.getval('ztpb_file').replace('%Y%m%d', date)
        except: ztpb_file = None
        try: pbjz_file = self.getval('pbjz_file').replace('%Y%m%d', date)
        except: pbjz_file = None
        try: pbcats_file = self.getval('pbcats_file').replace('%Y%m%d', date)
        except: pbcats_file = None
        
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
        newopen["reptype"] = 0
        newopen['sidcode'] = newopen.index
        newopen = newopen[["market", "sidcode", "reptype", "name", "weight", "shares"]]
        newopen.to_csv(csvfile, encoding='gbk', index=False)

        pbgjdata = newopen.copy()
        pbgjdata.columns = [s.decode('utf-8') for s in ["交易市场", "证券代码", "替换类型", "证券名称", "目标权重", "目标数量"]]
        df2xls(pbgj_file, pbgjdata)

        pbgfdata = newopen[['market', 'sidcode', 'reptype', 'weight', 'shares']]
        pbgfdata.columns = [s.decode('utf-8') for s in ["交易市场", "证券代码", "替换类型", "目标权重", "目标数量"]]
        df2xls(pbgf_file, pbgfdata)

        xtfsdata = newopen[['sidcode', 'name', 'shares', 'weight']].copy()
        xtfsdata["direction"] = 0
        xtfsdata["weight"] = 0.1
        xtfsdata.to_csv(xtfs_file, encoding='gbk', index=False)

        if hspb_file: 
            hspbdata = newopen[['sidcode', 'shares']].copy()
            hspbdata = [(row['sidcode'], row['shares']) for index, row in hspbdata.iterrows()]

            self.write_HSPB(hspb_file, hspbdata)

        if ztpb_file: 
            ztpbdata = newopen[['sidcode', 'name', 'market','shares','weight','reptype']].copy()
            ztpbdata["weight"] = 1
            ztpbdata.columns = [s.decode('utf-8') for s in ["证券代码","证券名称","市场", "每份数量","相对权重","说明"]]
    
            df2xls(ztpb_file, ztpbdata)

        if pbjz_file:
            pbjzdata =   newopen[['market', 'sidcode', 'reptype','name','weight','shares']].copy()
            pbjzdata["weight"] = 1
            pbjzdata = pbjzdata[pbjzdata["shares"]>0] 
            pbjzdata.columns = [s.decode('utf-8') for s in ["市场代码","证券代码","替换类型代码", "证券名称","目标权重","目标数量"]]
            df2xls(pbjz_file, pbjzdata)

        if pbcats_file:
            pbcatsdata =   newopen[['sidcode','name','shares','reptype','market','weight']].copy()
            pbcatsdata["weight"] = 'add'
            pbcatsdata["reptype"] = 0
            pbcatsdata["market"] = 0
            pbcatsdata = pbcatsdata[pbcatsdata['shares']>0]
            df2xls(pbcats_file, pbcatsdata, header = False)

    def write_HSPB(self, filename, rows_buy):
        book_buy = Workbook()
        sheet_buy = book_buy.add_sheet('sheet1')
        sheet_buy.write(0, 0, u'证券代码')
        sheet_buy.write(0, 1, u'证券名称')
        sheet_buy.write(0, 2, u'交易市场')
        sheet_buy.write(0, 3, u'委托方向')
        sheet_buy.write(0, 4, u'价格类型')
        sheet_buy.write(0, 5, u'委托价格')
        sheet_buy.write(0, 6, u'委托数量')
        sheet_buy.write(0, 7, u'委托金额')
        for i, row in enumerate(rows_buy):
            sheet_buy.write(i+1, 0, row[0][:6])
            if(row[0][:2]=='60'):
                sheet_buy.write(i+1, 2, u'1-上交所A')
            else:
                sheet_buy.write(i+1, 2, u'2-深交所A')
            sheet_buy.write(i+1, 3, u'1-买入')
            sheet_buy.write(i+1, 4, u'1-对手盘一档')
            sheet_buy.write(i+1, 6, row[1])
        book_buy.save(filename)

if __name__ == "__main__":
    job = NewOpen()
    job.run()

