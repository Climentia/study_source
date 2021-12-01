import pandas as pd
import numpy as np
import os
import csv
from decimal import Decimal, ROUND_HALF_UP


lambda_num = 0.137
iterate = 1000
pyramid = 5
mesh_range = 0.02


def if_else01(x):
    if (x.twoweeks_max < 0.001) and (x.nv < 0.001):
        x.twoweeks_max = np.nan
        x.nv = np.nan
        x.preal = np.nan
        x.preal_meshint = np.nan
        x.ppred = np.nan
        x.nv_max_perror = np.nan
        x.nv_meshint_max_perror = np.nan
    x.flo_lng = Decimal(str(x.flo_lng)).quantize(Decimal('0.0000001'), rounding=ROUND_HALF_UP)
    x.flo_lat = Decimal(str(x.flo_lat)).quantize(Decimal('0.0000001'), rounding=ROUND_HALF_UP)
    x.flo = Decimal(str(x.flo)).quantize(Decimal('0.0000001'), rounding=ROUND_HALF_UP)
    x.id_lat = Decimal(str(x.id_lat)).quantize(Decimal('0.00001'), rounding=ROUND_HALF_UP)
    x.id_lng = Decimal(str(x.id_lng)).quantize(Decimal('0.00001'), rounding=ROUND_HALF_UP)
    x.observed_max = Decimal(str(x.observed_max)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    x.env = Decimal(str(x.env)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    x.nv = Decimal(str(x.nv)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    x.nv_meshint = Decimal(str(x.nv_meshint)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    x.preal = Decimal(str(x.preal)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    x.preal_meshint = Decimal(str(x.preal_meshint)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    x.ppred = Decimal(str(x.ppred)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    x.nv_max_perror = Decimal(str(x.nv_max_perror)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    x.nv_meshint_max_perror = Decimal(str(x.nv_meshint_max_perror)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    x.id_lat_mesh = Decimal(str(x.id_lat_mesh)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    x.id_lng_mesh = Decimal(str(x.id_lng_mesh)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    x.pvrate = Decimal(str(x.pvrate)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    x.twoweeks_max = Decimal(str(x.twoweeks_max)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
    return x


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
    path_month = '../../../error_data/kanto_parameter_lambda_' + str(lambda_num) + '_iterate_' + str(iterate) + '_p' + str(pyramid) + '/' + str(month) + '月/'
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
        for tt in range(26):
            try:
                tt2 = 6.5 + 0.5 * tt
                read_path_com = '../../../preprocessing_data/mesh_com_kanto/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/mesh_com' + str(year) + str(month) + str(day) + str(tt2) + '.csv'
                read_path_int = '../../../preprocessing_data/4_interpolated_mesh/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/NV' + str(year) + str(month) + str(day) + str(tt2) + str(mesh_range) + '_int.csv'
                read_path_env = '../../../prediction_data/parameter_lambda_' + str(lambda_num) + '_iterate_' + str(iterate) + '_p' + str(pyramid) + '/env/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/NV' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '_env.csv'
                read_path_flo = '../../../prediction_data/parameter_lambda_' + str(lambda_num) + '_iterate_' + str(iterate) + '_p' + str(pyramid) + '/flo/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/NV' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '_flo.csv'
                write_path = path_day + 'error_' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '.csv'
                print(str(year) + str(month) + str(day) + str(tt2))
                # 補間後のメッシュデータを抽出
                with open(read_path_int) as f_int:
                    reader_int = csv.reader(f_int)
                    list_int = [row_int for row_int in reader_int]
                # 予測後のメッシュデータを抽出
                with open(read_path_env) as f_env:
                    reader_env = csv.reader(f_env)
                    list_env = [floater(row_env) for row_env in reader_env]
                # 予測後の動きデータを抽出
                with open(read_path_flo) as f_flo:
                    reader_flo = csv.reader(f_flo)
                    list_flo = [floater(row_flo) for row_flo in reader_flo]
                df_read_com = pd.read_csv(read_path_com, encoding='cp932')
                df_read_com['id_lat_num'] = (df_read_com['id_lat_mesh']-31.2) / 0.02
                df_read_com['id_lng_num'] = (df_read_com['id_lng_mesh']-129.6) / 0.02
                df_read_com = df_read_com[(df_read_com['id_lat_num'] >= 0) & (df_read_com['id_lat_num'] <= 431) & (df_read_com['id_lng_num'] >= 0) & (df_read_com['id_lng_num'] <= 601)]
                df_read_com['nv_meshint'] = df_read_com.apply(lambda x: list_int[int(x.id_lng_num)][int(x.id_lat_num)], axis = 1).astype(float)
                df_read_com['env'] = df_read_com.apply(lambda x: list_env[int(x.id_lng_num)][int(x.id_lat_num)], axis = 1).astype(float)
                df_read_com['flo_lng'] = df_read_com.apply(lambda x: list_flo[int(x.id_lng_num)][int((x.id_lat_num)*2+1)], axis = 1).astype(float) * (1/50)
                df_read_com['flo_lat'] = df_read_com.apply(lambda x: list_flo[int(x.id_lng_num)][int((x.id_lat_num)*2)], axis = 1).astype(float) * (1/50)
                df_read_com['flo'] = (df_read_com['flo_lng']**2) + (df_read_com['flo_lat']**2)**0.5
                df_read_com['preal'] = df_read_com['nv'] * df_read_com['twoweeks_max']
                df_read_com['preal_meshint'] = df_read_com['nv_meshint'] * df_read_com['twoweeks_max']
                df_read_com['ppred'] = df_read_com['env'] * df_read_com['twoweeks_max']
                df_read_com['nv_max_perror'] = ((df_read_com['ppred'] - df_read_com['preal'])*100) / df_read_com['observed_max']
                df_read_com['nv_meshint_max_perror'] = ((df_read_com['ppred'] - df_read_com['preal_meshint'])*100) / df_read_com['observed_max']
                df_write = df_read_com[['id', 'id_lat', 'id_lng', 'id_lat_mesh', 'id_lng_mesh', 'id_prefecture', 'pvrate', 'observed_max', 'twoweeks_max', 'flo_lng', 'flo_lat', 'flo', 'nv', 'nv_meshint', 'env', 'preal', 'preal_meshint', 'ppred', 'nv_max_perror', 'nv_meshint_max_perror']]
                df_write = df_write.apply(if_else01, axis=1)
                df_write.to_csv(write_path, encoding='cp932', index = False)
            except Exception as e:
                print(str(e))
