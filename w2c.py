#!/usr/bin/env python
#coding:utf-8
import re
import glob
from lib import create_docs as cd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import operator
import csv

def combine_names_values(names_,values_):
	uniq_names = list(set(names_))
	combine_value = []
	for u_name in uniq_names:
		uniq_name_indexs = [name for name in range(len(names_)) if names_[name] == u_name]
		if len(uniq_name_indexs) > 1 :
			combine_doc = ''
			for u_n_i in uniq_name_indexs:
				combine_doc += values_[u_n_i]
		else:
			combine_doc = values_[uniq_name_indexs[0]]
		combine_value.append(combine_doc)
	
	return uniq_names,combine_value

def split_names_values(split_names_,split_values_):
	return_names_ = []
	return_values_ = []
	for name_index_,name_ in enumerate(split_names_):
		if '|' in name_:
			ext_name_li = name_.split('|')
			return_names_.extend(ext_name_li)
			ext_values = [split_values_[name_index_]] * len(ext_name_li)
			return_values_.extend(ext_values)
		else:
			# print split_values_[name_index_]
			return_names_.append(name_)
			return_values_.append(split_values_[name_index_])

	return return_names_,return_values_


all_pathes = ['data/docs/','data/stop.txt','data/corpus.txt']
pre_docs, stop_lines, corpus_lines= cd.get_all_docs(all_pathes)

docs_pathes = glob.glob("data/docs/*.txt")
doc_owers = []
for doc_path in docs_pathes:
	with open(doc_path) as f:
		doc = f.read()
		doc_sp = doc.split('||||')
    	doc_owers.append(doc_sp[0])

# print '--'
# for o in doc_owers:
# 	print o

doc_owers,pre_docs = split_names_values(doc_owers,pre_docs)
doc_owers, pre_docs = combine_names_values(doc_owers,pre_docs)

# print '-a-'

# for o in doc_owers:
# 	print o
# print '--'

# for o in pre_docs:
# 	print o
# 	print '--'
# print '--'

#remove stop words
pre_docs = cd.remove_stop_words(pre_docs,stop_lines)
#rewrite corpus
pre_docs = cd.replace_corpus(pre_docs,corpus_lines)		
#create docs with corpus
after_docs = cd.rewrite_docs(pre_docs,corpus_lines)	

for o in after_docs:
	print o

count_model = CountVectorizer() # default unigram model

X = count_model.fit_transform(after_docs)
values = X.toarray().tolist()
print count_model.vocabulary_


orted_x = sorted(count_model.vocabulary_.items(), key=operator.itemgetter(1))
print count_model.vocabulary_
header = ['#']
for o in orted_x:
	header.append(o[0].encode('utf8'))

# for o in orted_x:
	# print o[0]

for i,owner in enumerate(doc_owers):
	values[i].insert(0,owner)


with open('data/export/w2c.csv', 'wb') as fh:
	writer = csv.writer(fh, delimiter=',')
	writer.writerow(header)
	writer.writerows(values)








