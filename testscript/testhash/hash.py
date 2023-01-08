import hashlib

# def getmd5(filename):
#     return m.hexdigest()

# file = "/home/daniel/Desktop/daffman/testscript/testhash/encryptme.txt"
file = "/home/daniel/Desktop/readme.txt"

output = hashlib.md5(open(file,'rb').read()).hexdigest()
print("File Name : " + file)
print("Hash: " + output)