import pandas as pd
import matplotlib.pyplot as plt
from dateutil.parser import parse

#  字典排序
def dict_sort(dic):
    dict = sorted(dic.items(), key=lambda d: d[0])
    return dict

def preci_interval(path):
    df = pd.read_csv(path, encoding='utf-8')
    x = []
    y = []

    for i in df.TIMESTAMP_START:
        x.append(i)
    for i in df.P_F:
        y.append(i)

    # 筛选雨量大于0的降水事件,求一个降水事件到上一个降水事件的时间间隔，单位转化成小时
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

    count = []
    span = []
    i = 5
    for x, y in dic:
        if i % 5 == 0:
            span.append(str(x) + 'h')
            i = 0
        else:
            span.append('')
        count.append(y)
        i += 1

    # 绘图
    plt.bar(range(len(count)), count, align='center', color='steelblue', alpha=0.8)
    # 添加轴标签
    plt.ylabel('count')
    # 添加标题
    plt.title('Precipitation interval statistics')
    # 添加X轴范围
    plt.xlim((-1, len(span)))
    # 设置Y轴的刻度范围
    # plt.ylim()
    # 添加X轴刻度标签
    plt.xticks(range(len(span)), span, rotation=0)

    # 为每个条形图添加数值标签
    for x, y in enumerate(count):
        if y > 1:
            plt.text(x, y + 3, '%s' % round(y, 1), ha='center')

    plt.savefig("preci_interval.png")
    plt.show()

if __name__ == '__main__':

    filepath = r'AR_Slu_data.csv'
    preci_interval(filepath)
