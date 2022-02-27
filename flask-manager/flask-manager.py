#!/usr/bin/env python3

#Python Flask File Manager

from flask import Flask, redirect, url_for, render_template, request, render_template_string
import os
import subprocess

app = Flask(__name__)

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

# run HTTP server
if(__name__ == '__main__'):
    app.run(debug=True, threaded=True)