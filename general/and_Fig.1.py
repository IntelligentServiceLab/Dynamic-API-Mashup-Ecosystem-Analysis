from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


#第一个子图 API和Mashup的提交量
def get_sumbit01():
    '''
    API的提交量
    :return: API提交量的y值
    '''
    API = pd.read_csv("../datasets/APIs.csv")

    # 对sumbit_date行进行切割
    API['newdate'] = API['SubmittedDate'].str.split("###")
    # 对newdate进行爆炸处理
    API = API.explode('newdate')

    # 对数据进行清洗 除去newdate中为nan的行,只返回newdate那一列
    date = API['newdate'].dropna()
    # 将series转换为时间格式,其中的format一定得是和文本格式一样
    date = pd.to_datetime(date, format="%m.%d.%Y")

    # 设定y值y表示从2005到2021年API每年的提交量
    y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    x = ['2005', '2006', '2007', '20008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017',
         '2018', '2019', '2020', '2021']

    for item in date:
        if item.year == 2005:
            y[0] += 1
        elif item.year == 2006:
            y[1] += 1
        elif item.year == 2007:
            y[2] += 1
        elif item.year == 2008:
            y[3] += 1
        elif item.year == 2009:
            y[4] += 1
        elif item.year == 2010:
            y[5] += 1
        elif item.year == 2011:
            y[6] += 1
        elif item.year == 2012:
            y[7] += 1
        elif item.year == 2013:
            y[8] += 1
        elif item.year == 2014:
            y[9] += 1
        elif item.year == 2015:
            y[10] += 1
        elif item.year == 2016:
            y[11] += 1
        elif item.year == 2017:
            y[12] += 1
        elif item.year == 2018:
            y[13] += 1
        elif item.year == 2019:
            y[14] += 1
        elif item.year == 2020:
            y[15] += 1
        elif item.year == 2021:
            y[16] += 1
    return y


def get_sumbit02():
    '''
    Mashup的提交量
    :return: 提交量的一个y值
    '''
    API = pd.read_csv("../datasets/Mashups.csv")

    # 对sumbit_date行进行切割
    API['newdate'] = API['submitted_date'].str.split("###")
    # 对newdate进行爆炸处理
    API = API.explode('newdate')

    # 对数据进行清洗 除去newdate中为nan的行,只返回newdate那一列
    date = API['newdate'].dropna()
    # 将series转换为时间格式,其中的format一定得是和文本格式一样
    date = pd.to_datetime(date, format="%m.%d.%Y")

    # 设定y值y表示从2005到2021年API每年的提交量
    y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    x = ['2005', '2006', '2007', '20008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017',
         '2018', '2019', '2020', '2021']

    for item in date:
        if item.year == 2005:
            y[0] += 1
        elif item.year == 2006:
            y[1] += 1
        elif item.year == 2007:
            y[2] += 1
        elif item.year == 2008:
            y[3] += 1
        elif item.year == 2009:
            y[4] += 1
        elif item.year == 2010:
            y[5] += 1
        elif item.year == 2011:
            y[6] += 1
        elif item.year == 2012:
            y[7] += 1
        elif item.year == 2013:
            y[8] += 1
        elif item.year == 2014:
            y[9] += 1
        elif item.year == 2015:
            y[10] += 1
        elif item.year == 2016:
            y[11] += 1
        elif item.year == 2017:
            y[12] += 1
        elif item.year == 2018:
            y[13] += 1
        elif item.year == 2019:
            y[14] += 1
        elif item.year == 2020:
            y[15] += 1
        elif item.year == 2021:
            y[16] += 1
    return y


def first_subgraph():
    y1 = get_sumbit01()
    y2 = get_sumbit02()

    return y1, y2

