# 予測データ(binファイルで生成)のコピーと名前の変更
import os
import shutil
mesh_range = 0.02

for month in range(12):
    month = month + 1
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
    path_month = "F:/study/preprocessing_data/4_interpolated_mesh/" + str(month) + "月"
    for day in range(day_max):
        day = day + 1
        path_day = path_month + "/" + str(month) + "月" + str(day) + "日"
        for tt in range(26):
            tt2 = 5.5 + 0.5 * tt
            path_origin = path_day + "/" + "NV" + str(year) + str(month) + str(day) + str(tt2) + str(mesh_range) + "_int.csv"
            path_copy1 = "E:/bin/" + "NVyy"+ str(year) + "mm" +str(month) + "dd" + str(day) + "tt" + str(tt2) + "_" + str(mesh_range) + "_int.csv"
            # path_copy2 = "F:/bin2/" + "NVyy"+ str(year) + "mm" +str(month) + "dd" + str(day) + "tt" + str(tt2) + "_" + str(mesh_range) + "_int.csv"
            # path_copy3 = "F:/bin3/" + "NVyy"+ str(year) + "mm" +str(month) + "dd" + str(day) + "tt" + str(tt2) + "_" + str(mesh_range) + "_int.csv"
            print(path_origin)
            cheack = os.path.exists(path_origin)
            if cheack == True:
                shutil.copy(path_origin, path_copy1)
                # shutil.copy(path_origin, path_copy2)
                # shutil.copy(path_origin, path_copy3)
