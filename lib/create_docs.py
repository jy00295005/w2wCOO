#!/usr/bin/env python
#coding:utf-8
import re
import glob

def get_all_docs(docs_path_):
	docs_pathes = glob.glob("%s*.txt" %docs_path_[0])
	pre_docs = []
	for doc_path in docs_pathes:
		with open(doc_path) as f:
			pre_docs.append(f.read())

	with open(docs_path_[1]) as f:
		stops = f.read().splitlines()

	with open(docs_path_[2]) as f:
		corpus = f.read().splitlines()

	return pre_docs,stops,corpus


def remove_stop_words(docs_,stops_):
	for stop in stops_:
		for pd_index, doc in enumerate(docs_):
			docs_[pd_index] = doc.replace(stop, '')

	return docs_


def replace_corpus(docs_,corpus_):
	for corpu_index,corpu in enumerate(corpus_):
		if '||||' in corpu:
			replace_list = corpu.split('||||')
			corpus_[corpu_index] = replace_list[0]
			for doc_index, doc in enumerate(docs_):
					docs_[doc_index] = re.sub(replace_list[1],replace_list[0],doc)
	return docs_

def rewrite_docs(docs_,corpus_):
	after_docs = []
	for i,pre_doc in enumerate(docs_):
		after_doc = ''
		for corpu in corpus_:
			after_doc += ' '+' '.join(re.findall(corpu, pre_doc))
		after_docs.append(after_doc)
	return after_docs

def split_docs_2_para(docs_):
	return_doc = []
	for doc in docs_:
		split_paras = doc.split('\n')
		for para in split_paras:
			if para is not '':
				return_doc.append(para)

	return return_doc



