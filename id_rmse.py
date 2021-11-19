import pandas as pd
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
weather_path = './weather/change_weather_25.csv'
extract_path = '../id_data/extract/extract_15.csv'
parameter_list = [[1, 1000, 5], [0.516, 1000, 5], [0.266, 1000, 5], [0.137, 1000, 5], [0.071, 1000, 5], [0.036, 1000, 5], [0.019, 1000, 5], [0.010, 1000, 5], [0.005, 1000, 5]]


def pdcal(path, df_change, df_unchange):
    df_id_annual = pd.read_csv(path, encoding='cp932')
    df_id_annual = df_id_annual[(df_id_annual['time'] > 6.5) & (df_id_annual['time'] < 18.5)]
    df_id_annual['se'] = (df_id_annual['preal'] - df_id_annual['ppred'])**2
    rmse_all = np.sqrt(df_id_annual['se'].mean())
    rmse_all = Decimal(str(rmse_all)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    df_id_annual = df_id_annual[(df_id_annual['time'] > 9.9) & (df_id_annual['time'] < 15.1)]
    df_id_annual_change = pd.merge(df_id_annual, df_change, on=['year', 'month', 'day', 'time'])
    rmse_change = np.sqrt(df_id_annual_change['se'].mean())
    rmse_change = Decimal(str(rmse_change)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    df_id_annual_unchange = pd.merge(df_id_annual, df_unchange, on=['year', 'month', 'day', 'time'])
    rmse_unchange = np.sqrt(df_id_annual_unchange['se'].mean())
    rmse_unchange = Decimal(str(rmse_unchange)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    re_list = [float(rmse_change), float(rmse_unchange), float(rmse_all)]
    return re_list


def pdcal_persist(path, df_change, df_unchange):
    df_id_annual = pd.read_csv(path, encoding='cp932')
    df_id_annual['ppred'] = df_id_annual['twoweeks_max'] * df_id_annual['env']
    df_id_annual = df_id_annual[(df_id_annual['time'] > 6.5) & (df_id_annual['time'] < 18.5)]
    df_id_annual['se'] = (df_id_annual['preal'] - df_id_annual['ppred'])**2
    rmse_all = np.sqrt(df_id_annual['se'].mean())
    rmse_all = Decimal(str(rmse_all)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    df_id_annual = df_id_annual[(df_id_annual['time'] > 9.9) & (df_id_annual['time'] < 15.1)]
    df_id_annual_change = pd.merge(df_id_annual, df_change, on=['year', 'month', 'day', 'time'])
    rmse_change = np.sqrt(df_id_annual_change['se'].mean())
    rmse_change = Decimal(str(rmse_change)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    df_id_annual_unchange = pd.merge(df_id_annual, df_unchange, on=['year', 'month', 'day', 'time'])
    rmse_unchange = np.sqrt(df_id_annual_unchange['se'].mean())
    rmse_unchange = Decimal(str(rmse_unchange)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    re_list = [float(rmse_change), float(rmse_unchange), float(rmse_all)]
    return re_list


df_write = pd.DataFrame(np.zeros((105, len(parameter_list)*3 + 8)))
col = {0: 'id', 1: 'id_lat', 2: 'id_lng', 3: 'id_lat_mesh', 4: 'id_lng_mesh', 5: 'id_prefecture', 6: 'pvrate', 7: 'observed_max'}
col[8] = ' change:persist'
col[9] = ' all_data:persist'
for a in range(len(parameter_list)):
    lambda_num = parameter_list[a][0]
    iterate = parameter_list[a][1]
    pyramid = parameter_list[a][2]
    col[a*2+10] = ' change l:' + str(lambda_num)
    col[a*2+11] = ' all_data l:' + str(lambda_num)
df_write = df_write.rename(columns=col)
df_write['id_prefecture'] = df_write['id_prefecture'].apply(lambda _: str(_))
df_weather = pd.read_csv(weather_path, encoding='cp932')
df_weather = df_weather[(df_weather['time'] > 9.9) & (df_weather['time'] < 15.1)]
df_change = df_weather[df_weather['change'] > 0]
df_unchange = df_weather[df_weather['change'] < 1]
df_extract = pd.read_csv(extract_path, encoding='cp932', usecols=[0, 1, 2, 3, 4, 5, 6, 7])
for i in range(len(df_extract)):
    rmse = []
    id = df_extract.iat[i, 0]
    print(id)
    lambda_num, iterate, pyramid = 0, 0, 0
    for k in range(8):
        df_write.iat[i, k] = df_extract.iat[i, k]
    path_per = '../annual_error_data/kanto_parameter_persist_nv_30min/error_' + str(id) + '.csv'
    persist_list = pdcal_persist(path_per, df_change, df_unchange)
    df_write.iat[i, 8] = persist_list[0]
    df_write.iat[i, 9] = persist_list[2]
    for j in range(len(parameter_list)):
        lambda_num = parameter_list[j][0]
        iterate = parameter_list[j][1]
        pyramid = parameter_list[j][2]
        path = '../annual_error_data/kanto_lambda_' + str(lambda_num) + '_iterate_' +str(iterate) + '_p' + str(pyramid) + '/error_' + str(id) + '.csv'
        rmse.append(pdcal(path, df_change, df_unchange))
        df_write.iat[i, 10+j*2] = rmse[j][0]
        df_write.iat[i, 11+j*2] = rmse[j][2]
# 読み込み
df_sum_annual = pd.read_csv('output_sum.csv', encoding='cp932')
# 持続予測の予測誤差_1年分
df_sum_annual['se:persist'] = (df_sum_annual['preal'] - df_sum_annual['output:persist'])**2
df_sum_annual = df_sum_annual[(df_sum_annual['time'] > 6.5) & (df_sum_annual['time'] < 18.5)]
rmse_sum_all = np.sqrt(df_sum_annual['se:persist'].mean())
# 持続予測の誤差_変化大
df_sum_change = df_sum_annual[(df_sum_annual['time'] > 9.9) & (df_sum_annual['time'] < 15.1)]
df_sum_change = pd.merge(df_sum_change, df_change, on=['year', 'month', 'day', 'time'])
rmse_sum_change = np.sqrt(df_sum_change['se:persist'].mean())
df_write.iat[len(df_extract)+1, 0] = 1
df_write.iat[len(df_extract)+1, 7] = df_sum_annual['observed_max'].sum()
df_write.iat[len(df_extract)+1, 8] = Decimal(str(rmse_sum_all)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
df_write.iat[len(df_extract)+1, 9] = Decimal(str(rmse_sum_change)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
# 各lambdaの計算
for m in range(len(parameter_list)):
    lambda_num = parameter_list[j][0]
    df_sum_annual['se_' + str(lambda_num)] = (df_sum_annual['preal'] - df_sum_annual['output:' + str(lambda_num)])**2
    rmse_sum_annual = np.sqrt(df_sum_annual['se_' + str(lambda_num)].mean())
    df_sum_change['se_' + str(lambda_num)] = (df_sum_change['preal'] - df_sum_change['output:' + str(lambda_num)])**2
    rmse_sum_change = np.sqrt(df_sum_change['se_' + str(lambda_num)].mean())
    df_write.iat[len(df_extract)+1, 10+m*2] = Decimal(str(rmse_sum_change)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    df_write.iat[len(df_extract)+1, 11+m*2] = Decimal(str(rmse_sum_annual)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
df_write = df_write[df_write['id'] > 0]
df_write.to_csv('id_rmse.csv', index=False, encoding='cp932')
