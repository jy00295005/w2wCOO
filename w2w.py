#!/usr/bin/env python
#coding:utf-8
import re
import glob
from lib import create_docs as cd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import csv
import operator
from sklearn import preprocessing
print np.__version__

#选择共现范围
co_occ_type = 'para'  #para / doc

#目录
all_pathes = ['data/docs/','data/stop.txt','data/corpus.txt']

#read all the files,stop words and corpus
pre_docs, stops, corpus= cd.get_all_docs(all_pathes)

if co_occ_type == 'para':
	pre_docs = cd.split_docs_2_para(pre_docs)	

#remove stop words
pre_docs = cd.remove_stop_words(pre_docs,stops)
#rewrite corpus
pre_docs = cd.replace_corpus(pre_docs,corpus)	
#create docs with corpus
after_docs = cd.rewrite_docs(pre_docs,corpus)		

def convert_sparse_2_w2w(mat_):
	mat_ = mat_.todense()
	mat_ = 1 <= mat_
	mat_ = 1 * mat_
	mat_dense = (mat_.T * mat_)
	new_mat = np.triu(mat_dense,0)
	np.fill_diagonal(new_mat, 0)
	# new_mat[np.diag_indices_from(new_mat)] /= 0
	return new_mat.tolist()

count_model = CountVectorizer() # default unigram model
X = count_model.fit_transform(after_docs)
values = convert_sparse_2_w2w(X)
print count_model.vocabulary_
print values
orted_x = sorted(count_model.vocabulary_.items(), key=operator.itemgetter(1))
header = ['#']
for o in orted_x:
	header.append(o[0].encode('utf8'))
for i,x in enumerate(values):
	values[i].insert(0, header[i+1])
with open('data/export/w2w_%s.csv' %co_occ_type, 'wb') as fh:
	writer = csv.writer(fh, delimiter=',')
	writer.writerow(header)
	writer.writerows(values)