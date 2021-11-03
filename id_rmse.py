import pandas as pd
import numpy as np
weather_path = './weather/change_weather_25.csv'
extract_path = '../id_data/extract/extract_15.csv'
parameter_list = [[1, 10, 1], [1, 1000, 1], [1, 1000, 5], [0.5, 1000, 5], [0.1, 1000, 5], [0.05, 1000, 5], [0.01, 1000, 5], [0.005, 1000, 5]]


df_write = pd.DataFrame(np.zeros((6200, len(parameter_list)*3 + 1)))
col = {0: 'id'}
for a in range(len(parameter_list)):
    print(a)
    lambda_num = parameter_list[a][0]
    iterate = parameter_list[a][1]
    pyramid = parameter_list[a][2]
    col[a*3+1] = ' change l:' + str(lambda_num) + ' i:' + str(iterate) + ' p:' + str(pyramid)
    col[a*3+2] = ' unchange l:' + str(lambda_num) + ' i:' + str(iterate) + ' p:' + str(pyramid)
    col[a*3+3] = ' all_data l:' + str(lambda_num) + ' i:' + str(iterate) + ' p:' + str(pyramid)
df_write = df_write.rename(columns=col)
print(df_write)
df_weather = pd.read_csv(weather_path, encoding='cp932')
df_weather = df_weather[(df_weather['time'] > 9.5) & (df_weather['time'] < 15.5)]
df_change = df_weather[df_weather['change'] > 0]
df_unchange = df_weather[df_weather['change'] < 1]
df_extract = pd.read_csv(extract_path, encoding='cp932', usecols=[0, 1, 2, 3, 4, 5, 6, 7])
for i in range(len(df_extract)):
    id = df_extract.iat[i, 0]
    print(str(id))
    
