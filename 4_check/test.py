#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal
import os
import datetime

class Check():
    def __init__(self):
        self.path = "/samba/0_Long_Prod/adjust"
        products = pd.read_csv("/home/jiangtz/TestExec/ProductName.csv", index_col = 0, header = None)
        self.products = list(products[1])
        self.date = datetime.datetime.now().strftime("%Y%m%d")
        self.ErrorProducts = []
        self.prods = []
        self.Hedge = ["flb", "ggt_ht", "rzy1_ggt", "yx_jx1", "yx_rj32"]

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

    def GetProds(self):
        for prod in self.products:
            tempPath = "/home/jiangtz/TestExec/1_target/{}/config".format(prod)
            self.readconfig(tempPath)
            for i in self.config:
                if "signal" in i:
                    self.prods.append(prod)
                    break
    def HedgeRun(self, prod):
        tempPath = "/home/jiangtz/TestExec/3_adjust/{}/datafold/{}_adjbuy_{}.csv".format(prod, prod, self.date)
        print(tempPath)
        if os.path.exists(tempPath):
            if prod == "ggt_ht":
                BuyFile = pd.read_csv(tempPath, index_col = 0)
                BuyCheckFile = pd.read_csv("/samba/moneymaker/adjust/{}/{}_adjbuy_{}_MTC.csv".format(prod, prod, self.date), index_col = 0)

                BuyFile = BuyFile[["数量"]]
                BuyCheckFile = BuyCheckFile[["数量"]]

            else:
                BuyFile = pd.read_csv(tempPath, index_col = 0)
                BuyCheckFile = pd.read_csv("/samba/moneymaker/adjust/{}/{}_adjbuy_{}_XT.csv".format(prod, prod, self.date), index_col = 0)

                BuyFile = BuyFile[["shares"]]
                BuyCheckFile = BuyCheckFile[["shares"]]
            temp = BuyFile.sub(BuyCheckFile, fill_value = 0)
            print(temp[temp>0].dropna())
            print(temp[temp<0].dropna())

        tempPath = "/home/jiangtz/TestExec/3_adjust/{}/datafold/{}_adjsel_{}.csv".format(prod, prod, self.date)
        if os.path.exists(tempPath):
            if prod == "ggt_ht":
                BuyFile = pd.read_csv(tempPath, index_col = 0)
                BuyCheckFile = pd.read_csv("/samba/moneymaker/adjust/{}/{}_adjsell_{}_MTC.csv".format(prod, prod, self.date), index_col = 0)

                BuyFile = BuyFile[["数量"]]
                BuyCheckFile = BuyCheckFile[["数量"]]

            else:
                BuyFile = pd.read_csv(tempPath, index_col = 0)
                BuyCheckFile = pd.read_csv("/samba/moneymaker/adjust/{}/{}_adjsel_{}_XT.csv".format(prod, prod, self.date), index_col = 0)

                BuyFile = BuyFile[["shares"]]
                BuyCheckFile = BuyCheckFile[["shares"]]
            temp = BuyFile.sub(BuyCheckFile, fill_value = 0)
            print(temp[temp>0].dropna())
            print(temp[temp<0].dropna())


    def run(self):
        self.GetProds()
        for prod in self.prods:
            print(prod)
            if prod in self.Hedge:
                if prod != "yx_jx1":
                    self.HedgeRun(prod)
                continue
            tempPath = "/home/jiangtz/TestExec/3_adjust/{}/datafold/{}_adjbuy_{}.csv".format(prod, prod, self.date)
            if os.path.exists(tempPath):
                BuyFile = pd.read_csv(tempPath, index_col = 0)
                BuyCheckFile = pd.read_csv(self.path + "/{}/{}_adjbuy_{}.csv".format(prod, prod, self.date), index_col = 0)
                try:
                    assert_frame_equal(BuyFile, BuyCheckFile)
                except:
                    self.ErrorProducts.append(prod)
                    print("{} BuyFile Error!".format(prod))

            tempPath = "/home/jiangtz/TestExec/3_adjust/{}/datafold/{}_adjsel_{}.csv".format(prod, prod, self.date)
            if os.path.exists(tempPath):
                SelFile = pd.read_csv(tempPath, index_col = 0)
                SelCheckFile = pd.read_csv(self.path + "/{}/{}_adjsel_{}.csv".format(prod, prod, self.date), index_col = 0)
                try:
                    assert_frame_equal(BuyFile, BuyCheckFile)
                except:
                    self.ErrorProducts.append(prod)
                    print("{} SelFile Error!".format(prod))

            tempPath = "/home/jiangtz/TestExec/3_adjust/{}/datafold/{}_adjust_{}.csv".format(prod, prod, self.date)
            if os.path.exists(tempPath):
                AdjustFile = pd.read_csv(tempPath, index_col = 0)
                AdjustCheckFile = pd.read_csv(self.path + "/{}/{}_adjust_{}.csv".format(prod, prod, self.date), index_col = 0)
                try:
                    assert_frame_equal(BuyFile, BuyCheckFile)
                except:
                    self.ErrorProducts.append(prod)
                    print("{} AdjustFile Error!".format(prod))

func = Check()
func.run()
