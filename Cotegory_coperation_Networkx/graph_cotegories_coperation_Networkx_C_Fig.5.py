from datetime import datetime
import itertools
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import random


import pyecharts.options as opts
from pyecharts.charts import Graph
from pyecharts.charts import Line
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts


# 导入输出图片工具
from pyecharts.render import make_snapshot
from snapshot_phantomjs import snapshot




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
                edgedata = G.get_edge_data(edge[0], edge[1])
                G.add_edge(edge[0], edge[1], weight = (edgedata["weight"]+1))
            #如果图中不存在该边,添加边然后设置权值为1
            else:
                G.add_edge(edge[0], edge[1], weight = 1)
    return G



def create_categories_network():
    '''
    创建一个关于目录的网络
    :return: 返回目录网络
    '''
    #获取协作网络图用于后面边的制作
    coperationGraph = create_coperation_networkx("../datasets/Mashups.csv")
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


def graphdata2csv(coperationNetwork):
    '''
    将目录协作网络图的节点和边的数据转换到csv中,用于后面利用gephi制作图
    :param coperation: 目录协作网络图
    :return: 返回生成的csv文件
    '''
    #拿到API协作网络中按度值排序的前五十个节点所形成的子网络
    #coperationNetwork.remove_nodes_from(list(nx.isolates(coperationNetwork)))
    nodes = dict(coperationNetwork.degree)
    nodes = sorted(nodes.items(), key=lambda e: e[1], reverse=True)
    nodes = dict(nodes)
    # 取度值从大到小排序的前50个
    top50 = list(nodes.keys())
    top50 = top50[0:50]
    #sub为所要取的的子网络
    sub = nx.subgraph(coperationNetwork, top50)
    #对sub子网络进行数据转换存储到csv中
    #遍历子图的边,将边的两端节点和权值存入edge_list中
    edg_list = []
    for (u, v) in sub.edges():
        edg_list.append([u, v, sub.get_edge_data(u, v)['weight']])
    cols = ['source', 'target', 'weight']
    file_data = pd.DataFrame(edg_list, index=range(len(edg_list)), columns=cols)
    file_data.to_csv("E:/categoriesGraphdata.csv")


if __name__ == "__main__":
    coperationNetwork = create_categories_network()
    graphdata2csv(coperationNetwork)

