import os

os.chdir("uploads/daniel")
dir = os.getcwd()

x = dir.replace("/home/daniel/Desktop/Flask-file-manager/flask-manager/", "")
listdir = x.split("/")
print("X = " + x)

for x in range(len(listdir)):
    print("listdir " + str(x) + " = " + listdir[x]) 

curdir = os.path.join(os.getcwd(), '/uploads')
print(curdir)