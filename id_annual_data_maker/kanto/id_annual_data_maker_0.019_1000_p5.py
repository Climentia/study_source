# 各時間帯のデータから任意のidの一年分のデータを抽出する
import pandas as pd
import numpy as np
import os

# 各パラメータ
mesh_range = 0.02
parameter_list = [0.019, 1000, 5]
lambda_num = parameter_list[0]
iterate = parameter_list[1]
pyramid = parameter_list[2]
# 書き込むファイルの雛形を作成
df_write0 = pd.DataFrame(np.zeros((35000, 22)))
df_write0 = df_write0.rename(columns={0: 'year', 1: 'month', 2: 'day', 3: 'time', 4: 'id', 5: 'id_lat', 6: 'id_lng', 7: 'id_lat_mesh', 8: 'id_lng_mesh', 9: 'id_prefecture', 10: 'pvrate', 11: 'observed_max', 12: 'twoweeks_max', 13: 'flo_lng', 14: 'flo_lat', 15: 'flo', 16: 'nv', 17: 'nv_meshint', 18: 'env', 19: 'preal', 20: 'preal_meshint', 21: 'ppred'})
df_write0['id_prefecture'] = df_write0['id_prefecture'].apply(lambda _: str(_))
# 抽出したいidがまとまっているファイルを開く
df_extract = pd.read_csv('../../../id_data/extract/extract_15.csv', encoding='cp932')
# 開いたファイルからid一つずつデータを抽出
for a in range(len(df_extract)):
    # 書き込むファイルを生成(初期化)
    df_write = df_write0.copy()
    # 抽出するid
    extract_id = df_extract.iat[a, 0]
    print(str(extract_id))
    count = 0
    # 月
    for i in range(12):
        # ８月から始まるようにする(データの区間が2013年8月~2014年7月までの期間なので)
        if i < 5:
            month = i + 8
        else:
            month = i - 4
        # 年を切り替え
        if month < 8:
            year = 14
        else:
            year = 13
        # 月によって日の数が違う為,月の日の数を指定
        if month == 2:
            day_max = 28
        elif month == 4 or month == 6 or month == 9 or month == 11:
            day_max = 30
        else:
            day_max = 31
        # 日
        for j in range(day_max):
            day = j+1
            # 各時間(30分おき)
            for tt in range(24):
                tt2 = 6.5 + 0.5 * tt
                # print(str(year) + str(month) + str(day) + str(tt2))
                # 書き込むデータファイルにcountの行においてyear, month, day, tt2 の値を入れる
                df_write.iat[count, 0] = year
                df_write.iat[count, 1] = month
                df_write.iat[count, 2] = day
                df_write.iat[count, 3] = tt2
                # 例外処理(読み込みたいファイルがなかった等の場合飛ばす)
                try:
                    # その時間帯の全idのデータが入っているファイルを読み込む
                    read_path = '../../../error_data/kanto_parameter_lambda_' + str(lambda_num) + '_iterate_' + str(iterate) + '_p' + str(pyramid) + '/' + str(month) + '月/' + str(month) + '月' + str(day) + '日/error_' + str(year) + str(month) + str(day) + str(tt2) + '_' + str(mesh_range) + '_' + str(lambda_num) + '_' + str(iterate) + '_p' + str(pyramid) + '.csv'
                    df_time = pd.read_csv(read_path, encoding='cp932')
                    # 抽出したいidをdf_timeから抽出
                    df_id = df_time[(df_time['id'] < extract_id+1) & (df_time['id'] > extract_id-1)].round({'id_lat':5, 'id_lng':5})
                    # 各情報を書き込むデータファイルのcountの行に代入
                    for k in range(18):
                        df_write.iat[count, k+4] = df_id.iat[0, k]
                    count = count + 1
                # 例外が起きた場合飛ばす
                except Exception as e:
                    print(str(e))
                # 時間が切り替わる時にcountを1進める
                count = count + 1
    # 余ってる行(全部0の行)があるはずなのでそれを除去
    df_write = df_write[df_write['id'] > 0]
    # df_writeファイルを書き込む
    path_log = '../../../annual_error_data/kanto_lambda' + str(lambda_num) + 'iterate' + str(iterate) + '_p' + str(pyramid) + '/'
    path_month_cheack = os.path.exists(path_log)
    if path_month_cheack == False:
        os.makedirs(path_log)
    df_write.to_csv(path_log + 'error_' + str(extract_id) + '.csv', encoding='cp932', index=False)
