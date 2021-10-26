import pandas as pd
import numpy as np


mesh_range = 0.02
parameter_list = [0.05, 1000, 5]
lambda_num = parameter_list[0]
iterate = parameter_list[1]
pyramid = parameter_list[2]
df_write0 = pd.DataFrame(np.zeros((35000, 22)))
df_write0 = df_write0.rename(columns={0: 'year', 1: 'month', 2: 'day', 3: 'time', 4: 'id', 5: 'id_lat', 6: 'id_lng', 7: 'id_lat_mesh', 8: 'id_lng_mesh', 9: 'id_prefecture', 10: 'pvrate', 11: 'observed_max', 12: 'twoweeks_max', 13: 'flo_lng', 14: 'flo_lat', 15: 'flo', 16: 'nv', 17: 'nv_meshint', 18: 'env', 19: 'preal', 20: 'preal_meshint', 21: 'ppred'})
df_write0['id_prefecture'] = df_write0['id_prefecture'].apply(lambda _: str(_))
print(df_write0)
df_extract = pd.read_csv('H:/study/id_data/extract/extract_15.csv', encoding='cp932')
print(df_extract)
for a in range(len(df_extract)):
    df_write = df_write0.copy()
    extract_id = df_extract.iat[a, 0]
    count = 0
    for i in range(12):
        if i < 5:
            month = i + 8
        else:
            month = i - 4
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
            for tt in range(25):
                tt2 = 6.5 + 0.5 * tt
                print(str(year) + str(month) + str(day) + str(tt2))
                df_write.iat[count, 0] = year
                df_write.iat[count, 1] = month
                df_write.iat[count, 2] = day
                df_write.iat[count, 3] = tt2
                try:
                    read_path = 'H:/study/error_data/parameter_lambda_' + str(lambda_num) + '_iterate_' + str(iterate) + '_p' + str(pyramid) + '/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/error_' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '.csv'
                    df_time = pd.read_csv(read_path, encoding='cp932')
                    df_id = df_time[(df_time['id'] < extract_id+1) & (df_time['id'] > extract_id-1)]
                    df_write.iat[count, 0] = year
                    df_write.iat[count, 1] = month
                    df_write.iat[count, 2] = day
                    df_write.iat[count, 3] = tt2
                    for k in range(18):
                        df_write.iat[count, k+4] = df_id.iat[0, k]
                    count = count + 1
                except Exception as e:
                    print(str(e))
                count = count + 1
    df_write = df_write[df_write['year'] > 0]
    df_write.to_csv('H://study/annual_error_data/error_' + str(extract_id) + '.csv', encoding='cp932', index=False)
