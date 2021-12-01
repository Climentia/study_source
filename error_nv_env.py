import pandas as pd
import numpy as np

parameter_list = [[1, 1000, 5], [0.516, 1000, 5], [0.266, 1000, 5], [0.137, 1000, 5], [0.071, 1000, 5], [0.036, 1000, 5], [0.019, 1000, 5], [0.010, 1000, 5], [0.005, 1000, 5]]
mesh_range = 0.02


count = 0
df_write = pd.DataFrame(np.zeros((25000, 7+len(parameter_list))))
col = {0: 'year', 1: 'month', 2: 'day', 3: 'time', 4: 'observed_max', 5: 'preal', 6: 'error:persist'}
for a in range(len(parameter_list)):
    lambda_num = parameter_list[a][0]
    iterate = parameter_list[a][1]
    pyramid = parameter_list[a][2]
    col[a+7] = 'error:' + str(lambda_num)
df_write = df_write.rename(columns=col)
for i in range(12):
    # ８月から始まるようにする(データの区間が2013年8月~2014年7月までの期間なので)
    if i < 5:
        month = i + 8
    else:
        month = i - 4
    # 年を切り替え
    if month < 8:
        year1 = 2014
        year = 14
    else:
        year1 = 2013
        year = 13
    # 月によって日の数が違う為,月の日の数を指定
    if month == 2:
        day_max = 28
    elif month == 4 or month == 6 or month == 9 or month == 11:
        day_max = 30
    else:
        day_max = 31
    # 日
    for j in range(day_max):
        day = j+1
        # 各時間(30分おき)
        for tt in range(24):
            try:
                tt2 = 6.5 + 0.5 * tt
                print(str(year) + str(month) + str(day) + str(tt2))
                read_path = '../error_data/kanto_parameter_persist_nv_30min/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/error_' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_presist_nv_30min.csv'
                df = pd.read_csv(read_path, encoding='cp932', usecols=['id', 'observed_max', 'preal', 'ppred'])
                df_write.iat[count, 0] = str(year)
                df_write.iat[count, 1] = str(month)
                df_write.iat[count, 2] = str(day)
                df_write.iat[count, 3] = str(tt2)
                for b in range(len(parameter_list)):
                    lambda_num = parameter_list[b][0]
                    iterate = parameter_list[b][1]
                    read_path = '../error_data/kanto_parameter_lambda_' + str(lambda_num) + '_iterate_' + str(iterate) + '_p' + str(pyramid) + '/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/error_' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '.csv'
                    pyramid = parameter_list[b][2]
                    df2 = pd.read_csv(read_path, encoding='cp932', usecols=['id', 'ppred'])
                    df2 = df2.rename(columns={'ppred': str(lambda_num)})
                    df = pd.merge(df, df2, on='id')
                df = df.dropna(how='any')
                real_sum = df['preal'].sum()
                obmx_sum = df['observed_max'].sum()
                pred_sum = df['ppred'].sum()
                df_write.iat[count, 4] = obmx_sum
                df_write.iat[count, 5] = real_sum
                df_write.iat[count, 6] = abs(real_sum - pred_sum)*100/obmx_sum
                df = df.rename(columns={'ppred': 'error:persist'})
                for c in range(len(parameter_list)):
                    lambda_num = parameter_list[c][0]
                    iterate = parameter_list[c][1]
                    pyramid = parameter_list[c][2]
                    df_write.iat[count, c+7] = abs(real_sum - df[str(lambda_num)].sum())*100/obmx_sum
                count += 1
            except Exception as e:
                print(str(e))
df_write = df_write[df_write['preal'] > 0]
df_write.to_csv('error_sum.csv', index=False)
