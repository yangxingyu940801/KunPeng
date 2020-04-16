import pandas as pd
import numpy as np
import os
import datetime
from TargetConfig import Config
from target import Target
from newopen import NewOpen
from adjust import Adjust
from check import Check
import paramiko

class Run():
    def __init__(self):
        #self.T0Prods = ["byjx1_zt"]
        self.mails = "18700857889@163.com yang942031628@163.com"
        self.NowDate = datetime.datetime.now().strftime("%Y%m%d")

    def CpFile(self, Products):
        for prod in Products:
            tempPath1 = "/home/jiangtz/KunPeng/2_newopen/{}/datafold/*_open_{}.csv".format(prod, self.NowDate)
            tempPath2 = "/home/jiangtz/KunPeng/3_adjust/{}/datafold/*_adjust_{}.csv".format(prod, self.NowDate)
            os.system("echo |mail -r ProdBasket -s ProdBasket_open_{} -a {} {}".format(self.NowDate, tempPath1, self.mails))
            os.system("echo |mail -r ProdBasket -s ProdBasket_adjust_{} -a {} {}".format(self.NowDate, tempPath2, self.mails))



    def run(self):

        while True:
            CheckFunc = Check()
            CheckFunc.run()

            Products = CheckFunc.Products
            self.CpFile(Products)

            ErrorProducts = CheckFunc.ErrorProducts
            if not len(ErrorProducts):
                print("Products Basket OK")
                os.system("echo Products Basket OK|mail -r ProductsBasket 18700857889@163.com")
                break

            TargetFunc = Target(ErrorProducts)
            TargetFunc.run()

            NewOpenFunc = NewOpen(ErrorProducts)
            NewOpenFunc.run()

            AdjustFunc = Adjust(ErrorProducts)
            AdjustFunc.run()

if __name__ == "__main__":
    job = Run()
    job.run()
