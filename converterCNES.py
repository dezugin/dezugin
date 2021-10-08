# Program to select unique healthcare workers based in their CNS number in the previous selection of CNES database workers in the city code of Belo Horizonte, MG

import pandas as pd

df = pd.read_csv("CentrosDeSaudeBHComCPFTraduzido.csv")


df = df.drop_duplicates(subset=['CNS_PROF'])
#print(len(df.index))
df.to_csv("ProfissionaisDeSaudeBHUNicos.csv")