#第二个子图 Total number of web APIs used by mashups
def numAPI_by_time(year):
    API = pd.read_csv("../datasets/Mashups.csv")

    # 对sumbit_date行进行切割
    API['newdate'] = API['submitted_date'].str.split("###")
    # 对newdate进行爆炸处理
    API = API.explode('newdate')

    # 对数据进行清洗 除去newdate中为nan的行,只返回newdate那一列
    date = API['newdate'].dropna()
    # # 将series转换为时间格式,其中的format一定得是和文本格式一样
    # date = pd.to_datetime(date, format="%m.%d.%Y")
    inx = API['newdate']
    inx = inx.tolist()

    inx_date = pd.to_datetime(inx, format="%m.%d.%Y")
    # 将dateframe的索引设置为时间
    API.index = inx_date

    #靠时间截取一部分
    dateBytime = API.loc[year]


    # 对related_apis行进行切割
    dateBytime['new_related_apis'] = dateBytime['related_apis'].str.split("###")
    # 对new_related_apis进行爆炸处理
    dateBytime = dateBytime.explode('new_related_apis')

    num = len(dateBytime['new_related_apis'].value_counts().index)

    return num

def second_subgraph():
    x = ['2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017',
         '2018', '2019', '2020', '2021']

    y = []

    for i in x:
        temp_num = numAPI_by_time(i)
        y.append(temp_num)
    return y



#第三个子图 API和Mashup的提交量
def numofAPI_category(year):
    '''
    返回该年year的API目录数量
    :param year: 年份
    :return: 该年的API目录数量
    '''
    API = pd.read_csv("../datasets/APIs.csv")
    # 对数据进行清洗 除去了在Categories中为nan值的一行
    API = API.dropna(subset=["Categories"])
    API = API.reset_index(drop=True)

    # 对数据进行清洗，除去了在SubmittedDate中为nan值的一行
    API = API.dropna(subset=["SubmittedDate"])
    API = API.reset_index(drop=True)

    # 对sumbit_date行进行切割
    API['newCategories'] = API['Categories'].str.split("###")
    newCategories = API['newCategories']
    # 将newCategories中全部缩减为只取一级标签
    for i in range(len(newCategories)):
        newCategories[i] = newCategories[i][0]
    # 将一级标签的series赋值于API数据中
    API['newCategories'] = newCategories

    # 对sumbit_date行进行切割
    API['newdate'] = API['SubmittedDate'].str.split("###")
    newdate = API['newdate']

    # 将newdate中全部缩减为只取一级标签
    for i in range(len(newdate)):
        newdate[i] = newdate[i][0]

    # 将一级标签的series赋值于API数据中
    API['newdate'] = newdate

    # 将时间做为索引
    inx = API['newdate']
    inx = inx.tolist()

    inx_date = pd.to_datetime(inx, format="%m.%d.%Y")
    # 将dateframe的索引设置为时间
    API.index = inx_date

    # 靠时间截取一部分
    dateBytime = API.loc[year]
    num = len(dateBytime['newCategories'].value_counts().index)

    return num

def numofMashup_category(year):
    '''
    返回该年year的Mashup目录数量
    :param year: 年份
    :return: 该年的Mashup目录数量
    '''
    API = pd.read_csv("../datasets/Mashups.csv")
    # 对数据进行清洗 除去了在Categories中为nan值的一行
    API = API.dropna(subset=["categories"])
    API = API.reset_index(drop=True)

    # 对数据进行清洗，除去了在SubmittedDate中为nan值的一行
    API = API.dropna(subset=["submitted_date"])
    API = API.reset_index(drop=True)

    # 对sumbit_date行进行切割
    API['newCategories'] = API['categories'].str.split("###")
    newCategories = API['newCategories']
    # 将newCategories中全部缩减为只取一级标签
    for i in range(len(newCategories)):
        newCategories[i] = newCategories[i][0]
    # 将一级标签的series赋值于API数据中
    API['newCategories'] = newCategories

    # 对sumbit_date行进行切割
    API['newdate'] = API['submitted_date'].str.split("###")
    newdate = API['newdate']

    # 将newdate中全部缩减为只取一级标签
    for i in range(len(newdate)):
        newdate[i] = newdate[i][0]

    # 将一级标签的series赋值于API数据中
    API['newdate'] = newdate

    # 将时间做为索引
    inx = API['newdate']
    inx = inx.tolist()

    inx_date = pd.to_datetime(inx, format="%m.%d.%Y")
    # 将dateframe的索引设置为时间
    API.index = inx_date

    # 靠时间截取一部分
    dateBytime = API.loc[year]
    num = len(dateBytime['newCategories'].value_counts().index)

    return num


