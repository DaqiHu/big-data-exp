import pandas as pd
import plotly.graph_objects as go

# 读取CSV文件的路径
file_path = [
    r"data//PRSA_Data_Aotizhongxin_20130301-20170228.csv",
    r"data//PRSA_Data_Changping_20130301-20170228.csv",
    r"data//PRSA_Data_Dingling_20130301-20170228.csv",
    r"data//PRSA_Data_Dongsi_20130301-20170228.csv",
    r"data//PRSA_Data_Guanyuan_20130301-20170228.csv",
    r"data//PRSA_Data_Gucheng_20130301-20170228.csv",
    r"data//PRSA_Data_Huairou_20130301-20170228.csv",
    r"data//PRSA_Data_Nongzhanguan_20130301-20170228.csv",
    r"data//PRSA_Data_Shunyi_20130301-20170228.csv",
    r"data//PRSA_Data_Tiantan_20130301-20170228.csv",
    r"data//PRSA_Data_Wanliu_20130301-20170228.csv",
    r"data//PRSA_Data_Wanshouxigong_20130301-20170228.csv",
]

position = [
    "Aotizhongxin",
    "Changping",
    "Dingling",
    "Dongsi",
    "Guanyuan",
    "Gucheng",
    "Huairou",
    "Nongzhanguan",
    "Shunyi",
    "Tiantan",
    "Wanliu",
    "Wanshouxigong",
]

# 初始化一个空的DataFrame来存储所有监测站的数据
all_data = pd.DataFrame()

for i, e in enumerate(file_path):
    df = pd.read_csv(e)
    df.drop(columns=["wd"], inplace=True)  # 删除风向列
    df.drop(columns=["RAIN"], inplace=True)  # 删除降雨量列

    all_data = pd.concat([all_data, df])

# 确保所有数值列的类型为浮点数或整数
cols_to_convert = [
    "PM2.5",
    "PM10",
    "SO2",
    "NO2",
    "CO",
    "O3",
    "TEMP",
    "PRES",
    "DEWP",
    "WSPM",
]
for col in cols_to_convert:
    all_data[col] = pd.to_numeric(all_data[col], errors="coerce")

# 将year, month, day, hour列组合成datetime
all_data["datetime"] = pd.to_datetime(all_data[["year", "month", "day", "hour"]])
all_data.set_index("datetime", inplace=True)

# 删除原始时间相关列
all_data.drop(columns=["No", "year", "month", "day"], inplace=True)

# 按小时和监测站分组并计算平均值
grouped_data = all_data.groupby([all_data.index.hour, "station"]).mean()

# 为每个指标生成一张热图
for col in cols_to_convert:
    heatmap_data = grouped_data[col].unstack()
    fig = go.Figure(
        data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale="Viridis",
        )
    )

    fig.update_layout(
        title=f"{col} 平均值热图", xaxis_title="监测站", yaxis_title="小时"
    )

    fig.show()
