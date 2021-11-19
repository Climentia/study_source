import pandas as pd
import numpy as np


df_write = pd.DataFrame(np.zeros((6200, 5)))
extract_path = 'H:/study/id_data/extract/extract_15.csv'
df_extract = pd.read_csv(extract_path, encoding='cp932')
# print(df_extract)
flag = 0
count = 1
num = 0
df_write = df_write.rename(columns={0: 'year', 1: 'month', 2: 'day', 3: 'time', 4: 'change'})
# print(df_write)
for i in range(12):
    if i <= 4:
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
        read_path = 'H:/study/preprocessing_data/weather_data_20/' + str(month) + '月/mesh_com' + str(year) + str(month) + str(day) + '.csv'
        df0 = pd.read_csv(read_path)
        print(df0)
        for tt in range(11):
            # try:
            flag = 0
            tt2 = 10.0 + 0.5 * tt
            print(str(year) + str(month) + str(day) + str(tt2))
            df = df0[['id', str(tt2)]]
            df2 = pd.merge(df_extract, df)
            main_count = df2[str(tt2)].count().sum()
            change_count = df2[str(tt2)].sum()
            num = change_count/main_count
            if num >= 0.80:
                flag = 1
            else:
                flag = 0
            df_write.iat[count, 0] = year
            df_write.iat[count, 1] = month
            df_write.iat[count, 2] = day
            df_write.iat[count, 3] = tt2
            df_write.iat[count, 4] = flag
            count = count + 1
            # except Exception as e:
                # print('!error!:' + str(e))
write_path = 'change_weather_25.csv'
df_write = df_write[df_write['year'] > 0]
df_write.to_csv(write_path, index=False)
