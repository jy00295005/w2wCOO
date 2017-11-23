#!/usr/bin/env python
#coding:utf-8
import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')
import json
import re
import glob
import codecs

search_word = '国家科技计划'


#读取txt文件
def get_raw_docs(docs_path_):
	docs_pathes = glob.glob("%s*.txt" %docs_path_[0])
	pre_docs = []
	pre_docs_names = []
	for doc_path in docs_pathes:
		with codecs.open(doc_path, "r", encoding='utf-8', errors='ignore') as f:
			pre_docs.append(f.read())
			pre_docs_names.append(f.name.split('raw_files/')[1].split('.')[0])
	return pre_docs,pre_docs_names

def cut_sentence(words):
    # words = (words).decode('utf8')
    start = 0
    i = 0
    sents = []
    punt_list = '.!?。！？'.decode('utf8')
    for word in words:
        if word in punt_list and token not in punt_list: #检查标点符号下一个字符是否还是标点
            sents.append(words[start:i+1])
            start = i+1
            i += 1
        else:
            i += 1
            token = list(words[start:i+2]).pop() # 取下一个字符
    if start < len(words):
        sents.append(words[start:])
    return sents

all_pathes = ['data/docs4split/raw_files/']
raw_docs,raw_docs_names = get_raw_docs(all_pathes)

# print len(raw_docs_names)
# # print raw_docs[0]
# # print raw_docs[0]
# print "=============="

# print raw_docs_names[1]
# # print raw_docs[1]
# print "=============="	

# print raw_docs_names[2]
# # print raw_docs[2]

doc_owers = []
raw_data = []
for ii, pre_doc in enumerate(raw_docs):
	print ii
	print pre_doc
	print "=============="
	if '||||' in pre_doc:
		doc_sp = pre_doc.split('||||')
		doc_owers.append(doc_sp[0])
		raw_data.append(doc_sp[1])
	else:
		doc_owers.append('')
		raw_data.append(pre_doc)
	
# search_word = '国际科技计划'

for i, doc in enumerate(raw_data):
	doc_ower = doc_owers[i]
	sent_list = cut_sentence(doc)
	doc_name = raw_docs_names[i]
	matches = filter(lambda s: search_word in str(s), sent_list)
	if matches:
		# print i
		# print doc_ower
		# print len(matches)
		for match_i, match in enumerate(matches):
			# print doc_ower
			text_file = open("data/docs4split/sentence/"+doc_name+"_"+str(match_i)+".txt", "w")
			text_file.write(doc_ower+'||||'+match)
			text_file.close()

