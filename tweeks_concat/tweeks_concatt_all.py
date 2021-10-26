import pandas as pd
import glob
import os


df1 = pd.read_csv('all_twoweeks_1.csv')
df2 = pd.read_csv('all_twoweeks_2.csv')
df3 = pd.read_csv('all_twoweeks_3.csv')
df4 = pd.read_csv('all_twoweeks_4.csv')
df5 = pd.read_csv('all_twoweeks_5.csv')
df6 = pd.read_csv('all_twoweeks_6.csv')

df123456 = pd.concat([df1, df2, df3, df4, df5, df6])


df123456.to_csv('all_twoweeks.csv', index=False)
