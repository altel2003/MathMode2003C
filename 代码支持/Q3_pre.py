import pandas as pd

# 汇总单品
df = pd.read_excel("ForQ3.xlsx")
# 使用groupby对同一名称和分类的数据进行分组，然后对每组进行求和和平均操作
result_df = df.groupby(["名称", "分类"]).agg({
    "总销量(千克)": "sum",
    "单品售价": "mean",
    "批发价": "mean",
    "损耗率": "mean"
}).reset_index()

result_df.to_excel("ForQ3_1.xlsx")

# 综合排序
data = {
    'Vegetable': ['Carrot', 'Broccoli', 'Spinach', 'Tomato'],
    'Model1_Rank': [2, 1, 4, 3],
    'Model2_Rank': [3, 2, 1, 4],
    'Model3_Rank': [1, 4, 3, 2]
}

df1 = pd.read_excel("all_sorted.xlsx")

# 计算总分
num_vegetables = len(df1)
rank_list = df1.columns.values[1:]
for model in rank_list:
    df1[model + '_Score'] = num_vegetables - df1[model] + 1

# 计算平均排名
score_list = [model + '_Score' for model in rank_list]
df1['平均排名'] = df1[score_list].mean(axis=1)

# 生成最终排名
df1 = df1.sort_values(by='平均排名')
df1['最终排名'] = range(1, len(df1) + 1)

# 打印最终排名
print(df1[['索引项', '最终排名']])
df1.to_excel("Q3_final_rank.xlsx")

