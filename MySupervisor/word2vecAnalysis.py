# -*- coding: utf-8 -*-
# @Time    : 2017/11/16 11:00
# @Author  : jaylin
# @Email   : jaylin008@qq.com
# @File    : word2vecAnalysis.py
# @Software: PyCharm Community Edition
# 使用word2vec和sentence2vec的方法实验

import random
import gensim
from gensim.models import word2vec
import numpy as np
import pandas as pd
import xgboost as xgb

corpusFile = '../data/seg_words.txt'
modelFile = '../model/w2v_model'
labelFile = '../data/model_data/x5.txt'

dimension = 150
def trainW2v(corpusFile,outModelFile):
    '''
    通过word2vec得到词向量
    :param corpusFile:
    :param outModelFile:
    :return:
    '''
    sentences=word2vec.Text8Corpus(u'../data/seg_words.txt')
    # 词最小出现的次数和向量维数
    model=word2vec.Word2Vec(sentences, min_count=1,size=dimension)
    print model
    print model.wv
    print model[u'，']
    print model.wv.syn0  # 向量列表
    # print model.wv.syn0norm
    # a = model.wv.vocab  # 是一个字典，键是所有的单词列表
    # print len(a.keys())
    # print model.wv.index2word  # 词典列表
    print model.wv.index2word[0]
    # print len(model.wv.index2word)
    # print model.wv.vector_size
    model.save(outModelFile)
    print "END..."
    # print model[u'好']
    # print len(model[u'好'])
    # y2=model.similarity(u"好", u"还行")
    # print y2
    #
    # for i in model.most_similar(u"好"):
    #     print i[0],i[1]

trainW2v(corpusFile,modelFile)

def genSentenceVec(sentStr,model,dimension=dimension):
    '''
    根据分好词的句子返回一个句子的向量化表示（所有词向量的均值）
    :param sentStr:
    :param modelFile:
    :return:
    '''
    wordsNum = 0
    resultVec = np.zeros((dimension,))
    for item in sentStr.strip().split(' '):
        # print item
        if item not in model.wv.index2word:  # 过滤不在模型中的词语
            continue
        if item != None and item != '':
            wordsNum += 1
            resultVec += np.array(model[item])

    if wordsNum == 0:
        return resultVec
    else:
        # print "_"*60
        return resultVec / wordsNum

def genTrainData(labelFile,sentFile,modelFile,dropNan=True):
    xDataFrame = pd.read_csv(labelFile, delimiter='\001', header=None)
    xDataFrame.columns = ['id', 'score', 'wordIndex']
    model = gensim.models.Word2Vec.load(modelFile)
    # dimensions = len(model[u'好'])
    # print scoreList
    allVec = []
    with open(corpusFile,'rb') as f:
        for lineno,line in enumerate(f):
            line = line.decode('utf-8')
            if lineno % 100 == 0:
                print "当前处理的行数为：",lineno
            lineVec = genSentenceVec(line.strip(),model,dimension=dimension)
            # print lineVec
            # break
            allVec.append(list(lineVec))

            # scoreList = xDataFrame['score'].values
    scoreList = []
    notnanIndexList = []
    if dropNan:
        xDataFrame['score'][xDataFrame['score'] == 'N.A.'] = np.nan
        # print xDataFrame.dtypes
        xDataFrame['score'] = xDataFrame['score'].astype('float')
        scoreList = xDataFrame['score'].dropna()
        scoreList = [float(item) for item in scoreList]
        for i in range(len(xDataFrame)):
            # print xDataFrame.loc[i, 'score']
            if np.isnan(xDataFrame.loc[i, 'score']):
                pass
            else:
                notnanIndexList.append(i)
    allVec = np.array(allVec)[notnanIndexList]
    print len(allVec)
    return np.array(scoreList),allVec

# genTrainData(labelFile,corpusFile,modelFile)

def trainXgbModle(test_size=0.3):

    y, x = genTrainData(labelFile,corpusFile,modelFile)
    y = y / 5
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
    #

    # 删除score空值：
    # 50 :[34]	train-mae:0.08929	test-mae:0.210637
    # 100:[37] train-mae:0.081816	test-mae:0.205678
    # 150:[26]	train-mae:0.095442	test-mae:0.214572
    # 200:[157]	train-mae:0.018517	test-mae:0.209841
    # 300:[54]	train-mae:0.056739	test-mae:0.208132
    y_pre = bst.predict(data_test).reshape(len(test_x), )
    # print test_y[:20]
    # print y_hat[:20]
    for i in range(50):
        print test_y[i] * 5, y_pre[i] * 5

trainXgbModle()