#!/usr/bin/env python38
#-*-coding:utf-8-*-
"""
逐字符分析文件。
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib,os
from matplotlib import cm
from tqdm import tqdm
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
import math as m
from mpl_toolkits.mplot3d import Axes3D

def getord(c):
    return ord(c.lower())-97
def getchr(c):
    return chr(c%26+97)
def setalpha2(x):
    return x*30+0.1 if x<0.03 else 1
def setalpha3(x):
    return x*100+0.001 if x<0.00999 else 1

def one_word(filename):
    limit = "abcdefghijklmnopqrstuvwxyz"
    word = {}
    for i in limit:
        word[i] = 0
    #word = {"a":0,"b":0,"c":0,"d":0,"e":0,"f":0,"g":0,"h":0,"i":0,"j":0,"k":0,"l":0,"m":0,"n":0,"o":0,
    #"p":0,"q":0,"r":0,"s":0,"t":0,"u":0,"v":0,"w":0,"x":0,"y":0,"z":0}
    num=0
    print("解析文件...")
    with open(filename,"r",encoding="utf8") as txt:
        for line in tqdm(txt):
            for i in line:
                mid = i.lower()
                if mid in limit:
                    num+=1
                    if mid not in word.keys():
                        word[mid] = 1
                    else:
                        word[mid] += 1

    print(sorted(word.items(), key = lambda kv:(kv[1], kv[0])))
    freq = word
    for i in freq.keys():
        freq[i] = freq[i]/num

    #print(sorted(freq.items(), key = lambda kv:(kv[1], kv[0])))

    # 设置matplotlib正常显示中文和负号
    matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
    matplotlib.rcParams['axes.unicode_minus']=False     # 正常显示负号

    plt.bar(word.keys(),word.values(),color='g')
    plt.legend()
    # 显示横轴标签
    plt.xlabel("字母")
    # 显示纵轴标签
    plt.ylabel("频率")
    # 显示图标题
    plt.title("频率分布直方图")
    plt.show()
def two_word(filename):
    limit = "abcdefghijklmnopqrstuvwxyz"
    word = np.zeros((26,26))
    #for i in range(26):
    #    for j in range(26):
    #        word[i][j] = 0
    num=0
    l_i =  ""
    print("解析文件...")
    with open(filename,"r",encoding="utf8") as txt:
        for line in tqdm(txt):
            for i in line:
                mid = i.lower()
                if(l_i == ""):
                    l_i = mid
                    continue
                if mid in limit:
                    num+=1
                    #print(l_i,mid,getord(l_i),getord(mid))
                    word[getord(l_i)][getord(mid)] += 1
                    l_i = mid
    ind = np.unravel_index(np.argmax(word, axis=None), word.shape)
    #print(sorted(word.items(), key = lambda kv:(kv[1], kv[0])))
    freq = np.zeros((26,26))
    for i in range(26):
        for j in range(26):
            freq[i][j] = word[i][j]/num
    print("最频繁："+getchr(ind[0])+getchr(ind[1])+" "+str(freq[ind[0]][ind[1]]))
    #print(sorted(freq.items(), key = lambda kv:(kv[1], kv[0])))
    ax = plt.subplot(projection="3d")
    # 设置matplotlib正常显示中文和负号
    matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
    matplotlib.rcParams['axes.unicode_minus']=False     # 正常显示负号
    print("绘制图像...")
    ls_x = []
    ls_y = []
    ls_z = []
    ls_f = []
    cm = plt.cm.get_cmap('Reds')  #颜色映射，为jet型映射规则
    for x in range(26):
        for y in range(26):
            ls_x.append(x)
            ls_y.append(y)
            ls_z.append(word[x][y])
            ls_f.append(freq[x][y])
            #ax.bar3d(x+0.1,y+0.1,0,dx=0.8,dy=0.8,dz=word[x][y],cmap = "Reds",alpha = setalpha2(freq[x][y]))
    ax.bar3d(ls_x,ls_y,0,dx=0.25,dy=0.25,dz=ls_z,zsort='average')#cmap = "Reds",alpha = setalpha2(freq[x][y]))
    # 显示横轴标签
    keys = []
    for i in limit:
        keys.append(i)
    ax.set_xticks(range(26))
    ax.set_xticklabels(keys)
    ax.set_yticks(range(26))
    ax.set_yticklabels(keys)
    ax.set_xlabel("字符一")
    # 显示纵轴标签
    ax.set_ylabel("字符二")
    # 显示竖轴标签
    ax.set_zlabel("频率")
    # 显示图标题
    plt.title("频率分布三维直方图")
    plt.show()
def three_word(filename):
    limit = "abcdefghijklmnopqrstuvwxyz"
    word = np.zeros((26,26,26))
    #for i in range(26):
    #    for j in range(26):
    #        word[i][j] = 0
    num=0
    l_i =  ""
    ll_i = ""
    print("解析文件...")
    with open(filename,"r",encoding="utf8") as txt:
        for line in tqdm(txt):
            for i in line:
                mid = i.lower()
                if(l_i == ""):
                    l_i = mid
                    continue
                if(ll_i==""):
                    ll_i = l_i
                    l_i = mid
                    continue
                if mid in limit:
                    num+=1
                    word[getord(ll_i)][getord(l_i)][getord(mid)] += 1
                    ll_i = l_i
                    l_i = mid
    ind = np.unravel_index(np.argmax(word, axis=None), word.shape)
    freq = np.zeros((26,26,26))
    ls_x = []
    ls_y = []
    ls_z = []
    ls_f = []
    ls_sort = []
    for i in range(26):
        for j in range(26):
            for k in range(26):
                freq[i][j][k] = word[i][j][k]/num#np.log10(word[i][j][k]/num)
                ls_x.append(i)
                ls_y.append(j)
                ls_z.append(k)
                ls_f.append(freq[i][j][k])
                ls_sort.append((i,j,k,freq[i][j][k]))
    '''
    for i in range(52):
        for j in range(52):
            for k in range(52):
                if((i % 2 == 0) & (i % 2 == 0) & (i % 2 == 0)):
                    freq[i][j][k] = word[i//2][j//2][k//2]/num
                    ls_x.append(i)
                    ls_y.append(j)
                    ls_z.append(k)
                    ls_f.append(freq[i][j][k])
                else:
                    ls_x.append(0)
                    ls_y.append(0)
                    ls_z.append(0)
                    ls_f.append(0)
    '''
    so = sorted(ls_sort, key=lambda f: f[3],reverse=True)[0:10]
    for i in so:
        print("字符串："+getchr(i[0])+getchr(i[1])+getchr(i[2])+" "+str(i[3]))
    fig = plt.figure()
    #ax = Axes3D(fig)
    ax = plt.subplot(111,projection="3d")
    # 设置matplotlib正常显示中文和负号
    matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
    matplotlib.rcParams['axes.unicode_minus']=False     # 正常显示负号
    print("绘制图像...")
    '''
    with tqdm(total=26*26*26) as pbar:
        for x in range(26):
            for y in range(26):
                for z in range(26):
                    ls_x
                    ax.bar3d(x+0.1,y+0.1,z+0.1,dx=0.8,dy=0.8,dz=0.8,color = "green",alpha = setalpha3(freq[x][y][z]))
                    pbar.update(1)
    '''
    X,Y,Z,Fr = np.array(ls_x),np.array(ls_y),np.array(ls_z),np.array(ls_f)
    cm = plt.cm.get_cmap('Reds')  #颜色映射，为jet型映射规则
    fig = ax.scatter3D(X,Y,Z, c = Fr, cmap=cm)
    
    keys = []
    for i in limit:
        keys.append(i)
    ax.set_xticks(range(26))
    ax.set_xticklabels(keys)
    ax.set_yticks(range(26))
    ax.set_yticklabels(keys)
    ax.set_zticks(range(26))
    ax.set_zticklabels(keys)
    ax.set_xlabel("字符一")
    # 显示纵轴标签
    ax.set_ylabel("字符二")
    # 显示竖轴标签
    ax.set_zlabel("字符三")
    # 显示图标题
    # plt.colorbar()
    plt.title("频率分布三维密度图")
    plt.show()

towhere = "0"
while(1):
    if(towhere == "0"):
        filename= "out2.txt" #os.path.split(os.path.realpath(__file__))[0] + os.sep + input("请输入要解析的文件名:")
    print("模式： 0-重新选择文件;1-单字符解析;2-双字符解析;3-三字符解析;其他-退出;")
    towhere = input("请选择：")
    if towhere == "1":
        one_word(filename)
    elif towhere == "2":
        two_word(filename)
    elif towhere == "3":
        three_word(filename)
    elif towhere == "0":
        continue
    else:
        print("感谢您的使用！")
        exit()
    