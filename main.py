# In[0] import and config

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob

# 设置包含CSV文件的目录路径
directory_path = 'data'  # 请确保替换为实际目录路径

# 读取CSV文件的路径
file_path = r'data/PRSA_Data_Aotizhongxin_20130301-20170228.csv'  # 请确保替换为实际文件路径

# In[1]

# 获取目录中所有CSV文件的文件路径列表
csv_files = glob.glob(os.path.join(directory_path, '*.csv'))

# 创建一个空列表，用于存储每个CSV文件的DataFrame
dataframes = []

# 遍历每个CSV文件路径，读取数据并添加到列表中
for file in csv_files:
    df = pd.read_csv(file)
    dataframes.append(df)

# 将所有DataFrame合并为一个DataFrame
combined_df = pd.concat(dataframes, ignore_index=True)

# 展示合并后的DataFrame前几行数据
print(combined_df.head())

# 检查合并后的DataFrame的数据类型
print(combined_df.dtypes)


# In[2]

# 从CSV文件读取数据
df = pd.read_csv(file_path)

# 展示前几行数据
print("Initial DataFrame:")
print(df.head())

# 检查数据类型
print("\nData types before conversion:")
print(df.dtypes)

# 确保所有数值列的类型为浮点数或整数
cols_to_convert = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
for col in cols_to_convert:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 将year, month, day, hour列组合成datetime
df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
df.set_index('datetime', inplace=True)

# 删除原始时间相关列
df.drop(columns=['No', 'year', 'month', 'day', 'hour'], inplace=True)

# 再次展示前几行数据
print("\nDataFrame after datetime processing and type conversion:")
print(df.head())

# 检查转换后的数据类型
print("\nData types after conversion:")
print(df.dtypes)

# In[3]

# 设置绘图风格
sns.set(style="whitegrid")

plt.figure(figsize=(10, 6))
sns.scatterplot(x='TEMP', y='PM2.5', data=df)
plt.title('Scatter plot of PM2.5 vs Temperature')
plt.xlabel('Temperature (°C)')
plt.ylabel('PM2.5 (µg/m³)')
plt.show()

plt.figure(figsize=(14, 7))
df['PM2.5'].plot()
plt.title('Time Series of PM2.5 Concentration')
plt.xlabel('Date')
plt.ylabel('PM2.5 (µg/m³)')
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(x=df['PM2.5'])
plt.title('Box plot of PM2.5')
plt.show()

mean_pm25 = df['PM2.5'].mean()
std_pm25 = df['PM2.5'].std()

# 3σ原则检测异常值
outliers = df[(df['PM2.5'] > mean_pm25 + 3 * std_pm25) | (df['PM2.5'] < mean_pm25 - 3 * std_pm25)]

# 删除异常值
df_cleaned = df.drop(outliers.index)

print(f"Number of outliers detected: {len(outliers)}")
print(f"Number of records after outlier removal: {len(df_cleaned)}")