def third_subgraph():
    x = ['2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017',
         '2018', '2019', '2020', '2021']

    y1 = []
    y2 = []

    for i in x:
        temp_num_API = numofAPI_category(i)
        temp_num_Mashup = numofMashup_category(i)
        y1.append(temp_num_API)
        y2.append(temp_num_Mashup)
    return y1, y2


#第四个子图
def get_avg(Mashups):
    '''
    计算每一个mashup所使用的平均api数量
    :param Mashup: 传递某个时间段的mashup
    :return: 所计算的值
    '''
    copy = Mashups.copy()

    Numofmashups = Mashups['mashups_name'].nunique()

    # 对Mashup目录进行切割
    Mashups['newcol'] = Mashups['categories'].str.split("###")
    # 对切割的函数进行爆炸处理
    Mashups = Mashups.explode('newcol')

    copy['newcol'] = copy['related_apis'].str.split("###")
    copy = copy.explode('newcol')

    # 计算每一个mashup所使用的平均api数量
    AverageofApipermashup = "%.2f" % (len(copy['newcol']) / Numofmashups)
    return float(AverageofApipermashup)

def get_Mashup_by_time(year):
    API = pd.read_csv("../datasets/Mashups.csv")

    # 对sumbit_date行进行切割
    API['newdate'] = API['submitted_date'].str.split("###")
    # 对newdate进行爆炸处理
    API = API.explode('newdate')

    # 对数据进行清洗 除去newdate中为nan的行,只返回newdate那一列
    date = API['newdate'].dropna()
    # # 将series转换为时间格式,其中的format一定得是和文本格式一样
    # date = pd.to_datetime(date, format="%m.%d.%Y")
    inx = API['newdate']
    inx = inx.tolist()

    inx_date = pd.to_datetime(inx, format="%m.%d.%Y")
    # 将dateframe的索引设置为时间
    API.index = inx_date

    # 靠时间截取一部分
    dateBytime = API.loc[year]
    return dateBytime


def forth_subgraph():
    x = ['2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017',
         '2018', '2019', '2020', '2021']

    y = []

    for i in x:
        y.append(get_avg(get_Mashup_by_time(i)))
    return y


