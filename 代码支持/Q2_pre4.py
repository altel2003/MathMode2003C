import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from pmdarima import auto_arima  # 参数自动选择
from docx import Document
from docx.shared import Inches

import io
from scipy.optimize import minimize

# 本代码同样被使用于第三问，详见注释

def ARIMA_forecast(data, forecast_steps):
    # 将日期列设置为索引
    data.set_index('date', inplace=True)

    # 生成多个可能的ARIMA模型并选择最佳模型
    stepwise_fit = auto_arima(data, seasonal=True, m=7, stepwise=True, trace=True)

    # 获取最佳模型的参数
    best_order = stepwise_fit.get_params()['order']

    # 拟合ARIMA模型
    model = sm.tsa.ARIMA(data, order=best_order)  # 使用最佳参数
    results = model.fit()

    # 生成未来一周的每天销售量预测
    forecast = results.get_forecast(steps=forecast_steps)
    sample_forecast = forecast.predicted_mean.values  # 预测值

    # 提取预测值和置信区间
    forecast_values = forecast.predicted_mean
    forecast_ci = forecast.conf_int()

    return forecast_values, forecast_ci


def func(x, r, r_s, h, k):  # r, rs 是np数组
    return h * np.sum((x - r) * r_s) + k * np.sum((r - x) * r_s)


# 准备销售数据
df = pd.read_excel("附件2_for_Q2_new.xlsx", sheet_name="Sheet1")

class_name = df["分类"].unique()
print(class_name)
for c in class_name:
    the_df = df[df["分类"] == c]
    print(the_df.head())
    forecast_steps = 7  # 预测7天

    data = the_df.loc[:, ["销售日期", "销量总和值"]]

    rounded_alpha_values = np.arange(0.1, 0.55, 0.05)
    alpha_values = np.round(rounded_alpha_values, 2)

    # 存储每个系数对应的样本
    samples_by_alpha = {}

    predictions_sell_out = []  # 预期销量(r)
    p_rs = []  # p(r)
    # predictions_sell_P 预期批发价
    # predictions_sell 预期售价

    # 对于预期销量
    for alpha in alpha_values:
        # 创建数据副本以确保每次都使用原始数据
        data_copy = data.copy()

        data_copy['smoothed'] = data_copy['销量总和值'].ewm(alpha=alpha).mean()
        data_copy.drop(columns=['销量总和值'], inplace=True)

        data_copy.columns = ['date', 'smoothed']
        data_copy['date'] = pd.to_datetime(data_copy['date'])
        forecast_values, _ = ARIMA_forecast(data_copy, forecast_steps)

        # 输出未来一周的销售预测
        print("Sales Forecast for the Next Week:")
        print(forecast_values.values)

        predictions_sell_out.append(forecast_values.values)
        plt.plot(forecast_values, label=f'{alpha}')
        # plt.fill_between(forecast_index, forecast_ci.iloc[:, 0], forecast_ci.iloc[:, 1], color='gray', alpha=0.2)

    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.title('Sales Forecast for the Next Week')
    plt.show()

    predictions_sell_out = np.array(predictions_sell_out).T
    for i, day_data in enumerate(predictions_sell_out):
        p_r = np.array([1 / len(day_data) for _ in range(len(day_data))])
        p_rs.append(p_r)
        print(f'第{i + 1}天预测的r:{day_data},p(r):{p_r}')
    predictions_sell_out = np.array(predictions_sell_out)

    # 预测售价
    data = the_df.loc[:, ["销售日期", "售价平均值"]]
    data_copy = data.copy()
    data_copy.columns = ['date', 'avg_price_out']
    data_copy['date'] = pd.to_datetime(data_copy['date'])

    forecast_values, _= ARIMA_forecast(data_copy, forecast_steps)
    print(f'预测的售价:{forecast_values.values}')
    predictions_sell = forecast_values.values

    # 预测批发价
    data = the_df.loc[:, ["销售日期", "批发价平均值"]]
    data_copy = data.copy()
    data_copy.columns = ['date', 'avg_price']
    data_copy['date'] = pd.to_datetime(data_copy['date'])
    forecast_values, _= ARIMA_forecast(data_copy, forecast_steps)
    print(f'预测的批发价:{forecast_values.values}')
    predictions_sell_P = forecast_values.values


    # print(predictions_sell)
    # print(predictions_sell_P)
    # print(p_rs)
    # print(predictions_sell_out)

    print(f'class:{c}')
    print(f"预期销量r：{predictions_sell_out}")
    print(f"预期售价：{predictions_sell}")
    print(f"预期批发价h：{predictions_sell_P}")
    print(f"p(r):{p_rs}")

    with open("result_q2.txt", "a") as f:
        f.write(f'class:{c}\n')
        f.write(f"预期销量r：{predictions_sell_out}\n")
        f.write(f"预期售价：{predictions_sell}\n")
        f.write(f"预期批发价h：{predictions_sell_P}\n")
        f.write(f"p(r):{p_rs}\n")
        f.write("…….\n")


    for i in range(forecast_steps):
        x_gauss = predictions_sell_out[i]
        r = predictions_sell_out[i]
        rs = p_rs[i]
        h = predictions_sell_P[i]
        k = predictions_sell[i]- h
        try:
            result = minimize(func, x0=x_gauss, args=(r, rs, h, k))
            # 提取优化后的x值
            optimized_x = result.x

            # 打印优化后的x值和函数值
            print(f"第{i + 1}天优化后的x值:{optimized_x},函数值:{result.fun}")
        except:
            print("优化失败")


# # 用于第三问的预测
# df = pd.read_excel("附件2_for_Q3.xlsx")
# forecast_steps = 1
#
# goods_names = df["名称"].unique()
# for goods_name in goods_names:
#     the_df = df[df["名称"] == goods_name]
#     # 预测销售量
#     data = the_df.loc[:, ["销售日期", "总销量(千克)"]]
#     data_copy = data.copy()
#     data_copy.columns = ['date', 'all_sales']
#     data_copy['date'] = pd.to_datetime(data_copy['date'])
#
#     forecast_values,_= ARIMA_forecast(data_copy, forecast_steps)
#     print(f'name:{goods_name}-预测的销售量:{forecast_values.values}')
#
#     with open("result_q3.txt", "a") as f:
#         f.write(f'name:{goods_name}-预测的销售量:{forecast_values.values}\n')





