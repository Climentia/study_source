import csv
import glob
import numpy as np
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

parameter_list = [[1, 1000, 5], [0.516, 1000, 5], [0.266, 1000, 5], [0.137, 1000, 5], [0.071, 1000, 5], [0.036, 1000, 5], [0.019, 1000, 5], [0.010, 1000, 5], [0.005, 1000, 5]]
mesh_range = 0.02
year = 14
month = 9
day = 5
time = 13.5
t = str(year) + str(month) + str(day) + str(time)


def flo_calculation():
    print('-----flo_calculation-----')
    for parameter in parameter_list:
        print(parameter)
        lambda_num = parameter[0]
        iterate = parameter[1]
        pyramid = parameter[2]
        file_path = '../../prediction_data/parameter_lambda_' + str(lambda_num) + '_iterate_' + str(iterate) + '_p' + str(pyramid) + '/flo/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/NV' + str(year) + str(month) + str(day) + str(time) + '_' + str(mesh_range) + '_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '_flo.csv'
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
        df = pd.read_csv(read_path, header=None, names=['lat', 'lng', 'x_flo', 'y_flo'])
        lat_list.append(df['lat'].values.tolist())
        lng_list.append(df['lng'].values.tolist())
        x_list.append(df['x_flo'].values.tolist())
        y_list.append(df['y_flo'].values.tolist())
        count = count + 1
    # fig = plt.figure(figsize=(20, 15))
    # fig.patch.set_facecolor('white')
    # fig.suptitle('vectorplot:' + t)
    # グラフ描画場所作成
    fig, axes = plt.subplots(3, 3, figsize=(30, 40))
    one_dimension_axes = axes.ravel()
    count = 0
    for i, ax in enumerate(one_dimension_axes):
        ax.set_xlabel("longitude", fontsize=10)
        ax.set_ylabel("latitude", fontsize=10)
        ax.quiver(lng_list[count], lat_list[count], x_list[count], y_list[count], color="blue", angles='xy', scale_units='xy', scale=1)
        ax.set_ylim(34.9083, 37.1570)
        ax.set_xlim(138.3806, 140.8588)
        xlim0 = ax.get_xlim()
        ylim0 = ax.get_ylim()
        ax.set_title('lambda:' + str(parameter_list[count][0]) + ' iterate:' + str(parameter_list[count][1]) + 'pyramid:' + str(parameter_list[count][2]), fontsize=10)
        ax.imshow(im, extent=[*xlim0, *ylim0], aspect='auto', alpha=0.9)
        count += 1
    fig.subplots_adjust(wspace=0.2, hspace=0.2)
    fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9)
    # plt.show()
    fig.savefig('vector' + t + '.png')


flo_calculation()
kanto_sort()
visualization()
