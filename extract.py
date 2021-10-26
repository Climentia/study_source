import pandas as pd
import numpy as np
import math

R = 6356.752
main_km = 15

df = pd.read_csv('./id_all_data.csv', encoding='cp932')
lat_center = 35.78
lng_center = 140.04
df['lat_km'] = R * 2 * math.pi / 360
df['lng_km'] = R * 2 * math.pi * np.cos(df['id_lat']*math.pi/180) / 360
df['r'] = np.sqrt(((df['id_lat'] - lat_center)*df['lat_km'])**2 + ((df['id_lng'] - lng_center)*df['lng_km'])**2)
df2 = df[df['r'] <= main_km]
# df3 = df2.drop_duplicates(subset=('id_lat_mesh', 'id_lng_mesh')).dropna(how='any')
df2.dropna(how='any').to_csv('./extract/extract_' + str(main_km) + '.csv', encoding='cp932', index=False)
