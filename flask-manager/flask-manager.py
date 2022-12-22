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
@app.route('/')
def base():
    return redirect('/browser')

@app.route('/browser') # Flask decorator
def index():
    rootpath = '/home/daniel/Desktop/Flask-file-manager/flask-manager/uploads'
    current_dir = os.getcwd()
    if current_dir == '/home/daniel/Desktop/Flask-file-manager/flask-manager':
        os.chdir(rootpath)
    
    current_dir = os.getcwd()
    path = current_dir.replace("/home/daniel/Desktop/Flask-file-manager/flask-manager", ".")
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


     # scan for md5 of each file
    hash_list = []
    for item in files[0: -1]:
            if '.' in item:
                namefile = current_dir + '/' + item
                query = "select md5 from hash where filename = '%s' ; " % (namefile)
                dbcursor.execute(query)
                result = dbcursor.fetchall()
                # print("Query result: ", end="")
                for x in result:
                    # print(x[0])
                    hash = x[0]
                hash_list.append((item, hash))
                # print("hash_list = ", end="")
                # print(hash_list)



    return render_template("manager.html",
    current_dir = current_dir,
    path = path,
    files = files,
    note = note,
    numfiles = numfiles,
    numfolder = numfolder,
    hash_list = hash_list
    )
    

# handle cd command
@app.route('/cd') # Flask decorator
def cd():
    # run cd command
    os.chdir(request.args.get('path'))
    #redirect to file manager
    return redirect('/browser')



# handle cat command
@app.route('/view') # Flask decorator
def view():
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
    # run cd command
    foldername = request.args.get('folder')
    if foldername != '':
        os.mkdir(request.args.get('folder'))
    #redirect to file manager
    return redirect('/browser')


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
    error = True
    if request.method == 'POST':
        f = request.files['file']
        if f.filename == '':
            pass
        else:
            f.save(secure_filename(f.filename))
            dir = os.getcwd()
            file = "%s/%s" % (dir,f.filename)
            hash = hashlib.md5(open(f.filename,'rb').read()).hexdigest()
            query = "select * from hash where filename='%s' and md5='%s'; " % (file, hash)
            print("\n\nUploaded File: " + file)
            print("Uploaded Hash: "+ hash) 
            dbcursor.execute(query)
            result = dbcursor.fetchall()
            rows = dbcursor.rowcount

            if rows == 0:
                query = "insert into hash(filename, md5) values ('%s', '%s')" % (file, hash)
                dbcursor.execute(query)
                db.commit()
                print("File uploaded")
            else:
                print("File already exists")

        return redirect('/browser')

#delete files from the server directory
@app.route('/delete', methods = ['GET'])
def delete_file():
    file = request.args.get('file')
    query = "DELETE FROM hash WHERE filename='%s' " % (file)
    dbcursor.execute(query)
    db.commit()
    os.remove(file)

    return redirect('/browser')

@app.route('/delete_dir', methods = ['GET'])
def delete_dir():
    dir = request.args.get('dir')
    content = os.listdir(dir)
    if len(content) == 0:
        os.rmdir(dir)
    else:
        shutil.rmtree(dir, ignore_errors=True)
    #redirect to file manager
    return redirect('/browser')

# ====================================================================
# ====================================================================

# run HTTP server
if(__name__ == '__main__'):
    app.run(debug=True, threaded=True)