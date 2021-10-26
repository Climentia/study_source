import pandas as pd
import os
import csv
import re
import numpy as np


mesh_range = 0.02


def isfloat(parameter):
    if not parameter.isdecimal():
        try:
            float(parameter)
            return True
        except ValueError:
            return False
    else:
        return False


def floater(list):
    list2 = [0] * len(list)
    for i in range(len(list)):
        # print(list[i])
        num_ch = isfloat(list[i])
        if num_ch == True:
            list2[i] = str(list[i])
        else:
            list2[i] = 'NaN'
    return list2


for i in range(12):
    month = i + 1
    path_month = 'F:/study/error_data/parameter_persist_30min/' + str(month) + '月/'
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
        path_day = path_month + str(month) + '月' + str(day) + '日/'
        path_day_cheack = os.path.exists(path_day)
        if path_day_cheack == False:
            os.makedirs(path_day)
        for tt in range(25):
            try:
                tt2 = round(7.0 + 0.5 * tt, 1)
                read_path_com = 'F:/study/preprocessing_data/mesh_com/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/mesh_com' + str(year) + str(month) + str(day) + str(tt2) + '.csv'
                read_path_int = 'F:/study/preprocessing_data/4_interpolated_mesh/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/NV' + str(year) + str(month) + str(day) + str(tt2) + str(mesh_range) + '_int.csv'
                read_path_old = 'F:/study/preprocessing_data/mesh_com/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/mesh_com' + str(year) + str(month) + str(day) + str(round(tt2 - 0.5, 1)) + '.csv'
                write_path = path_day + 'error_' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_presist_30min.csv'
                print(str(year) + str(month) + str(day) + str(tt2))
                # 補間後のメッシュデータを抽出
                with open(read_path_int) as f_int:
                    reader_int = csv.reader(f_int)
                    list_int = [floater(row_int) for row_int in reader_int]
                # 予測後のメッシュデータを抽出
                df_old = pd.read_csv(read_path_old, encoding='cp932')
                df_old1 = df_old[['id', 'twoweeks_max', 'nv']]
                df_old2 = df_old1.rename(columns={'nv': 'env', 'twoweeks_max': 'twoweeks_max_old'})
                # 予測後の動きデータを抽出
                df_read_com0 = pd.read_csv(read_path_com, encoding='cp932')
                df_read_com = pd.merge(df_read_com0, df_old2)
                df_read_com['id_lat_num'] = (df_read_com['id_lat_mesh']-31.2) / 0.02
                df_read_com['id_lng_num'] = (df_read_com['id_lng_mesh']-129.6) / 0.02
                df_read_com = df_read_com[(df_read_com['id_lat_num'] >= 0) & (df_read_com['id_lat_num'] <= 431) & (df_read_com['id_lng_num'] >= 0) & (df_read_com['id_lng_num'] <= 601)]
                df_read_com['nv_meshint'] = df_read_com.apply(lambda x: list_int[int(x.id_lng_num)][int(x.id_lat_num)], axis = 1).astype(float)
                df_read_com['preal'] = df_read_com['nv'] * df_read_com['twoweeks_max']
                df_read_com['preal_meshint'] = df_read_com['nv_meshint'] * df_read_com['twoweeks_max']
                df_read_com['ppred'] = df_read_com['env'] * df_read_com['twoweeks_max_old']
                df_read_com['nv_error'] = df_read_com['env'] - df_read_com['nv']
                df_read_com['nv_perror'] = (df_read_com['nv_error']*100) / df_read_com['nv']
                df_read_com['nv_max_perror'] = ((df_read_com['ppred'] - df_read_com['preal'])*100) / df_read_com['observed_max']
                df_read_com['nv_meshint_error'] = df_read_com['env'] - df_read_com['nv']
                df_read_com['nv_meshint_perror'] = (df_read_com['nv_meshint_error']*100) / df_read_com['nv']
                df_read_com['nv_meshint_max_perror'] = ((df_read_com['ppred'] - df_read_com['preal_meshint'])*100) / df_read_com['observed_max']
                df_write = df_read_com[['id', 'id_lat', 'id_lng', 'id_lat_mesh', 'id_lng_mesh', 'id_prefecture', 'pvrate', 'observed_max', 'twoweeks_max_old', 'twoweeks_max', 'nv', 'nv_meshint', 'env', 'preal', 'preal_meshint', 'ppred', 'nv_error', 'nv_perror', 'nv_max_perror', 'nv_meshint_error', 'nv_meshint_perror', 'nv_meshint_max_perror']]
                df_write.to_csv(write_path, encoding='cp932', index = False)
            except Exception as e:
                print(str(e))
