import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
id = 1680000063
year = 13
month = '09'
day = '01'
time = 11.5


def if_else01(x):
    if x.month > 7:
        x.year = int(2013)
    else:
        x.year = int(2014)
    if '.5' in str(x.tt):
        x.min = int(30)
    else:
        x.min = int(0)
    x.time = pd.Timestamp(year=int(x.year), month=int(x.month), day=int(x.day), hour=int(x.tt), minute=x.min)
    return x


read_path = '../preprocessing_data/0_original_data/PV発電量データ_1308-1401/20' + str(year) + '年' +  str((month)) + '月' + '/2_分別利用電力情報20' + str(year) + '年' + str((month)) + '月分.csv'
df = pd.read_csv(read_path, names=('ユーザID', 'データ計測日時', '買電電力量', '売電電力量', '発電電力量', '全消費電力量'))
df = df[df['ユーザID'] == id]
df['データ計測日時'] = pd.to_datetime(df['データ計測日時'])
df['time'] = (pd.to_datetime(df['データ計測日時'], format='%H:%M:%S').dt.time).astype(str)
df.index = df['データ計測日時']
print(df.dtypes)
print(df)
year2 = int('20' + str(year))
# df_display = df['20' + str(year) + '-' + str(month) + '-' + str(day) : '20' + str(year) + '-' + str(month) + '-' + str(day)]
# print(df_display['発電電力量'][(df_display['発電電力量'] > 0) & (df_display['ユーザID'] == id)])
# read_path = 'H:/study/preprocessing_data/1_twoweeks_nv_sort/' + str(id) +'.csv'
# df = pd.read_csv(read_path, encoding='cp932', names=('year', 'month', 'day', 'tt', 'prate', 'nv', 'twoweeks_max', 'preal'))
# df['time'] = 0
# df['min'] = 0
# df = df.apply(if_else01, axis=1)
# print(df)
# df['time'] = pd.Timestamp(int(),12,18)
fig, ax = plt.subplots()
for i in range(15):
    npArray_time = []
    npArray_preal = []
    day_f = int(day) + i
    df2 = df['20' + str(year) + '-' + str(month) + '-' + str(day_f) : '20' + str(year) + '-' + str(month) + '-' + str(day_f)]
    npArray_time = df2[['time']].to_numpy().tolist()
    npArray_preal = df2[['発電電力量']].astype(np.float64).values
    print((npArray_preal))
    ax.plot(npArray_preal, label=str(month)+str(day_f), c='#6495ed', marker='.', alpha=0.7)
    alen = len(npArray_time)
    arg = np.arange(alen)
# day_f = int(day) + 15
# df2 = df[(df['month'] == month) & (df['day'] == day_f)]
# print(df2[df2['time'] == time])
# npArray_time = df2[['tt']].values
# npArray_preal = df2[['preal']].values
# npArray_twoweeks_max = df2[['twoweeks_max']].values
# ax.plot(npArray_time, npArray_preal, label=str(month)+str(day_f), c='#ff8c00', marker='.', alpha=0.3)
 #ax.plot(npArray_time, npArray_twoweeks_max, label=str(month)+str(day_f) + '_twoweeks_max', c='#dc143c', marker='.', alpha=0.1)
read_path2 = '../preprocessing_data/1_two_weeks_nv/' + str(id) + '.csv'
df3 = pd.read_csv(read_path2, encoding='cp932', names=('year', 'month', 'day', 'tt', 'prate', 'nv', 'twoweeks_max'))
df3['time'] = 0
df3['min'] = 0
df3 = df3.apply(if_else01, axis=1)
day_f = int(day) + 15
df4 = df3[(df3['month'] == int(month)) & (df3['day'] == day_f)]
print(df4)
# npArray_preal = df4[['preal']].values
npArray_twoweeks_max = df4[['twoweeks_max']].values
# ax.plot(npArray_preal, label=str(month)+str(day_f), c='#ff8c00', marker='.', alpha=0.7)
ax.plot(npArray_twoweeks_max, label=str(month)+str(day_f), c='#dc143c', marker='.', alpha=0.7)
for j in range(alen):
    npArray_time[j] = npArray_time[j][0]
plt.xticks(arg, npArray_time, rotation=90)
plt.legend()
plt.ylim(-5, 10000)
plt.show()
