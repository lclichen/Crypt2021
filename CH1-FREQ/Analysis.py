#!/usr/bin/env python3
#-*-coding:utf-8-*-
"""
使用Kasiski方法分析文件。
Kasiski方法：
"""
import math
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

class Analysis():
    def __init__(self) -> None:
        self.d=[]
        self.num = 0
        self.words = "lpr"
        self.flag1 = 0
        self.flag2 = 0
        self.gcdlist = {}

    def input_file(self,file):
        with open("./out2.txt","r",encoding="utf8")as txt:
            for line in txt:
                for i in line:
                    if i == self.words[0] and self.flag1 == 0 and self.flag2 == 0:
                        self.d.append(self.num)
                        self.flag1 = 1
                        self.num += 1
                        continue
                    if i != self.words[1] and self.flag1 == 1 and self.flag2 == 0:
                        self.d.pop()
                        self.flag1 = 0
                        self.num += 1
                        continue
                    elif i == self.words[1] and self.flag1 == 1 and self.flag2 == 0:
                        self.flag2 = 1
                        self.num += 1
                        continue
                    if i != self.words[2] and self.flag1 == 1 and self.flag2 == 1:
                        self.d.pop()
                        self.flag1 = 0
                        self.flag2 = 0
                    else:
                        self.flag1 = 0
                        self.flag2 = 0
                    self.num += 1
    def output_list(self):
        for i in self.d:
            for j in self.d:
                if i <= j:
                    continue
                gcdnum = str(math.gcd(i,j))
                if gcdnum not in self.gcdlist.keys():
                    self.gcdlist[gcdnum] = 0
                else:
                    self.gcdlist[gcdnum] += 1

        print(sorted(self.gcdlist.items(), key = lambda kv:(kv[1], kv[0])))

with PyCallGraph(output=GraphvizOutput()):
    filedir = "./"
    filename = "out.txt"
    analysis = Analysis()
    analysis.input_file(filedir + filename)
    print(analysis.d)
    analysis.output_list()