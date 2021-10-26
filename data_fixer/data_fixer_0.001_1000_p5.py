import pandas as pd
from decimal import Decimal, ROUND_HALF_UP
mesh_range = 0.02
parameter_list = [[0.001, 1000, 5]]


for parameter in parameter_list:
    print(parameter)
    lambda_num = parameter[0]
    iterate = parameter[1]
    pyramid = parameter[2]
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
            for tt in range(26):
                try:
                    tt2 = 6.5 + 0.5 * tt
                    time = str(year) + str(month) + str(day) + str(tt2)
                    print(time)
                    read_path = 'H:/study/error_data/parameter_lambda_' + str(lambda_num) + '_iterate_' + str(iterate) + '_p' + str(pyramid) + '/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/error_' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '.csv'
                    write_path = 'H:/study/error_data/parameter_lambda_' + str(lambda_num) + '_iterate_' + str(iterate) + '_p' + str(pyramid) + '/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/error_' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '.csv'
                    df = pd.read_csv(read_path, encoding='cp932', engine='python')
                    df2 = df.copy()
                    column_list_00000001 = ['flo_lng', 'flo_lat', 'flo']
                    column_list_000001 = ['id_lat', 'id_lng']
                    column_list_0001 = ['observed_max', 'env', 'nv', 'nv_meshint', 'preal', 'preal_meshint', 'ppred', 'nv_error', 'nv_perror', 'nv_max_perror', 'nv_meshint_error', 'nv_meshint_perror', 'nv_meshint_max_perror']
                    column_list_001 = ['id_lat_mesh', 'id_lng_mesh', 'pvrate']
                    for my_col in df.columns:
                        if my_col in column_list_00000001:
                            df2[my_col] = df2[my_col].map(lambda x: float(Decimal(str(x)).quantize(Decimal('0.0000001'), rounding=ROUND_HALF_UP)))
                        elif my_col in column_list_000001:
                            df2[my_col] = df2[my_col].map(lambda x: float(Decimal(str(x)).quantize(Decimal('0.00001'), rounding=ROUND_HALF_UP)))
                        elif my_col in column_list_0001:
                            df2[my_col] = df2[my_col].map(lambda x: float(Decimal(str(x)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)))
                        elif my_col in column_list_001:
                            df2[my_col] = df2[my_col].map(lambda x: float(Decimal(str(x)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)))
                    # print(df2)
                    # input()
                    df2.to_csv(write_path, encoding='cp932', index=False)
                    # df2.round({'id_lat':5, 'id_lng':5, 'observed_max':1, 'env':3, 'nv':3, 'nv_meshint':3, 'preal':3, 'preal_meshint':3, 'ppred':3, 'nv_error':3, 'nv_perror':3, 'nv_max_perror':3, 'nv_meshint_error':3, 'nv_meshint_perror':3, 'nv_meshint_max_perror':3, 'id_lat_mesh':2, 'id_lng_mesh':2, 'pvrate':2, 'flo_lng':7, 'flo_lat':7, 'flo':7}).to_csv(write_path, encoding='cp932', index=False)
                # print(df2)
                except Exception as e:
                    print(str(e))
