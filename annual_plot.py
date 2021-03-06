import pandas as pd
import matplotlib.pyplot as plt


id = 6620000089
month = 6
day = 30
j = 0
read_path = 'H:/study/preprocessing_data/1_twoweeks_nv/' + str(id) + '.csv'
df = pd.read_csv(read_path, encoding='cp932', names=('year', 'month', 'day', 'tt', 'prate', 'nv', 'twoweeks_max', 'preal'))
fig = plt.figure()
fig.patch.set_facecolor('white')
# グラフ描画場所作成
ax0 = fig.add_subplot(121)
ax1 = fig.add_subplot(122)
for i in range(15):
    npArray_time = []
    npArray_preal = []
    day_f = day + i - j
    df2 = df[(df['month'] == month) & (df['day'] == day_f)]
    df2['preal'] = df2['nv'] * df2['twoweeks_max']
    npArray_time = df2[['tt']].values
    npArray_preal = df2[['preal']].values
    if i == 14:
        df2 = df[(df['month'] == month) & (df['day'] == day_f)]
        df2['preal'] = df2['nv'] * df2['twoweeks_max']
        npArray_nv = df2[['nv']].values
        npArray_preal = df2[['preal']].values
        npArray_twoweeks_max = df2[['twoweeks_max']].values
        ax0.plot(npArray_time, npArray_preal, label='$P(t)$ of ' + str(month)+'/'+str(day_f), c='#ff8c00', marker='.', alpha=0.7)
        ax0.plot(npArray_time, npArray_twoweeks_max, label='$P_{2w}(t)$ of ' + str(month) + '/' +str(day_f), c='#dc143c', marker='.', alpha=0.7)
        ax1.plot(npArray_time, npArray_nv, label=str(month)+'/'+str(day_f) + ' Normalized Value', c='#ff8c00', marker='.', alpha=0.7)
    elif i == 0:
        ax0.plot(npArray_time, npArray_preal, label='$P(t)$ in last 2 weeks', c='#6495ed', marker='.', alpha=0.1)
    else:
        ax0.plot(npArray_time, npArray_preal, c='#6495ed', marker='.', alpha=0.1)
        # print('skip')
    if (month == 4 or month == 6 or month == 9 or month == 11) and day_f == 30:
        month = month + 1
        day = 1
        j = i+1
    elif month == 2 and day_f == 28:
        month = month + 1
        day = 1
        j = i+1
    elif day_f == 31:
        month = month + 1
        day = 1
        j = i+1
# ax0.set_title('Output of the drastic change day', fontsize=25)
# ax1.set_title('Normalization of the drastic change day', fontsize=25)
ax0.legend(fontsize=12, loc='upper right')
ax1.legend(fontsize=12, loc='upper right')
ax0.set_xlabel("Time[h]", fontsize=20)
ax0.set_ylabel("Power generation output[w]", fontsize=20)
ax1.set_xlabel("Time[h]", fontsize=20)
ax1.set_ylabel("Normalized Value", fontsize=20)
ax0.set_xlim(4.0, 19.0)
ax1.set_ylim(0, 1)
ax1.set_xlim(4.0, 19.0)
# ax0.axvspan(7, 17.5, color="coral", alpha=0.2)
# ax0.axvspan(7.45, 7.55, color="red", alpha=0.2)
# ax0.axvspan(13.45, 13.55, color="red", alpha=0.2)
# ax1.axvspan(7, 17.5, color="coral", alpha=0.2)
# ax1.axvspan(7.45, 7.55, color="red", alpha=0.2)
# ax1.axvspan(13.45, 13.55, color="red", alpha=0.2)
plt.show()
fig.savefig("300_dpi_scatter.png", format="png", dpi=300)
