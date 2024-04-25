import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import re


def month_get(date_str):
    # 使用正则表达式匹配日期中的月份
    pattern = r'(\d+)/(\d+)/(\d+)'
    match = re.search(pattern, date_str)
    year = int(match.group(1))
    month = int(match.group(2))
    return year, month


df1 = pd.read_excel("附件2_for_Q2_1.xlsx", sheet_name="year1", index_col=2)
df2 = pd.read_excel("附件2_for_Q2_1.xlsx", sheet_name="year2", index_col=2)
df3 = pd.read_excel("附件2_for_Q2_1.xlsx", sheet_name="year3", index_col=2)
print(df1)

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

sell_out = [[], [], []]
R_out = [[], [], []]
class_names = df1["分类"].unique()
for class_name in class_names:
    df_data = [df1[df1["分类"] == class_name].values, df2[df2["分类"] == class_name].values, df3[df3["分类"] == class_name].values]
    plt.figure(figsize=(20,20))
    plt.subplot(221)
    plt.plot(df_data[0][:, 2],color='red', label="year1")
    plt.plot(df_data[1][:, 2],color='blue', label="year2")
    plt.plot(df_data[2][:, 2],color='green', label="year3")
    plt.legend()
    plt.title(class_name)

    plt.subplot(222)
    plt.plot(df_data[0][:, 3],color='brown', label="R")
    plt.plot(df_data[0][:, 2],color='yellow', label="sell")
    plt.title("year1")


    plt.subplot(223)
    plt.plot(df_data[1][:, 3],color='brown', label="R")
    plt.plot(df_data[1][:, 2],color='yellow', label="sell")
    plt.title("year2")

    plt.subplot(224)
    plt.plot(df_data[2][:, 3],color='brown', label="R")
    plt.plot(df_data[2][:, 2],color='yellow', label="sell")
    plt.title("year3")

    plt.savefig(f"imgs/Q2_1/{class_name}.png")
    plt.show()




