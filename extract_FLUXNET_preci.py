import pandas as pd
import matplotlib.pyplot as plt

def extract_preci(path):
    x = []
    y = []
    df = pd.read_csv(path, encoding='utf-8')
    #提取起始时间和降水数据
    for i in df.TIMESTAMP_START:
        x.append(i)
    for i in df.P_F:
        y.append(i)

    # 筛选雨量大于0的降水事件，并制作标签数组
    label = []
    value = []
    i = 50
    for x_, y_ in zip(x, y):
        if y_:
            if i % 50 == 0:
                label.append(x_)
            else:
                label.append('')
            value.append(y_)
            i += 1

    # 绘图
    plt.bar(range(len(value)), value, align='center', color='steelblue', alpha=0.8)
    # 添加轴标签
    plt.ylabel('precipitation')
    # 添加标题
    plt.title('Comparing about precipitation')
    # 添加X轴范围
    plt.xlim((-5, len(label) + 50))
    # 设置Y轴的刻度范围
    # plt.ylim()
    # 添加X轴刻度标签
    plt.xticks(range(len(label)), label, rotation=45)
    plt.savefig("precipitation.png")
    plt.show()

if __name__ == '__main__':

    filepath = r'AR_Slu_data.csv'
    extract_preci(filepath)

