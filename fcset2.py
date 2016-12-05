# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 12:04:41 2016

@author: luzhangqin
"""
import time

#打印运行时间
def deco(func):
    def _deco(*args, **kwargs):
        print("begin %s is running." % func.__name__)
        begin_time = time.time()
        ret = func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - begin_time
        print("end %s is running,total time is %.2f s" %(func.__name__, total_time))
        return ret
    return _deco

#读取字典
@deco
def load_dic(filename):
    f = open(filename,'r')#读取字典文件
    word_dic = set()#设置一个集合类似list但是是无序的
    max_length = 1#设置一个默认的词语最大长度
    for line in f:#遍历字典文件
        word = unicode(line.strip('\n'),'utf8')#删除末尾\n，并用转成utf8的字符编码
        #word = word.strip()
        word = word.split()#用空格作为标记 将 后面的字符串变成 list AT&T 3 nz 这个用的jieba 的字典
        word_dic.add(word[0])#将字典载入到集合
        if len(word[0]) > max_length:#如果list中的字典长度大于默认则修改为list中字典的长度
            max_length = len(word[0])
    return max_length, word_dic#返回字典中词的最大长度和集合

#中文分词算法之最大正向匹配算法
@deco
def fmm_word_seg(sentence, word_dic, max_length):
    sentence = unicode(sentence, 'utf8')#将句子的字符集编码变成utf8
    begin = 0#设置一个起始位置
    words = []#保存返回的分词后的字符串list

    while begin < len(sentence):#遍历句子
    #for i in range（5,0,-1）表示i 5,4,3,2,1
    #min(begin + max_len, len(sentence))防止begin + max_len越界
        for end in range(min(begin + max_length, len(sentence)), begin, -1):
            #sentence[begin : end]切片
            #a = '123' a[0:2]->'12'
            word = sentence[begin : end]#取出 begin : end 的字符串
            if word in word_dic or end == begin + 1:#如果字符在字典中存在或者只有一个字符则进入下面的步骤
                words.append(word)#将字符串保存到words中
                break#跳出for循环
        begin = end#修改起始位置
    return words#返回


#中文分词算法之最大逆向匹配算法
@deco
def bmm_word_seg(sentence, word_dic, max_length):
    sentence = unicode(sentence, 'utf8')#将句子的字符集编码变成utf8
    end = len(sentence)#设置一个起始位置
    words = []#保存返回的分词后的字符串list
    
    while end > 0:
        for begin in range(max(end - max_length, 0), end, 1):
            word = sentence[begin : end]
            if word in word_dic or end == begin + 1:
                words.insert(0,word)
                break
        end = begin
    return words

#中文分词算法之双向最大匹配算法
@deco
def bm_word_seg(sentence, word_dic, max_length):
    bm_words = []
    fmm_words = fmm_word_seg(sentence, word_dic, max_length)
    bmm_words = bmm_word_seg(sentence, word_dic, max_length)

    fmm_count = 0
    bmm_count = 0

    for fmm_word in fmm_words:
        fmm_count += len(fmm_word)**2
    
    for bmm_word in bmm_words:
        bmm_count += len(bmm_word)**2  
    
    if fmm_words == bmm_words:#分词结果相同
        bm_words = fmm_words
    elif len(fmm_words) != len(bmm_words):#分词结果词数不同，取分词数量较少的
        bm_words = fmm_words if len(fmm_words) < len(bmm_words) else bmm_words
    elif fmm_count >= bmm_count:#分词结果不同，返回其中权重的那个
        bm_words = bmm_words
    else:
        bm_words = fmm_words
        
    return bm_words

#中文分词算法之全分词算法
@deco
def all_word_seg(sentence, word_dic, max_length):
    sentence = unicode(sentence, 'utf8')#将句子的字符集编码变成utf8
    begin = 0#设置一个起始位置
    words = []#保存返回的分词后的字符串list
    isflag = 0

    while begin < len(sentence):
        for end in range(min(begin + max_length, len(sentence)), begin, -1):
            word = sentence[begin : end]
            if word in word_dic or end == begin + 1:
                if isflag != 0 and end == begin +1:
                    break
                    #pass
                else:
                    words.append(word)
                    if isflag < len(word):
                        isflag = len(word)
        begin += 1
        isflag -= 1
    return words


if __name__ == '__main__': 
    max_len, word_dic = load_dic('dict.txt')
    test_str = '研究生命起源学说'
    
    #中文分词算法之最大正向匹配算法
    words = fmm_word_seg(test_str, word_dic, max_len)
    print ('/').join(words)

    #中文分词算法之最大逆向匹配算法
    words = bmm_word_seg(test_str, word_dic, max_len)
    print ('/').join(words)
    
    #中文分词算法之全分词算法
    words = all_word_seg(test_str, word_dic, max_len)
    print ('/').join(words)
    
    #中文分词算法之双向最大匹配算法
    words = bm_word_seg(test_str, word_dic, max_len)
    print ('/').join(words)