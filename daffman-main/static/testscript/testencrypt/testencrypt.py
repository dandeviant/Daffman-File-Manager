import pyAesCrypt

inputfile = "encryptme.txt"
outputfile = "encryptme.txt.aes"
decryptfile = "iamdecrypted.txt"

password = "a really long password"

pyAesCrypt.encryptFile(inputfile, outputfile, password)

pyAesCrypt.decryptFile(outputfile, decryptfile, password)