if __name__ == "__main__":
    x = ['2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017',
         '2018', '2019', '2020', '2021']
    first_y1, first_y2 =first_subgraph()

    second_y = second_subgraph()

    third_y1, third_y2 = third_subgraph()

    forth_y = forth_subgraph()

    # 设置图例并且设置图例的字体及大小
    font1 = {'family': 'Times New Roman',
             'weight': 'bold',
             'size': 8,
             }

    # 设置横纵坐标的名称以及对应字体格式
    font2 = {'family': 'Times New Roman',
             'weight': 'bold',
             'size': 15,
             }


    # 设置图片大小
    fig = plt.figure(figsize=(20, 9))

    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.35)

    for i in range(1, 5):
        #子图
        ax = plt.subplot(2, 2, i)
        ax.tick_params(which='both', direction='in', width=3, colors='black', labelsize=8)

        if i==1:
            A, = ax.plot(x, first_y1, label='API Submit', linewidth=3, color='red', marker='o', markerfacecolor='blue',
                          markersize=10)
            B, = ax.plot(x, first_y2, label='Mashup Submit', linewidth=3, color='black', marker='*', markerfacecolor='blue',
                          markersize=15)


            # 修改坐标轴字体及大小
            for temp in ax.get_xticklabels():
                temp.set_fontweight("bold")
            for temp in ax.get_yticklabels():
                temp.set_fontweight("bold")

            legend = ax.legend(handles=[A, B], prop=font1)

            ax.set_xlabel('Time (year)', font2, labelpad=0)
            ax.set_ylabel('Number of Web APIs/Mashups', font2)
            ax.set_title('(a) Number of Web APIs/Mashups from 2005 to 2021', font2, y=-0.21)

            # 设置坐标轴轴线的颜色
            ax.spines['top'].set_color('black')
            ax.spines['top'].set_linewidth(2)
            ax.spines['right'].set_color('black')
            ax.spines['right'].set_linewidth(2)
            ax.spines['left'].set_color('black')
            ax.spines['left'].set_linewidth(2)
            ax.spines['bottom'].set_color('black')
            ax.spines['bottom'].set_linewidth(2)
        if i==2:
            A, = ax.plot(x, second_y, label='API', linewidth=4, color='red', marker='o', markerfacecolor='blue',
                          markersize=10)
            # 修改坐标轴字体及大小
            for temp in ax.get_xticklabels():
                temp.set_fontweight("bold")
            for temp in ax.get_yticklabels():
                temp.set_fontweight("bold")

            ax.set_xlabel('Time (year)', font2, labelpad=0)
            ax.set_ylabel('Number of Web APIs', font2)
            ax.set_title('(b) Number of Web APIs used by Mashups from 2005 to 2021', font2, y=-0.21)

            # 设置坐标轴轴线的颜色
            ax.spines['top'].set_color('black')
            ax.spines['top'].set_linewidth(2)
            ax.spines['right'].set_color('black')
            ax.spines['right'].set_linewidth(2)
            ax.spines['left'].set_color('black')
            ax.spines['left'].set_linewidth(2)
            ax.spines['bottom'].set_color('black')
            ax.spines['bottom'].set_linewidth(2)
        if i==3:
            A, = plt.plot(x, third_y1, label='API category Submit', linewidth=4, color='red', marker='o',
                          markerfacecolor='blue', markersize=10)
            B, = plt.plot(x, third_y2, label='Mashup category Submit', linewidth=4, color='black', marker='*',
                          markerfacecolor='blue', markersize=15)
            # 修改坐标轴字体及大小
            for temp in ax.get_xticklabels():
                temp.set_fontweight("bold")
            for temp in ax.get_yticklabels():
                temp.set_fontweight("bold")

            legend = plt.legend(handles=[A, B], prop=font1)

            ax.set_xlabel('Time (year)', font2, labelpad=0)
            ax.set_ylabel('Number of Web API/Mashup categories', font2)
            ax.set_title('(c) Number of Web API/Mashup categories from 2005 to 2021', font2, y=-0.21)

            # 设置坐标轴轴线的颜色
            ax.spines['top'].set_color('black')
            ax.spines['top'].set_linewidth(2)
            ax.spines['right'].set_color('black')
            ax.spines['right'].set_linewidth(2)
            ax.spines['left'].set_color('black')
            ax.spines['left'].set_linewidth(2)
            ax.spines['bottom'].set_color('black')
            ax.spines['bottom'].set_linewidth(2)
        if i==4:
            A, = ax.plot(x, forth_y, label='API', linewidth=4, color='red', marker='o', markerfacecolor='blue',
                          markersize=10)
            # 修改坐标轴字体及大小
            for temp in ax.get_xticklabels():
                temp.set_fontweight("bold")
            for temp in ax.get_yticklabels():
                temp.set_fontweight("bold")


            ax.set_xlabel('Time (year)', font2, labelpad=0)
            ax.set_ylabel('Average number of Web APIs', font2)
            ax.set_title('(d) Average number of Web APIs used by Mashups from 2005 to 2021', font2, y=-0.21)

            # 设置坐标轴轴线的颜色
            ax.spines['top'].set_color('black')
            ax.spines['top'].set_linewidth(2)
            ax.spines['right'].set_color('black')
            ax.spines['right'].set_linewidth(2)
            ax.spines['left'].set_color('black')
            ax.spines['left'].set_linewidth(2)
            ax.spines['bottom'].set_color('black')
            ax.spines['bottom'].set_linewidth(2)
    plt.savefig('E:/IntelligentServiceLab/动态分析论文/picture/3.1dynamic analysis/and.svg', format='svg', bbox_inches='tight', dpi=600)
    #plt.savefig('E:/IntelligentServiceLab/动态分析论文/picture/3.1dynamic analysis/and.png', format='png', dpi=600)
    #plt.savefig('E:/IntelligentServiceLab/动态分析论文/picture/3.1dynamic analysis/and.tif', format='tif', dpi=600)
    plt.show()