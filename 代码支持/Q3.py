import re
import pandas as pd

# 读取文本文件
with open('result_q3.txt', 'r') as file:
    content = file.read()

# 使用正则表达式匹配文本中的蔬菜名称和预测售价
pattern = r'name:(.*?)-预测的销售量:\[(.*?)\]'
matches = re.findall(pattern, content)

# 创建一个包含蔬菜名称和预测售价的列表
vegetables = []
prices = []

for match in matches:
    vegetable_name = match[0].strip()  # 去除名称前后的空格
    predicted_price = float(match[1])  # 将预测售价转换为浮点数
    vegetables.append(vegetable_name)
    prices.append(predicted_price)

# 创建DataFrame
df = pd.DataFrame({'单品': vegetables, '预测销量': prices})
select_goods_needs_df =df[df["预测销量"]>2.5]
print(select_goods_needs_df)

# 导入排名数据
rank_df = pd.read_excel("Q3_final_rank.xlsx")
rank_dict = {}
for line in rank_df.values:
    rank_dict[line[1]] = line[-1]

# 导入数据构造单品与品类的简化字典
dict_df = pd.read_excel("ForQ3_1.xlsx")
all_goods_names = dict_df["名称"].unique()
dict = {}
for goods_name in all_goods_names:
    dict[goods_name] = dict_df[dict_df["名称"] == goods_name].values[0][2]

# 依照排名顺序选取排名在前 select_num 的品类
select_num = 27
sorted_products = sorted(select_goods_needs_df.items(), key=lambda item: rank_dict.get(item[0], float('inf')))
print("******")
print(sorted_products[0][1][:select_num].values)
top_products_dict ={}
other_products = {}
for i in range(select_goods_needs_df.shape[0]):
    if i < select_num:
        top_products_dict[sorted_products[0][1].values[i]] = sorted_products[1][1].values[i]
    else:
        other_products[sorted_products[0][1].values[i]] = sorted_products[1][1].values[i]

# 额外内容
list_good = []
for j in range(33):
    list_good.append(sorted_products[0][1].values[j])
from Q2_pre4 import ARIMA_forecast
# 用于第三问的预测
df = pd.read_excel("附件2_for_Q3.xlsx")
forecast_steps = 1

goods_names = list_good
for goods_name in goods_names:
    the_df = df[df["名称"] == goods_name]
    # 预测销售量
    data = the_df.loc[:, ["销售日期", "单品售价"]]
    data_copy = data.copy()
    data_copy.columns = ['date', 'all_sales']
    data_copy['date'] = pd.to_datetime(data_copy['date'])

    forecast_values, _ = ARIMA_forecast(data_copy, forecast_steps)
    print(f'name:{goods_name}-预测的单品售价:{forecast_values.values}')

    with open("result_q3_price.txt", "a") as f:
        f.write(f'name:{goods_name}-预测的单品售价:{forecast_values.values}\n')


#
# 观察品类分布
out_dict = {}
for good,weight in top_products_dict.items():
    if dict[good] not in out_dict:
        out_dict[dict[good]] = [1,weight]
    else:
        out_dict[dict[good]][0] += 1
        out_dict[dict[good]][1] += weight
print(out_dict)

# 品类需求，来自第二问的解
class_needs = {"花菜类": 22.394, "花叶类": 141.352, "辣椒类": 88.6289, "茄类": 23.701, "食用菌": 43.893, "水生根茎类": 13.668}


print("………………\n")
print(f'分类索引字典: {dict}')
print(f'现有品类下单品数目与重量: {out_dict}')
print(f'分数排名: {select_goods_needs_df}')
# 找到不足的品类并补充，因为情况较复杂且代码不会有通用性，代码只进行半加工，剩余工作人工完成
for the_class, need in class_needs.items():
    if the_class not in out_dict:
        print(f'待补充{need}, 在{the_class}品类')
        # 选择该品类下评分最高的单品进行补充
        # for data in rank_df.values:
        #     if dict[data[1]] == the_class:
        #         top_products_dict[data[1]] = need
        #         break
        continue
    if out_dict[the_class][1] < need:
        print(f'待补充{need - out_dict[the_class][1]}, 在{the_class}品类')
        # for data in rank_df.values:
        #     if dict[data[1]] == the_class:
        #         if data[1] not in top_products_dict:
        #             top_products_dict[data[1]] = need
        #         else:
        #             top_products_dict[data[1]] += need - out_dict[the_class][1]
        #         break
print(f'现有单品重量: {top_products_dict}')
print(f'剩余未选中单品需求: {other_products}，可从中选{33 - select_num}个')
