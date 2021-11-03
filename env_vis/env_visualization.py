import csv
import glob
import numpy as np
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

parameter_list = [[0.05, 1000, 5]]
mesh_range = 0.02
year = 14
month = 4
day = 6
time = 14.0
t = str(year) + str(month) + str(day) + str(time)


def env_calculation():
    print('-----int_copy-----')
    for parameter in parameter_list:
        print(parameter)
        lambda_num = parameter[0]
        iterate = parameter[1]
        pyramid = parameter[2]
        file_path = 'H:/study/prediction_data/parameter_lambda_' + str(lambda_num) + '_iterate_' + str(iterate) + '_p' + str(pyramid) + '/env/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/NV' + str(year) + str(month) + str(day) + str(time) + '_' + str(mesh_range) + '_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '_env.csv'
        with open(file_path) as f:
            reader = csv.reader(f)
            list = [row for row in reader]
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


def kanto_sort():
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
        lng_max = 140.86
        df2 = df[(lat_min <= df['lat']) & (lat_max > df['lat']) & (lng_min <= df['lng']) & (lng_max > df['lng'])]
        df2.to_csv(write_path, index=False, header=False)



def visualization():
    im = Image.open("./kanto.png")
    print('-----visualization-----')
    count = 0
    lat_list = []
    lng_list = []
    x_list = []
    y_list = []
    for parameter in parameter_list:
        print(parameter)
        lambda_num = parameter[0]
        iterate = parameter[1]
        pyramid = parameter[2]
        read_path = 'sort_kanto' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '.csv'
        df = pd.read_csv(read_path, header=None, names=['lat', 'lng', 'env'])
        lat_list.append(df['lat'].values.tolist())
        lng_list.append(df['lng'].values.tolist())
        x_list.append(df['env'].values.tolist())
        count = count + 1
    fig = plt.figure(figsize=(20, 15))
    fig.patch.set_facecolor('white')
    fig.suptitle('vectorplot:' + t)
    # グラフ描画場所作成
    ax0 = fig.add_subplot(111)
    ax0.set_ylim(34.8, 37.2)
    ax0.set_xlim(138.36, 140.86)
    colorlist = ["#FFDBC9", "#FFC7AF", "#FFAD90", "#FF9872", "#FF8856", "#FF773E", "#FF6928", "#FF5F17", "#FF570D", "#FF4F02"]
    for i in range(len(lat_list[0])):
        try:
            color_num = int(round(x_list[0][i], 1)*10) - 1
            c = colorlist[color_num]
            x_min = (lng_list[0][i]-0.01)
            x_max = (lng_list[0][i]+0.01)
            x_1 = round((x_min-138.36)/2.5, 4)
            x_2 = round((x_max-138.36)/2.5, 4)
            ax0.axhspan(round(lat_list[0][i]-0.01, 4), round(lat_list[0][i]+0.01, 4), x_1, x_2, color=c, alpha=0.8)
        except Exception as e:
            x_min = (lng_list[0][i]-0.01)
            x_max = (lng_list[0][i]+0.01)
            x_1 = round((x_min-138.36)/2.5, 4)
            x_2 = round((x_max-138.36)/2.5, 4)
            ax0.axhspan(round(lat_list[0][i]-0.01, 4), round(lat_list[0][i]+0.01, 4), x_1, x_2, color='black', alpha=0.8)
    # 軸ラベル設定
    ax0.set_xlabel("longitude", fontsize=8)
    ax0.set_ylabel("latitude", fontsize=8)
    # タイトル設定
    ax0.set_ylim(34.9083, 37.1570)
    ax0.set_xlim(138.3806, 140.8588)
    # 大きさ取得
    ylim0 = ax0.get_ylim()
    xlim0 = ax0.get_xlim()
    ax0.set_title('lambda:1 iterate:1000 pyramid:5', fontsize=10)
    ax0.imshow(im, extent=[*xlim0, *ylim0], aspect='auto', alpha=0.9)
    fig.subplots_adjust(wspace=0.2, hspace=0.2)
    fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9)
    # plt.show()
    fig.savefig('int' + t + '.png')


env_calculation()
kanto_sort()
visualization()
