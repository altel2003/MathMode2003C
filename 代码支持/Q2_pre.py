# 先建立分析表表终极版,但忽略打折，细分单品
# 可以稍作修改，不忽略，用于问题三
import pandas as pd

df = pd.read_excel("附件2_pre.xlsx")
class_df = pd.read_excel("附件1.xlsx")
new_def = []
date = ["start"]  # 简易处理
goods = []
# all_goods = []
sum_dict_df = {}

# select_df = df[df["是否打折销售"] == "否"]  # 对于问题1和2取舍


# # 下面段的代码用于问题三，不用时注释掉
# select_names = pd.read_excel("Q3_final_rank.xlsx").values[:, 1]
# select_df = df[df["单品名称"].isin(select_names)]


# 计算销量总和
for lines in df.values:
    number = str(lines[2])
    if lines[0] != date[-1]:
        # all_goods.append(goods)
        sum_dict_df[lines[0] + "&" + number] = [lines[3], lines[4], lines[7]]
        goods = []
        goods.append(number)
        date.append(lines[0])
        continue
    if number not in goods:
        sum_dict_df[lines[0] + "&" + number] = [lines[3], lines[4], lines[7]]
        goods.append(number)
    else:
        sum_dict_df[lines[0] + "&" + number][0] += lines[3]

df_out = [(key, value) for key, value in sum_dict_df.items()]

sum_dict_df = pd.DataFrame(df_out, columns=['销售日期 + 单品编号', '总销量(千克) + 单品售价 + 名称'], index=None)
print(sum_dict_df.head())

# 引入单品与分类对应字典
class_goods_dict = {}
for lines in class_df.values:
    class_goods_dict[lines[1]] = lines[3]

# 引入进货字典
purchase_price_df = pd.read_excel("附件3_pre.xlsx")
PP_dict = {}
for lines in purchase_price_df.values:
    PP_dict[lines[0] + "&" + str(lines[1])] = lines[2]
# print(PP_dict)
# 引入损耗率字典
loss_rate_df = pd.read_excel("附件4.xlsx", sheet_name="Sheet1")
loss_dict = {}
for lines in loss_rate_df.values:
    loss_dict[lines[1]] = lines[2]
# print(loss_dict)
# 建立新表
data_values = []
for line in sum_dict_df.values:
    data_values.append([line[0], line[1][0], line[1][1],line[1][2], PP_dict[line[0]], loss_dict[line[1][2]], class_goods_dict[line[1][2]]])

final_df_out = pd.DataFrame(data_values, columns=['销售日期 + 单品编码', '总销量(千克)',' 单品售价', '名称', '批发价','损耗率','分类'], index=None)


final_df_out.to_excel("附件2_for_Q1.xlsx")
# final_df_out.to_excel("附件2_for_Q2.xlsx")
# final_df_out.to_excel("附件2_for_Q3.xlsx")  # 用于问题三

# 方便起见，得到表后要人工处理分列后才能运行下面的分品类方法，注意修改文件名

# 对六个品类分别得到R与销量的关系
df_3 = pd.read_excel("附件2_for_Q1.xlsx", sheet_name="Sheet1")

class_this = df_3["分类"].unique()
result_df = pd.DataFrame()
for this_class in class_this:
    this_df = df_3[df_3["分类"] == this_class]
    groups = this_df.groupby("销售日期")

    for date, group in groups:
        # 计算销量和R的平均值
        sales_mean = group["总销量(千克)"].sum()
        r_mean = group["R"].mean()
        sell_in = group["批发价"].mean()
        sells_p = group["单品售价"].mean()

        # 将结果添加到result_df中
        result_df = result_df.append({"分类": this_class, "销售日期": date, "销量总和值": sales_mean, "R平均值": r_mean,
                                      "售价平均值": sells_p, "批发价平均值": sell_in},
                                     ignore_index=True)

# 打印结果
print(result_df)
result_df.to_excel("附件2_for_Q1_new.xlsx")

