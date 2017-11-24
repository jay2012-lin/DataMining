# -*- coding: utf-8 -*-
# @Time    : 2017/11/21 10:06
# @Author  : jaylin
# @Email   : jaylin008@qq.com
# @File    : GeneralView.py
# @Software: PyCharm Community Edition
import os
from collections import Counter
import datetime
import numpy as np
import json
import pandas as pd
import matplotlib.pyplot as plt

data2013_07 = '../data/201307-citibike-tripdata.csv'
data2013_08 = '../data/201308-citibike-tripdata.csv'
data2013_09 = '../data/201309-citibike-tripdata.csv'
data2013_10 = '../data/201310-citibike-tripdata.csv'
data2013_11 = '../data/201311-citibike-tripdata.csv'
data2013_12 = '../data/201312-citibike-tripdata.csv'
data2014_01 = '../data/201401-citibike-tripdata.csv'
data2014_02 = '../data/201402-citibike-tripdata.csv'
data2014_03 = '../data/201403-citibike-tripdata.csv'
data2014_04 = '../data/201404-citibike-tripdata.csv'
data2014_05 = '../data/201405-citibike-tripdata.csv'
data2014_06 = '../data/201406-citibike-tripdata.csv'
data2014_07 = '../data/201407-citibike-tripdata.csv'
data2014_08 = '../data/201408-citibike-tripdata.csv'
data2014_09 = '../data/201409-citibike-tripdata.csv'
data2014_10 = '../data/201410-citibike-tripdata.csv'
data2014_11 = '../data/201411-citibike-tripdata.csv'
data2014_12 = '../data/201412-citibike-tripdata.csv'
data2015_01 = '../data/201501-citibike-tripdata.csv'
data2015_02 = '../data/201502-citibike-tripdata.csv'
data2015_03 = '../data/201503-citibike-tripdata.csv'
data2015_04 = '../data/201504-citibike-tripdata.csv'
data2015_05 = '../data/201505-citibike-tripdata.csv'
data2015_06 = '../data/201506-citibike-tripdata.csv'
data2015_07 = '../data/201507-citibike-tripdata.csv'
data2015_08 = '../data/201508-citibike-tripdata.csv'
data2015_09 = '../data/201509-citibike-tripdata.csv'
data2015_10 = '../data/201510-citibike-tripdata.csv'
data2015_11 = '../data/201511-citibike-tripdata.csv'
data2015_12 = '../data/201512-citibike-tripdata.csv'
data2016_01 = '../data/201601-citibike-tripdata.csv'
data2016_02 = '../data/201602-citibike-tripdata.csv'
data2016_03 = '../data/201603-citibike-tripdata.csv'
data2016_04 = '../data/201604-citibike-tripdata.csv'
data2016_05 = '../data/201605-citibike-tripdata.csv'
data2016_06 = '../data/201606-citibike-tripdata.csv'
data2016_07 = '../data/201607-citibike-tripdata.csv'
data2016_08 = '../data/201608-citibike-tripdata.csv'
data2016_09 = '../data/201609-citibike-tripdata.csv'
data2016_10 = '../data/201610-citibike-tripdata.csv'
data2016_11 = '../data/201611-citibike-tripdata.csv'
data2016_12 = '../data/201612-citibike-tripdata.csv'
data2017_01 = '../data/201701-citibike-tripdata.csv'
data2017_02 = '../data/201702-citibike-tripdata.csv'
data2017_03 = '../data/201703-citibike-tripdata.csv'

stationFile = '../data/process/station.csv'
jsonDataDir = '../data/json/'

dataFileList = [data2013_07,data2013_08,data2013_09,data2013_10,data2013_11,data2013_12,
                data2014_01, data2014_02, data2014_03, data2014_04, data2014_05, data2014_06,
                data2014_07, data2014_08, data2014_09, data2014_10, data2014_11, data2014_12,
                data2015_01, data2015_02, data2015_03, data2015_04, data2015_05, data2015_06,
                data2015_07, data2015_08, data2015_09, data2015_10, data2015_11, data2015_12,
                data2016_01, data2016_02, data2016_03, data2016_04, data2016_05, data2016_06,
                data2016_07, data2016_08, data2016_09, data2016_10, data2016_11, data2016_12,
                data2017_01, data2017_02, data2017_03,
                ]

def getAllLines():
    '''
    获取各个文件的行数
    :return: 返回行数列表
    '''
    bufferSize = 65536
    linesList = []
    for filename in dataFileList:
        with open(filename,'rb') as f:
            lines = 0
            while True:
                bufferStr = f.read(bufferSize)
                if not bufferStr:
                    break
                lines += bufferStr.count('\n')

        linesList.append(lines)
    return linesList

