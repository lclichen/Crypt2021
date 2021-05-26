#!/usr/bin/env python39
import os
import random
import re
import time

import numpy as np
import pyperclip
from tqdm import tqdm

#行移位
def shiftRows(state):
    result = np.zeros([4,4],dtype=np.ubyte)
    # 4行分别循环左移0，1，2，3位
    for i in range(4):
        for j in range(4):
            result[i][j] = state[i][(j + i) % 4]
    return result

#逆行移位
def invshiftRows(state):
    result = np.zeros([4,4],dtype=np.ubyte)
    # 4行分别循环左移0，3，2，1位
    for i in range(4):
        for j in range(4):
            result[i][j] = state[i][(j - i + 4) % 4]
    return result

#逆列混淆（用于逆轮密钥）
def invMixColumns(state):
    state = state.T
    result = np.zeros([4,4],dtype=np.ubyte)
    Mt = np.array(((0x0E, 0x09, 0x0D, 0x0B),(0x0B, 0x0E, 0x09, 0x0D),(0x0D, 0x0B, 0x0E, 0x09),(0x09, 0x0D, 0x0B, 0x0E)),dtype=np.ubyte)#.T
    for i in range(4):
        for j in range(4):
            for k in range(4):
                result[i][j]  = result[i][j] ^ SimpleCal(state[i][k],Mt[k][j])
    return result.T
    #孩子人都傻了.jpg，改这玩意改了五天，明明重构之前是正常的，结果稍微整理了下代码之后就出问题了（呆滞）

def add_round_key(state,Kc,k):
    #data = state.copy()
    for i in range(4):
        for j in range(4):
            state[i][j] = state[i][j] ^ Kc[i][j+k*4]
    return state
"""
加密轮函数
"""
def en_round(data,Kc,T,Sbox):
    k = 0
    data = add_round_key(data,Kc,k)
    print("Round"+str(k),[hex(i) for i in np.nditer(data.copy(), order='F')])
    result = np.zeros([4,4],dtype=np.ubyte)
    for k in range(1,10):
        for i in range(4):
            for j in range(4):
                result[i][j] = (T[0][data[0][j] & 0xff][i] ^ T[1][data[1][(j + 1) % 4] & 0xff][i] ^ T[2][data[2][(j + 2) % 4] & 0xff][i] ^ T[3][data[3][(j + 3) % 4] & 0xff][i] ^ Kc[i][k*4+j])
        data = result.copy()
        print("Round"+str(k),[hex(i) for i in np.nditer(result.copy(), order='F')])
    k = 10
    for i in range(4):
        for j in range(4):
            result[i][j] = Sbox[data[i][j] & 0xff]
    result = shiftRows(result)
    data = add_round_key(result,Kc,k)
    print("Round"+str(k),[hex(i) for i in np.nditer(data.copy(), order='F')])
    return data

