import numpy as np
import pandas as pd
import time
import os


def sort(YY, MM, DD, TT):
    # 時系列順に整理したデータのpath
    path1 = "G:\\id_time\\real_place\\" + MM + "月" + "\\" + MM + "月" + DD + "日" +"\\NV" + YY + MM + DD + TT + "_time_sort.csv"
    print(path1)
    path3_1 = "G:\\id_time\\mesh_place\\" + MM + "月"
    path3_1_ch = os.path.exists(path3_1)
    if path3_1_ch == False:
        os.mkdir(path3_1)
    path3_2 = "G:\\id_time\\mesh_place\\" + MM + "月\\" + MM + "月" + DD + "日"
    path3_2_ch = os.path.exists(path3_2)
    if path3_2_ch == False:
        os.mkdir(path3_2)
    # mesh化書き込みファイル
    path3 = "G:\\id_time\\mesh_place\\" + MM + "月\\" + MM + "月" + DD + "日" + "\\NV" + YY + MM + DD + TT + "_time_sort.csv"
    # 元データ(nv設置場所ごとのデータ)を開く
    df = pd.read_csv(path1, names=('id', 'lat', 'lng', 'nv'))
    check = len(df["nv"])
    if check == 0:
        with open(path3, "w") as fw:
            for i in range(431):
                for j in range(601):
                    lat = round(31.2 + i * 0.02, 2)
                    lng = round(129.6 + j * 0.02, 2)
                    txt = str(round(lat, 2)) + "," + str(round(lng, 2)) + "," + str("NaN") + "\n"
                    fw.writelines(txt)
    else:
        with open(path3, "w") as fw:
            # 緯度経度0.02度gridデータを開く
            for i in range(431):
                for j in range(601):
                    lat = round(31.2 + i * 0.02, 2)
                    lng = round(129.6 + j * 0.02, 2)
                    mesh_place = "G:/id_time/data/mesh_data/id_list_" + str(lat) + "_" + str(lng) + ".txt"
                    mesh_place_ch = os.path.exists(mesh_place)
                    # print(str(lat) + str(lng))
                    if mesh_place_ch  == False:
                        txt = str(round(lat, 2)) + "," + str(round(lng, 2)) + "," + str("NaN") + "\n"
                        fw.writelines(txt)
                    else:
                        with open(mesh_place) as fr:
                            lists = fr.readlines()
                            id_list = []
                            for line in lists:
                                list = line.split(",")
                                id = int(list[0])
                                id_list.append(id)
                        nv_list = []
                        for id_used in id_list:
                            df2 = df[(df["id"] == id_used)]
                            check = df2["nv"].sum()
                            if check > 0:
                                nv = df2.iat[0, 3]
                                nv_list.append(nv)
                        if len(nv_list) > 0:
                            ave = sum(nv_list)/len(nv_list)
                            txt = str(round(lat, 2)) + "," + str(round(lng, 2)) + "," + str(round(ave, 3)) + "\n"
                            fw.writelines(txt)
                        else:
                            txt = str(round(lat, 2)) + "," + str(round(lng, 2)) + "," + str("NaN") + "\n"
                            fw.writelines(txt)


def main():
    for i in range(1):
        MM = i + 4
        if MM == 2:
            DD_max = 28
        elif MM == 4 or MM == 6 or MM == 9 or MM == 11:
            DD_max = 30
        else:
            DD_max = 31
        if MM < 8:
            YY = 14
        elif MM >= 8:
            YY = 13
        for j in range(DD_max):
            DD = 1 + j
            for k in range(28):
                TT = 5 + k * 0.5
                start_time = time.perf_counter()
                sort(str(YY), str(MM), str(DD), str(TT))
                execution_time = time.perf_counter() - start_time
                print(execution_time)


main()
