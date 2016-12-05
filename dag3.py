# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 20:57:00 2016

@author: luzhangqin
"""
import math
import time

def deco(func):
    def _deco(*arg, **kwargs):
        print ('func %s begin ' %(func.__name__))
        begin = time.time()
        ret = func(*arg, **kwargs)
        end = time.time()
        print ('func %s end, run time %.2fs' %(func.__name__, end - begin))        
        return ret
    return _deco
        
        

#前缀数组字典
@deco
def prefix(filename):
    pfarray = {}
    word = ''
    freq = 0.0
    totalfreq = 0.0
    
    f = open(filename, 'r')
    
    for line in f.readlines():
        line = line.strip('\n')
        word, freq = line.split(' ')[:2:]
        totalfreq += float(freq)
        if word not in pfarray:
            pfarray[word] = float(freq)
        else:
            pfarray[word] = pfarray[word] if pfarray[word] > float(freq) else float(freq)
        wfrag =''
        for ch in word:
           wfrag += ch
           if wfrag not in pfarray:
               pfarray[wfrag] = 0
    f.close()   
    return pfarray, totalfreq

#得到又向无环图（DAG）
@deco
def getdag(sentence, dictionary):
    DAG = {}
    tmplist = []
    ch = ''

    for id_word, word in enumerate(sentence):
        ch = ''
        tmplist = []
        if word not in dictionary:
            pass
        else:
            for i in range(id_word, len(sentence)):
                ch += sentence[i]
                if ch in dictionary:
                    tmplist.append(i)
                else:
                    ch = ch[: len(ch) - 1:]
                    while not dictionary[ch]:
                       tmplist.pop()
                       ch = ch[0: len(ch) - 1:]
                    break
        #print(tmplist)
        if not len(tmplist):
            tmplist.append(id_word)
        DAG[id_word] = tmplist
     
    return DAG

#动态规划 P[1,2,3,4] = P[4] + P[3] + p[2] + P[1]
@deco
def dp(sentence, dictionary, DAG, totalfreq):
    route = {}
    N = len(sentence)
    route[N] = (0, 0)
    logtotal = math.log(totalfreq)
    for idx in range(N - 1, -1, -1):
        #元组大小比较 1e-12 为了防止字典value为0的数据导致匹配成功
        route[idx] = max((math.log(
            (1e-12 if sentence[idx:x + 1] not in dictionary.keys() else dictionary[sentence[idx:x + 1]] or 1e-12)
                ) -logtotal + route[x + 1][0], x) for x in DAG[idx])
    return route

@deco
def translate(sentence, route):
    begin = 0
    end = 0
    words = []
    while begin < len(sentence):
        end = route[begin][1] + 1
        words.append(sentence[begin:end:])
        begin = end
    return words


if __name__ == '__main__':
    filename = 'out.txt'
    sentence = '冰与火之歌'
    dictionary, totalfreq = prefix(filename)
    dag = getdag(sentence, dictionary)
    route = dp(sentence, dictionary, dag, totalfreq)
    words = translate(sentence, route)
    
    print('|'.join(words))
    
    
    