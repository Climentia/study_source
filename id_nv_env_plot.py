import pandas as pd
import matplotlib.pyplot as plt
lambda_num = 0.005
iterate = 1000
pyramid = 5


def if_else01(x):
    if x.month > 7:
        x.year = int(2013)
    else:
        x.year = int(2014)
    if '.5' in str(x.time):
        x.min = int(30)
    else:
        x.min = int(0)
    x.dtime = pd.Timestamp(year=int(x.year), month=int(x.month), day=int(x.day), hour=int(x.time), minute=x.min)
    x.dtime2 = pd.Timestamp(year=int(x.year), month=int(x.month), day=int(x.day), hour=int(x.time), minute=x.min)
    return x


id = 1680000218
month = 7
day = 15
# reading_persist_forecasting
read_pathp = '../error_data/kanto_parameter_persist_nv_30min/error_' + str(id) + '_presist_nv_30min.csv'
read_path = '../annual_error_data/kanto_lambda_' + str(lambda_num) + '_iterate_' + str(iterate) + '_p' + str(pyramid) + '/error_' + str(id) + '.csv'
df = pd.read_csv(read_path, encoding='cp932')
df['dtime'] = 0
df['dtime2'] = 0
df['min'] = 0
df2 = df.apply(if_else01, axis=1)
fig = plt.figure()
fig.patch.set_facecolor('white')
# グラフ描画場所作成
ax0 = fig.add_subplot(111)
df_extract = df2[(df2['month'] == int(month)) & (df2['day'] > day-1) & (df2['day'] < day+1)]
df_extract2 = df3[(df3['month'] == int(month)) & (df3['day'] > day-1) & (df3['day'] < day+1)]
time_index = pd.date_range(start=str(month) + '/' + str(day-1) + '/2014', end=str(month) + '/' + str(day+1) + '/2014', freq='30min')
df_time = pd.DataFrame(range(2*48+1), index=time_index)
df_extract = df_extract.set_index('dtime2')
print(df_time)
print(df_extract)
df_extract = pd.merge(df_extract, df_time, how='outer', left_index=True, right_index=True)
npArray_time = df_extract[['dtime']].values
npArray_preal = df_extract[['preal']].values
npArray_ppred = df_extract[['ppred']].values
# npArray_twoweeks_max = df[['twoweeks_max']].values
ax0.plot(npArray_time, npArray_preal, c='#ff8c00', marker='.', alpha=0.7)
ax0.plot(npArray_time, npArray_ppred, c='#3299FF', marker='.', alpha=0.7)
ax0.set_title('PV', fontsize=12)
ax0.legend(fontsize=8, loc='upper right')
ax0.set_xlabel("Time[h]", fontsize=10)
ax0.set_ylabel("Output[w]", fontsize=10)
# ax0.set_xlim(4, 19)
plt.show()
