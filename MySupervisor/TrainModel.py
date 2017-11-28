# -*- coding: utf-8 -*-
# @Time    : 2017/11/15 10:14
# @Author  : jaylin
# @Email   : jaylin008@qq.com
# @File    : TrainModel.py
# @Software: PyCharm Community Edition
import random
import xgboost as xgb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

xFile = '../data/model_data/x5.txt'

def conTrainData(inFile):
    '''
    根据格式化的数据返回结构化的向量数据，包含训练特征和标签
    :param inFile:model_data中的x数据
    :return: 特征向量列表，标签值列表
    '''
    lexiconWordsLength = 13259  # 字典长度
    xDataFrame = pd.read_csv(inFile,delimiter ='\001',header=None)
    xDataFrame.iloc[:,1][xDataFrame.iloc[:,1] == 'N.A.'] = np.nan
    xDataFrame.iloc[:, 1] = xDataFrame.iloc[:, 1].astype('float')
    xDataFrame.columns = ['id','score','wordIndex']
    # score 列的空值处理方法
    # xDataFrame['score'] = xDataFrame['score'].fillna(allMean)
    xDataFrame['wordIndex'] = xDataFrame['wordIndex'].fillna("无数据")
    print xDataFrame['score'].isnull().sum()  # 空值长度：1415  总长度：3926
    xDataFrame = xDataFrame.dropna()
    # print xDataFrame.head()
    # print xDataFrame.index
    tempDF = xDataFrame.groupby(['id'])['score'].agg(['mean'])  # 获取平均值，用于空值填充
    # print xDataFrame.reset_index().index
    # print tempDF.indexmeiyo
    # print xDataFrame[1]  注意loc和iloc的区别
    # for i in range(len(xDataFrame)):  # 将空值置换成每一个用户的平均值
    #     if np.isnan(xDataFrame.loc[i,'score']):  # 只能这样判断是否为nan,不能直接等于
    #         xDataFrame.loc[i,'score'] = tempDF.loc[xDataFrame.loc[i,'id'],'mean']
    # allMean = xDataFrame['score'].mean()  # 整体得分的均值
    # xDataFrame['score'] = xDataFrame['score'].fillna(allMean)
    # xDataFrame['wordIndex'] = xDataFrame['wordIndex'].fillna("无数据")

    resultVectors = np.zeros((len(xDataFrame),lexiconWordsLength))
    for no,i in enumerate(xDataFrame.index):
        wordsIndex = xDataFrame.loc[i,'wordIndex']
        # print wordsIndex
        if wordsIndex == '无数据':
            # print i
            # print wordsIndex
            continue
        # re.split()  正则替换
        wordList = [int(item) for item in wordsIndex.split(',')]
        for index in wordList:
            resultVectors[no,index] += 1

    # print resultVectors[0].sum()
    # print resultVectors[1].sum()
    # print resultVectors[2].sum()
    # print tempDF.head(40)
    # print xDataFrame.dtypes
    # print xDataFrame.head(20)
    return resultVectors,xDataFrame['score'].values

# conTrainData(xFile)

def plotBoxPlot(data):
    fig = plt.figure(figsize=(8, 6))
    # plt.axis([-6, 6, -0.5, 20])

    plt.boxplot(data,
                # notch=False,  # box instead of notch shape
                # sym='rs',    # red squares for outliers
                showmeans=True,
                vert=True)  # vertical box aligmnent

    # plt.xticks([y + 1 for y in range(len(ff_list_new))], type_name)
    # plt.xlabel('Profile Image')
    # plt.ylabel('FF')
    # plt.title('FF Boxplot')
    # plt.savefig('../pic/FF.png')
    plt.show()

# _,y = conTrainData(xFile)
# plotBoxPlot(y)

def trainXgbModel(test_size=0.3):
    '''
    训练xgboost模型
    :return:
    '''
    x,y = conTrainData(xFile)
    y = y/5
    allLen = len(x)
    allIndex = range(allLen)
    random.shuffle(allIndex)
    trainLen = int(allLen * (1 - test_size))

    train_x = x[[allIndex[:trainLen]]]
    test_x = x[[allIndex[trainLen:]]]
    train_y = y[[allIndex[:trainLen]]]
    test_y = y[[allIndex[trainLen:]]]

    data_train = xgb.DMatrix(train_x, label=train_y)
    data_test = xgb.DMatrix(test_x, label=test_y)
    watch_list = [(data_train, 'train'), (data_test, 'test')]
    # 默认gbtree 改变参数损失值还是基本不变
    param = {'booster': 'gbtree', 'max_depth': 7, 'gamma': 0.000001, 'eta': 0.2, 'silent': 1,
             'objective': 'reg:logistic', 'eval_metric': 'mae'}
    bst = xgb.train(param, data_train, num_boost_round=5000, evals=watch_list, early_stopping_rounds=200)
    # [340]	train-mae:0.094387	test-mae:0.177679
    # [145] train-rmse:0.152448 test-rmse:0.231229

    # 删除score空值：
    # [381]	train-mae:0.06829	test-mae:0.166588
    y_pre = bst.predict(data_test).reshape(len(test_x),)
    # print test_y[:20]
    # print y_hat[:20]
    for i in range(50):
        print test_y[i] * 5,y_pre[i] * 5

trainXgbModel()