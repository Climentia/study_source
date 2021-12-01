import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
parameter_list = [[1, 1000, 5], [0.516, 1000, 5], [0.266, 1000, 5], [0.137, 1000, 5], [0.071, 1000, 5], [0.036, 1000, 5], [0.019, 1000, 5], [0.010, 1000, 5], [0.005, 1000, 5]]
place = 'kanto'
mesh_range = 0.02
year = 13
month = 9
day = 5
tt2 = 12.5


def dfmaker(parameter):
    lambda_num = parameter[0]
    iterate = parameter[1]
    pyramid = parameter[2]
    name = 'LMD:' + str(parameter[0])
    read_path = 'H:/study/error_data/kanto_parameter_lambda_' + str(lambda_num) + '_iterate_' + str(iterate) + '_p' + str(pyramid) + '/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/' + 'error_' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '.csv'
    df_read0 = pd.read_csv(read_path, encoding='cp932')
    # df_dup0 = df_read0.drop_duplicates(subset=('id_lat_mesh', 'id_lng_mesh')).dropna(how='any')
    df_dup = pd.merge(df_read0, df_40)
    df_dup[name] = (((100*(df_dup['preal_meshint']-df_dup['ppred']).abs())/df_dup['observed_max']))
    df = df_dup[['id', name]]
    return df


def dfmaker_persist():
    name = 'persist'
    # H:\study\error_data\kanto_parameter_persist_nv_30min\9月\9月5日
    read_path = 'H:/study/error_data/kanto_parameter_persist_nv_30min' + '/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/' + 'error_' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_presist_30min.csv'
    df_read0 = pd.read_csv(read_path, encoding='cp932')
    # df_dup0 = df_read0.drop_duplicates(subset=('id_lat_mesh', 'id_lng_mesh')).dropna(how='any')
    df_dup = pd.merge(df_read0, df_40)
    df_dup[name] = (((100*(df_dup['preal_meshint']-df_dup['ppred']).abs())/df_dup['observed_max']))
    df = df_dup[['id', name]]
    return df


def dfmaker_persist_nv():
    name = 'persist_nv'
    read_path = 'H:/study/error_data/kanto_parameter_persist_nv_30min' + '/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/' + 'error_' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_presist_nv_30min.csv'
    df_read0 = pd.read_csv(read_path, encoding='cp932')
    # df_dup0 = df_read0.drop_duplicates(subset=('id_lat_mesh', 'id_lng_mesh')).dropna(how='any')
    df_dup = pd.merge(df_read0, df_40)
    df_dup[name] = (((100*(df_dup['preal_meshint']-df_dup['ppred']).abs())/df_dup['observed_max']))
    df = df_dup[['id', name]]
    return df


# 'id', 'id_lat', 'id_lng', 'id_lat_mesh', 'id_lng_mesh', 'id_prefecture', 'pvrate', 'observed_max', 'twoweeks_max_old', 'twoweeks_max', 'nv', 'nv_meshint', 'env', 'preal', 'preal_meshint', 'ppred', 'nv_error', 'nv_perror', 'nv_max_perror', 'nv_meshint_error', 'nv_meshint_perror', 'nv_meshint_max_perror'
base_frame0 = pd.DataFrame(np.zeros((9000, 8)))
base_frame = base_frame0.rename(columns={0: 'year', 1: 'month', 2: 'day', 3: 'time',  4: 'MAPE(/nv)', 5: 'MAPE(/observed_max)', 6: 'RMSPE(/nv)', 7: 'RMSPE(/observed_max)'})
# input()
df_400 = pd.read_csv('H:/study/id_data/extract/extract_15.csv', encoding='cp932')
df_40 = df_400[['id', 'id_prefecture']]
count = 0
df_write = base_frame.copy()
time = str(year) + str(month) + str(day) + str(tt2)
print(time)
fig, ax = plt.subplots()
df_list = []
df_list.append(dfmaker_persist_nv())
for parameter in ((parameter_list)):
    df_list.append(dfmaker(parameter))
for k in range(len(df_list)-1):
    df_list[0] = pd.merge(df_list[0], df_list[k+1], how='outer')
print(df_list)
cl_list = list(df_list[0].columns)
count = count + 1
boxplot = df_list[0].boxplot(column=cl_list[1:], whis=[0, 100], showmeans=True)
boxplot.plot()
count_df = df_list[0]['id'].count()
print(df_list[0].count())
plt.xlabel('Parameter')
plt.ylabel('Abusolute Error[%]')
plt.title('Box plot   time:' + time + '   Number of data:' + str(count_df))
plt.show()
df_write = df_list.describe()
df_wirte.to_csv()
# read_path_com = 'F:/study/preprocessing_data/mesh_com/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/error_' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '.csv'
# write_path = path_day + 'error_' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '.csv'
