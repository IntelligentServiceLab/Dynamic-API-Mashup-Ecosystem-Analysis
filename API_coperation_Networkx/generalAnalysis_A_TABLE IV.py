###制作API Coperation Network 然后对其网络进行动态的度中心性分析
###对协作网络2005-2009、2005-2015、2005-2021网络做度中心分析,分析出每个网络的度中心性前五的API
import itertools

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import scipy
from pyecharts import options as opts
from pyecharts.charts import Graph
import random


def create_coperation_networkx(filepath):
    '''
    从csv文件中将数据装换为协作网络图
    :param filepath:文件路径
    :return: 所得的图
    '''
    #读取mashup文件
    data = pd.read_csv(filepath)
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
    #建立没有边的图
    G = nx.Graph()
    G.add_nodes_from(nodes)
    #对于还没有爆炸处理的newcol,那么比如['A','B','C']就称他们之间有连接的边,对图添加边，其中判断如果有边则权值加1，无边就之间加
    #其中难点就是对于['A','B','C']中要判断三组边 该如何去表示
    for i in range(coperation.size):
        #对coperation每个元素制作边,其中这里面coperation数据存在NAN，此时要进行处理
        Totaledge = itertools.combinations(coperation[i], r=2)          #这里用组合函数
        Totaledge = list(Totaledge)
        for j in range(len(Totaledge)):
            #如果图中存在该边,该边其权值
            edge = Totaledge[j]
            if G.has_edge(edge[0], edge[1]):
                edgedata = G.get_edge_data(edge[0],edge[1])
                G.add_edge(edge[0], edge[1], weight = (edgedata["weight"]+1))
            #如果图中不存在该边,添加边然后设置权值为1
            else:
                G.add_edge(edge[0], edge[1], weight = 1)
    return G




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


def degreeCentrality(coperation):
    degree_centrality = nx.degree_centrality(coperation)
    #对度中心性的字典按值排序
    degree_centrality_sorted = sorted(degree_centrality.items(), key=lambda x:x[1], reverse=True)
    top5 = []
    for i in range(5):
        top5.append(degree_centrality_sorted[i][0])
    return top5



def avgdegreeofnetwork(coperationGraph):
    '''
    计算平均度,返回平均度。
    :param coperationGraph:协作网络
    :return: 平均度
    '''
    NumofNodes = len(coperationGraph.nodes)
    NumofEdges = len(coperationGraph.edges)
    d = dict(nx.degree(coperationGraph))
    AverageofDegree = sum(d.values()) / len(coperationGraph.nodes)
    return AverageofDegree


def diameterofnetwork(coperationGraph):
    '''
    计算协作网络的直径,返回直径
    :param coperationGraph:协作网络
    :return: 直径
    '''
    # 此处存在孤立的节点 先去除孤立节点 然后再算直径
    coperationGraph.remove_nodes_from(list(nx.isolates(coperationGraph)))
    # 算出最大连接子图，然后对其计算直径
    largest = max(nx.connected_components(coperationGraph), key=len)
    largest_connected_subgraph = coperationGraph.subgraph(largest)
    # 其中nx.dimeter是处理连接图，而这里所得的图为非连接图，需要获取最大的连接子图
    diameter = nx.diameter(largest_connected_subgraph)
    return diameter



def avgshortestpathlen(coperationGraph):
    # 此处存在孤立的节点 先去除孤立节点 然后再算直径
    coperationGraph.remove_nodes_from(list(nx.isolates(coperationGraph)))
    # 算出最大连接子图，然后对其计算直径
    largest = max(nx.connected_components(coperationGraph), key=len)
    largest_connected_subgraph = coperationGraph.subgraph(largest)
    # 其中nx.dimeter是处理连接图，而这里所得的图为非连接图，需要获取最大的连接子图
    avgshortestpathlen = nx.average_shortest_path_length(largest_connected_subgraph)
    return avgshortestpathlen




if __name__ == "__main__":
    #coperation = create_coperation_networkx("../datasets/Mashups.csv")
    network_05_to_09 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2009)
    # network_05_to_10 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2010)
    # network_05_to_11 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2011)
    # network_05_to_12 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2012)
    network_05_to_13 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2013)
    # network_05_to_14 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2014)
    #network_05_to_15 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2015)
    # network_05_to_16 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2016)
    network_05_to_17 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2017)
    # network_05_to_18 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2018)
    # network_05_to_19 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2019)
    # network_05_to_20 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2020)
    network_05_to_21 = create_coperation_networkx_by_time("datasets/Mashups.csv", 2005, 2021)


    list_network = [network_05_to_09, network_05_to_13, network_05_to_17, network_05_to_21]

    str_list_network = ['network_05_to_09', 'network_05_to_13', 'network_05_to_17', 'network_05_to_21']

    #平均最短路径距离
    avg_shortest_distance = []
    #网络直径
    diamiter = []
    #平均度
    avg_degree = []
    #平均聚集系数
    avg_cluster = []

    #中心性最大的节点
    list_center_network = []

    for i in range(len(list_network)):
        avg_shortest_distance.append(avgshortestpathlen(list_network[i]))
        diamiter.append(diameterofnetwork(list_network[i]))
        avg_degree.append(avgdegreeofnetwork(list_network[i]))
        avg_cluster.append(nx.average_clustering(list_network[i]))
    dict_degreecenter_networkx = dict(zip(str_list_network, list_center_network))
    print(dict_degreecenter_networkx)

