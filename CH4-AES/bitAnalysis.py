def anylsis(filename,n):
    if(n == 1):
        count = {"0":0,"1":0}
        with open(filename,"rb") as fbin:
            while(1):
                data = fbin.read(1)
                if(data):
                    bitdata = int(data.hex(),16)
                    #print(bin(bitdata)[2:])
                    for i in range(8):
                        if(bitdata & (0x80>>i)):
                            tmp = "1"
                        else:
                            tmp = "0"
                        count[tmp] += 1
                else:
                    break
            print(count)
    elif(n >= 2):
        count = {}
        first = 1
        for i in range(pow(2,n)):
            count[format(i, '0'+str(n)+'b')] = 0
        flag = []            
        with open(filename,"rb") as fbin:
            while(1):
                data = fbin.read(1)
                if(data):
                    bitdata = int(data.hex(),16)
                    #print(bin(bitdata)[2:])
                    
                    for i in range(8):
                        if(bitdata & (0x80>>i)):
                            tmp = "1"
                        else:
                            tmp = "0"
                        if(first == 1):
                            flag.append(tmp)
                            if(len(flag) == n-1):
                                first = 0
                            continue
                        stmp = "".join(flag)+tmp
                        count[stmp] += 1
                        flag.pop(0)
                        flag.append(tmp)
                else:
                    break
            print(count)
print("未加密：")
for i in range(1,5):
    anylsis("decrypted_sea.txt",i)
print("加密后：")
for i in range(1,5):
    anylsis("encrypted_sea.bin",i)
