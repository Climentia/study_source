import pandas as pd
import glob
import os


path_list = glob.glob('../../preprocessing_data/1_twoweeks_nv/*.csv')
df0 = pd.read_csv(path_list[3000], names=('year', 'month', 'day', 'time', 'prate', 'nv', 'twoweeks_max'))
df0['id'] = str(os.path.split(path_list[3000])[1]).replace('.csv', '')
df01 = df0[['id', 'year', 'month', 'day', 'time', 'nv', 'twoweeks_max']]
# print(df0)
# for i in range(10)
print(len(path_list)-1)
for i in range(3001, 4000):
    print(str(i) + ':' + path_list[i])
    df1 = pd.read_csv(path_list[i], names=('year', 'month', 'day', 'time', 'prate', 'nv', 'twoweeks_max'))
    df1['id'] = str(os.path.split(path_list[i])[1]).replace('.csv', '')
    df11 = df1[['id', 'year', 'month', 'day', 'time', 'nv', 'twoweeks_max']]
    df01 = pd.concat([df01, df11])
df01.to_csv('all_twoweeks_4.csv', index=False)
