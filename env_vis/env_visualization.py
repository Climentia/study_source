import csv
import os
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
mesh_range = 0.02
parameter_list = [[1, 1000, 5], [0.516, 1000, 5], [0.266, 1000, 5], [0.137, 1000, 5], [0.071, 1000, 5], [0.036, 1000, 5], [0.019, 1000, 5], [0.010, 1000, 5], [0.005, 1000, 5]]


def isfloat(parameter):
    if not parameter.isdecimal():
        try:
            float(parameter)
            return True
        except ValueError:
            return False
    else:
        return False


def floater(list):
    list2 = [0] * len(list)
    for i in range(len(list)):
        # print(list[i])
        num_ch = isfloat(list[i])
        if num_ch == True:
            list2[i] = str(list[i])
        else:
            list2[i] = 'NaN'
    return list2


def int_calculation(year, month, day, time):
    print('-----env_copy-----')
    for parameter in parameter_list:
        print(parameter)
        lambda_num = parameter[0]
        iterate = parameter[1]
        pyramid = parameter[2]
        file_path = '../../prediction_data/parameter_lambda_' + str(lambda_num) + '_iterate_' + str(iterate) + '_p' + str(pyramid) + '/env/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/NV' + str(year) + str(month) + str(day) + str(time) + '_' + str(mesh_range) + '_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '_env.csv'
        with open(file_path) as f:
            reader = csv.reader(f)
            list = [floater(row) for row in reader]
        write_path = 'sort_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '.csv'
        with open(write_path, "w") as fw:
            for i in range(601):
                for j in range(431):
                    lng = 129.6 + 0.02 * i
                    lat = 31.2 + 0.02 * j
                    try:
                        env = float(list[i][j])
                    except Exception as e:
                        env = "NaN"
                        print(str(e))
                    try:
                        txt = str(round(lat, 2)) + "," + str(round(lng, 2)) + "," + str(env) + "\n"
                    except Exception as e:
                        txt = str(round(lat, 2)) + "," + str(round(lng, 2)) + "," + str(env) + "\n"
                    fw.write(txt)


def kanto_sort(year, month, day, time):
    print('-----kanto_sort-----')
    for parameter in parameter_list:
        print(parameter)
        lambda_num = parameter[0]
        iterate = parameter[1]
        pyramid = parameter[2]
        read_path = 'sort_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '.csv'
        df = pd.read_csv(read_path, header=None, names=['lat', 'lng', 'env'])
        write_path = 'sort_kanto' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '.csv'
        lat_min = 34.8
        lat_max = 37.2
        lng_min = 138.36
        lng_max = 141
        df2 = df[(lat_min <= df['lat']) & (lat_max > df['lat']) & (lng_min <= df['lng']) & (lng_max > df['lng'])]
        df2.to_csv(write_path, index=False, header=False)


