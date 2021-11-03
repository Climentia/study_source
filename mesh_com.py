# 各時間帯の規格化した値と二週間最大値をidの各情報があるファイルと結合
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP
import os


# idの情報と結合したいidが入っているファイルを読み込む
df_all = pd.read_csv('../id_data/extract/extract_15.csv', encoding='cp932')
# 2週間最大値と規格化値が入っているファイルが全部入っているデータ
df_two_nv2 = pd.read_csv('./tweeks_concat/all_twoweeks.csv', encoding='cp932')
for i in range(12):
    month = i + 1
    path_month = '../preprocessing_data/mesh_com_kanto/' + str(month) + '月/'
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
            tt2 = 6.5 + 0.5 * tt
            print(str(year) + str(month) + str(day) + str(tt2))
            df_two_nv3 = df_two_nv2[(df_two_nv2['year'] == year) & (df_two_nv2['month'] == month) & (df_two_nv2['day'] == day) & (df_two_nv2['time'] < tt2 + 0.1) & (df_two_nv2['time'] > tt2 - 0.1)]
            df_write = pd.merge(df_all, df_two_nv3, on='id', how = 'outer')
            df_write2 = df_write[['id', 'id_lat', 'id_lng', 'id_lat_mesh', 'id_lng_mesh', 'id_prefecture', 'pvrate', 'observed_max', 'nv', 'twoweeks_max']]
            write_path = path_day + 'mesh_com' + str(year) + str(month) + str(day) + str(tt2) + '.csv'
            column_list_000001 = ['id_lat', 'id_lng']
            column_list_0001 = ['observed_max', 'nv']
            column_list_001 = ['id_lat_mesh', 'id_lng_mesh', 'pvrate']
            df_write2 = df_write2[df_write2['id_lat']>0]
            for my_col in df_write2.columns:
                if my_col in column_list_000001:
                    df_write2[my_col] = df_write2[my_col].map(lambda x: float(Decimal(str(x)).quantize(Decimal('0.00001'), rounding=ROUND_HALF_UP)))
                elif my_col in column_list_0001:
                    df_write2[my_col] = df_write2[my_col].map(lambda x: float(Decimal(str(x)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)))
                elif my_col in column_list_001:
                    df_write2[my_col] = df_write2[my_col].map(lambda x: float(Decimal(str(x)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)))
            df_write2.to_csv(write_path, encoding='cp932', index=False)
