import pandas as pd
import numpy as np
import os
import math

place = 'national'
lambda_num = 0.01
iterate = 1000
pyramid = 5
mesh_range = 0.02

# 'id', 'id_lat', 'id_lng', 'id_lat_mesh', 'id_lng_mesh', 'id_prefecture', 'pvrate', 'observed_max', 'twoweeks_max_old', 'twoweeks_max', 'nv', 'nv_meshint', 'env', 'preal', 'preal_meshint', 'ppred', 'nv_error', 'nv_perror', 'nv_max_perror', 'nv_meshint_error', 'nv_meshint_perror', 'nv_meshint_max_perror'
base_frame0 = pd.DataFrame(np.zeros((9000, 8)))
base_frame = base_frame0.rename(columns={0: 'year', 1: 'month', 2: 'day', 3: 'time',  4: 'MAPE(/nv)', 5: 'MAPE(/observed_max)', 6: 'RMSPE(/nv)', 7: 'RMSPE(/observed_max)'})
# input()
write_path = './mape_' + str(place) + '_' + str(mesh_range) + '_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '.csv'
count = 0
df_write = base_frame.copy()
for i in range(12):
    month = i + 1
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
        for tt in range(24):
            try:
                tt2 = 6.5 + 0.5 * tt
                print(str(year) + str(month) + str(day) + str(tt2))
                read_path = 'F:/study/error_data/parameter_lambda_' + str(lambda_num) + '_iterate_' + str(iterate) + '_p' + str(pyramid) + '/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/' + 'error_' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '.csv'
                df_read0 = pd.read_csv(read_path, encoding='cp932')
                df_dup = df_read0.drop_duplicates(subset=('id_lat_mesh', 'id_lng_mesh')).dropna(how='any')
                # print(df_dup)
                df_write.iat[count, 0] = int(year)
                df_write.iat[count, 1] = int(month)
                df_write.iat[count, 2] = int(day)
                df_write.iat[count, 3] = round(float(tt2), 2)
                df_write.iat[count, 4] = (((100*(df_dup['preal_meshint']-df_dup['ppred']).abs())/df_dup['preal_meshint']).mean())
                df_write.iat[count, 5] = (((100*(df_dup['preal_meshint']-df_dup['ppred']).abs())/df_dup['observed_max']).mean())
                df_write.iat[count, 6] = math.sqrt(((df_dup['preal_meshint']-df_dup['ppred'])**2).sum()/((df_dup['nv_meshint']**2).sum()))
                df_write.iat[count, 7] = math.sqrt(((df_dup['preal_meshint']-df_dup['ppred'])**2).sum()/(df_dup['observed_max']**2).sum())
                count = count + 1
            except Exception as e:
                print('error' + str(e))
df_write2 = df_write[df_write['year'] > 0]
df_write2.to_csv(write_path)
            # read_path_com = 'F:/study/preprocessing_data/mesh_com/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/error_' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '.csv'
            # write_path = path_day + 'error_' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '.csv'
