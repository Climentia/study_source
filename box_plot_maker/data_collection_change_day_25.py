import pandas as pd
import numpy as np
parameter_list = [[1, 10, 1], [1, 1000, 1], [1, 1000, 5], [0.5, 1000, 5], [0.1, 1000, 5], [0.05, 1000, 5], [0.01, 1000, 5], [0.005, 1000, 5], [0.001, 1000, 5]]
place = 'kanto'
mesh_range = 0.02


def dfmaker(parameter, year, month, day, tt2, df_extract):
    year = int(year)
    month = int(month)
    day = int(day)
    tt2 = round(float(tt2), 2)
    lambda_num = parameter[0]
    iterate = parameter[1]
    pyramid = parameter[2]
    name = 'LMD:' + str(parameter[0]) + '::ITR:' + str(parameter[1]) + '::PRM:' + str(parameter[2])
    read_path = 'H:/study/error_data/kanto_parameter_lambda_' + str(lambda_num) + '_iterate_' + str(iterate) + '_p' + str(pyramid) + '/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/' + 'error_' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '.csv'
    df_read0 = pd.read_csv(read_path, encoding='cp932')
    df_dup = pd.merge(df_read0, df_extract, on='id')
    # df_dup[name] = (((100*(df_dup['preal']-df_dup['ppred']).abs())/df_dup['observed_max']))
    df_dup[name] = (df_dup['nv']-df_dup['env']).abs() * 100
    df_dup['year'] = year
    df_dup['month'] = month
    df_dup['day'] = day
    df_dup['time'] = tt2
    df = df_dup[['id', 'year', 'month', 'day', 'time', name]]
    print(df)
    return df


def dfmaker_persist(year, month, day, tt2, df_extract):
    year = int(year)
    month = int(month)
    day = int(day)
    tt2 = round(float(tt2), 2)
    name = 'persist'
    read_path = 'H:/study/error_data/parameter_persist_30min' + '/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/' + 'error_' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_presist_30min.csv'
    df_read0 = pd.read_csv(read_path, encoding='cp932')
    df_dup = pd.merge(df_read0, df_extract)
    # df_dup[name] = (((100*(df_dup['preal_meshint']-df_dup['ppred']).abs())/df_dup['observed_max']))
    df_dup['year'] = year
    df_dup['month'] = month
    df_dup['day'] = day
    df_dup['time'] = tt2
    df = df_dup[['id', 'year', 'month', 'day', 'time', name]]
    return df


def dfmaker_persist_nv(year, month, day, tt2, df_extract):
    year = int(year)
    month = int(month)
    day = int(day)
    tt2 = round(float(tt2), 2)
    name = 'persist_nv'
    read_path = 'H:/study/error_data/kanto_parameter_persist_nv_30min' + '/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/' + 'error_' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_presist_nv_30min.csv'
    df_read0 = pd.read_csv(read_path, encoding='cp932')
    df_dup = pd.merge(df_read0, df_extract)
    # df_dup[name] = (((100*(df_dup['preal']-df_dup['ppred']).abs())/df_dup['observed_max']))
    df_dup[name] = (df_dup['nv']-df_dup['env']).abs() * 100
    df_dup['year'] = year
    df_dup['month'] = month
    df_dup['day'] = day
    df_dup['time'] = tt2
    df = df_dup[['id', 'year', 'month', 'day', 'time', name]]
    return df


def parameter_fanc():
    count = 0
    extract_path = 'H:/study/id_data/extract/extract_15.csv'
    df_extract0 = pd.read_csv(extract_path, encoding='cp932')
    df_extract = df_extract0[['id', 'r']]
    df_change_weather = pd.read_csv('H:/study/source/weather/change_weather_25.csv',
                                    encoding='cp932')
    df_change_weather = df_change_weather[df_change_weather['change'] > 0]
    for parameter in parameter_list:
        print(parameter)
        lambda_num = parameter[0]
        iterate = parameter[1]
        pyramid = parameter[2]
        year = df_change_weather.iat[0, 0]
        month = df_change_weather.iat[0, 1]
        day = df_change_weather.iat[0, 2]
        tt2 = df_change_weather.iat[0, 3]
        time = str(year) + str(month) + str(day) + str(tt2)
        df = dfmaker(parameter, year, month, day, tt2, df_extract)
        for i in range(df_change_weather['year'].count()-1):
            i = i+1
            year = df_change_weather.iat[i, 0]
            month = df_change_weather.iat[i, 1]
            day = df_change_weather.iat[i, 2]
            tt2 = df_change_weather.iat[i, 3]
            time = str(year) + str(month) + str(day) + str(tt2)
            print(time)
            df2 = dfmaker(parameter, year, month, day, tt2, df_extract)
            df = pd.concat([df, df2])
            count = count + 1
        write_path = './change_error/change_error_' + 'lambda_' + str(lambda_num) + '_iterate_' + str(iterate) + '_p' + str(pyramid) + '_25.csv'
        df.to_csv(write_path, index=False)


def persist_fanc():
    extract_path = 'H:/study/id_data/extract/extract_15.csv'
    df_extract0 = pd.read_csv(extract_path, encoding='cp932')
    df_extract = df_extract0[['id', 'r']]
    df_change_weather = pd.read_csv('H:/study/source/weather/change_weather_25.csv',
                                    encoding='cp932')
    df_change_weather = df_change_weather[df_change_weather['change'] > 0]
    for i in range(1):
        year = df_change_weather.iat[0, 0]
        month = df_change_weather.iat[0, 1]
        day = df_change_weather.iat[0, 2]
        tt2 = df_change_weather.iat[0, 3]
        time = str(year) + str(month) + str(day) + str(tt2)
        df = dfmaker_persist_nv(year, month, day, tt2, df_extract)
        for i in range(df_change_weather['year'].count()-1):
            i = i+1
            year = df_change_weather.iat[i, 0]
            month = df_change_weather.iat[i, 1]
            day = df_change_weather.iat[i, 2]
            tt2 = df_change_weather.iat[i, 3]
            time = str(year) + str(month) + str(day) + str(tt2)
            print(time)
            df2 = dfmaker_persist_nv(year, month, day, tt2, df_extract)
            df = pd.concat([df, df2])
            print(df)
        write_path = './change_error/change_error_' + 'persist_nv_25.csv'
        df.to_csv(write_path, index=False)


parameter_fanc()
persist_fanc()
# for parameter in parameter_list:
