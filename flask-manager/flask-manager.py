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
import pyAesCrypt

db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dane@1710",
        database="flaskmanager"
    )
dbcursor = db.cursor(buffered=True)

here = os.getcwd()


static_url_path='sa',
app = Flask(__name__,
static_folder = here + '/static'
)

app.secret_key = 'any random string'
Markdown(app)
Bootstrap(app)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

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
forbidpath = '/home/daniel/Desktop/Flask-file-manager/flask-manager'
rootfolder= 'uploads'

os.chdir(rootpath)

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
    session['editpermit'] = False

    return render_template("login.html",
    wrongcred = wrongcred,
    wrongpass = wrongpass
    )

#check login creds
@app.route('/verifylogin', methods=['POST'])
def verifylogin():
    print("============================== VERIFYLOGIN ==============================")
    global wrongcred
    global wrongpass
    
    wrongcred = False
    username = request.form['username']
    rawinputpass = request.form['password']
    session['rawpass'] = rawinputpass
    hashinputpass = hashlib.sha256(rawinputpass.encode('utf-8')).hexdigest()
    print("Entered name: " + username)
    print("Input pass: " + rawinputpass)
    print("Input pass hash: " + hashinputpass)
    
    query = 'select * from user where user_name="%s"; ' % (username)
    print("Login query: " + query)
    dbcursor.execute(query)
    account = dbcursor.fetchone()
    print("Account list: " + str(account))
    if account:
        print("Account : " + str(account[1]))
        print("Password : " + str(account[2]))
        password = account[2]

        # use sha256 to hash the input password and compare the hash



        # session['password'] = password
        if hashinputpass != password:
            session['wrongcred'] = False
            session['wrongpass'] = True
            return redirect('/login')
        else:
            # print("Session user: " + session['username'])
            session['foldermissing'] = False
            session['username'] = account[1]
            session['password'] = account[2]
            session['fullname'] = account[3]
            print("Session username : " + session['username'])
            if session['username'] == "admin":
                session['admin'] = True
            else:
                session['admin'] = False
                session['editpermit'] = False
            os.chdir(rootpath)
            print("Check editpermit: " + str(session['editpermit']))
            return redirect("/browser")
    else:
        session['wrongcred'] = True
        session['wrongpass'] = False
        print("No user found")
        print("Check editpermit: " + str(session['editpermit']))
        return redirect('/login')


@app.route('/logout')
def logout():
    #initiate login page 

    global wrongcred
    global wrongpass
    global fileexist
    global filemissing
    global filesuccess
    global folderexist
    global foldermissing
    global foldersuccess
    
    wrongcred, wrongpass = False, False
    fileexist = False
    filemissing = False
    filesuccess = False
    folderexist = False
    foldermissing = False
    foldersuccess = False

    session.clear()
    return redirect("/")


# for Home button, return to root folder 'uploads'
@app.route('/reset')
def reset():
    global rootpath
    os.chdir(rootpath)
    return redirect('/browser')

