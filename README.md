# DAFFMAN: a Python-based Debian File Manager

<b>(short for Daniel's Flask File Manager)</b>

---

GitHub repository: https://github.com/dandeviant/Flask-file-manager

Progress Reminder:<br>
- Data deduplication is completed via Python MD5, but client-side process is not possible.<br>
- For now, every process is server-side only.<br>
<br>

Next task:<br>
- Add a login page only as a start, no serious codes needed
- Write the code for AES encryption using PyAesCrypt
- Extension used is .enc or .aes
<br>

Later:<br>
- User profiling and login system
- User Dashboard 
- Do not allow files with same contents for storage, even for files with different names.
- The process happens during upload process
- If file has different name, but same contents with files in database, ABORT UPLOAD and display error message.
- SELECT * FROM hash where md5=" " - to list all files with same content
- In the error message box, list out all file names with similar contents if found

---

File Manager using Python Flask<br>
This project actually started as my side timekiller during COVID lockdown<br>
Now I've improved this project for my final year project<br>
The system is fully Linux Debian-based. <b>DO NOT RUN ON ANY OTHER OPERATING SYSTEM UNLESS YOU KNOW WHAT YOU'RE DOING</b>

---


### How to run the app in development env
<code>$ python3 flask-manager.py</code><br>
<b>OR</b><br>
<code>$ flask --app flask-manager.py run</code>

Gonna look into gunicorn to deploy this app locally from my Raspberry Pi server

---

### Added/Planned features:

1. File download/upload (completed)
2. User profiling with session login (incomplete)
3. MD5 file deduplication  (completed || server-side only)
4. AES encryption using Python modules (incomplete)

---

### Python Modules (installed thru pip3):

1. Python Flask framework
2. Flask Markdown
3. werkzeug.utils (secure_filename)
4. hashlib
5. mysql-connector-python (import mysql.connector)
6. pycrypto
7. Crypto (for AES)
8. pyaescrypt - PyAesCrypt

---

### Other Requirements:

1. MySQL database for user profiling and hash checking
2. Bootstrap CSS framework for UI (config files in folder 'static'). DO NOT TOUCH THAT FOLDER

