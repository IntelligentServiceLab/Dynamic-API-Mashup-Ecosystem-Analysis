import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame

from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts

APIs = pd.read_csv("../datasets/APIs.csv")
Mashups = pd.read_csv("../datasets/Mashups.csv")
sdk = pd.read_csv("../datasets/SDKs.csv")
copy = Mashups.copy()


NumofAPI = APIs['APIName'].nunique()
Numofmashups = Mashups['mashups_name'].nunique()

#对APIs目录进行切割
APIs['newcol'] = APIs['Categories'].str.split("###")
#对切割的函数进行爆炸处理
APIs = APIs.explode('newcol')

#对Mashup目录进行切割
Mashups['newcol'] = Mashups['categories'].str.split("###")

#对切割的函数进行爆炸处理
Mashups = Mashups.explode('newcol')

copy['newcol'] = copy['related_apis'].str.split("###")
copy = copy.explode('newcol')

TotalAPIbyMashup = copy['newcol'].nunique()
#TotalAPIproviders = sdk['SDK Provider'].nunique()

#计算每一个mashup所使用的平均api数量
AverageofApipermashup = '%.2f' % (len(copy['newcol'])/Numofmashups)


#统计APIs不同的category
NumofAPIcate = APIs['newcol'].nunique()

#统计Mashup不同的category
Numofmashupscate = Mashups['newcol'].nunique()




#绘制表格
label = ['Property', 'Value']

text = [['Number of mashups', Numofmashups], ['Number of web APIs', NumofAPI], ['Total number of web APIs used by mashups', TotalAPIbyMashup],
        ['Average number of Web APIs used per Mashup ', AverageofApipermashup], ['Number of web API categories', NumofAPIcate], ['Number of mashup categories', Numofmashupscate]]


table = Table()
table.add(label, text)
table.set_global_opts(
        title_opts=ComponentTitleOpts(title="STATISTICAL PROPERTIES OF THE DATASET")
)
table.render("baseStatics.html")