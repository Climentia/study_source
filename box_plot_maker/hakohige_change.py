import pandas as pd
import matplotlib.pyplot as plt


parameter_list = [[1, 1000, 5], [0.516, 1000, 5], [0.266, 1000, 5], [0.137, 1000, 5], [0.071, 1000, 5], [0.036, 1000, 5], [0.019, 1000, 5], [0.010, 1000, 5], [0.005, 1000, 5]]
mesh_range = 0.02
df_persist_nv = pd.read_csv('./change_error/change_error_persist_nv_25.csv')
for i in range(len(parameter_list)):
    df = pd.read_csv('./change_error/change_error_lambda_' + str(parameter_list[i][0]) + '_iterate_' + str(parameter_list[i][1]) + '_p' + str(parameter_list[i][2]) + '_25.csv')
    if i == 0:
        df_all = pd.merge(df_persist_nv, df, on=['id', 'year', 'month', 'day', 'time'], how='outer')
    else:
        df_all = pd.merge(df_all, df, on=['id', 'year', 'month', 'day', 'time'], how='outer')
print(df_persist_nv.dtypes)
# df_all = df_all[(df_all['time']>9.5) & (df_all['time']<15.0)]
df_all = df_all.drop_duplicates(subset=('id', 'year', 'month', 'day', 'time'))
df_all.to_csv('test.csv', index=False)
df_all = df_all.dropna()
df_all = df_all.drop('year', axis=1)
df_all = df_all.drop('month', axis=1)
df_all = df_all.drop('day', axis=1)
df_all = df_all.drop('time', axis=1)
# print(df_all)
count_df = df_all['id'].count()
cl_list = list(df_all.columns)
fig, ax = plt.subplots()
plt.ylabel('Abusolute Error[%]', fontsize=15)
plt.title('Box plot Abusolute_error_distribution(changetime)' + '     Number of data:' + str(count_df), fontsize=20)
# boxplot = df_all.boxplot(column=cl_list[1:], whis="range", showmeans=True, fontsize=8)
boxplot = df_all.boxplot(column=cl_list[1:], whis=[0, 100], showmeans=True, fontsize=15, notch=False)
df_write = df_all.describe()
plt.ylim(-5, 100)
plt.show()
df_write.to_csv('write.csv')
