import numpy as np
from tqdm import tqdm

def mod(p,num):
    return chr((getord(p)+num)%26 + 97)

def getord(c):
    return ord(c.lower())-97

def getchr(c):
    return chr(c%26+97)

limit = "abcdefghijklmnopqrstuvwxyz"
key = "ohmygodthatisinteresting"
c = ""
keycode = []
j_max = len(key)
for i in range(j_max):
    keycode.append(getord(key[i].lower()))
j = 0
with open ("sea.txt","r",encoding="utf8") as txt:
    for line in tqdm(txt):
        for i in line:
            if i in limit:
                c += mod(i.lower(),keycode[j])
                j += 1
                if(j == j_max):
                    j=0

with open("out2.txt","w+",encoding="utf8") as txtout:
    txtout.write(c)