# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 17:49:57 2022
word frequency from mendeley library
@author: shouy
"""
import enchant
import pandas as pd
import stardict

mydict = stardict.open_dict('ecdict.csv')
list0 = pd.read_csv('PageTerms.csv') #读取csv
words0 = list0['term']
word = []
phonetic = []
translation = []
pwl = enchant.request_pwl_dict("coca_20000.txt")
for i in words0:
    if not pd.isnull(i) and pwl.check(i):
        t = mydict.query(i)
        if not t is None:
            word.append(t['word'])
            phonetic.append(t['phonetic'])
            translation.append(t['translation'])
words = pd.DataFrame({'word': word, 'phonetic': phonetic, 'translation': translation})
words.to_csv('words.csv')
words_simple = pd.DataFrame(word)
words_simple.to_csv('words_simple.csv')