# print getAllLines()
# [843417, 1001959, 1001959, 1037713, 675775, 443967, 300401, 224737, 439118, 670781,
#  866118, 936881, 968843, 963490, 953888, 828712, 529189, 399070, 285553, 196931, 341827,
#  652391, 961987, 941220, 1085677, 1179045, 1289700, 1212278, 987246, 804126, 509479, 560875,
#  919922, 1013150, 1212281, 1460319, 1380111, 1557664, 1648857, 1573873, 1196943, 812193,
#  726677, 791648, 727666]


def plotBar():
    '''
    通过条形图展示发展情况(整体的使用次数)
    :return:
    '''
    recordsList = [843417, 1001959, 1034360, 1037713, 675775, 443967, 300401, 224737, 439118, 670781,
                   866118, 936881, 968843, 963490, 953888, 828712, 529189, 399070, 285553, 196931, 341827,
                   652391, 961987, 941220, 1085677, 1179045, 1289700, 1212278, 987246, 804126, 509479, 560875,
                   919922, 1013150, 1212281, 1460319, 1380111, 1557664, 1648857, 1573873, 1196943, 812193,
                   726677, 791648, 727666]
    timeList = ['13_07','13_08','13_09','13_10','13_11','13_12',
                '14_01', '14_02', '14_03', '14_04', '14_05', '14_06',
                '14_07', '14_08', '14_09', '14_10', '14_11', '14_12',
                '15_01', '15_02', '15_03', '15_04', '15_05', '15_06',
                '15_07', '15_08', '15_09', '15_10', '15_11', '15_12',
                '16_01', '16_02', '16_03', '16_04', '16_05', '16_06',
                '16_07', '16_08', '16_09', '16_10', '16_11', '16_12',
                '17_01', '17_02', '17_03',]

    print len(recordsList)
    print len(timeList)
    # 开始绘图
    x_pos = list(range(len(recordsList)))
    plt.bar(x_pos, recordsList, align='center', alpha=0.5)

    plt.grid()

    max_y = max(recordsList)
    plt.xlim([-1, len(recordsList)])
    plt.ylim([0, max_y * 1.04])

    plt.ylabel('Usage Counts(/Thousand)')
    plt.xlabel('Year & Month')
    # rotation参数表示倾斜的角度
    # plt.xticks(x_pos,type_name,size='small',rotation=60)
    plt.xticks(x_pos, timeList, size='small', rotation=60)
    # 设置y轴的标签
    ax = plt.gca()
    yTicks = ax.get_yticks()
    ax.set_yticklabels(str(int(item)/1000)+'K' for item in yTicks)
    plt.title("Bar Plot of Each Month's Usage Counts")

    for a, b in zip(x_pos, recordsList):
        plt.text(a, b + 0.005, '%.1f' %(float(b)/1000), ha='center', va='bottom', fontsize=7)

    # plt.savefig('../pic/type_percent.png')
    plt.show()

# plotBar()

def genAllStation():
    '''
    查看所有的站点的信息(遍历所有的文件)
    :return:
    '''
    print datetime.datetime.now()
    stationDF = None
    for no,onefile in enumerate(dataFileList):
        dataDF = pd.read_csv(onefile)
        # print dataDF.head(5)
        # print dataDF.dtypes
        if no <= 38:
            startStationDF = dataDF.groupby(["start station name"])[
                "start station latitude","start station longitude"].agg(["max"]).reset_index()
            endStationDF = dataDF.groupby(["end station name"])[
                "end station latitude", "end station longitude"].agg(["max"]).reset_index()
        else:
            startStationDF = dataDF.groupby(["Start Station Name"])[
                "Start Station Latitude","Start Station Longitude"].agg(["max"]).reset_index()
            endStationDF = dataDF.groupby(["End Station Name"])[
                "End Station Latitude", "End Station Longitude"].agg(["max"]).reset_index()
        # print startStationDF.head(5)
        # print endStationDF.head(5)
        startStationDF.columns = ["station","latitude","longitude"]
        endStationDF.columns = ["station","latitude","longitude"]
        # print startStationDF.head(5)
        # print endStationDF.head(5)
        print "*" * 80
        print no,onefile
        # print startStationDF.shape
        # print endStationDF.shape
        # 下面两种方式必须要加.drop_duplicates()  否则出现重复,该函数是判断某些列上的数值是否重复
        tempDF = pd.concat([startStationDF,endStationDF],axis=0,join='outer').drop_duplicates(subset=["station"])
        stationDF = pd.concat([tempDF,stationDF],axis=0,join='outer').drop_duplicates(subset=["station"])
        # tempDF = startStationDF.append(endStationDF,ignore_index = False).drop_duplicates()
        # stationDF = tempDF.append(stationDF,ignore_index = False).drop_duplicates()
        print "该文件中的站点数量的分布：",tempDF.shape
        print "目前的站点总数量的分布：",stationDF.shape
        # print startStationDF.head(5)
        # print startStationDF.columns
        # print startStationDF["latitude"][:10]
        # print endStationLatitudeDF.shape
        # break

    stationDF.to_csv(stationFile,index=False)

