import pandas as pd
import numpy as np
import os
import csv
from decimal import Decimal, ROUND_HALF_UP


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
    path_month = '../../../error_data/kanto_parameter_persist_nv_30min/' + str(month) + '???/'
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
        path_day = path_month + str(month) + '???' + str(day) + '???/'
        path_day_cheack = os.path.exists(path_day)
        if path_day_cheack == False:
            os.makedirs(path_day)
        for tt in range(25):
            try:
                tt2 = round(7.0 + 0.5 * tt, 1)
                read_path_com = '../../../preprocessing_data/mesh_com_kanto/' + str(month) + '???/' + str(month) + '???' + str(day) + '???/mesh_com' + str(year) + str(month) + str(day) + str(tt2) + '.csv'
                read_path_int = '../../../preprocessing_data/4_interpolated_mesh/' + str(month) + '???/' + str(month) + '???' + str(day) + '???/NV' + str(year) + str(month) + str(day) + str(tt2) + str(mesh_range) + '_int.csv'
                read_path_old = '../../../preprocessing_data/mesh_com_kanto/' + str(month) + '???/' + str(month) + '???' + str(day) + '???/mesh_com' + str(year) + str(month) + str(day) + str(round(tt2 - 0.5, 1)) + '.csv'
                write_path = path_day + 'error_' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_presist_nv_30min.csv'
                print(str(year) + str(month) + str(day) + str(tt2))
                # ??????????????????????????????????????????
                with open(read_path_int) as f_int:
                    reader_int = csv.reader(f_int)
                    list_int = [row_int for row_int in reader_int]
                # ??????????????????????????????????????????
                df_old = pd.read_csv(read_path_old, encoding='cp932')
                df_old1 = df_old[['id', 'twoweeks_max', 'nv']]
                df_old2 = df_old1.rename(columns={'nv': 'env', 'twoweeks_max': 'twoweeks_max_old'})
                # ????????????????????????????????????
                df_read_com0 = pd.read_csv(read_path_com, encoding='cp932')
                df_read_com = pd.merge(df_read_com0, df_old2)
                df_read_com['id_lat_num'] = (df_read_com['id_lat_mesh']-31.2) / 0.02
                df_read_com['id_lng_num'] = (df_read_com['id_lng_mesh']-129.6) / 0.02
                df_read_com = df_read_com[(df_read_com['id_lat_num'] >= 0) & (df_read_com['id_lat_num'] <= 431) & (df_read_com['id_lng_num'] >= 0) & (df_read_com['id_lng_num'] <= 601)]
                df_read_com['nv_meshint'] = df_read_com.apply(lambda x: list_int[int(x.id_lng_num)][int(x.id_lat_num)], axis = 1).astype(float)
                df_read_com['preal'] = df_read_com['nv'] * df_read_com['twoweeks_max']
                df_read_com['preal_meshint'] = df_read_com['nv_meshint'] * df_read_com['twoweeks_max']
                df_read_com['ppred'] = df_read_com['env'] * df_read_com['twoweeks_max']
                df_read_com['nv_max_perror'] = ((df_read_com['ppred'] - df_read_com['preal'])*100) / df_read_com['observed_max']
                df_read_com['nv_meshint_max_perror'] = ((df_read_com['ppred'] - df_read_com['preal_meshint'])*100) / df_read_com['observed_max']
                df_write = df_read_com[['id', 'id_lat', 'id_lng', 'id_lat_mesh', 'id_lng_mesh', 'id_prefecture', 'pvrate', 'observed_max', 'twoweeks_max', 'nv', 'nv_meshint', 'env', 'preal', 'preal_meshint', 'ppred', 'nv_max_perror', 'nv_meshint_max_perror']]
                df_write = df_write.apply(if_else01, axis=1)
                df_write.to_csv(write_path, encoding='cp932', index = False)
            except Exception as e:
                print(str(e))
