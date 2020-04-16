import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal
import os
import datetime

class Check():
    def __init__(self):
        products = pd.read_csv("/home/jiangtz/KunPeng/ProductName.csv", index_col = 0, header = None)
        self.products = list(products[1])
        self.date = datetime.datetime.now().strftime("%Y%m%d")
        self.ErrorProducts = []
        self.Products = []
        self.prods = []

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
        DateList = pd.read_csv("/13data/QuantData/DailyData/Info/csv/tradedays", index_col = 0)
        DateList = [str(i) for i in DateList["tradedays"] if str(i) < self.date]
        lastdate = DateList[-1]
        for prod in self.products:
            tempPath = "/home/jiangtz/KunPeng/1_target/{}/config".format(prod)
            self.readconfig(tempPath)
            TargetConfig = self.config
            tempPath = "/home/jiangtz/KunPeng/3_adjust/{}/config".format(prod)
            self.readconfig(tempPath)
            AdjustConfig = self.config
            holdfile = AdjustConfig["holdfile"].replace("%Y%m%d", lastdate)
            for i in TargetConfig:
                if "signal" in i and os.path.exists(holdfile):
                    self.prods.append(prod)
                    break

    def run(self):
        self.GetProds()
        for prod in self.prods:
            Adjust = "/home/jiangtz/KunPeng/3_adjust/{}/datafold/{}_adjust_{}.csv".format(prod, prod, self.date)
            if os.path.exists(Adjust):
                self.Products.append(prod)
            else:
                self.ErrorProducts.append(prod)
                print("{} AdjustFile Error!".format(prod))

if __name__ == "__main__":
    func = Check()
    func.run()
