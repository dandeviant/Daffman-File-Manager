import hashlib

file = "readme2.txt"

hashoutput = hashlib.md5(open(file,'rb').read()).hexdigest()
print(" md5 file %s : %s " %(file, hashoutput))

