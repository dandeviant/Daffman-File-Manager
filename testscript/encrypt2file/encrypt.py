# This test script will encrypt 2 files with same contents, same password, different filename
# Compare the resulting hash and report it.

# result discussion:

# 1. for file with different filename, same password, same content,
# no matter how many times you encrypt, each encryption will giveout different result hash.
# Same goes to same filenames, same password, same contents. 




# ===================================================================================================


import pyAesCrypt
import hashlib


inputfile = 'readme.txt'

# outputfile1 = 'file1/readme1.txt.aes'
# outputfile2 = 'file2/readme1.txt.aes'

outputfile1 = 'readme1.txt.aes'
# outputfile2 = 'readme2.txt.aes'
password = 'readme'


pyAesCrypt.encryptFile(inputfile, outputfile1, password)
# pyAesCrypt.encryptFile(inputfile, outputfile2, password)

hashoutput1 = hashlib.md5(open(outputfile1,'rb').read()).hexdigest()
# hashoutput2 = hashlib.md5(open(outputfile2,'rb').read()).hexdigest()

print(" md5 file %s : %s " %(outputfile1, hashoutput1))
# print(" md5 file %s : %s " %(outputfile2, hashoutput2))



