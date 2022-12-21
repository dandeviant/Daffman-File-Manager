#!/usr/bin/env python3

#Python Flask File Manager

from flask import Flask, send_file, send_from_directory, redirect, url_for, render_template, request, render_template_string
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
Markdown(app)
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
@app.route('/') # Flask decorator
def index():
    current_dir = os.getcwd()
    path = current_dir.replace("/home/daniel/Desktop/Flask-file-manager/flask-manager", ".")
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
    
    arrayhash = [['h'] * 2] * numfiles
    x = 0
    for item in files[0: -1]:
        if '.' not in item:
            x = x
        else:
            # col 1 is item, col 2 is hash, x is files
            hash = hashlib.md5(open(item,'rb').read()).hexdigest()
            print(item)
            arrayhash[x][0] = item
            arrayhash[x][1] = hash
            print(hash)
            x += 1
            # use MySQL for hash checking


    notepath = '/home/daniel/Desktop/Flask-file-manager/README.md'
    note = subprocess.check_output(('cat ' + notepath), shell=True).decode('utf-8')
    return render_template("manager.html",
    current_dir = current_dir,
    path = path,
    files = files,
    note = note,
    numfiles = numfiles,
    numfolder = numfolder,
    arrayhash = arrayhash
    )
    

# def hash(files):
#     for item in files:
#         print("")

# handle cd command
@app.route('/cd') # Flask decorator
def cd():
    # run cd command
    os.chdir(request.args.get('path'))
    #redirect to file manager
    return redirect('/')



# handle cat command
@app.route('/view') # Flask decorator
def view():
    # return render_template_string('''
    # <a href="/"><strong>Go Back</strong></a> <br><br><br>
    # ''') + subprocess.check_output('cat ' + request.args.get('file'), shell=True).decode('utf-8')
    file = request.args.get('file')
    output = subprocess.check_output('more ' + request.args.get('file'), shell=True).decode('utf-8')
    filename = request.args.get('item')
    query = 'SELECT md5 FROM hash WHERE filename = %s '

    dbcursor.execute(query, [filename])
    result = dbcursor.fetchall()
    rows = dbcursor.rowcount
    
    if rows == 0:
        hash = "No hash found" 
    else:
        for x in result:
            hash = '%s' % (x) 
            print(hash)
    # filehash = hashlib.md5(open(file,'rb').read()).hexdigest()


    
    return render_template('view.html',
    file = file,
    output = output,
    filename = filename,
    hash = hash
    )


# handle cd command
@app.route('/md') # Flask decorator
def md():
    # run cd command
    foldername = request.args.get('folder')
    if foldername != '':
        os.mkdir(request.args.get('folder'))
    #redirect to file manager
    return redirect('/')


# download file from server
@app.route('/download', methods=['GET'])
def download():
    if request.method == 'GET':
        print("")
    file = request.args.get('file')
    return send_file(file, as_attachment=True)

# upload files from filesystem
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if f.filename == '':
            pass
        else:
            f.save(secure_filename(f.filename))
        return redirect('/')

#delete files from the server directory
@app.route('/delete', methods = ['GET'])
def delete_file():
    file = request.args.get('file')
    os.remove(file)
    return redirect('/')

@app.route('/delete_dir', methods = ['GET'])
def delete_dir():
    dir = request.args.get('dir')
    content = os.listdir(dir)
    if len(content) == 0:
        os.rmdir(dir)
    else:
        shutil.rmtree(dir, ignore_errors=True)
    #redirect to file manager
    return redirect('/')

# ====================================================================
# ====================================================================

# run HTTP server
if(__name__ == '__main__'):
    app.run(debug=True, threaded=True)