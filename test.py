import pandas as pd
import numpy as np
import os

path = "/home/jiangtz/KunPeng"
for root, dirs, files in os.walk(path):
    for i in files:
        if "20200409" in i:
            os.system("rm -rf " + os.path.join(root, i))
