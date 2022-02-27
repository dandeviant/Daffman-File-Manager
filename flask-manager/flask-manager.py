#Python Flask File Manager

from flask import Flask, redirect, url_for, render_template, request
#!/usr/bin/env python3

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

# run HTTP server
if(__name__ == '__main__'):
    app.run(debug=True, threaded=True)