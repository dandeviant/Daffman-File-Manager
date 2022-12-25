#!/usr/bin/env python3

#Python Flask File Manager

from flask import Flask, send_file, session, send_from_directory, redirect, url_for, render_template, request, render_template_string, Response, escape, request
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from flaskext.markdown import Markdown
from array import *
import os
import subprocess
import hashlib
import shutil
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Dane@1710",
  database="flaskmanager"
)

dbcursor = db.cursor()

app = Flask(__name__)
app.secret_key = 'any random string'
Markdown(app)
Bootstrap(app)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

# @app.route('/', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != 'admin' or request.form['password'] != 'admin':
#             error = 'Invalid Credentials. Please try again.'
#         else:
#             return redirect(url_for('home'))
#     return render_template('login.html', error=error)

# handle root route


# Declaring global variables for messages
fileexist = False
filemissing = False
filesuccess = False
fileuploaded = ''
folderexist = False
foldermissing = False
foldersuccess = False
foldercreated = ''

rootpath = '/home/daniel/Desktop/Flask-file-manager/flask-manager/uploads'
rootfolder= 'uploads'

wrongcred = False
wrongpass = False

@app.route('/')
def base():
    # reset session
    session.clear()
    return redirect('/login')

# Flask decorator
@app.route('/login')
def login():
    #initiate login page 

    global wrongcred
    global wrongpass

    return render_template("login.html",
    wrongcred = wrongcred,
    wrongpass = wrongpass
    )

#check login creds
@app.route('/verifylogin', methods=['POST'])
def verifylogin():
    
    global wrongcred
    global wrongpass

    wrongcred = False
    username = request.form['username']
    inputpass = request.form['password']
    print("Entered name: " + username)
    
    
    query = 'select * from user where user_name="%s"; ' % (username)
    dbcursor.execute(query)
    account = dbcursor.fetchone()
    print("Account : " + str(account))
    if account:
        print("Account : " + str(account[1]))
        print("Password : " + str(account[2]))
        password = account[2]
        # session['password'] = password
        if inputpass != password:
            wrongcred = False
            wrongpass = True
            return redirect('/login')
        else:
            # print("Session user: " + session['username'])
            session['foldermissing'] = False

            session['username'] = account[1]
            print("Session username : " + session['username'])
            return redirect("/browser")
    else:
        wrongcred = True
        wrongpass = False
        print("No user found")
        return redirect('/login')


@app.route('/logout')
def logout():
    #initiate login page 

    global wrongcred
    global wrongpass
    wrongcred, wrongpass = False, False
    session.clear()
    
    return redirect("/login")


# for Home button, return to root folder 'uploads'
@app.route('/reset')
def reset():
    global rootpath
    os.chdir(rootpath)
    return redirect('/browser')

