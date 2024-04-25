import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import re
import plotly.express as px


def year_month_get(date_str):
    # 使用正则表达式匹配日期中的年份和月份
    pattern = r'(\d+)/(\d+)/(\d+)'
    match = re.search(pattern, date_str)
    year = int(match.group(1))  # 获取年份部分并转换为整数
    month = int(match.group(2))  # 获取月份部分并转换为整数
    return f"{year}/{month:02d}"  # 返回形如"2020/07"的日期格式


def gray_relation_degree(list1, list2):  # 计算灰度关系
    # 标准化
    reference_mean = np.mean(list1)
    reference_std = np.std(list1)
    compared_mean = np.mean(list2)
    compared_std = np.std(list2)

    list1 = (list1 - reference_mean) / reference_std
    list2 = (list2 - compared_mean) / compared_std

    # 计算关联系数
    c = 0.5  # 控制因子，可以根据需要进行调整
    gray_relation_coefficient = np.exp(-c * np.abs(list1 - list2))

    # 计算关联度
    gray_relation_degree = np.mean(gray_relation_coefficient)

    return gray_relation_degree


def z_score_nor(matrix):
    mean = np.mean(matrix)
    std_dev = np.std(matrix)
    normalized_matrix = (matrix - mean) / std_dev
    return normalized_matrix


def cv_cal(data):  # 计算变异系数
    mean = np.mean(np.array(data))  # 计算平均值
    std = np.std(data, ddof=0)  # 计算标准差
    cv = std / mean
    return cv


def stl_cal(df, title):
    try:
        stl = sm.tsa.seasonal_decompose(df, model='additive', period=7)
        # 绘制分解结果
        plt.figure(figsize=(12, 8))
        plt.subplot(411)
        plt.plot(df, label='原始数据')
        plt.legend(loc='upper left')
        plt.subplot(412)
        plt.plot(stl.trend, label='趋势')
        plt.legend(loc='upper left')
        plt.subplot(413)
        plt.plot(stl.seasonal, label='季节性')
        plt.legend(loc='upper left')
        plt.subplot(414)
        plt.plot(stl.resid, label='残差')
        plt.legend(loc='upper left')
        plt.tight_layout()

        plt.savefig(f"imgs/Q1_4/stl-{title}.png")
        plt.show()
    except:
        print(f'{title}异常')
        if len(df) > 0:
            plt.plot(df)
            plt.savefig(f"imgs/Q1_4/{title}.png")
            plt.show()


plt.rcParams['font.sans-serif'] = ['SimHei']  # 支持中文
plt.rcParams['axes.unicode_minus'] = False
df1 = pd.read_excel("附件2_for_Q1.xlsx")  # 各个单品的


goods_names = df1["名称"].unique().tolist()
data_dict = {}  # 字典存储数据
for good in goods_names:
    data_dict[good] = pd.concat([df1[df1["名称"] == good].iloc[:, 1], df1[df1["名称"] == good].iloc[:, 3]], axis=1)

