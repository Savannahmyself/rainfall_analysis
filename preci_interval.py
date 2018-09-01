import pandas as pd
import matplotlib.pyplot as plt
from dateutil.parser import parse


def dict_sort(dic):
    dict = sorted(dic.items(), key=lambda d: d[0])
    return dict


x = []
y = []
df = pd.read_csv(r'AR_Slu_data.csv', encoding='utf-8')

for i in df.TIMESTAMP_START:
    x.append(i)

for i in df.P_F:
    y.append(i)

x = [x[i] for i in range(len(y)) if y[i] > 0]
x = [parse(str(i)) for i in x]
x_delta = [x[i] - x[i - 1] for i in range(1, len(x))]


dic = {}
for i in x_delta:
    span = i.days * 24 + i.seconds / 3600
    if dic.get(span):
        dic[span] += 1
    else:
        dic[span] = 1
dic = dict_sort(dic)

values = []
span = []
for x,y in dic:
    values.append(x)
    span.append(y)

# y = y[0:1000]
# 中文乱码的处理
# plt.rcParams['font.sans-serif'] =['Microsoft YaHei']
# plt.rcParams['axes.unicode_minus'] = False


# 绘图
plt.bar(range(len(span)), span, align='center', color='steelblue', alpha=0.8)
# 添加轴标签
plt.ylabel('frequency')
plt.xlabel('hour')
# 添加标题
# plt.title('Comparing about precipitation')
# # 添加刻度标签
plt.xticks(range(len(span)),values)
# # 设置Y轴的刻度范围
# plt.ylim([5000,15000])

# 为每个条形图添加数值标签
# for x, y in enumerate(y):
#     plt.text(x, y + 100, '%s' % round(y, 1), ha='center') # 显示图形plt.show()
plt.show()

print 'done!'