@app.route('/browser', methods=['GET', 'POST']) # Flask decorator
def index():
    # if session['username'] is None:
    #     return redirect(url_for('/logout'))

    global rootpath
    global rootfolder
    current_dir = os.getcwd()
    if rootfolder not in current_dir:
        os.chdir(rootpath)
    
    current_dir = os.getcwd()
    path = current_dir.replace("/home/daniel/Desktop/Flask-file-manager/flask-manager", ".")
    listdir = path.split("/")
    numdir = len(listdir)
    # for x in range(len(listdir)):

    # create tuple named file
    files = subprocess.check_output('ls', shell=True).decode('utf-8').split('\n')
    


    numfiles = 0
    for item in files[0: -1]:
        if '.' not in item:
            numfiles = numfiles
        else:
            numfiles += 1

    numfolder = 0
    for item in files[0: -1]:
        if '.' not in item:
            if item != '__pycache__' and item != 'static' and item != 'templates' :
                numfolder += 1
            else:
                numfolder = numfolder
        else:
            numfolder = numfolder
        

    # >>> array = [['h']*2] * 2
    # >>> print(array)
    # [['h', 'h'], ['h', 'h']]
    
    # use MySQL for hash checking

    query = "SELECT * FROM hash"
    dbcursor.execute(query)
    result = dbcursor.fetchall()
    # print("Result: ", end="")
    # print(result)
    # print("Files: ", end="")
    # print(files)
    notepath = '/home/daniel/Desktop/Flask-file-manager/README.md'
    note = subprocess.check_output(('cat ' + notepath), shell=True).decode('utf-8')


     # scan for md5 and file size of each file
    hash_list = []
    for item in files[0: -1]:
            if '.' in item:
                namefile = current_dir + '/' + item
                query = "select md5, filesize from hash where filename = '%s' ; " % (namefile)
                dbcursor.execute(query)
                result = dbcursor.fetchall()
                # print("Query result: ", end="")
                print("Result: " + str(result))
                for x in result:
                    # print(x[0])
                    hash = x[0]
                    filesize = x[1]
                hash_list.append((item, filesize, hash))
                # print("hash_list = ", end="")
                # print(hash_list)
    # assets = '../'            
    # picfolder = os.path.join(assets, 'folder.svg')
    picfolder = '/home/daniel/Desktop/Flask-file-manager/flask-manager/folder.svg'
    # svg = open(picfolder).read()

    global fileexist
    global filemissing
    global folderexist
    global foldermissing


    return render_template("manager.html",
    mimetype='image/svg+xml',
    current_dir = current_dir,
    path = path,
    files = files,
    note = note,
    numfiles = numfiles,
    numfolder = numfolder,
    hash_list = hash_list,
    numdir = numdir,
    listdir = listdir,
    # svg = svg,
    picfolder = picfolder,
    fileexist = fileexist,
    filemissing = filemissing,
    filesuccess = filesuccess,
    fileuploaded = fileuploaded,
    folderexist = folderexist,
    foldermissing = foldermissing,
    foldersuccess = foldersuccess,
    foldercreated = foldercreated,
    session = session
    )

# handle cd command
@app.route('/cd') # Flask decorator
def cd():
    global folderexist
    global foldermissing
    global foldersuccess
    global foldercreated
    global filemissing
    global fileexist
    global filesuccess
    fileexist = False
    filemissing = False
    filesuccess = False
    fileuploaded = ''
    folderexist = False
    foldermissing = False
    foldersuccess = False
    foldercreated = ''

    # run cd command
    os.chdir(request.args.get('path'))
    #redirect to file manager
    return redirect('/browser')



# handle cat command
@app.route('/view') # Flask decorator
def view():
    global folderexist
    global foldermissing
    global foldersuccess
    global foldercreated
    global filemissing
    global fileexist
    global filesuccess

    fileexist = False
    filemissing = False
    filesuccess = False
    fileuploaded = ''
    folderexist = False
    foldermissing = False
    foldersuccess = False
    foldercreated = ''
    
    if session['username']:
        return redirect('/logout')


    # return render_template_string('''
    # <a href="/"><strong>Go Back</strong></a> <br><br><br>
    # ''') + subprocess.check_output('cat ' + request.args.get('file'), shell=True).decode('utf-8')
    file = request.args.get('file')
    output = subprocess.check_output('more ' + request.args.get('file'), shell=True).decode('utf-8')
    filename = request.args.get('item')
    print("item: " + file)
    query = "SELECT md5 FROM hash WHERE filename = '%s' " % (file)
    dbcursor.execute(query)
    result = dbcursor.fetchone()
    rows = dbcursor.rowcount
    
    if rows == 0:
        hash = "No hash found" 
    else:
        for x in result:
            hash = '%s' % (x) 
            print(hash)


    
    return render_template('view.html',
    file = file,
    output = output,
    filename = filename,
    hash = hash
    )


