import csv
import os
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
mesh_range = 0.02


def int_calculation(year, month, day, time):
    print('-----int_copy-----')
    file_path = 'H:/study/preprocessing_data/3_mesh_place/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/NV' + str(year) + str(month) + str(day) + str(time) + '_int.csv'
    with open(file_path) as f:
        reader = csv.reader(f)
        list = [row for row in reader]
    write_path = 'sort.csv'
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
    read_path = 'H:/study/preprocessing_data/3_mesh_place/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/NV' + str(year) + str(month) + str(day) + str(time) + '_time_sort.csv'
    df = pd.read_csv(read_path, header=None, names=['lat', 'lng', 'env'])
    write_path = 'sort_kanto.csv'
    lat_min = 34.8
    lat_max = 37.2
    lng_min = 138.36
    lng_max = 141
    df2 = df[(lat_min <= df['lat']) & (lat_max > df['lat']) & (lng_min <= df['lng']) & (lng_max > df['lng'])]
    df2.to_csv(write_path, index=False, header=False)


def visualization(year, month, day, time):
    t = str(year) + str(month) + str(day) + str(time)
    im = Image.open("./kanto.png")
    print('-----visualization-----')
    lat_list = []
    lng_list = []
    x_list = []
    read_path = 'sort_kanto.csv'
    df = pd.read_csv(read_path, header=None, names=['lat', 'lng', 'env'])
    lat_list.append(df['lat'].values.tolist())
    lng_list.append(df['lng'].values.tolist())
    x_list.append(df['env'].values.tolist())
    fig = plt.figure(figsize=(20, 15))
    fig.patch.set_facecolor('white')
    fig.suptitle('vectorplot:' + t, fontsize=15)
    # グラフ描画場所作成
    ax0 = fig.add_subplot(111)
    ax0.set_ylim(34.8, 37.2)
    ax0.set_xlim(138.36, 141)
    colorlist = ['#FFFFFF', "#FCECEC", "#FADADA", "#F8C7C8", "#F6B5B6", "#F4A3A4", "#F29092", "#F07E80", "#EE6C6E", "#EC595C", "#EC595C", 'blue']
    names_list = ['0<=nv<0.1', '0.1<=nv<0.2', '0.2<=nv<0.3', '0.3<=nv<0.4', '0.4<=nv<0.5', '0.5<=nv<0.6', '0.6<=nv<0.7', '0.7<=nv<0.8', '0.8<=nv<0.9', '0.9<=nv<1.0']
    for i in range(len(lat_list[0])):
        try:
            color_num = int(round(x_list[0][i], 1)*10)
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
    for j in range(10):
        j = 9-j
        ax0.scatter(0, 0, label=names_list[j], c=colorlist[j], edgecolors="black")
    ax0.scatter(0, 0, label='blank', c="black", edgecolors="black")
    ax0.set_xlabel("longitude", fontsize=12)
    ax0.set_ylabel("latitude", fontsize=12)
    # タイトル設定
    ax0.set_ylim(34.9083, 37.1570)
    ax0.set_xlim(138.3806, 140.8588)
    # 大きさ取得
    ylim0 = ax0.get_ylim()
    xlim0 = ax0.get_xlim()
    ax0.imshow(im, extent=[*xlim0, *ylim0], aspect='auto', alpha=0.9)
    fig.subplots_adjust(wspace=0.2, hspace=0.2)
    fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9)
    ax0.legend(loc='lower right')
    fig.savefig('./' + str(year) + str(month) + str(day) + '/int' + t + '.png')


def main():
    for month in range(1):
        month = month + 7
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
            day = day + 14
            for time in range(15):
                tt2 = 9.0 + 0.5 * time
                t = str(year) + str(month) + str(day) + str(tt2)
                print(t)
                path_day = './' + str(year) + str(month) + str(day) + '/'
                path_day_cheack = os.path.exists(path_day)
                if path_day_cheack == False:
                    os.makedirs(path_day)
                # int_calculation(year, month, day, tt2)
                kanto_sort(year, month, day, tt2)
                visualization(year, month, day, tt2)


print('start')
main()
