import csv
import glob
import numpy as np
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

parameter_list = [[1, 10, 1], [1, 1000, 1], [1, 1000, 5], [0.1, 1000, 5], [0.01, 1000, 5]]
mesh_range = 0.02
year = 14
month = 3
day = 21
time = 13.0
t = str(year) + str(month) + str(day) + str(time)


def flo_calculation():
    print('-----flo_calculation-----')
    for parameter in parameter_list:
        print(parameter)
        lambda_num = parameter[0]
        iterate = parameter[1]
        pyramid = parameter[2]
        file_path = 'F:/study/prediction_data/parameter_lambda_' + str(lambda_num) + '_iterate_' + str(iterate) + '_p' + str(pyramid) + '/flo/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/NV' + str(year) + str(month) + str(day) + str(time) + '_' + str(mesh_range) + '_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '_flo.csv'
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
                        flo_y = float(list[i][j*2]) * 1/50
                        flo_x = float(list[i][(j*2)+1]) * 1/50
                    except Exception as e:
                        flo_y = "NaN"
                        flo_x = "NaN"
                        print(str(e))
                    try:
                        txt = str(round(lat, 2)) + "," + str(round(lng, 2)) + "," + str(flo_x) + "," + str(flo_y) + "\n"
                    except Exception as e:
                        txt = str(round(lat, 2)) + "," + str(round(lng, 2)) + "," + str(flo_x) + "," + str(flo_y) + "\n"
                    fw.write(txt)


def kanto_sort():
    print('-----kanto_sort-----')
    for parameter in parameter_list:
        print(parameter)
        lambda_num = parameter[0]
        iterate = parameter[1]
        pyramid = parameter[2]
        read_path = 'sort_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '.csv'
        df = pd.read_csv(read_path, header=None, names=['lat', 'lng', 'x_flo', 'y_flo'])
        write_path = 'sort_kanto' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '.csv'
        with open(write_path, "w") as fw:
            for i in range(24):
                for j in range(24):
                    lat = 34.8 + 0.1 * i
                    lat_min = lat-0.05
                    lat_max = lat+0.05
                    lng = 138.4 + 0.1 * j
                    lng_min = lng-0.05
                    lng_max = lng+0.05
                    df2 = df[(lat_min <= df['lat']) & (lat_max > df['lat']) & (lng_min <= df['lng']) & (lng_max > df['lng'])]
                    flo_x = df2['x_flo'].mean()
                    flo_y = df2['y_flo'].mean()
                    txt = str(round(lat, 2)) + "," + str(round(lng, 2)) + "," + str(flo_x) + "," + str(flo_y) + "\n"
                    fw.write(txt)


def visualization():
    im = Image.open("./kanto.png")
    print('-----visualizatio-----')
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
        df = pd.read_csv(read_path, header=None, names=['lat', 'lng', 'x_flo', 'y_flo'])
        lat_list.append(df['lat'].values.tolist())
        lng_list.append(df['lng'].values.tolist())
        x_list.append(df['x_flo'].values.tolist())
        y_list.append(df['y_flo'].values.tolist())
        count = count + 1
    fig = plt.figure(figsize=(20, 20))
    fig.patch.set_facecolor('white')
    fig.title('vectorplot:' + t)
    # グラフ描画場所作成
    ax0 = fig.add_subplot(231)
    ax1 = fig.add_subplot(232)
    ax2 = fig.add_subplot(233)
    ax3 = fig.add_subplot(234)
    ax4 = fig.add_subplot(235)
    # 軸ラベル設定
    ax0.set_xlabel("longitude", fontsize=8)
    ax0.set_ylabel("latitude", fontsize=8)
    ax1.set_xlabel("longitude", fontsize=8)
    ax1.set_ylabel("latitude", fontsize=8)
    ax2.set_xlabel("longitude", fontsize=8)
    ax2.set_ylabel("latitude", fontsize=8)
    ax3.set_xlabel("longitude", fontsize=8)
    ax3.set_ylabel("latitude", fontsize=8)
    ax4.set_xlabel("longitude", fontsize=8)
    ax4.set_ylabel("latitude", fontsize=8)
    # タイトル設定
    ax0.quiver(lng_list[0], lat_list[0], x_list[0], y_list[0], color="blue", angles='xy', scale_units='xy', scale=1)
    ax1.quiver(lng_list[1], lat_list[1], x_list[1], y_list[1], color="blue", angles='xy', scale_units='xy', scale=1)
    ax2.quiver(lng_list[2], lat_list[2], x_list[2], y_list[2], color="blue", angles='xy', scale_units='xy', scale=1)
    ax3.quiver(lng_list[3], lat_list[3], x_list[3], y_list[3], color="blue", angles='xy', scale_units='xy', scale=1)
    ax4.quiver(lng_list[4], lat_list[4], x_list[4], y_list[4], color="blue", angles='xy', scale_units='xy', scale=1)
    # 大きさ取得
    xlim0 = ax0.get_xlim()
    ylim0 = ax0.get_ylim()
    xlim1 = ax1.get_xlim()
    ylim1 = ax1.get_ylim()
    xlim2 = ax2.get_xlim()
    ylim2 = ax2.get_ylim()
    xlim3 = ax3.get_xlim()
    ylim3 = ax3.get_ylim()
    xlim4 = ax4.get_xlim()
    ylim4 = ax4.get_ylim()
    ax0.set_title('lambda:1 iterate:10 pyramid:1', fontsize=10)
    ax1.set_title('lambda:1 iterate:1000 pyramid:1', fontsize=10)
    ax2.set_title('lambda:1 iterate:1000 pyramid:5', fontsize=10)
    ax3.set_title('lambda:0.1 iterate:1000 pyramid:5', fontsize=10)
    ax4.set_title('lambda:0.01 iterate:1000 pyramid:5', fontsize=10)
    ax0.imshow(im, extent=[*xlim0, *ylim0], aspect='auto', alpha=0.9)
    ax1.imshow(im, extent=[*xlim1, *ylim1], aspect='auto', alpha=0.9)
    ax2.imshow(im, extent=[*xlim2, *ylim2], aspect='auto', alpha=0.9)
    ax3.imshow(im, extent=[*xlim3, *ylim3], aspect='auto', alpha=0.9)
    ax4.imshow(im, extent=[*xlim4, *ylim4], aspect='auto', alpha=0.9)
    fig.savefig('vector' + t + '.png')


# flo_calculation()
# kanto_sort()
visualization()
