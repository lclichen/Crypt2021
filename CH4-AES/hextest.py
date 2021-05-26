from re import ASCII
import numpy as np
import hashlib,os,random
key = random.randbytes(16)
k = ''
for i in range(16):
    x = random.randint(32,255)
    print(x,chr(x),ord(chr(x)))
    if x == 127:
        print("111")
        continue
    k += chr(x)
print(k)
print((key).hex())
print([chr(i) for i in key])
exit()
'''
for i in range(9,0,-1):
    print(i)
'''
'''
c = b'\x0e'
cutnum = int.from_bytes(c,byteorder='big')
print(cutnum)
'''
'''
Mt = np.array(((0x0E, 0x09, 0x0D, 0x0B),(0x0B, 0x0E, 0x09, 0x0D),(0x0D, 0x0B, 0x0E, 0x09),(0x09, 0x0D, 0x0B, 0x0E)),dtype=np.ubyte).T
print(Mt)
with open(os.path.split(os.path.realpath(__file__))[0] + os.sep +"testcipher.txt","rb") as fp:
    b = fp.read()
    print([hex(i) for i in b])
    #print(b)
exit()
'''
'''
key = bytearray("ei3^dfie(&^%kshd",encoding="ASCII")
for i in key:
    print(hex(i))

a = 4
b = 0b10010101
c = 0x95

print(hex(b))
result = ((c << a & 0xff) | (c >> (8-a)))
print(bin(result))
exit()
'''
'''
with open(os.path.split(os.path.realpath(__file__))[0] + os.sep +"out.txt","rb") as fp:
    b = fp.read()
    print([hex(i) for i in b])
    #print(b)
exit()
'''
'''
with open(os.path.split(os.path.realpath(__file__))[0] + os.sep +"test.txt","wb") as fp:
    b = bytes.fromhex('00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff')
    fp.write(b)
exit()
'''
'''
a = "abcdefghijklmn"
for i in range(4):
    print(a[i:i+4])
x = b'aaa'
print(type(x)==(str))
'''
'''
M_t0 = np.array((0x02,0x01,0x01,0x03),dtype=np.ubyte)
M_t1 = np.append(M_t0[3].copy(),M_t0[0:3].copy())
M_t2 = np.append(M_t1[3].copy(),M_t1[0:3].copy())
M_t3 = np.append(M_t2[3].copy(),M_t2[0:3].copy())
print(M_t0,M_t1,M_t2,M_t3)
exit()
''
with open(os.path.split(os.path.realpath(__file__))[0] + os.sep +"keys/Sboxin.npy","rb") as Sbox:
    Sin = np.load(Sbox)
for i in range(0x10):
    print([hex(Sin[i][j]) for j in range(0x10)])
exit()
''
for i in range(1):
    for j in range(16):
        print(int(T[i][j][0]),(T[i][j][1]),(T[i][j][2]),(T[i][j][3]))
exit()
'''
with open(os.path.split(os.path.realpath(__file__))[0] + os.sep +"keys/11a535d23a5aa23d22f8a025ad4253c6_T.npy","rb") as Tbox:
    T = np.load(Tbox)
for i in range(1,2):
    for j in range(47,48):
        print([(T[i][j][0]),(T[i][j][1]),(T[i][j][2]),(T[i][j][3])])
exit()
t0 = T[0].copy()
t1 = T[1].copy()
t2 = T[2].copy()
t3 = T[3].copy()
print(t0[0:4])
print(t1[0:4])
print(t2[0:4])
print(t3[0:4])


'''
with open(os.path.split(os.path.realpath(__file__))[0] + os.sep +"keys/Sboxin_.npy","rb") as Sin:
    S_in = np.load(Sin)
print(hex(S_in[0x00]))
exit()
'''
for k in range(9,0,-1):
    print(k)

data = b'assdsgdsasd'
data += ((b'0'*(15-len(data)))+bytes(chr(16-len(data)),encoding='ASCII'))

print(data)
print((data[15]))

exit()
for i in range(1,9):
    print(i)
def SimpleCal(x1,x2):
    value = 0
    for i in range(32):
        if(x1 & (1<<i)):
            value = value ^ (x2<<i)
    return value
# 求最高幂次数
def Nonzero_MSB(value):
    v2str = '{:09b}'.format(value)
    for i in range(9):
        if int(v2str[i]):
            return 9-i
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
#a=0x10
#b = 0xF0
#print(bin(a),bin(b),bin(a^b))

#key = """ei3^dfie(&^%kshd"""
#hashKey = hashlib.shake_256(key.encode()).hexdigest(16)
#print(hashKey)
print(bin(SimpleCal(0b111, 0b101)))
print(bin(Mode2_div(0b11011, 0b1011)[1]))
exit()
w = np.zeros([4,44])
print(w)
Rc = np.array((0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36),dtype="ubyte")
print(Rc)
Rcon = np.zeros([4,10],dtype=np.ubyte)
Rcon[0][...] = Rc
print(Rcon)
for j in range(10):
    print(Rcon[...,(j+1):(j+2)])
'''
# 将字符串转为16进制ascii码 format "02X"表示16进制大写两位0填充空位 最开始使用hex无法填充空位
def convert_hex(string):
    result = "".join([format(ord(i), "02X") for i in string])
    return result
# 16进制ascii码转为str 
def convert_str(string):
    result = "".join([chr(int(i, 16)) for i in string])
    return result
print(convert_hex(''))
'''