import pandas as pd
import numpy as np
import os


def read_pa(path, tt2):
    df = pd.read_csv(path, encoding='cp932')
    # print(df)
    df[str(tt2)] = df['nv']
    df2 = df[['id', str(tt2)]]
    return df2


def func_check(x):
    if x >= 0.15:
        return 1
    elif x < 0.15:
        return 0
    else:
        return np.nan


for i in range(12):
    month = i + 1
    path_month = 'H:/study/preprocessing_data/weather_data_15/' + str(month) + '月/'
    path_month_cheack = os.path.exists(path_month)
    if path_month_cheack == False:
        os.makedirs(path_month)
    if month < 8:
        year = 14
    else:
        year = 13
    if month == 2:
        day_max = 28
    elif month == 4 or month == 6 or month == 9 or month == 11:
        day_max = 30
    else:
        day_max = 31
    for j in range(day_max):
        day = j+1
        read_path0 = 'H:/study/preprocessing_data/mesh_com/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/' + 'mesh_com' + str(year) + str(month) + str(day) + str(6.5) + '.csv'
        df0 = read_pa(read_path0, 9.0)
        for tt in range(12):
            tt2 = 10.0 + 0.5 * tt
            read_path = 'H:/study/preprocessing_data/mesh_com/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/' + 'mesh_com' + str(year) + str(month) + str(day) + str(round(tt2, 2)) + '.csv'
            df = read_pa(read_path, tt2)
            df0 = pd.merge(df0, df, on='id', how='outer')
            df0 = df0.drop_duplicates(subset=('id')).dropna(how='all')
        df = df0.set_index('id')
        df_diff = df.diff(axis=1).abs()
        df_diff = df_diff.applymap(lambda x: func_check(x))
        print(df_diff)
        write_path = path_month + 'mesh_com' + str(year) + str(month) + str(day) + '.csv'
        df_diff.to_csv(write_path)
