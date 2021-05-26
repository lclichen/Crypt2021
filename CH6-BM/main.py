from tqdm import tqdm
import time

class BM():
    def __init__(self,data):
        self.data = data
        self.TD = []
        self.CD = [1]
        self.L = 0
        self.m = 0
        self.BD = [1]
        self.j = 0
        self.CN = len(self.CD)
        self.N = len(data)
        print(self.N)
    def round2(self):# 计算离差，如果无偏差就到下一位，有偏差就对数据再进行处理。
        self.d = int(data[self.j])
        self.m += 1
        if(self.L == 0):
            return
        for i in range(1,self.L+1):
            #print(i,self.j,self.d)
            self.d ^= (int(data[self.j - i]) * self.CD[i] ) # mod 2
        #print(self.d)
    #def round3(self):
    #    self.m += 1
    def round4(self):
        if(self.d != 0):
            self.TD = self.CD.copy()
            for i in range(len(self.BD)):
                if(self.CN-1 < i + self.m):
                    #print(self.CD)
                    for j in range(self.CN,i + self.m):
                        self.CD.append(0)
                    #print(self.CD)
                    self.CD.append(0 ^ self.BD[i])
                    self.CN = len(self.CD)
                    #print(self.CD)
                else:
                    self.CD[i+self.m] ^= self.BD[i] #CD长度足够，直接异或，长度不足，末尾续0
            #if(self.L * 2 <= self.j ):
            if(self.L <= self.j/2 ):
                self.L = self.j + 1 - self.L
                self.BD = self.TD
                self.m = 0
        #print(self.j, self.data[self.j], self.d, self.m, self.TD, self.CD, self.L, self.BD)
    #def round5(self):
        self.j += 1
    def cal(self):
        pbar = tqdm(total=self.N)
        time_start = time.time()
        #print("\nj s d m TD CD L BD")
        while(self.j < self.N):
            self.round2()
            #self.round3()
            self.round4()
            #print(self.j,self.d,self.m,self.CD,self.L,self.BD)
            #self.round5()
            pbar.update(1)
        time_end = time.time()
        pbar.close()
        print('Time cost',time_end-time_start,'s')
        return(self.L,self.CD)

choice = 1
if(choice == 0):
    testdata = "0011011111111111111111000001010101001111010"
    #testdata = "1001101001101"
    #testdata = "001101110"
    #testdata = "00101101"
    #testdata = "10101111"
    data = testdata
    print(data)
else:
    testfile = "test.bin"
    binfile = "encrypted_sea.bin"

    pos = 96995
    with open(binfile,"rb") as fin:
        fin.seek(pos) #随机偏移
        bindata = fin.read(250)
    datastr = bin(int(bindata.hex(), 16))[2:]

    data = []

    if(len(datastr) % 8 > 0):
        for i in range(8-len(datastr) % 8 ):
            data.append(0)
    for i in datastr:
        data.append(int(i))
    datastr = ''

cal = BM(data)
L,CD = cal.cal()
print("线性复杂度为"+str(L))
outtext = "The LFSR = <"+str(L)+", 1"
if len(CD) == 1:
    outtext += ">"
    print(outtext)
    exit()
for i in range(1,len(CD)):
    if(CD[i]):
        outtext += "+D"+str(i)
outtext += ">"
if(L<=20):
    print(outtext)
with open("LFSR.txt","w",encoding="ASCII") as fout:
    fout.write(outtext)