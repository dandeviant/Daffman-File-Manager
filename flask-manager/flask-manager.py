#!/usr/bin/env python3

#Python Flask File Manager

from flask import Flask, send_file, send_from_directory, redirect, url_for, render_template, request, render_template_string
from werkzeug.utils import secure_filename
import os
import subprocess
import hashlib
import shutil


app = Flask(__name__)
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
    return render_template("manager.html",
    current_dir = os.getcwd(), 
    files = subprocess.check_output('ls', shell=True).decode('utf-8').split('\n')
    )

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
    return render_template_string('''
    <a href="/cd?path=.."><strong>Go Back</strong></a> <br><br><br>
    ''') + subprocess.check_output('cat ' + request.args.get('file'), shell=True).decode('utf-8')

# handle cd command
@app.route('/md') # Flask decorator
def md():
    # run cd command
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