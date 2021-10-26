import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
parameter_list = [[1, 10, 1], [0.01, 1000, 5], [0.1, 1000, 5], [1, 1000, 1], [1, 1000, 5]]
place = 'kanto'
mesh_range = 0.02


def dfmaker(parameter):
    lambda_num = parameter[0]
    iterate = parameter[1]
    pyramid = parameter[2]
    name = 'LMD:' + str(parameter[0]) + '::ITR:' + str(parameter[1]) + '::PRM:' + str(parameter[2])
    read_path = 'F:/study/error_data/parameter_lambda_' + str(lambda_num) + '_iterate_' + str(iterate) + '_p' + str(pyramid) + '/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/' + 'error_' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '.csv'
    df_read0 = pd.read_csv(read_path, encoding='cp932')
    df_dup0 = df_read0.drop_duplicates(subset=('id_lat_mesh', 'id_lng_mesh')).dropna(how='any')
    df_dup = pd.merge(df_dup0, df_40)
    df_dup[name] = (((100*(df_dup['preal_meshint']-df_dup['ppred']).abs())/df_dup['observed_max']))
    df = df_dup[['id', name]]
    return df


def dfmaker_persist():
    name = 'persist'
    read_path = 'F:/study/error_data/parameter_persist' + '/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/' + 'error_' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_presist.csv'
    df_read0 = pd.read_csv(read_path, encoding='cp932')
    df_dup0 = df_read0.drop_duplicates(subset=('id_lat_mesh', 'id_lng_mesh')).dropna(how='any')
    df_dup = pd.merge(df_dup0, df_40)
    df_dup[name] = (((100*(df_dup['preal_meshint']-df_dup['ppred']).abs())/df_dup['observed_max']))
    df = df_dup[['id', name]]
    return df


def dfmaker_persist_nv():
    name = 'persist_nv'
    read_path = 'F:/study/error_data/parameter_persist_nv' + '/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/' + 'error_' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_presist.csv'
    df_read0 = pd.read_csv(read_path, encoding='cp932')
    df_dup0 = df_read0.drop_duplicates(subset=('id_lat_mesh', 'id_lng_mesh')).dropna(how='any')
    df_dup = pd.merge(df_dup0, df_40)
    df_dup[name] = (((100*(df_dup['preal_meshint']-df_dup['ppred']).abs())/df_dup['observed_max']))
    df = df_dup[['id', name]]
    return df


# 'id', 'id_lat', 'id_lng', 'id_lat_mesh', 'id_lng_mesh', 'id_prefecture', 'pvrate', 'observed_max', 'twoweeks_max_old', 'twoweeks_max', 'nv', 'nv_meshint', 'env', 'preal', 'preal_meshint', 'ppred', 'nv_error', 'nv_perror', 'nv_max_perror', 'nv_meshint_error', 'nv_meshint_perror', 'nv_meshint_max_perror'
base_frame0 = pd.DataFrame(np.zeros((9000, 8)))
base_frame = base_frame0.rename(columns={0: 'year', 1: 'month', 2: 'day', 3: 'time',  4: 'MAPE(/nv)', 5: 'MAPE(/observed_max)', 6: 'RMSPE(/nv)', 7: 'RMSPE(/observed_max)'})
# input()
df_400 = pd.read_csv('F:/study/id_data/extract_40.csv', encoding='utf-8')
df_40 = df_400[['id', 'id_prefecture']]
count = 0
df_write = base_frame.copy()
for i in range(1):
    month = i + 3
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
    for j in range(1):
        day = j+21
        for tt in range(1):
            tt2 = 12.0 + 0.5 * tt
            time = str(year) + str(month) + str(day) + str(tt2)
            print(time)
            fig, ax = plt.subplots()
            df_list = []
            df_list.append(dfmaker_persist())
            df_list.append(dfmaker_persist_nv())
            for parameter in ((parameter_list)):
                df_list.append(dfmaker(parameter))
            for k in range(len(df_list)-1):
                df_list[0] = pd.merge(df_list[0], df_list[k+1])
            print(df_list[0])
            cl_list = list(df_list[0].columns)
            count = count + 1
            boxplot = df_list[0].boxplot(column=cl_list[1:], whis="range", showmeans=True)
            boxplot.plot()
            plt.ylabel('Abusolute Error[%]')
            plt.title('Box plot   time:' + time)
            plt.show()
            # read_path_com = 'F:/study/preprocessing_data/mesh_com/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/error_' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '.csv'
            # write_path = path_day + 'error_' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '.csv'
