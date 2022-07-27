# -*- coding: utf-8 -*-
"""
Created on Sun May 31 17:05:01 2020
pdf 词频统计
@author: shou
"""
import sys
import importlib
importlib.reload(sys)
from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

import glob
import os
pdf_path = ""
pdfs = glob.glob("*.pdf")
n=len(pdfs)

for i in range(n):
    fp = open(pdfs[i], 'rb') # 以二进制读模式打开
    #用文件对象来创建一个pdf文档分析器
    praser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    praser.set_document(doc)
    doc.set_parser(praser)
 
    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()
 
    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
 
        # 循环遍历列表，每次处理一个page的内容
        for page in doc.get_pages(): # doc.get_pages() 获取page列表
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    with open(r'shou.txt', 'a', encoding='utf-8') as f:
                        results = x.get_text()
                        f.write(results + '\n')
 

def solve():
    # e10.3CalThreeKingdoms.py
    import jieba
    excludes = {}
    txt = open('shou.txt', "r", encoding='utf-8').read()
    txt =txt.lower()
    words = jieba.lcut(txt)
    counts = {}
    for word in words:
        if len(word) == 1:  # 排除单个字符的分词结果
            continue
        else:
            counts[word] = counts.get(word, 0) + 1
    for word in excludes:
        del (counts[word])
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)
    for i in range(30):
        word, count = items[i]
        print("{:*<10}{:->5}".format(word, count))
    
    fo = open("shou.csv", "w")
    # print(items[:10])
    for item in items:
        # print(type(item))
        ls = list(item)
        # print(type(ls))
        ls[1] = str(ls[1])
 
        # print(ls)
        fo.write(",".join(ls) + "\n")
    fo.close()
    
if __name__ == '__main__':
    solve()