"""
加密主函数
"""
def en(filename,output_filename,Sen,Ken,Ten):
    print("加密开始...")
    en_start_time = time.time()
    inputFilePath = os.path.split(os.path.realpath(__file__))[0] + os.sep +filename
    fsize = os.path.getsize(inputFilePath)
    with open(inputFilePath,"rb") as f_in:
        with open(os.path.split(os.path.realpath(__file__))[0] + os.sep +output_filename,"wb")as f_out:
            notend = True
            with tqdm(total=fsize//16) as fil:
                while(notend):
                    data = f_in.read(16)
                    if (len(data)<16):
                        notend = False
                        #读取到文件末尾，用\x00以及不足的数目进行补齐
                        
                        data += (random.randbytes(15-len(data))+bytes(chr(16-len(data)),encoding='ASCII'))
                    print(data)
                    #初始化矩阵
                    x = [i for i in data]
                    p = np.array(x).reshape(4, 4).T
                    #轮迭代
                    c = en_round(p,Ken,Ten,Sen)
                    for i in np.nditer(c.copy(), order='F'):
                        f_out.write(i)
                    fil.update(1)
    en_end_time = time.time()
    print("Encrypt Cost Time",en_end_time-en_start_time,"s")
    print("加密完成！")

def de_round(data,Kc,T,Sbox_):
    k = 10
    print("Round"+str(k),[hex(i) for i in np.nditer(data.copy(), order='F')])
    data = add_round_key(data,Kc,k)
    result = np.zeros([4,4],dtype=np.ubyte)
    print("Round"+str(k),[hex(i) for i in np.nditer(data.copy(), order='F')])
    for k in range(9,0,-1):
        for i in range(4):
            for j in range(4):
                result[i][j] = (T[0][data[0][j] & 0xff][i] ^ T[1][data[1][(j + 3) % 4] & 0xff][i] ^ T[2][data[2][(j + 2) % 4] & 0xff][i] ^ T[3][data[3][(j + 1) % 4] & 0xff][i] ^ Kc[i][k*4+j])
        data = result.copy()
        print("Round"+str(k),[hex(i) for i in np.nditer(result.copy(), order='F')])
        pass
    k = 0
    result = invshiftRows(data)
    data = result.copy()
    for i in range(4):
        for j in range(4):
            result[i][j] = Sbox_[data[i][j] & 0xff]
    data = add_round_key(result,Kc,k)
    return data

def de(filename,output_filename,Sde,Kde,Tde):
    print("解密开始...")
    de_start_time = time.time()
    inputFilePath = os.path.split(os.path.realpath(__file__))[0] + os.sep +filename
    fsize = os.path.getsize(inputFilePath)
    with open(inputFilePath,"rb") as f_in:
        with open(os.path.split(os.path.realpath(__file__))[0] + os.sep +output_filename,"wb")as f_out:
            cutnum = 0
            with tqdm(total=fsize//16) as fil:
                while(1):
                    data = f_in.read(16)
                    if (len(data)<16):
                        #切除之前为了补齐16byte补充的内容
                        if (cutnum!=0):
                            f_out.seek(-cutnum,2)
                            f_out.truncate()
                        break
                    #初始化矩阵
                    x = [i for i in data]
                    c = np.array(x).reshape(4, 4).T
                    #轮迭代
                    p = de_round(c,Kde,Tde,Sde)
                    cutnum = int.from_bytes(p[3][3],byteorder='big')
                    print([hex(i) for i in np.nditer(p.copy(), order='F')])
                    for i in np.nditer(p.copy(), order='F'):
                        f_out.write(i)
                    fil.update(1)
    print("解密完成！")
    de_end_time = time.time()
    print("Encrypt Cost Time",de_end_time-de_start_time,"s")

def g_key(w,Rc,S_in):
    tmp = w.copy()
    tmp[0:3] = w[1:4]
    tmp[3] = w[0]
    for i in range(4):
        tmp[i] = (S_in[tmp[i] & 0xff])
    tmp[0] = Rc ^ tmp[0]
    return tmp

def round_next_key(Kw,Rc,S_in):
    w = Kw.copy()
    next_w = np.zeros([4,4],dtype=np.ubyte)
    tmp = g_key(w[...,3],Rc,S_in)
    for i in range(4):
        next_w[i,0] = tmp[i] ^ w[i,0]
        next_w[i,1] = w[i,1] ^ next_w[i,0]
        next_w[i,2] = w[i,2] ^ next_w[i,1]
        next_w[i,3] = w[i,3] ^ next_w[i,2]
    return next_w

# 求最高幂次数
def Nonzero_MSB(value):
    v2str = '{:12b}'.format(value)
    for i in range(12):
        if v2str[i] != ' ' and int(v2str[i]):
            return 12-i

# 模2除法：m为被除数。b为除数，q为商，r为余数
def Mode2_div(fx, gx):
    n = Nonzero_MSB(fx)
    m = Nonzero_MSB(gx)
    if n < m:
        return [0, fx]
    deg = n - m
    fx = fx ^ (gx << deg)
    [q, r] = Mode2_div(fx, gx) 
    return [(1 << deg)|q, r]

# x3 = x1 - q3 * x2
def Calculate(x1, q3, x2):
    value = 0
    for i in range(32):
        if(q3 & (1<<i)):
            value = value ^ (x2<<i)
    return x1^value

def SimpleCal(x2, x1):
    value = 0
    for i in range(32):
        if(x1 & (1<<i)):
            value ^= (x2<<i)
    if value == 0:
        return 0
    [q,r] = Mode2_div(value,0x11B)
    return r

#扩展欧几里得算法
def poly_gcd(d1, d2, x1=1, x2=0, y1=0, y2=1):
    
    if d2==0 or d2==1:  return y2
    q3, d3 = Mode2_div(d1, d2)  # q3(x)=d1(x) // d2(x), d2(x)=d1(x) mod d2(x)
    x3 = Calculate(x1, q3, x2)  # x3 = x1 - q3 * x2
    y3 = Calculate(y1, q3, y2)  # y3 = y1 - q3 * y2
    return poly_gcd(d2,d3,x2,x3,y2,y3)

#S盒字节变换
def byteTransformation(a, x):
    tmp = np.zeros([8],dtype="ubyte")
    for i in range(8):
        tmp[i]= (((a>>i)&0x1)^((a>>((i+4)%8))&0x1)^((a>>((i+5)%8))&0x1)^((a>>((i+6)%8))&0x1)^((a>>((i+7)%8))&0x1)^((x>>i)&0x1)) << i
    tmp[0] = tmp[0]+tmp[1]+tmp[2]+tmp[3]+tmp[4]+tmp[5]+tmp[6]+tmp[7]
    return tmp[0]

#逆S盒字节变换
def invByteTransformation(a, x):
    tmp = np.zeros([8],dtype="ubyte")
    for i in range(8):
        tmp[i]= (((a>>((i+2)%8))&0x1)^((a>>((i+5)%8))&0x1)^((a>>((i+7)%8))&0x1)^((x>>i)&0x1)) << i
    tmp[0] = tmp[0]+tmp[1]+tmp[2]+tmp[3]+tmp[4]+tmp[5]+tmp[6]+tmp[7]
    return tmp[0]

def build_key(key):
    build_start_time = time.time()
    if(os.path.exists(os.path.split(os.path.realpath(__file__))[0] + os.sep +"keys") == False):
        os.makedirs(os.path.split(os.path.realpath(__file__))[0] + os.sep +"keys")

#生成S盒
    if(os.path.exists(os.path.split(os.path.realpath(__file__))[0] + os.sep +"keys/Sboxin.npy") != True):
        print("S盒生成中...")
        Sbox = np.zeros([16,16],dtype="ubyte")
        for i in range(0x10):
            for j in range(0x10):
                Sbox[i][j] = ((i << 4) & 0xF0) + ( j & (0xF))
        for i in range(0x10):
            for j in range(0x10):
                Sbox[i][j] = poly_gcd(0x11B,Sbox[i][j])
        Sbox[0][0] = 0
        for i in range(0x10):
            for j in range(0x10):
                Sbox[i][j] = byteTransformation(Sbox[i][j],0x63)
        print("S盒生成成功")
        Sbox = Sbox.flatten()
        with open(os.path.split(os.path.realpath(__file__))[0] + os.sep +"keys/Sboxin.npy","wb") as Sin:
            np.save(Sin,Sbox.flatten())
    else:
        with open(os.path.split(os.path.realpath(__file__))[0] + os.sep +"keys/Sboxin.npy","rb") as Sin:
            Sbox = np.load(Sin).flatten()
#生成逆S盒
    if(os.path.exists(os.path.split(os.path.realpath(__file__))[0] + os.sep +"keys/Sboxni.npy") != True):
        print("逆S盒生成中...")
        Sbox_ = np.zeros([256],dtype="ubyte")
        tmp = Sbox.copy().reshape(16,16)
        for i in range(0x10):
            for j in range(0x10):
                n = tmp[i][j]
                Sbox_[n] = i*0x10+j
        #Sbox_.shape=[16,16]
        print("逆S盒生成成功")
        with open(os.path.split(os.path.realpath(__file__))[0] + os.sep +"keys/Sboxni.npy","wb") as Sni:
            np.save(Sni,Sbox_.flatten())
    else:
        with open(os.path.split(os.path.realpath(__file__))[0] + os.sep +"keys/Sboxni.npy","rb") as Sni:
            Sbox_ = np.load(Sni).flatten()

#生成轮密钥表
    print("轮密钥表生成中...")
    x = [i for i in key]
    k0 = np.array(x,dtype=np.ubyte).reshape(4, 4).T
    Kbox = np.zeros([4,44],dtype=np.ubyte)
    Rc = bytearray([0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36])
    for i in range(4):
        Kbox[...,i]=k0[...,i]
    for j in range(10):
        Kbox[...,(j+1)*4:(j+2)*4] = round_next_key(Kbox[...,j*4:(j+1)*4],Rc[j],Sbox)
    print("轮密钥生成成功.")
#生成逆轮密钥表
    print("逆轮密钥表生成中...")
    Kbox_ = Kbox.copy()
    for j in range(1,10):
        Kbox_[...,j*4:(j+1)*4] = invMixColumns(Kbox_[...,j*4:(j+1)*4])
    print("逆轮密钥生成成功.")

#生成T盒
    if(os.path.exists(os.path.split(os.path.realpath(__file__))[0] + os.sep +"keys/Tboxin.npy") != True):
        print("T盒生成中...")
        M_t0 = np.array((0x02,0x01,0x01,0x03),dtype=np.ubyte)
        M_t1 = np.array((0x03,0x02,0x01,0x01),dtype=np.ubyte)
        M_t2 = np.array((0x01,0x03,0x02,0x01),dtype=np.ubyte)
        M_t3 = np.array((0x01,0x01,0x03,0x02),dtype=np.ubyte)
        Tbox = np.zeros([4,256,4],dtype=np.ubyte)
        for j in range(256):
            for k in range(4):
                Tbox[0][j][k] = SimpleCal(Sbox[j], M_t0[k])
                Tbox[1][j][k] = SimpleCal(Sbox[j], M_t1[k])
                Tbox[2][j][k] = SimpleCal(Sbox[j], M_t2[k])
                Tbox[3][j][k] = SimpleCal(Sbox[j], M_t3[k])
        print("T盒生成成功")
        with open(os.path.split(os.path.realpath(__file__))[0] + os.sep +"keys/Tboxin.npy","wb") as Tin:
            np.save(Tin,Tbox)
    else:
        with open(os.path.split(os.path.realpath(__file__))[0] + os.sep +"keys/Tboxin.npy","rb") as Tin:
            Tbox = np.load(Tin)
#生成逆T盒
    if(os.path.exists(os.path.split(os.path.realpath(__file__))[0] + os.sep +"keys/Tboxni.npy") != True):

        print("逆T盒生成中...")
        M_t4 = np.array((0x0E, 0x09, 0x0D, 0x0B),dtype=np.ubyte)
        M_t5 = np.array((0x0B, 0x0E, 0x09, 0x0D),dtype=np.ubyte)
        M_t6 = np.array((0x0D, 0x0B, 0x0E, 0x09),dtype=np.ubyte)
        M_t7 = np.array((0x09, 0x0D, 0x0B, 0x0E),dtype=np.ubyte)
        Tbox_ = np.zeros([4,256,4],dtype=np.ubyte)
        for j in range(256):
            for k in range(4):
                Tbox_[0][j][k] = SimpleCal(Sbox_[j], M_t4[k])
                Tbox_[1][j][k] = SimpleCal(Sbox_[j], M_t5[k])
                Tbox_[2][j][k] = SimpleCal(Sbox_[j], M_t6[k])
                Tbox_[3][j][k] = SimpleCal(Sbox_[j], M_t7[k])
        print("逆T盒生成成功")
        with open(os.path.split(os.path.realpath(__file__))[0] + os.sep +"keys/Tboxni.npy","wb") as Tni:
            np.save(Tni,Tbox_)
    else:
        with open(os.path.split(os.path.realpath(__file__))[0] + os.sep +"keys/Tboxni.npy","rb") as Tni:
            Tbox_ = np.load(Tni)

#返回各种盒
    build_end_time = time.time()
    print("BuildKeys Cost Time:",build_end_time-build_start_time,"s")
    return (Sbox,Sbox_,Kbox,Kbox_,Tbox,Tbox_)

#Main Code
key = ''
havekey = False
while(1):
    if(havekey == False):
        start = input("请选择：\n1 手动输入密钥\n2 选择密钥文件（需与程序文件同目录）\n3 使用默认测试密钥（0x00 - 0xff | 128bit）\n4 生成随机密钥\n其他内容 退出\n输入：")
        #start = '3'
        if(start == '1'):
            key = input("输入密钥：")
            if(len(key)>16):
                if(type(key)==(str)):
                    ascii_pattern = re.compile("\S+",re.ASCII)
                    key = ascii_pattern.match(key).string
                    if(len(key)==16):
                        key = key.encode()
                    else:
                        try:
                            key = bytes.fromhex(key)
                        except:
                            print("输入有误，请重新选择或输入~")
                            continue
            elif(len(key)==16):
                if(type(key)==(str)):
                    ascii_pattern = re.compile("\S+",re.ASCII)
                    key = ascii_pattern.match(key).string
                    key = key.encode()
            else:
                print("输入有误，请重新选择或输入~")
                continue
        elif(start == '2'):
            fileList = os.listdir(os.path.realpath(__file__)[0])
            i = 1
            for n in fileList:
                print(str(i)+' '+n)
                i += 1
            keyFile = input("输入文件编号：(0-返回最开始)")
            if(keyFile == "0"):
                continue
            with open(os.path.split(os.path.realpath(__file__))[0] + os.sep + fileList[int(keyFile) - 1],"rb") as kf:
                key = kf.read(16)
        elif(start == '3'):
            key = bytes.fromhex('00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f')
        elif(start == '4'):
            chk = input("生成随机密钥\n0 返回上一层\n1 存为文件（默认名称：aes.key）\n2 生成HEX值并复制到剪贴板\n3 存为hex文本文件（默认名称：aeskey.txt）\n其他内容 退出\n输入：")
            key = random.randbytes(16)
            if(chk == '0'):
                continue
            elif(chk == '1'):
                #1 存为文件（默认名称：aes.key）
                with open(os.path.split(os.path.realpath(__file__))[0] + os.sep + "aes.key","wb") as kf:
                    kf.write(key)
            elif(chk == '2'):
                #3 生成HEX值并复制到剪贴板
                pyperclip.copy(key.hex())
            elif(chk == '3'):
                #4 将HEX值存为文本文件（默认名称：aeskey.txt）
                with open(os.path.split(os.path.realpath(__file__))[0] + os.sep + "aeskey.txt","wb") as kf:
                    kf.write(key.hex())
            else:
                exit()
        else:
            exit()
        if(len(key)==16):
            (_Sbox,_Sbox_,_Kbox,_Kbox_,_Tbox,_Tbox_) = build_key(key)
            havekey = True
        else:
            print("输入有误，请重新选择或输入~")
            continue
    
    next = input("选择您要进行的操作：\n1 加密文件\n2 解密文件\n3 重新设定密钥\n其他内容 退出\n输入：")
    #next = "1"
    if(next == "1"):
        enFilename = "test.txt"#input("请输入要加密的文件名：")
        outputFilename = "test.bin"#input("请输入输出的文件名：")
        en(enFilename,outputFilename,_Sbox,_Kbox,_Tbox)
    elif(next == "2"):
        deFilename = "test.bin"#input("请输入要解密的文件名：")
        outputFilename = "decrypted_test.txt"#input("请输入输出的文件名：")
        de(deFilename,outputFilename,_Sbox_,_Kbox_,_Tbox_)
    elif(next == "3"):
        havekey = False
    else:
        exit()
