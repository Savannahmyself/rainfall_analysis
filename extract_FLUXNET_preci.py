import pandas as pd
import matplotlib.pyplot as plt
from dateutil.parser import parse

x = []
y = []
df = pd.read_csv(r'AR_Slu_data.csv', encoding='utf-8')

#提取起始时间数据
for i in df.TIMESTAMP_START:
    x.append(i)
#提取降水数据
for i in df.P_F:
    y.append(i)

y = [x for x in y if x>0]

# 绘图
plt.bar(range(len(y)), y, align='center', color='steelblue', alpha=0.8)
# 添加轴标签
plt.ylabel('precipitation(mm)')
# 添加标题
plt.title('Comparing about precipitation')
plt.savefig("precipitation.png")
plt.show()