# handle cd command
@app.route('/md') # Flask decorator
def md():

    global folderexist
    global foldermissing
    global foldersuccess
    global foldercreated
    global filemissing
    global fileexist
    global filesuccess

    filemissing = False
    fileexist = False
    filesuccess = False
    #get folder name from HTML form
    foldername = request.args.get('folder')

    #scan for all folders
    files = subprocess.check_output('ls', shell=True).decode('utf-8').split('\n')
    for item in files[0: -1]:
        if foldername == item:
            folderexist = True
            foldermissing = False
            foldersuccess = False
            return redirect('/browser')
        else:
            folderexist = False
    # run cd command
    if foldername != '':
        os.mkdir(request.args.get('folder'))
        foldermissing = False
        foldersuccess = True
        foldercreated = request.args.get('folder')
    else:
        foldermissing = True
        foldersuccess = False
    #redirect to file manager
    return redirect('/browser')


# download file from server
@app.route('/download', methods=['GET'])
def download():

    global folderexist
    global foldermissing
    global foldersuccess
    global foldercreated
    global filemissing
    global fileexist
    global filesuccess
    fileexist = False
    filemissing = False
    filesuccess = False
    fileuploaded = ''
    folderexist = False
    foldermissing = False
    foldersuccess = False
    foldercreated = ''

    if request.method == 'GET':
        print("")
    file = request.args.get('file')
    return send_file(file, as_attachment=True)

# upload files from filesystem
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():

    global filemissing
    global fileexist
    global filesuccess
    global fileuploaded
    global folderexist
    global foldermissing
    global foldersuccess

    folderexist = False
    foldermissing = False
    foldersuccess = False

    if request.method == 'POST':
        f = request.files['file']
        if f.filename == '':
            filemissing = True
            filesuccess = False
        else:
            filemissing = False
            filesuccess = True
            f.save(secure_filename(f.filename))
            dir = os.getcwd()
            file = "%s/%s" % (dir,f.filename)
            filestat = os.stat(f.filename)

            # print(f'File Size in MegaBytes is {file_stats.st_size / (1024 * 1024)}')

            
            hash = hashlib.md5(open(f.filename,'rb').read()).hexdigest()
            filesize = round(filestat.st_size / (1024), 1)
            roundedsize = str(filesize)
            print("\n\nUploaded File: " + file)
            print("File Size = " + roundedsize + "MB")
            print("Uploaded Hash: "+ hash)

            query = "select * from hash where filename='%s' and md5='%s'; " % (file, hash)
            dbcursor.execute(query)
            result = dbcursor.fetchall()
            rows = dbcursor.rowcount

            if rows == 0:
                query = "insert into hash(filename, md5, filesize) values ('%s', '%s', '%s')" % (file, hash, filesize)
                dbcursor.execute(query)
                db.commit()
                print("File uploaded")
                fileexist = False
                filesuccess = True
                fileuploaded = f.filename
            else:
                print("File already exists")
                fileexist = True
                filesuccess = False
                fileuploaded = ''


        return redirect('/browser')

#delete files from the server directory
@app.route('/delete', methods = ['GET'])
def delete_file():

    global folderexist
    global foldermissing
    global foldersuccess
    global foldercreated
    global filemissing
    global fileexist
    global filesuccess
    fileexist = False
    filemissing = False
    filesuccess = False
    fileuploaded = ''
    folderexist = False
    foldermissing = False
    foldersuccess = False
    foldercreated = ''
    file = request.args.get('file')
    query = "DELETE FROM hash WHERE filename='%s' " % (file)
    dbcursor.execute(query)
    db.commit()
    os.remove(file)
    return redirect('/browser')

@app.route('/delete_dir', methods = ['GET'])
def delete_dir():

    global folderexist
    global foldermissing
    global foldersuccess
    global foldercreated
    global filemissing
    global fileexist
    global filesuccess
    fileexist = False
    filemissing = False
    filesuccess = False
    fileuploaded = ''
    folderexist = False
    foldermissing = False
    foldersuccess = False
    foldercreated = ''
    dir = request.args.get('dir')
    content = os.listdir(dir)
    if len(content) == 0:
        os.rmdir(dir)
    else:
        shutil.rmtree(dir, ignore_errors=True)
    #redirect to file manager
    return redirect('/browser')

@app.route('/profile')
def profile():
    return render_template("profile.html")


# ====================================================================
# ====================================================================

# run HTTP server
if(__name__ == '__main__'):
    app.run(debug=True, threaded=True)