# cv_list = []
# name_list = []
# for name, data_df in data_dict.items():
#     cv_list.append(cv_cal(data_df["总销量(千克)"].values))
#     name_list.append(name)
# cv_df = pd.DataFrame({"名称": name_list, "cv": cv_list})
#
# # 自定义分类类数量
# class_num = 16
# length = len(name_list)
# for cv in range(class_num):
#     size = (4, 4)
#     fig, axs = plt.subplots(size[0], size[1], figsize=(20, 20))
#     axs = axs.flatten()
#
#     if ((cv + 1) * 16) <= length:
#         div = [cv * 16, (cv + 1) * 16]
#     else:
#         div = [cv * 16, length]
#     for idx, good in enumerate(name_list[div[0]:div[1]]):
#         # # 绘出STL图,使用请注释掉其它绘图部分
#         # the_df2 = data_dict[good]["总销量(千克)"].copy()
#         # stl_cal(the_df2, good)
#
#         # 解析日期并添加年份和月份列
#         the_df1 = data_dict[good].copy()
#         the_df1['年份月份'] = the_df1['销售日期'].map(year_month_get)
#
#         # 按月份分组并绘制箱型图
#         the_df1.boxplot(column='总销量(千克)', by='年份月份', showfliers=False, ax=axs[idx], rot=45)
#         axs[idx].set_title(f'商品: {good} 每月销量箱型图')
#         axs[idx].set_xlabel('月份')
#         axs[idx].set_ylabel('销量')
#     # axs[idx].set_xticklabels(the_df1['年份月份'].unique(), rotation=45)
#
# plt.tight_layout()
# plt.subplots_adjust(top=0.8, bottom=0.1, wspace=0.4, hspace=0.2)
#
# # 添加一个位于所有子图上方的标题
# plt.suptitle(f'class: {cv + 1}', fontsize=40, y=0.95)
#
# # 保存图像
# plt.savefig(f"imgs/Q1_1/{cv}.png")
# plt.show()


df2 = pd.read_excel("附件2_for_Q1_new.xlsx")  # 各个品类的
# class_names = df2["分类"].unique().tolist()
# data2_dict = {}
# for the_class in class_names:
#     data2_dict[the_class] = pd.concat(
#         [df2[df2["分类"] == the_class].iloc[:, 2], df2[df2["分类"] == the_class].iloc[:, 3]], axis=1)
#
# for idx, the_class_name in enumerate(class_names):
#     # 解析日期并添加年份和月份列
#     the_df1 = data2_dict[the_class_name].copy()
#     the_df1['年份月份'] = the_df1['销售日期'].map(year_month_get)
#
#     # 按月份分组并绘制箱型图
#     plt.figure(figsize=(12, 8))
#     the_df1.boxplot(column='销量总和值', by='年份月份', showfliers=False, rot=45)
#     plt.xlabel('月份')
#     plt.ylabel('销量')
#     plt.title(f'商品: {the_class_name} 每月销量箱型图')
#
#     plt.savefig(f"imgs/Q1_3/{the_class_name}.png")
#     plt.show()
#
#     # 绘出STL图
#     the_df2 = data2_dict[the_class_name]["销量总和值"].copy()
#     stl_cal(the_df2, the_class_name)


# 得到灰度关联矩阵
# 对各个单品

# 使用 pivot 函数将长格式转换为宽格式
pivot_df = df1.pivot(index='销售日期', columns='名称', values='总销量(千克)')
# 如果需要将 NaN 值替换为 0，可以使用 fillna 函数
pivot_df.fillna(0, inplace=True)
good_list = pivot_df.columns.tolist()
values = pivot_df.values
corr_values = z_score_nor(values)

mic_result = np.zeros((len(good_list), len(good_list)))
for i in range(len(good_list)):
    for j in range(len(good_list)):
        mic_result[i][j] = gray_relation_degree(corr_values[:,i], corr_values[:,j])
df3_out = pd.DataFrame(mic_result, index=good_list, columns=good_list)
# df3_out.to_excel("gray_corr_Q1.xlsx")
fig = px.imshow(df3_out, x=good_list, y=good_list)
fig.show()

# 对每个品类
pivot_df2 = df2.pivot(index='销售日期', columns='分类', values='销量总和值')
pivot_df2.fillna(0, inplace=True)
class_list = pivot_df2.columns.tolist()
values = pivot_df2.values
corr2_values = z_score_nor(values)

mic_result2 = np.zeros((len(class_list), len(class_list)))
for i in range(len(class_list)):
    for j in range(len(class_list)):
        mic_result2[i][j] = gray_relation_degree(corr2_values[:,i], corr2_values[:,j])
df3_out2 = pd.DataFrame(mic_result2, index=class_list, columns=class_list)
# df3_out2.to_excel("gray_corr_Q1_new.xlsx")

fig = px.imshow(df3_out2, x=class_list, y=class_list)
fig.show()


