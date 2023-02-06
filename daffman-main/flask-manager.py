#!/usr/bin/env python3

#Python Flask File Manager

from flask import Flask, send_file, session, redirect, render_template, request
from flask_bootstrap import Bootstrap
from distutils.log import debug
from fileinput import filename
import time
from werkzeug.utils import secure_filename
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
        password="mysql@1234",
        database="flaskmanager"
    )
dbcursor = db.cursor(buffered=True)

here = os.getcwd()


static_url_path='sa',
app = Flask(__name__,
static_folder = here + '/static'
)

app.secret_key = 'any random string'
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

rootpath = '/home/daniel/uploads'
forbidpath = '/home/daniel/'
rootfolder = 'uploads'

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
    session['userpassraw'] = rawinputpass
    hashinputpass = hashlib.sha256(rawinputpass.encode('utf-8')).hexdigest()
    print("Entered name: " + username)
    print("Input pass: " + rawinputpass)
    print("Input pass hash: " + hashinputpass)
    
    query = 'select * from user where user_name="%s"; ' % (username)
    print("Login query: " + query)
    dbcursor.execute(query)
    account = dbcursor.fetchone()
    print("Account list: " + str(account))
    print("================= User Database =================")
    if account:
        session['user_id'] = str(account[0])
        session['username'] = account[1]
        session['userpasshash'] = account[2]
        session['userfullname'] = account[3]
        print("User  ID  : " + session['user_id'])
        print("username  : " + session['username'])
        print("Password  : " + session['userpasshash'])
        print("Password raw  : " + session['userpassraw'])
        print("Full Name : " + session['userfullname'])
        print("==================================")
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

    print("====================== EDIT PERMIT ======================")
    # session['editpermit'] = True
    current_dir = os.getcwd()
    current_dir = current_dir.replace(forbidpath, '')
    print("Current Dir : " + current_dir)
    print("Current User: " + session['username'])

    if session['username'] == 'admin':
        if current_dir == rootfolder:
            session['editpermit'] = False
        else:
            session['editpermit'] = True
    else:
        if current_dir == rootpath:
            session['editpermit'] = False
        else:
            dir = current_dir.replace(forbidpath, '')
            if session['username'] not in dir:
                session['editpermit'] = False
            else:
                session['editpermit'] = True

    print("Edit permit : " + str(session['editpermit']))
    print("")
    print("=========================================================")

    # if session['admin'] == False:
    #     if compare not in current_dir:
    #         print("Upload not allowed")
    #         session['folderpermit'] = False
    #     else:
    #         session['editpermit'] = True
    # else:
    #     session['editpermit'] = True



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
    # notepath = '/home/daniel/Desktop/Flask-file-manager/README.md'
    # note = subprocess.check_output(('cat ' + notepath), shell=True).decode('utf-8')


     # scan for md5 and file size of each file
    hash_list = []

    for item in files[0: -1]:
        if '.' in item:
            if '.enc' not in item:
                os.remove(item)
                return redirect('/browser')

    for item in files[0: -1]:
            if '.' in item:
                namefile = current_dir + '/' + item
                namefile = namefile.replace(forbidpath, '')
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
                print("hash_list = ", end="")
                print(hash_list)
    # assets = '../'            

    global fileexist
    global filemissing
    global folderexist
    global foldermissing

    # current_dir = os.getcwd()

    print("Check editpermit: " + str(session['editpermit']))
    print("Current Dir     : " + current_dir)
    return render_template("manager.html",
    rootpath = rootpath,
    rootfolder = rootfolder,
    forbidpath = forbidpath,
    mimetype='image/svg+xml',
    current_dir = current_dir,
    path = path,
    files = files,
    # note = note,
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
    if target_dir == '..':
        os.chdir(target_dir)
    else:
        os.chdir(forbidpath + target_dir)

    current_dir = request.args.get('path')
    compare = rootfolder + '/' + session['username']
    print("Compare : " + compare)
    usercd = session['username']
    print("Requested Dir : " + current_dir)
    print("Usercd : " + usercd)

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
        os.mkdir(foldername)
        foldermissing = False
        foldersuccess = True
        foldercreated = request.args.get('folder')
    else:
        foldermissing = True
        foldersuccess = False
    #redirect to file manager
    return redirect('/browser')

@app.route('/decryptFile')
def decryptFile():
    return render_template('decrypt.html')

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

    current_dir = os.getcwd()
    print("Current Dir        : " + current_dir)
    current_dir = current_dir.replace(forbidpath, '')
    file = request.form['downloadfile']
    inputpass = request.form['password']
    inputpasshash = hashlib.sha256(inputpass.encode('utf-8')).hexdigest()
    filename = current_dir + '/' + file
    print("Requested File Name: " + file)
    print("File Name in DB    : " + filename)

    hashquery = "select * from hash where filename = '%s' ;" % (filename)
    print("hashquery          : " + hashquery)
    dbcursor.execute(hashquery)
    hashresult = dbcursor.fetchone()
    filename = str(hashresult[0])
    filepasshash = str(hashresult[3])
    ownerid = str(hashresult[5])

    userquery = "select user_name from user where user_id='%s'; " % (ownerid)
    print("userquery           : " + userquery)
    dbcursor.execute(userquery)
    userresult = dbcursor.fetchone()
    print("User Result         : " + str(userresult))
    ownerusername = userresult[0]

    print("Hash Result         : " + str(hashresult))
    print("=================================")
    print("Download File       : " + filename)
    print("File Owner User ID  : " + ownerid)
    print("File Owner username : " + ownerusername)
    print("Input Password      : " + inputpass)
    print("Input Password Hash : " + inputpasshash)
    print("Actual Password Hash: " + filepasshash)


    if inputpasshash == filepasshash:
        print("Password Match      : True")
        session['downloadpass'] = True
        print("Downloaded File : " + filename)
        # print("====================== DECRYPT FILE ======================")
        # outputfile = file.replace('.aes', '')
        # print("Input file   : " + file)
        # print("Output file  : " + outputfile)
        # print("Password     : " + inputpass)
        # pyAesCrypt.decryptFile(file, outputfile, inputpass)
        # downloadfile = filename.replace('.aes', '')
        # print("Downloading %s%s" % (forbidpath, downloadfile))
        return send_file(forbidpath + filename, as_attachment=True)
    else:
        print("Password Match      : False")
        session['downloadpass'] = False
        return index(session['downloadpass'])

@app.route('/startupload', methods=['GET'])
def startupload():
    session['filemissing'] = False
    session['fileexist'] = False
    session['fileuploaded'] = False

    return redirect('/newupload')

@app.route('/newupload', methods=['GET'])
def newupload():
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

@app.route('/checkupload', methods=['POST'])
def checkupload():
    print("============================== VERIFY UPLOAD ==============================")
    print("sdasdasdasa 123")
    newfile = request.files['newfile']
    print("sdasdasdasa 12343")
    print("New filename = " + newfile.filename)
    
    filepassword = request.form['decryptpass']
    print("sdasdasdasa")
    if newfile.filename == '' or filepassword == '':
        session['filemissing'] = True
        session['fileexist'] = False
        session['filesuccess'] = False
    else:
        session['filemissing'] = False
        session['fileexist'] = False
        session['filesuccess'] = False
        current_dir = os.getcwd()
 
        filesize = request.form['filesize']
        
        filehash = request.form['md5']
        print("================ File Summary =======================")
        print("File Name : " + newfile.filename)
        print("File Size : " + str(filesize) + " KB")
        print("File Hash : " + filehash)
        print("================ User Summary =======================")
        print("Current Username : " + session['username'])
        print("Current User ID  : " + str(session['user_id']))
        print("================ Check From Database ================")
        print("user_id  : " + str(session['user_id']))
        print("username : " + session['username'])
        checkquery = "select * from hash where user_id=%s and md5='%s' " % (str(session['user_id']), filehash)
        dbcursor.execute(checkquery)
        checkresult = dbcursor.fetchall()
        checkrow = dbcursor.rowcount
        print("Query   : " + checkquery)
        print("")
        print("Result : " + str(checkresult))
        print("")
        print("Similar File Count: " + str(checkrow))
        
        
        if checkrow == 0:
            session['fileexist'] = True
            newfile.save(secure_filename(newfile.filename))
            print("File '" + newfile.filename + "' saved to server")
            if ' ' in newfile.filename:
                    print("Whitespace detected")
                    newfile.filename = newfile.filename.replace(" ", '_')
                    print("Whitespace replaced with underscore")
                    print("New name : " + newfile.filename)


            print("================ FILE ENCRYPTION =================")
            # AES encryption process
            inputfile = newfile.filename
            # outputfile = inputfile + ".aes"
            # encodepassword =  filepassword.encode('utf-8')
            # hashedpass = hashlib.sha256(encodepassword).hexdigest()
            hashedpass = request.form['decryptpasshash']
            # filepathencrypt = current_dir + '/' + outputfile
            filepathencrypt = current_dir + '/' + inputfile
            filepathencrypt = filepathencrypt.replace(forbidpath, '')
            filepathraw = current_dir + '/' + newfile.filename
            print("Input file : " + inputfile)
            # print("Output file: " + outputfile)
            print("File path  : " + filepathencrypt)
            print("File Password Hashed    : " + hashedpass)
            print("File Password from Input: " + request.form['decryptpass'])
            print("File Password variable  : " + filepassword)
            
            # pyAesCrypt.encryptFile(inputfile, outputfile, filepassword) # encrypt raw file
            # os.remove(filepathraw) # delete unencrypted file

            print()
            print("================ Upload to Database =================")
            print("Current dir: " + current_dir)
            
            print("user_id  : " + str(session['user_id']))
            print("username : " + session['username'])
            print("File name: " + newfile.filename)
            print("File path: " + filepathencrypt)
            print("File Size: " + str(filesize))
            print("File Hash: " + hashedpass)
            print("filepasshash : " + hashedpass)
            print("filepassraw  : " + filepassword + "\n") # session['userpassraw']
            
            uploadquery = "INSERT INTO hash(filename, md5, filesize, filepasshash, filepassraw, user_id) VALUES ('%s','%s','%s','%s','%s',%d)" % (filepathencrypt, filehash, str(filesize), hashedpass, filepassword, session['user_id'])
            print("Upload Query : " + uploadquery)
            dbcursor.execute(uploadquery)
            db.commit()
            session['filemissing'] = False
            session['fileexist'] = False
            session['filesuccess'] = True
            return redirect('/browser')
        else:
            # os.remove(newfile.filename)
            print("File existed. Canceling upload")
            print("===================== FILE DUPES FOUND =====================")
            for x in checkresult:
                print("")
                print("File name : " + x[0])
                print("file hash : " + x[1])
                print("Owner ID  : " + str(x[5]))
                ownerquery = "select user_name from user where user_id =%d;" % (x[5])
                dbcursor.execute(ownerquery)
                result = dbcursor.fetchone()
                ownername = result[0]
                print("Owner Username : " + ownername)
                print("")

            current_dir = os.getcwd()
            path = current_dir.replace(forbidpath, ".")
            listdir = path.split("/")
            numdir = len(listdir)
            timeend = time.time()
            timeelapsed = timeend - timeend
            print("\n\nTime Start: " + str(timeelapsed))
            print("Time End: " + str(timeend))
            print("Time Elapsed: " + str(timeelapsed))
            print("===================== FILE UPLOAD END =====================")
            session['filemissing'] = False
            session['fileexist'] = True
            session['filesuccess'] = False


                # create tuple named file
            files = subprocess.check_output('ls', shell=True).decode('utf-8').split('\n')
            return render_template('upload.html',
                listdir = listdir,
                numdir = numdir,
                current_dir = current_dir,
                checkresult = checkresult,
                ownername = ownername
            )

    return redirect('/newupload')

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

    print("==================== DELETE FILE ====================")
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
    print("Filepath db   : " + file)
    filepath = forbidpath + file
    print("Filepath full : " + filepath)
    query = "DELETE FROM hash WHERE filename='%s' " % (file)
    print("Query = " + query)
    dbcursor.execute(query)
    db.commit()
    os.remove(filepath)
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


    dir = forbidpath + request.args.get('dir')
    content = os.listdir(dir)
    if len(content) == 0:
        os.rmdir(dir)
    else:
        print("Directory not empty")
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
            print("Old Password Raw  : " + session['userpassraw'])
            print("New Password Hash : " + newpasshash)
            print("Old Password Hash : " + oldpasshash)
            print("Similar Password  : " + str(session['sameadminhash']))
            session['userpassraw'] = newadminpass
    
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
                session['passmatch'] = False
            except mysql.connector.Error as error:
                print("Failed to insert record into user table {}".format(error))
        else:
            session['passmatch'] = True
    return redirect("/admin")

@app.route('/deleteuser')
def deleteuser():
    
    session['passmatch'] = False
    id = request.args.get('id')
    username = request.args.get('username')
    print("Deleted ID = " + str(id))
    query = "delete from user where user_id=%s ;" % (id)
    dbcursor.execute(query)
    db.commit()

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
    rawpass = session['userpassraw']
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
    olduserpass = session['userpassraw']
    newuserpass = request.form['newuserpass']
    confirmpass = request.form['passmatch']
    newuserpasshash = hashlib.sha256(newuserpass.encode('utf-8')).hexdigest()

    # filequery = "select * from hash where user_id=%s " % (str(session['user_id']))
    # print("File Query : " + filequery)
    # dbcursor.execute(filequery)
    # numfiles = dbcursor.rowcount
    # print("File Owned by %s : " + str(numfiles)) % (session['username'])


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
            session['userpassraw'] = newuserpass

    return redirect('/profile')


# ====================================================================
# ====================================================================

# run HTTP server
if(__name__ == '__main__'):
    app.run(debug=True, port=80)
    # app.run('192.168.0.18')
