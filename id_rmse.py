import pandas as pd
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
weather_path = './weather/change_weather_25.csv'
extract_path = '../id_data/extract/extract_15.csv'
parameter_list = [[1, 10, 1], [1, 1000, 1], [1, 1000, 5], [0.5, 1000, 5], [0.1, 1000, 5], [0.05, 1000, 5], [0.01, 1000, 5], [0.005, 1000, 5]]


def pdcal(path, df_change, df_unchange):
    df_id_annual = pd.read_csv(path, encoding='cp932')
    df_id_annual = df_id_annual[(df_id_annual['time'] > 9.9) & (df_id_annual['time'] < 15.1)]
    df_id_annual['se'] = (df_id_annual['preal'] - df_id_annual['ppred'])**2
    rmse_all = np.sqrt(df_id_annual['se'].mean())
    rmse_all = Decimal(str(rmse_all)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    df_id_annual_change = pd.merge(df_id_annual, df_change, on=['year', 'month', 'day', 'time'])
    rmse_change = np.sqrt(df_id_annual_change['se'].mean())
    rmse_change = Decimal(str(rmse_change)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    df_id_annual_unchange = pd.merge(df_id_annual, df_unchange, on=['year', 'month', 'day', 'time'])
    rmse_unchange = np.sqrt(df_id_annual_unchange['se'].mean())
    rmse_unchange = Decimal(str(rmse_unchange)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    re_list = [float(rmse_change), float(rmse_unchange), float(rmse_all)]
    return re_list


df_write = pd.DataFrame(np.zeros((6200, len(parameter_list)*3 + 8)))
col = {0: 'id', 1: 'id_lat', 2: 'id_lng', 3: 'id_lat_mesh', 4: 'id_lng_mesh', 5: 'id_prefecture', 6: 'pvrate', 7: 'observed_max'}
for a in range(len(parameter_list)):
    lambda_num = parameter_list[a][0]
    iterate = parameter_list[a][1]
    pyramid = parameter_list[a][2]
    col[a*3+8] = ' change l:' + str(lambda_num) + ' i:' + str(iterate) + ' p:' + str(pyramid)
    col[a*3+9] = ' unchange l:' + str(lambda_num) + ' i:' + str(iterate) + ' p:' + str(pyramid)
    col[a*3+10] = ' all_data l:' + str(lambda_num) + ' i:' + str(iterate) + ' p:' + str(pyramid)
df_write = df_write.rename(columns=col)
df_write['id_prefecture'] = df_write['id_prefecture'].apply(lambda _: str(_))
df_weather = pd.read_csv(weather_path, encoding='cp932')
df_weather = df_weather[(df_weather['time'] > 9.9) & (df_weather['time'] < 15.1)]
df_change = df_weather[df_weather['change'] > 0]
df_unchange = df_weather[df_weather['change'] < 1]
df_extract = pd.read_csv(extract_path, encoding='cp932', usecols=[0, 1, 2, 3, 4, 5, 6, 7])
print(df_extract)
input()
for i in range(len(df_extract)):
    rmse = []
    id = df_extract.iat[i, 0]
    lambda_num, iterate, pyramid = 0, 0, 0
    for k in range(7):
        df_write.iat[i, k] = df_extract.iat[i, k]
    for j in range(len(parameter_list)):
        lambda_num = parameter_list[j][0]
        iterate = parameter_list[j][1]
        pyramid = parameter_list[j][2]
        path = '../annual_error_data/kanto_lambda_' + str(lambda_num) + '_iterate_' +str(iterate) + '_p' + str(pyramid) + '/error_' + str(id) + '.csv'
        rmse.append(pdcal(path, df_change, df_unchange))
        df_write.iat[i, 8+j*3] = rmse[j][0]
        df_write.iat[i, 9+j*3] = rmse[j][1]
        df_write.iat[i, 10+j*3] = rmse[j][2]
df_write.to_csv('test.csv', index=False)
