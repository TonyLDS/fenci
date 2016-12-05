中文分词自己玩的,分2.X版本的3.X版本的,文件名用2结尾的是2.X版本,文件名用3结尾的是3.X版本。
代码部分是参考别人的，也把别人的代码上传上来了。

#copyfenci2
	gen_trie() trie树的方法加载字典
	gen_pfdict() 前缀树的方式加载字典

#fcset2
	用set作为字典储存方式

	中文分词算法之最大正向匹配算法
    	words = fmm_word_seg(test_str, word_dic, max_len)
    	print ('/').join(words)

    	中文分词算法之最大逆向匹配算法
    	words = bmm_word_seg(test_str, word_dic, max_len)
    	print ('/').join(words)
    
    	中文分词算法之全分词算法
    	words = all_word_seg(test_str, word_dic, max_len)
    	print ('/').join(words)
    
    	中文分词算法之双向最大匹配算法
    	words = bm_word_seg(test_str, word_dic, max_len)
    	print ('/').join(words)

#trie3
	trie树的方法加载字典

	#中文分词算法之最大正向匹配算法
    	#words = fmm_word_seg(test_str, trie)
    	#print(('/').join(words))
    
   	#中文分词算法之全分词算法
    	words = all_word_seg(test_str, trie)
    	print(('/').join(words))

#dag3
	前缀树的方式加载字典
	DAG
	动态规划

#sougou2
	用搜狗词库扩充词库，但是没有词性

#dict,out
	dict.txt 结巴分词的字典
	out.txt 自己的字典