@app.route('/browser', methods=['GET', 'POST']) # Flask decorator
def index(downloadpass = True):
    print("============================== FILE BROWSER INDEX ==============================")
    # if session['username'] is None:
    #     return redirect(url_for('/logout'))

    global rootpath
    global forbidpath
    global rootfolder
    current_dir = os.getcwd()
    if rootfolder not in current_dir:
        os.chdir(rootpath)

    session['downloadpass'] = downloadpass

    query = "select user_id from user where user_name = '%s'; " % (session['username'])
    print("Query : " + query)
    dbcursor.execute(query)
    result = dbcursor.fetchone()
    session['user_id'] = result[0]
    print("Result          : " + str(result))
    print("Current User ID : " + str(session['user_id']))

    filequery = "select * from hash; "
    print("File Query : " + filequery)
    dbcursor.execute(filequery)
    resultfile = dbcursor.fetchall()
    numfiles = dbcursor.rowcount
    session['numfileowned'] = numfiles
    print("======================================")
    print("File Result : " + str(resultfile))
    print("======================================")
    print("No. of File Owned by %s : %s" % (session['username'], str(session['numfileowned'])))


    # session['editpermit'] = True
    current_dir = os.getcwd()
    compare = rootfolder + "/" + session['username']
    print("Compare : " + compare)
    usercd = session['username']
    print("Dir : " + current_dir)
    print("Usercd : " + usercd) 


    if session['username'] == "admin":
        session['admin'] = True
    else:
        session['admin'] = False

    if session['admin'] == False:
        if compare not in current_dir:
            print("Upload not allowed")
            session['folderpermit'] = False
        else:
            session['editpermit'] = True
    else:
        session['editpermit'] = True



    print("Browser session: " + session['username'])
    path = current_dir.replace(forbidpath, ".")
    listdir = path.split("/")
    numdir = len(listdir)
    # for x in range(len(listdir)):

    # create tuple named file
    files = subprocess.check_output('ls', shell=True).decode('utf-8').split('\n')
    print("Files = " + str(files))


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
    print("Files = ", end="")
    print(files)
    notepath = '/home/daniel/Desktop/Flask-file-manager/README.md'
    note = subprocess.check_output(('cat ' + notepath), shell=True).decode('utf-8')


     # scan for md5 and file size of each file
    hash_list = []
    for item in files[0: -1]:
            if '.' in item:
                namefile = current_dir + '/' + item
                query = "select md5, filesize, user_id from hash where filename = '%s' ; " % (namefile)
                dbcursor.execute(query)
                result = dbcursor.fetchall()
                # print("Query result: ", end="")
                print("Result: " + str(result))
                for x in result:
                    # print(x[0])
                    hash = x[0]
                    filesize = x[1]
                    owner_id = x[2]
                    ownerquery = "select user_name from user where user_id = %s;" % (owner_id)
                    dbcursor.execute(ownerquery)
                    ownerresult = dbcursor.fetchone()
                    owner_name = str(ownerresult[0])
                    print("Owner Name: " + str(owner_name))
                hash_list.append((item, filesize, hash, owner_name))
                # print("hash_list = ", end="")
                # print(hash_list)
    # assets = '../'            

    global fileexist
    global filemissing
    global folderexist
    global foldermissing

    print("Check editpermit: " + str(session['editpermit']))
    return render_template("manager.html",
    rootpath = rootpath,
    forbidpath = forbidpath,
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
    folderexist = False
    foldermissing = False
    foldersuccess = False   


    session['editpermit'] = False
    target_dir = request.args.get('path')
    print("Target dir: " + target_dir)

    os.chdir(request.args.get('path'))

    current_dir = request.args.get('path')
    compare = rootfolder + "/" + session['username']
    print("Compare : " + compare)
    usercd = session['username']
    print("Requested Dir : " + current_dir)
    print("Usercd : " + usercd)

    # if session['username'] == "admin":
    #     session['admin'] = True
    # else:
    #     session['admin'] = False

    if session['admin'] == False:
        if compare not in current_dir:
            print("Upload not allowed")
            session['editpermit'] = False
        else:
            session['editpermit'] = True
    else:
        session['editpermit'] = True

    print("Check editpermit: " + str(session['editpermit']))

    # run cd command
    
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

    current_dir = os.getcwd()
    compare = rootfolder + "/" + session['username']
    print("Compare : " + compare)
    usercd = session['username']
    print("Dir : " + current_dir)
    print("Usercd : " + usercd)

    if session['username'] == "admin":
        session['admin'] = True
    else:
        session['admin'] = False

    if session['admin'] == False:
        if compare not in current_dir:
            print("Upload not allowed")
            session['editpermit'] = False
        else:
            session['editpermit'] = True
    else:
        session['editpermit'] = True
        print("resultcheck : " + str(session['editpermit']))


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
@app.route('/download', methods=['POST','GET'])
def download():
    print("============================== DOWNLOAD FILE ==============================")
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

    file = request.form['downloadfile']
    inputpass = request.form['password']
    hashinputpass = hashlib.sha256(inputpass.encode('utf-8')).hexdigest()
    print("file: " + file)
    hashquery = "select * from hash where filename like '%"+file+"%' ;"
    print("hashquery: " + hashquery)
    dbcursor.execute(hashquery)
    hashresult = dbcursor.fetchone()
    filename = str(hashresult[0])
    actualpass = str(hashresult[1])
    ownerid = str(hashresult[3])

    userquery = "select * from user where user_id='%s'; " % (ownerid)
    print("userquery: " + userquery)
    dbcursor.execute(userquery)
    userresult = dbcursor.fetchone()
    print("User Result         : " + str(userresult))
    ownerusername = userresult[1]
    ownerpasshash = userresult[2]
    
    print("Hash Result         : " + str(hashresult))
    print("Download File       : " + filename)
    print("File Owner ID       : " + ownerid)
    print("File Owner username : " + ownerusername)
    print("Input Password      : " + inputpass)
    print("Input Password Hash : " + hashinputpass)
    print("Actual Password Hash: " + ownerpasshash)


    if hashinputpass == ownerpasshash:
        print("Password Match      : True")
        session['downloadpass'] = True
        return send_file(filename, as_attachment=True)
    else:
        print("Password Match      : False")
        session['downloadpass'] = False
        return index(session['downloadpass'])

    
# upload files from filesystem
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    print("\n============================== UPLOAD FILE ==============================")

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

    session['editpermit'] = True

    current_dir = os.getcwd()
    compare = rootfolder + "/" + session['username']
    print("Compare : " + compare)
    usercd = session['username']
    print("Dir : " + current_dir)
    print("Usercd : " + usercd)

    # if session['username'] == "admin":
    #     session['admin'] = True
    # else:
    #     session['admin'] = False

    # if session['admin'] == False:
    #     if compare not in current_dir:
    #         print("Upload not allowed")
    #         session['editpermit'] = False
    #         return redirect('/browser')
    #     else:
    #         session['editpermit'] = True
    # else:
    #     session['editpermit'] = True
    
    # print("resultcheck : " + str(session['editpermit']))

        
    if request.method == 'POST':
        f = request.files['file']
        if f.filename == '':
            filemissing = True
            filesuccess = False
        else:
            filemissing = False
            filesuccess = True
            f.save(secure_filename(f.filename))
            print("Save successful")
            print("File saved : " + f.filename)
            if ' ' in f.filename:
                print("Whitespace detected")
                f.filename = f.filename.replace(" ", '_')
                print("Whitespace replaced with underscore")
                print("New name : " + f.filename)
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

            # Get user id for db update
            query = "select user_id from user where user_name = '%s'; " % (session['username'])
            print("Query: " + query)
            dbcursor.execute(query)
            result = dbcursor.fetchone()
            print("Result: " + str(result))
            user_id = result[0]
            password = session['password']
            print('User ID: ' + str(result[0]))
            print('User Password: ' + password)

            query = "select * from hash where filename='%s' and md5='%s'; " % (file, hash)
            print("Query: " + query)
            dbcursor.execute(query)
            result = dbcursor.fetchall()
            rows = dbcursor.rowcount

            if rows == 0:

                # AES encryption process
                inputfile = file
                outputfile = file + ".aes"
                encodedpass = password.encode('utf-8')
                hashedpass = hashlib.sha256(encodedpass)
                print("Input file : " + inputfile)
                print("Output file: " + outputfile)
                print("File Password Unhashed: " + password)
                print("File Password Hashed: " + str(hashedpass.hexdigest()))
                
                pyAesCrypt.encryptFile(inputfile, outputfile, password)
                
                query = "insert into hash(filename, md5, filesize, user_id) values ('%s', '%s', '%s', %d)" % (outputfile, hash, filesize, user_id)
                dbcursor.execute(query)
                db.commit()
                os.remove(file)
                print("File uploaded")
                fileexist = False
                filesuccess = True
                fileuploaded = f.filename+'.aes'

            else:
                print("File already exists")
                fileexist = True
                filesuccess = False
                fileuploaded = ''
    return redirect('/browser')


@app.route('/startupload', methods=['GET'])
def startupload():
    print("============================== NEW UPLOAD ==============================")

    # os.chdir(rootpath + "/daniel/testdaniel")
    current_dir = os.getcwd()
    path = current_dir.replace(forbidpath, ".")
    listdir = path.split("/")
    numdir = len(listdir)
    # for x in range(len(listdir)):

    # create tuple named file
    files = subprocess.check_output('ls', shell=True).decode('utf-8').split('\n')
    return render_template('upload.html',
        listdir = listdir,
        numdir = numdir,
        current_dir = current_dir
    )

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

    session['deletepermit'] = True

    current_dir = os.getcwd()
    compare = rootfolder + "/" + session['username']
    print("Compare : " + compare)
    usercd = session['username']
    print("Dir : " + current_dir)
    print("Usercd : " + usercd)
    if session['username'] == "admin":
        session['admin'] = True
    if session['admin'] == False:
        if compare not in current_dir:
            print("Delete not allowed")
            session['editpermit'] = False
            return redirect('/browser')
        else:
            session['editpermit'] = True
    

    print("resultcheck : " + str(session['deletepermit']))
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

    current_dir = os.getcwd()
    compare = rootfolder + "/" + session['username']
    print("Compare : " + compare)
    usercd = session['username']
    print("Dir : " + current_dir)
    print("Usercd : " + usercd)
    if session['username'] == "admin":
        session['admin'] = True
    if session['admin'] == False:
        if compare not in current_dir:
            print("Delete not allowed")
            session['editpermit'] = False
            return redirect('/browser')
        else:
            session['editpermit'] = True
    

    print("resultcheck : " + str(session['editpermit']))


    dir = request.args.get('dir')
    content = os.listdir(dir)
    if len(content) == 0:
        os.rmdir(dir)
    else:
        shutil.rmtree(dir, ignore_errors=True)
    #redirect to file manager
    return redirect('/browser')


@app.route('/adminstart')
def adminstart():
    session['nousername'] = False
    session['passmatch'] = False
    session['matchadminpass'] = False
    session['blankadminpass'] = False
    session['newadminpass'] = False
    session['sameadminhash'] = False
    return redirect("/admin")

@app.route('/admin')
def admin():
    print("===================== ADMIN =====================")
    queryadmin = "select password from user where user_id='1' "
    dbcursor.execute(queryadmin)
    result = dbcursor.fetchall()
    resultpass = str(result[0])
    password = resultpass.encode('utf-8')
    hashedpass = hashlib.sha256(password).hexdigest()
    print("Hashed Password : " + hashedpass)


    query = "select * from user;"
    dbcursor.execute(query)
    result = dbcursor.fetchall()
    return render_template("admin.html", result=result, resultpass=resultpass, hashedpass = hashedpass)


@app.route('/changepassadmin', methods=['POST'])
def changepassadmin():
    print("\n============================== CHANGE PASSWORD ADMIN ==============================")
    newadminpass = request.form['newadminpass']
    passmatch = request.form['passmatch']
    
    if newadminpass == '' and passmatch == '':
        session['matchadminpass'] = False
        session['blankadminpass'] = True
        session['newadminpass'] = False
        session['sameadminhash'] = False
        print("session['blankadminpass'] = " + str(session['blankadminpass']))
        print("session['newadminpass']   = " + str(session['newadminpass']))
        print("session['sameadminhash']  = " + str(session['sameadminhash']))
        print("session['matchadminpass'] = " + str(session['matchadminpass']))
    elif newadminpass != passmatch:
        session['matchadminpass'] = True
        session['blankadminpass'] = False
        session['newadminpass'] = False
        session['sameadminhash'] = False
        print("session['blankadminpass'] = " + str(session['blankadminpass']))
        print("session['newadminpass']   = " + str(session['newadminpass']))
        print("session['sameadminhash']  = " + str(session['sameadminhash']))
        print("session['matchadminpass'] = " + str(session['matchadminpass']))
    else: 
        session['matchadminpass'] = False
        session['blankadminpass'] = False
        passquery = "select password from user where user_name='admin'; "
        dbcursor.execute(passquery)
        resultpass = dbcursor.fetchone()
        print("Query result: " + str(resultpass))
        print("====================================")
        oldpasshash = str(resultpass[0])
        newpasshash = hashlib.sha256(newadminpass.encode('utf-8')).hexdigest()
        if newpasshash == oldpasshash:
            session['sameadminhash'] = True
            session['newadminpass'] = False
        else:
            session['sameadminhash'] = False
            session['newadminpass'] = True
            print("session['blankadminpass'] = " + str(session['blankadminpass']))
            print("session['newadminpass']   = " + str(session['newadminpass']))
            print("session['sameadminhash']  = " + str(session['sameadminhash']))
            print("session['matchadminpass'] = " + str(session['matchadminpass']))
            print("====================================")
            # session['newadminpass'] = True
            # query = "UPDATE user SET password = '%s' WHERE user_name = 'admin'; " % (newpasshash)
            query = "UPDATE user SET password = '" + newpasshash + "' WHERE user_name = 'admin'; "
            print("Query: " + query)
            dbcursor.execute(query)
            db.commit()
            print("New Admin Request : " + newadminpass)
            print("Confirm Password  : " + passmatch)
            print("Old Password Raw  : " + session['rawpass'])
            print("New Password Hash : " + newpasshash)
            print("Old Password Hash : " + oldpasshash)
            print("Similar Password  : " + str(session['sameadminhash']))
            session['rawpass'] = newadminpass
    
    return redirect('/admin')


@app.route('/newprofile', methods = ['POST'])
def newprofile():
    print("============================== FILE BROWSER INDEX ==============================")
    newusername = request.form['newusername']
    newuserpass = request.form['newuserpass']
    newfullname = request.form['newfullname']
    passmatch = request.form['passmatch']
    print("New Fullname : " + newfullname)
    print("New Username : " + newusername)
    print("New Password : " + newuserpass)
    print("Confirm Password : " + passmatch)

    if newusername == '':
        session['nousername'] = True
        session['passmatch'] = False
        print("No username")
        return redirect("/admin")
    else:
        session['nousername'] = False
        session['passmatch'] = False
        if passmatch == newuserpass:
            try:
                hashedpass = hashlib.sha256(newuserpass.encode('utf-8')).hexdigest()
                print("Hashed Password : " + hashedpass)
                query = ''' INSERT INTO `flaskmanager`.`user` 
                (`user_id`, `user_name`, `password`, `full_name`) 
                VALUES (default, '%s', '%s', '%s'); ''' % (newusername, hashedpass, newfullname)
                dbcursor.execute(query)
                db.commit()
                print("User " + newusername + " inserted successfully")
                os.mkdir(rootpath + "/" + newusername)
                session['passmatch'] = True
            except mysql.connector.Error as error:
                print("Failed to insert record into user table {}".format(error))
        else:
            session['passmatch'] = True
            session['nousername'] = False
    return redirect("/admin")

@app.route('/deleteuser')
def deleteuser():
    
    session['passmatch'] = True
    id = request.args.get('id')
    username = request.args.get('username')
    print("Deleted ID = " + str(id))
    query = "delete from user where user_id=%s ;" % (id)
    dbcursor.execute(query)
    target = rootpath + "/" + username
    shutil.rmtree(target)
    return redirect('/admin')

@app.route('/profilestart')
def profilestart():
    session['nousername'] = False
    session['passmatch'] = False
    session['matchuserpass'] = False
    session['blankuserpass'] = False
    session['newuserpass'] = False
    session['sameuserhash'] = False
    return redirect("/profile")

@app.route('/profile')
def profile():
    print("\n============================== PROFILE ==============================")


    print("Session username: " + session['username'])
    query = 'select password from user where user_name="%s"; ' % (session['username'])
    print("Query = " + query)
    dbcursor.execute(query)
    result = dbcursor.fetchone()
    rawpass = session['rawpass']
    password = str(result[0])
    hashedpass = password
    print("Raw Password    : " + rawpass)
    print("Hashed Password : " + hashedpass)

    return render_template("profile.html",
        hashedpass = hashedpass
    )

@app.route('/changepass', methods=['POST'])
def changepass():
    print("\n============================== CHANGE PASSWORD USER ==============================")

    current_user = session['username']
    olduserpass = session['rawpass']
    newuserpass = request.form['newuserpass']
    confirmpass = request.form['passmatch']
    newuserpasshash = hashlib.sha256(newuserpass.encode('utf-8')).hexdigest()

    filequery = "select * from hash where user_id=%s " % (str(session['user_id']))
    print("File Query : " + filequery)
    dbcursor.execute(query)
    numfiles = dbcursor.rowcount()
    print("File Owned by %s : " + numfiles) % (session['username'])


    query = "select password from user where user_name = '%s'; " % (current_user)
    print("Select Query  : " + query)
    dbcursor.execute(query)
    result = dbcursor.fetchone()
    print("Result        : " + str(result))
    print("=============================")
    olduserpasshash = result[0]
    print("Current Username  : " + current_user)
    print("New user password : " + newuserpass)
    print("Confirm password  : " + confirmpass)
    print("Old user password : " + olduserpass)
    print("Old password hash : " + olduserpasshash)
    print("New password hash : " + newuserpasshash)

    if newuserpass == '' and confirmpass == '':
        session['matchuserpass'] = False
        session['blankuserpass'] = True
        session['newuserpass'] = False
        session['sameuserhash'] = False
        print("session['blankuserpass'] = " + str(session['blankuserpass']))
        print("session['newuserpass']   = " + str(session['newuserpass']))
        print("session['sameuserhash']  = " + str(session['sameuserhash']))
        print("session['matchuserpass'] = " + str(session['matchuserpass']))
    elif newuserpass != confirmpass:
        session['matchuserpass'] = True
        session['blankuserpass'] = False
        session['newuserpass'] = False
        session['sameuserhash'] = False
        print("session['blankuserpass'] = " + str(session['blankuserpass']))
        print("session['newuserpass']   = " + str(session['newuserpass']))
        print("session['sameuserhash']  = " + str(session['sameuserhash']))
        print("session['matchuserpass'] = " + str(session['matchuserpass']))
    else: 
        session['matchuserpass'] = False
        session['blankuserpass'] = False
        if newuserpasshash == olduserpasshash:
            session['sameuserhash'] = True
            session['newuserpass'] = False
        else:
            session['sameuserhash'] = False
            session['newuserpass'] = True
            print("session['blankuserpass'] = " + str(session['blankuserpass']))
            print("session['newuserpass']   = " + str(session['newuserpass']))
            print("session['sameuserhash']  = " + str(session['sameuserhash']))
            print("session['matchuserpass'] = " + str(session['matchuserpass']))
            print("====================================")
            query = "UPDATE user SET password = '" + newuserpasshash + "' WHERE user_name = '%s'; " % (current_user)
            print("Update Query      : " + query)
            dbcursor.execute(query)
            db.commit()
            session['rawpass'] = newuserpass

    return redirect('/profile')


# ====================================================================
# ====================================================================

# run HTTP server
if(__name__ == '__main__'):
    app.run(debug=True, threaded=True)
    # app.run('192.168.0.18')