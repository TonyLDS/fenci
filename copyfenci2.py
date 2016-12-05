# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 15:36:25 2016

@author: luzhangqin

"""
import logging

logger = logging.getLogger('test')

def gen_trie(f_name):  
    lfreq = {}  
    trie = {}  
    ltotal = 0.0  
    with open(f_name, 'r') as f:  
        lineno = 0   
        for line in f.read().rstrip().decode('utf-8').split('\n'):  
            lineno += 1  
            try:  
                word,freq,_ = line.split(' ')
                freq = float(freq)  
                lfreq[word] = freq  
                ltotal+=freq  
                p = trie  
                for c in word:  
                    if c not in p:  
                        p[c] ={}  
                    p = p[c]  
                p['']='' #ending flag  
            except ValueError, e:  
                logger.debug('%s at line %s %s' % (f_name,  lineno, line))  
                raise ValueError, e  
    return trie, lfreq, ltotal
    
def gen_pfdict(f_name):
    lfreq = {}
    ltotal = 0
    f = open(f_name,'r')
    for lineno, line in enumerate(f, 1):
        try:
            line = line.strip().decode('utf-8')
            word, freq = line.split(' ')[:2]
            freq = int(freq)
            lfreq[word] = freq
            ltotal += freq
            for ch in xrange(len(word)):
                wfrag = word[:ch + 1]
                if wfrag not in lfreq:
                    lfreq[wfrag] = 0
        except ValueError:
            raise ValueError(
            'invalid dictionary entry in %s at Line %s: %s' % (f_name, lineno, line))
    f.close()
    return lfreq, ltotal

#trie, lfreq, ltotal = gen_trie('test4.txt')
#lfreq, ltotal = gen_pfdict('test4.txt')