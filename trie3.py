# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 15:48:17 2016

@author: luzhangqin
"""
import time

def deco(func):
    def _deco(*args, **kwargs):
        begin = 0
        print('beginning %s' %(func.__name__))
        begin = time.time()
        ret = func(*args, **kwargs)
        end = time.time()
        print('ending %s' %(func.__name__))
        print('run time %.2f' %(end - begin))
        
        return ret
    return _deco

#loading dict
@deco
def get_trie(fileName):
    word = ''#词组
    freq = 0.0#词频率    
    nominal = ''#词性
    
    trie = {}#trie树
    freqTrie = {}#trie词频
    totalTrie = 0.0#trie总词频
    
    lineno = 0#文件计算行数
    
    fileWord = open(fileName,'r')
    for lineWord in fileWord.readlines():
        lineno += 1
        word, freq, nominal = lineWord.strip('\n').split(' ')
        
        totalTrie += float(freq)
        freqTrie[word] = float(freq)
        p = trie
        for character in word:
            if character not in p:
                p[character] = {}
            p = p[character]
        p[''] = ''#end
    return trie, freqTrie, totalTrie
    
#
    
#中文分词算法之最大正向匹配算法
@deco
def fmm_word_seg(sentence, word_dic):
    words = []
    
    p = word_dic    
    flag = ''
    flag_mv = ''
    begin = 0
    begin_mv = 0
    
    while len(sentence) > begin:
        sentence = sentence[begin::]
        
        p = word_dic    
        flag = ''
        flag_mv = ''
        begin = 0
        begin_mv = 0
        
        for word in sentence:
            if word not in p:
                if begin_mv == 0:
                    words.append(word)
                    begin = 1
                    break
                else:
                    words.append(flag_mv)
                    begin = begin_mv
                    break
            else:
                flag += word
                begin += 1
                p = p[word]
                if '' in p:
                    begin_mv = begin
                    flag_mv = flag
                if len(sentence) <= begin:
                    words.append(sentence[1::] if flag_mv == 0 else flag_mv )
                    begin = 1 if begin_mv == 0 else begin_mv
    return words

#中文分词算法之全分词算法
@deco
def all_word_seg(sentence, word_dic):
    words = []
    
    p = word_dic
    
    flag = ''
    flag_mv = ''
    begin = 0
    begin_mv = 0    
    
    for idWord, word in enumerate(sentence):
        flag = ''
        flag_mv = ''
        begin = 0
        p = word_dic
        
        if word in p:
            begin += 1
            p = p[word]
            flag += word
            
            if idWord + 1 < len(sentence):
                for word2 in sentence[idWord + 1::]:
                    if word2 in p:
                        p = p[word2]
                        begin += 1
                        flag += word2
                        if '' in p:
                            words.append(flag)
                            begin_mv = begin if begin_mv < begin else begin_mv
                    elif begin_mv == 0:
                        words.append(word)
                        begin_mv += 1
                        break
                    else:
                        break
            elif begin_mv == 0:
                words.append(word)
                begin_mv += 1
        elif begin_mv == 0:
            words.append(word)
            begin_mv += 1
        else:
            pass
        begin_mv -= 1
        
    return words

if __name__ == '__main__':                 
    trie, freqTrie, totalTrie = get_trie('dict.txt')
    test_str = '我在研究生命起源学说的课本是不是在你那边'
    
    #中文分词算法之最大正向匹配算法
    #words = fmm_word_seg(test_str, trie)
    #print(('/').join(words))
    
   #中文分词算法之全分词算法
    words = all_word_seg(test_str, trie)
    print(('/').join(words))


    