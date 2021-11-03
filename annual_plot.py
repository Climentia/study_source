import pandas as pd
import matplotlib.pyplot as plt


id = 1680000002
month = 10
day = 1
time = 11.5
read_path = 'H:/study/preprocessing_data/1_twoweeks_nv/' + str(id) + '.csv'
df = pd.read_csv(read_path, encoding='cp932', names=('year', 'month', 'day', 'tt', 'prate', 'nv', 'twoweeks_max', 'preal'))
fig = plt.figure()
fig.patch.set_facecolor('white')
# グラフ描画場所作成
ax0 = fig.add_subplot(121)
ax1 = fig.add_subplot(122)
for i in range(14):
    npArray_time = []
    npArray_preal = []
    day_f = day + i
    df2 = df[(df['month'] == month) & (df['day'] == day_f)]
    print(df2)
    print(df2[df2['tt'] == time])
    df2['preal'] = df2['nv'] * df2['twoweeks_max']
    npArray_time = df2[['tt']].values
    npArray_preal = df2[['preal']].values
    print(npArray_preal)
    ax0.plot(npArray_time, npArray_preal, label=str(month)+'/'+str(day_f) + ' $P$', c='#6495ed', marker='.', alpha=0.7)
day_f = day + 14
df2 = df[(df['month'] == month) & (df['day'] == day_f)]
df2['preal'] = df2['nv'] * df2['twoweeks_max']
print(df2[df2['tt'] == time])
npArray_time = df2[['tt']].values
npArray_nv = df2[['nv']].values
npArray_preal = df2[['preal']].values
npArray_twoweeks_max = df2[['twoweeks_max']].values
ax0.plot(npArray_time, npArray_preal, label=str(month)+'/'+str(day_f) + ' $P$', c='#ff8c00', marker='.', alpha=0.7)
ax0.plot(npArray_time, npArray_twoweeks_max, label=str(month)+'/'+str(day_f) + ' $P_{2w}$', c='#dc143c', marker='.', alpha=0.7)
ax1.plot(npArray_time, npArray_nv, label=str(month)+'/'+str(day_f) + ' Normalized Value', c='#ff8c00', marker='.', alpha=0.7)
ax0.set_title('Output of the last 14 days and the current day', fontsize=12)
ax1.set_title('Normalization', fontsize=12)
ax0.legend(fontsize=8, loc='upper right')
ax1.legend(fontsize=8, loc='upper left')
ax0.set_xlabel("Time[h]", fontsize=10)
ax0.set_ylabel("Output[w]", fontsize=10)
ax1.set_xlabel("Time[h]", fontsize=10)
ax1.set_ylabel("Normalized Value", fontsize=10)
ax0.set_xlim(4, 19)
ax1.set_ylim(0, 1)
ax1.set_xlim(4, 19)
plt.show()
