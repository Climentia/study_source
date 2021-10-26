import os
import glob
import shutil
mesh_range = 0.02
lambda_num = 1
iterate = 1000
pyramid = 1


kameda_path = 'F:/bin2/exp/PSNR_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '/'
kameda_cheack = os.path.exists(kameda_path)
if kameda_cheack == True:
    path_list_env = glob.glob(kameda_path + '*_zero.csv')
    path_list_flo = glob.glob(kameda_path + '*_flo.csv')
    for i in range(12):
        month = i + 1
        if month < 8:
            year = 14
        else:
            year = 13
        path_month_env = 'F:/study/prediction_data/parameter_lambda_' + str(lambda_num) + '_iterate_' + str(iterate) + '_p' + str(pyramid) + '/env/' + str(month) + '月/'
        path_month_flo = 'F:/study/prediction_data/parameter_lambda_' + str(lambda_num) + '_iterate_' + str(iterate) + '_p' + str(pyramid) + '/flo/' + str(month) + '月/'
        path_month_ch_env = os.path.exists(path_month_env)
        path_month_ch_flo = os.path.exists(path_month_flo)
        if path_month_ch_env == False:
            os.makedirs(path_month_env)
        if path_month_ch_flo == False:
            os.makedirs(path_month_flo)
        if month == 2:
            day_max = 28
        elif month == 4 or month == 6 or month == 9 or month == 11:
            day_max = 30
        else:
            day_max = 31
        for j in range(day_max):
            day = j+1
            path_day_env = path_month_env + '/' + str(month) + '月' + str(day) + '日/'
            path_day_ch_env = os.path.exists(path_day_env)
            path_day_flo = path_month_flo + '/' + str(month) + '月' + str(day) + '日/'
            path_day_ch_flo = os.path.exists(path_day_flo)
            if path_day_ch_env == False:
                os.makedirs(path_day_env)
            if path_day_ch_flo == False:
                os.makedirs(path_day_flo)
            for tt in range(30):
                tt2 = 6.5 + 0.5 * tt
                unit = "NVyy" + str(year) + "mm" + str(month) + "dd" + str(day) + "tt" + str(tt2) + "_" + str(mesh_range) +"_int"
                print(unit)
                extraction_env = [path for path in path_list_env if unit in path]
                if len(extraction_env) > 0:
                    path_origin_env = extraction_env[0]
                    # print(extraction_env)
                    path_copy_env = path_day_env + "/NV" + str(year) + str(month) + str(day) + str(tt2) + "_" + str(mesh_range) + "_" + str(lambda_num) + "_" + str(iterate) + "_p" + str(pyramid) + "_env.csv"
                    # print(path_origin_env)
                    cheack = os.path.exists(path_origin_env)
                    if cheack == True:
                        shutil.copy(path_origin_env, path_copy_env)
                        print('copy!\nfrom:'+ path_origin_env + '\nto:' + path_copy_env)
                extraction_flo = [path for path in path_list_flo if unit in path]
                if len(extraction_flo) > 0:
                    path_origin_flo = extraction_flo[0]
                    # print(extraction_flo)
                    path_copy_flo = path_day_flo + "/NV" + str(year) + str(month) + str(day) + str(tt2) + "_" + str(mesh_range) + "_" + str(lambda_num) + "_" + str(iterate) + "_p" + str(pyramid) + "_flo.csv"
                    # sprint(path_origin_flo)
                    cheack = os.path.exists(path_origin_flo)
                    if cheack == True:
                        shutil.copy(path_origin_flo, path_copy_flo)
                        print('copy!\nfrom:'+ path_origin_flo + '\nto:' + path_copy_flo)
                print('/////////////////////////////////////////////////////')