# genAllStation()

def viewJson():
    '''
    观察热力图所需的数据
    多个列表里面的数据不重复
    :return:
    '''
    jsonFile = '../data/json/hangzhou.json'
    with open(jsonFile,'rb') as f:
        jsonData = json.load(f)
    print jsonData
    print len(jsonData)
    print type(jsonData)
    coords = []
    for list1 in jsonData:
        for item in list1:
            coords.append(item['coord'])

    print len(coords)
    coords = [str(item) for item in coords]
    print coords
    print len(Counter(coords))

# viewJson()

def genHeatMapJson():
    '''
    生成绘制热力图所需要的json文件(按照日期计算)
    :return:
    '''
    print datetime.datetime.now()
    def returnDay(x):
        '''
        根据一个时间，返回时间中的日期 2016-11-01 00:00:08 => 01
        :param x:
        :return:
        '''
        x = x.split(' ')[0]
        if '/' in x:
            x = x.split('/')[1]
        if '-' in x:
            x = x.split('-')[-1]
        return x if len(x) == 2 else "0" + x

    stationDic = {}
    with open(stationFile,'rb') as f:
        for lineNo,line in enumerate(f):
            if lineNo == 0:
                continue
            lineList = line.strip().split(',')
            if lineList[0] in stationDic.keys():
                print lineList[0]
            stationDic[lineList[0]] = (float(lineList[2]),float(lineList[1]))  #经纬度数据弄反了
    print "站点数量：",len(stationDic.keys())
    for no,dataFile in enumerate(dataFileList):
        print "-" * 80
        print no,dataFile
        month = dataFile.split('/')[-1][:6]
        tempDir = jsonDataDir + month + '/'
        if not os.path.exists(tempDir):
            print "当前文件夹不存在！"
            os.mkdir(tempDir)

        dataDF = pd.read_csv(dataFile)
        if no <= 38:
            dataDF['starttime'] = dataDF['starttime'].apply(returnDay)
            dataDF['stoptime'] = dataDF['stoptime'].apply(returnDay)
            startGroupByDF = dataDF.groupby(['starttime','start station name'])['gender'].agg(['count'])
            endGroupByDF = dataDF.groupby(['stoptime','end station name'])['gender'].agg(['count'])

        else:
            dataDF = pd.read_csv(dataFile)
            dataDF['Start Time'] = dataDF['Start Time'].apply(returnDay)
            dataDF['Stop Time'] = dataDF['Stop Time'].apply(returnDay)
            startGroupByDF = dataDF.groupby(['Start Time', 'Start Station Name'])['Gender'].agg(['count'])
            endGroupByDF = dataDF.groupby(['Stop Time', 'End Station Name'])['Gender'].agg(['count'])

        # print startGroupByDF.loc["01"].loc["1 Ave & E 15 St"]
        startIndex1 = startGroupByDF.index.levels[0]
        startIndex2 = startGroupByDF.index.levels[1]
        endIndex1 = endGroupByDF.index.levels[0]
        endIndex2 = endGroupByDF.index.levels[1]
        # print startGroupByDF.index.levels[0]  # 多重索引遍历的写法
        for stime in startIndex1: # 开始位置
            index_ = startGroupByDF.loc[stime].index
            jsonList = []
            for stationName in startIndex2:
                if stationName in index_:
                    tempDic = {}
                    # print stationName
                    count = startGroupByDF.loc[stime].loc[stationName]["count"] # 多重索引获取数据
                    # print count
                    coord = stationDic[stationName]
                    tempDic['lng'] = coord[0]
                    tempDic['lat'] = coord[1]
                    tempDic['count'] = int(count)  # 必须转化成int类型 否则：TypeError: 74 is not JSON serializable
                    jsonList.append(tempDic)
                # print stationName


            # jsonList = json.dumps(jsonList,cls=ListEncoder)
            # print jsonList[:20]
            jsonFileName = tempDir + stime + '_start.json'
            with open(jsonFileName,'wb') as f:
                json.dump(jsonList,f)
            # break
        for etime in endIndex1: # 结束位置
            index_ = endGroupByDF.loc[etime].index
            jsonList = []
            for stationName in endIndex2:
                if stationName not in index_:
                    continue
                tempDic = {}
                # print stationName
                count = endGroupByDF.loc[etime].loc[stationName]["count"]  # 多重索引获取数据
                coord = stationDic[stationName]
                tempDic['lng'] = coord[0]
                tempDic['lat'] = coord[1]
                tempDic['count'] = int(count)  # 必须转化成int类型 否则：TypeError: 74 is not JSON serializable
                jsonList.append(tempDic)

            jsonFileName = tempDir + etime + '_end.json'
            with open(jsonFileName,'wb') as f:
                json.dump(jsonList,f)
        # break
    print datetime.datetime.now()
    print "END..."

genHeatMapJson()