def visualization(year, month, day, time):
    t = str(year) + str(month) + str(day) + str(time)
    print('-----visualization-----')
    im = Image.open("./kanto.png")
    for parameter in parameter_list:
        print(parameter)
        lambda_num = parameter[0]
        iterate = parameter[1]
        pyramid = parameter[2]
        lat_list = []
        lng_list = []
        x_list = []
        read_path = 'sort_kanto' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '.csv'
        df = pd.read_csv(read_path, header=None, names=['lat', 'lng', 'env'])
        lat_list.append(df['lat'].values.tolist())
        lng_list.append(df['lng'].values.tolist())
        x_list.append(df['env'].values.tolist())
        fig = plt.figure(figsize=(20, 15))
        fig.patch.set_facecolor('white')
        fig.suptitle('vectorplot:' + t, fontsize=20)
        # グラフ描画場所作成
        ax0 = fig.add_subplot(111)
        ax0.set_ylim(34.8, 37.2)
        ax0.set_xlim(138.36, 141)
        colorlist = ['#FFFFFF', "#FCECEC", "#FADADA", "#F8C7C8", "#F6B5B6", "#F4A3A4", "#F29092", "#F07E80", "#EE6C6E", "#EC595C", "#EC595C", "#EC595C", 'blue']
        names_list = ['0<=nv<0.1', '0.1<=nv<0.2', '0.2<=nv<0.3', '0.3<=nv<0.4', '0.4<=nv<0.5', '0.5<=nv<0.6', '0.6<=nv<0.7', '0.7<=nv<0.8', '0.8<=nv<0.9', '0.9<=nv<1.0']
        for i in range(len(lat_list[0])):
            c = colorlist[10]
            try:
                color_num = int(round(x_list[0][i], 1)* 10)
                c = colorlist[color_num]
                x_min = (lng_list[0][i]-0.01)
                x_max = (lng_list[0][i]+0.01)
                x_1 = round((x_min-138.36)/2.5, 4)
                x_2 = round((x_max-138.36)/2.5, 4)
                if c == 'blue':
                    print('----------------------------------------')
                    print(str(round(x_list[0][i]*10, 1)))
                    print(str(color_num))
                    print(str(int(round(x_list[0][i])*10)))
                    print('----------------------------------------')
                    input()
                if color_num < 0:
                    print('----------------------------------------')
                    print(str(round(x_list[0][i]*10, 1)))
                    print(str(color_num))
                    print(str(int(round(x_list[0][i])*10)))
                    print('----------------------------------------')
                    input()
                ax0.axhspan(round(lat_list[0][i]-0.01, 4), round(lat_list[0][i]+0.01, 4), x_1, x_2, color=c, alpha=0.8)
            except Exception as e:
                x_min = (lng_list[0][i]-0.01)
                x_max = (lng_list[0][i]+0.01)
                x_1 = round((x_min-138.36)/2.5, 4)
                x_2 = round((x_max-138.36)/2.5, 4)
                ax0.axhspan(round(lat_list[0][i]-0.01, 4), round(lat_list[0][i]+0.01, 4), x_1, x_2, color='black', alpha=0.8)
        # 軸ラベル設定
        for j in range(10):
            j = 9-j
            ax0.scatter(0, 0, label=names_list[j], c=colorlist[j], edgecolors="black")
        ax0.scatter(0, 0, label='blank', c="black", edgecolors="black")
        ax0.set_xlabel("longitude", fontsize=18)
        ax0.set_ylabel("latitude", fontsize=18)
        # タイトル設定
        ax0.set_ylim(34.9083, 37.1570)
        ax0.set_xlim(138.3806, 140.8588)
        # 大きさ取得
        ylim0 = ax0.get_ylim()
        xlim0 = ax0.get_xlim()
        ax0.imshow(im, extent=[*xlim0, *ylim0], aspect='auto', alpha=0.9)
        fig.subplots_adjust(wspace=0.2, hspace=0.2)
        fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9)
        ax0.tick_params(axis='x', labelsize=12)
        ax0.legend(loc='lower right')
        fig.savefig('./' + str(year) + str(month) + str(day) + '/' + str(lambda_num) + '/env' + t + '_lambda_' + str(lambda_num) + '_iterate_' + str(iterate) + '_p' + str(pyramid) + '.png')
        plt.clf()


def main():
    for month in range(1):
        month = month + 4
        if month == 2:
            day_max = 28
        elif month == 4 or month == 6 or month == 9 or month == 11:
            day_max = 30
        else:
            day_max = 31
        if month < 8:
            year = 14
        else:
            year = 13
        for day in range(1):
            day = day + 6
            for time in range(14):
                tt2 = 14.0 + 0.5 * time
                t = str(year) + str(month) + str(day) + str(tt2)
                print(t)
                path_day = './' + str(year) + str(month) + str(day) + '/'
                path_day_cheack = os.path.exists(path_day)
                if path_day_cheack == False:
                    os.makedirs(path_day)
                for parameter in parameter_list:
                    lambda_num = parameter[0]
                    lambda_path = path_day + str(lambda_num) + '/'
                    path_day_cheack = os.path.exists(lambda_path)
                    if path_day_cheack == False:
                        os.makedirs(lambda_path)
                int_calculation(year, month, day, tt2)
                kanto_sort(year, month, day, tt2)
                visualization(year, month, day, tt2)


print('start')
main()
