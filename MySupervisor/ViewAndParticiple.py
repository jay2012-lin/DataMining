# -*- coding: utf-8 -*-
# @Time    : 2017/11/14 10:20
# @Author  : jaylin
# @Email   : jaylin008@qq.com
# @File    : ViewAndParticiple.py
# @Software: PyCharm Community Edition

import re
from collections import Counter
import numpy as np
import jieba
import sklearn

evaluateDataFile = '../data/mysupervisor_out.txt'
evaluateWordsFile = '../data/evaluate_words.txt'
segFile = '../data/seg_words.txt'
wordsCountFile = '../data/words_count.txt'

def getWordsFile(inFile,outFile):
    '''
    将原始数据中的文本提取出来，形成新的文件
    :param inFile:
    :param outFile:
    :return:
    '''
    allEvaluates = []
    with open(inFile,'rb') as f:
        for line in f:
            lineList = line.split('\001')
            words = ' '.join(lineList[-5:])
            allEvaluates.append(words)

    print "总的评价文本长度为："
    print len(allEvaluates)
    with open(outFile,'wb') as f:
        for item in allEvaluates:
            item = re.sub('[ \t]{2,}',' ',item)
            f.write(item)

# getWordsFile(evaluateDataFile,evaluateWordsFile)

def participle(inFile,outFile):
    '''
    分词，用空格隔开
    :param inFile:
    :param outFile:
    :return:
    '''
    resultList = []
    with open(inFile,'rb') as f:
        for line in f:
            seg_list = jieba.cut(line)
            resultList.append(' '.join(seg_list))

    print "数据的总长度为：",len(resultList)
    with open(outFile,'wb') as f:
        for item in resultList:
            f.write(item.encode('utf-8'))

    print "END..."

# participle(evaluateWordsFile,segFile)

def countWords(inFile,outFile):
    '''
    统计分好词的文本的词频
    :param inFile:
    :param outFile:
    :return:
    '''
    allWords = []
    with open(inFile,'rb') as f:
        for line in f:
            allWords.extend(line.strip().split(' '))

    counter = Counter(allWords)  # 不过滤 14072
    counter = sorted(counter.iteritems(),key=lambda x:x[1],reverse=True)
    with open(outFile,'wb') as f:
        for word, i in counter:
            if re.match('\A[,.;:\'\"!?~`/<>\[\]\{\}()\-\+_=，。：；‘’“”！？~·、《》（）—…@#$%\^&*￥]+\Z',word) \
                    or re.match('\A\w+\Z', word) or word =='':
                continue
            f.write(word + ' ' + str(i) + '\n')

    print "END..."

# countWords(segFile,wordsCountFile)

def vectorize(lexcion,sentence):
    '''
    根据词典将句子向量化
    :param lexcion: 词典列表
    :param sentence:
    :return:
    '''
    resultVector = np.zeros((len(lexcion),))
    seg_list = jieba.cut(sentence)
    for word in seg_list:
        if word in lexcion:
            resultVector[lexcion.index(word)] += 1

    return list(resultVector)

def vectorizeIndex(lexcion,sentence):
    '''
    根据词典将句子向量化,返回向量保数据量太大，返回index的列表
    :param lexcion: 词典列表
    :param sentence:
    :return:
    '''
    resultIndex = []
    seg_list = jieba.cut(sentence)
    seg_list = list(seg_list)
    # print seg_list
    for word in seg_list:
        if word in lexcion:
            resultIndex.append(lexcion.index(word))
    # print resultIndex
    return resultIndex

def splitEvaluation(lexiconFile,inFile):
    '''
    根据原始数据按照不同的评价指标分离，分词向量化之后写入文件
    :param inFile:
    :return:
    '''
    file1 = '../data/model_data/x1.txt'
    file2 = '../data/model_data/x2.txt'
    file3 = '../data/model_data/x3.txt'
    file4 = '../data/model_data/x4.txt'
    file5 = '../data/model_data/x5.txt'

    f1 = open(file1,'wb')
    f2 = open(file2,'wb')
    f3 = open(file3,'wb')
    f4 = open(file4,'wb')
    f5 = open(file5,'wb')

    lexicon = []
    with open(lexiconFile,'rb') as f:
        for line in f:
            lexicon.append(line.split(' ')[0].decode('utf-8'))
    print lexicon
    with open(inFile,'rb') as f:
        for lineNo,line in enumerate(f):
            if lineNo % 200 == 0:
                print "当前正在处理的行数为：",lineNo
            lineList = line.strip().split('\001')
            id = lineList[0]
            x1 = lineList[1]
            x2 = lineList[2]
            x3 = lineList[3]
            x4 = lineList[4]
            l1 = lineList[5]
            l2 = lineList[6]
            l3 = lineList[7]
            l4 = lineList[8]
            l5 = lineList[9]

            allEvaluate = ""
            v1 = ""
            v2 = ""
            v3 = ""
            v4 = ""
            v5 = ""
            if l1 != None:
                v1 = vectorizeIndex(lexicon,l1)
                allEvaluate += l1
            if l2 != None:
                v2 = vectorizeIndex(lexicon,l2)
                allEvaluate += l2
            if l3 != None:
                v3 = vectorizeIndex(lexicon,l3)
                allEvaluate += l3
            if l4 != None:
                v4 = vectorizeIndex(lexicon,l4)
                allEvaluate += l4
            if l5 != None:
                allEvaluate += l5
            v5 = vectorizeIndex(lexicon,allEvaluate)
            # print id,x1,x2,x3,x4,l1,l2,l3,l4,l5
            # 获得平均得分
            notNA = 0
            totalScore = 0
            if x1 != 'N.A.':
                notNA += 1
                totalScore += int(x1)
            if x2 != 'N.A.':
                notNA += 1
                totalScore += int(x2)
            if x3 != 'N.A.':
                notNA += 1
                totalScore += int(x3)
            if x4 != 'N.A.':
                notNA += 1
                totalScore += int(x4)

            if notNA == 0:
                meanScore = 'N.A.'
            else:
                meanScore = float(totalScore) / notNA
            # print meanScore

            # 将分词统计结果写入文件
            f1.write(str(id)+'\001'+str(x1)+'\001'+str(meanScore)+'\001'+','.join([str(item) for item in v1])+'\n')
            f2.write(str(id)+'\001'+str(x2)+'\001'+str(meanScore)+'\001'+','.join([str(item) for item in v2])+'\n')
            f3.write(str(id)+'\001'+str(x3)+'\001'+str(meanScore)+'\001'+','.join([str(item) for item in v3])+'\n')
            f4.write(str(id)+'\001'+str(x4)+'\001'+str(meanScore)+'\001'+','.join([str(item) for item in v4])+'\n')
            f5.write(str(id)+'\001'+str(meanScore)+'\001'+','.join([str(item) for item in v5])+'\n')

        f1.close()
        f2.close()
        f3.close()
        f4.close()
        f5.close()

splitEvaluation(wordsCountFile,evaluateDataFile)

