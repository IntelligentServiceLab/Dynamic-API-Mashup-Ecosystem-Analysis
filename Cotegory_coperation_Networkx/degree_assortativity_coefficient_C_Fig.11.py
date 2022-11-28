###对网络进行同配系数分析
import itertools

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from networkx import Graph
import networkx as nx
import scipy

from collections import Counter

def getdictoftime():
    '''
    得到API和对应提交时间的字典
    '''
    API = pd.read_csv("./datasets/APIs.csv")
    #对数据进行清洗 除去了在Categories中为nan值的一行
    API = API.dropna(subset=["SubmittedDate"])
    API = API.reset_index(drop=True)
    #对sumbit_date行进行切割
    API['newdate'] = API['SubmittedDate'].str.split("###")
    newdate = API['newdate']
    #将newCategories中全部缩减为只取一级标签
    for i in range(len(newdate)):
        newdate[i] = newdate[i][0]
    # 将series转换为时间格式,其中的format一定得是和文本格式一样
    newdate = pd.to_datetime(newdate, format="%m.%d.%Y")
    #将一级标签的series赋值于API数据中
    API['newdate'] = newdate
    keys = list(API['APIName'])
    values = list(API['newdate'])
    dictofAPIDate = dict(zip(keys, values))
    return dictofAPIDate


def getdictofcategory():
    '''
    得到API和目录一级类别的字典
    '''
    API = pd.read_csv("../datasets/APIs.csv")
    #对数据进行清洗 除去了在Categories中为nan值的一行
    API = API.dropna(subset=["Categories"])
    API = API.reset_index(drop=True)
    #对sumbit_date行进行切割
    API['newCategories'] = API['Categories'].str.split("###")
    newCategories = API['newCategories']
    #将newCategories中全部缩减为只取一级标签
    for i in range(len(newCategories)):
        newCategories[i] = newCategories[i][0]
    #将一级标签的series赋值于API数据中
    API['newCategories'] = newCategories
    keys = list(API['APIName'])
    values = list(API['newCategories'])
    dictofAPICategories = dict(zip(keys, values))
    return dictofAPICategories




def create_coperation_networkx_by_time(filepath,starttime,endtime):
    '''
    从csv文件中将数据按照时间转换为协作网络图
    :param filepath:文件路径
    :return: 所得的图
    '''
    #读取mashup文件
    data = pd.read_csv(filepath)
    #获取API对应的时间字典用于后面的查询
    menu = getdictoftime()
    keysofmenu = list(menu.keys())
    #将mashup中的相关API部分进行切割爆炸然后获取不相同的API列表，那么这个列表就是我们的节点
    # 对相关的api进行切割
    data['newcol'] = data['related_apis'].str.split("###")
    #newcol进行保存也就是节点之间存在的边
    coperation = data['newcol']
    #对coperation进行数据处理将空值删除掉
    coperation = coperation.fillna('None')
    # 对切割的newcol进行爆炸处理
    data = data.explode('newcol')
    #制作节点,将newcol单独提取出来进行数据清洗删去所有重复的行
    newcol = data['newcol']
    newcol.duplicated()
    nodes = newcol.drop_duplicates()
    #把nodes的空值去掉
    nodes = nodes.fillna('None')
    #转为list
    nodes = list(nodes)

    #将2005-2010的节点筛选出来
    for i in range(len(nodes)):
        if nodes[i] in keysofmenu:
            if menu[nodes[i]].year < starttime or menu[nodes[i]].year > endtime:
                nodes[i] = np.nan
        else:
            nodes[i] = np.nan
    newnodes = nodes.copy()
    while np.nan in newnodes:
        newnodes.remove(np.nan)

    #建立没有边的图
    G = nx.Graph()
    G.add_nodes_from(newnodes)
    #对于还没有爆炸处理的newcol,那么比如['A','B','C']就称他们之间有连接的边,对图添加边，其中判断如果有边则权值加1，无边就之间加
    #其中难点就是对于['A','B','C']中要判断三组边 该如何去表示
    for i in range(coperation.size):
        #对coperation每个元素制作边,其中这里面coperation数据存在NAN，此时要进行处理
        Totaledge = itertools.combinations(coperation[i], r=2)          #这里用组合函数
        Totaledge = list(Totaledge)
        for j in range(len(Totaledge)):
            #如果图中存在该边,该边其权值
            edge = Totaledge[j]
            if edge[0] in newnodes and edge[1] in newnodes:
            #如果边的两个节点都在newnodes中就进行下列的操作,建立新的边
                if G.has_edge(edge[0], edge[1]):
                    edgedata = G.get_edge_data(edge[0], edge[1])
                    G.add_edge(edge[0], edge[1], weight = (edgedata["weight"]+1))
                #如果图中不存在该边,添加边然后设置权值为1
                else:
                    G.add_edge(edge[0], edge[1], weight = 1)
    return G




