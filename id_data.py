import pandas as pd
import math


def return_mesh(x):
    x = float(x)
    y = math.floor(x*100)
    if y % 2 == 0:
        z = round(y/100, 2)
    else:
        z = round(y/100, 2) + 0.01
    return z


df = pd.read_csv('F:/study/id_data/ID_max.csv', encoding='cp932')
df2 = pd.read_csv('F:/study/id_data/ID_prefecture.csv')
df3 = pd.merge(df, df2, on='id')
df3['id_lat_mesh'] = df3['id_lat'].apply(return_mesh)
df3['id_lng_mesh'] = df3['id_lng'].apply(return_mesh)
df4 = df3[['id', 'id_lat', 'id_lng', 'id_lat_mesh', 'id_lng_mesh', 'id_prefecture', 'pvrate', 'observed_max']]
print(df4)
df4.to_csv('id_all_data.csv', encoding='cp932', index=False)
