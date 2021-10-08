# concatenator to concatenate individual employment history files in one csv for analysis, also to proper comma separated values
import pandas as pd
import os
import glob
path = '/home/dez/Downloads/historico/'
csv_files = glob.glob(os.path.join(path, "*.csv"))
res = None
count = 0
for f in csv_files:
    if res is None:
      res = pd.read_csv(f, sep=';')
    else:
      res = pd.concat([res, pd.read_csv(f, sep=';')])  
    count = count + 1
    print(count)
res.to_csv("HistoricoMedicoBH.csv")