def create_category_network_by_time(coperationbytime):
    '''
    创建一个按时间关于目录的网络
    :return: 返回某个时间段的目录网络
    '''
    #获取协作网络图用于后面边的制作
    coperationGraph = coperationbytime
    #获取API和Categories字典用于后面的查询
    menuofApiCate = getdictofcategory()
    listofAPI = list(menuofApiCate.keys())
    #把所有的一级目录当做为节点
    nodes = list(set(list(menuofApiCate.values())))
    #建立没有边的图
    G = nx.Graph()
    G.add_nodes_from(nodes)
    #建立有边的图,遍历我们之前就制作的协作网络图的边
    for edge in coperationGraph.edges():
        edgedata = coperationGraph.get_edge_data(edge[0], edge[1])     #得到协作网络边的信息, 用于后面的目录边的权值的构建
        if edge[0] in listofAPI and edge[1] in listofAPI:
            #如果边两边的API都在所爬取的api之中，就可以进行处理
            edgeofcategories = [menuofApiCate[edge[0]], menuofApiCate[edge[1]]]
            if G.has_edge(edgeofcategories[0], edgeofcategories[1]):
                #有边那么获取其权值进行加成就行
                tempdata = G.get_edge_data(edgeofcategories[0], edgeofcategories[1])
                G.add_edge(edgeofcategories[0],edgeofcategories[1], weight = (tempdata["weight"]+edgedata["weight"]))
            #如果图中不存在该边,添加边然后设置权值为1
            else:
                G.add_edge(edgeofcategories[0], edgeofcategories[1], weight = edgedata["weight"])
    return G



if __name__ == "__main__":

    network_05_to_06 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2006)
    network_05_to_07 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2007)
    network_05_to_08 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2008)
    network_05_to_09 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2009)
    network_05_to_10 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2010)
    network_05_to_11 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2011)
    network_05_to_12 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2012)
    network_05_to_13 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2013)
    network_05_to_14 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2014)
    network_05_to_15 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2015)
    network_05_to_16 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2016)
    network_05_to_17 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2017)
    network_05_to_18 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2018)
    network_05_to_19 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2019)
    network_05_to_20 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2020)
    network_05_to_21 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2021)

    category_05_to_06 = create_category_network_by_time(network_05_to_06)
    category_05_to_07 = create_category_network_by_time(network_05_to_07)
    category_05_to_08 = create_category_network_by_time(network_05_to_08)
    category_05_to_09 = create_category_network_by_time(network_05_to_09)
    category_05_to_10 = create_category_network_by_time(network_05_to_10)
    category_05_to_11 = create_category_network_by_time(network_05_to_11)
    category_05_to_12 = create_category_network_by_time(network_05_to_12)
    category_05_to_13 = create_category_network_by_time(network_05_to_13)
    category_05_to_14 = create_category_network_by_time(network_05_to_14)
    category_05_to_15 = create_category_network_by_time(network_05_to_15)
    category_05_to_16 = create_category_network_by_time(network_05_to_16)
    category_05_to_17 = create_category_network_by_time(network_05_to_17)
    category_05_to_18 = create_category_network_by_time(network_05_to_18)
    category_05_to_19 = create_category_network_by_time(network_05_to_19)
    category_05_to_20 = create_category_network_by_time(network_05_to_20)
    category_05_to_21 = create_category_network_by_time(network_05_to_21)

    x = ['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']
    y = []


    list_network = [category_05_to_06, category_05_to_07, category_05_to_08, category_05_to_09, category_05_to_10, category_05_to_11, category_05_to_12, category_05_to_13, category_05_to_14, category_05_to_15, category_05_to_16, category_05_to_17, category_05_to_18, category_05_to_19, category_05_to_20, category_05_to_21]

    for temp in list_network:
        y.append(nx.degree_assortativity_coefficient(temp))



    # 设置输出的图片大小
    figsize = 20, 9
    figure, ax = plt.subplots(figsize=figsize)

    A, = plt.plot(x, y, label='API Sumbit', linewidth=4, color='red', marker='o', markerfacecolor='blue',
                  markersize=15)

    # 修改坐标轴字体及大小
    plt.yticks(fontproperties='Times New Roman', size=18, weight='bold')  # 设置大小及加粗
    plt.xticks(fontproperties='Times New Roman', size=18, weight='bold')

    # 设置图例并且设置图例的字体及大小
    font1 = {'family': 'Times New Roman',
             'weight': 'bold',
             'size': 20,
             }
    #legend = plt.legend(handles=[A], prop=font1)



    # 设置横纵坐标的名称以及对应字体格式
    font2 = {'family': 'Times New Roman',
             'weight': 'bold',
             'size': 30,
             }



    plt.xlabel('Time in year', font2, labelpad=2, loc='center')
    plt.ylabel('Assortativity degree', font2)
    # plt.title('Dynamic of the mixing pattern indicator', font2)

    # 修改坐标轴字体及大小
    for temp in ax.get_xticklabels():
        temp.set_fontweight("bold")
    for temp in ax.get_yticklabels():
        temp.set_fontweight("bold")

    #设置坐标轴轴线的颜色
    ax.spines['top'].set_color('black')
    ax.spines['top'].set_linewidth(3)
    ax.spines['right'].set_color('black')
    ax.spines['right'].set_linewidth(3)
    ax.spines['left'].set_color('black')
    ax.spines['left'].set_linewidth(3)
    ax.spines['bottom'].set_color('black')
    ax.spines['bottom'].set_linewidth(3)


    plt.savefig("E:/IntelligentServiceLab/动态分析论文/picture/3.3 category_coperation/degree_assortativity_coefficient.svg", format='svg', bbox_inches='tight', dpi=600)
    #plt.savefig("E:/IntelligentServiceLab/动态分析论文/picture/3.3 category_coperation/degree_assortativity_coefficient.png", format='png', dpi=600)
    plt.show()










