import hashlib

# def getmd5(filename):
#     return m.hexdigest()

file = "/home/daniel/Desktop/Flask-file-manager/flask-manager/readme.txt"

output = hashlib.md5(open(file,'rb').read()).hexdigest()
print("File Name : " + file)
print("Hash: " + output)