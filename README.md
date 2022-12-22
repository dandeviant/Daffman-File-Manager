# DAFFMAN: a Python-based Debian File Manager
#### (short for Daniel's Flask File Manager)

---

GitHub repository: https://github.com/dandeviant/Flask-file-manager

Progress Reminder:<br>
Next task:<br>
- Achieve objective 1: Prevent data deduplication<br>
- check the md5 of new file with the ones in database<br>
- if matches found, abort upload<br>
- if not, continue with upload<br>
<br>

Later:<br>
- encrypt file with AES-256 using python module<br>
- remote directory management via Flask


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
3. MD5 file deduplication  (incomplete)
4. AES encryption using Python modules (incomplete)

---

### Python Modules (installed thru pip3):

1. Python Flask framework
2. Flask Markdown
3. werkzeug.utils (secure_filename)
4. hashlib
5. mysql-connector-python (import mysql.connector)

---

### Other Requirements:

1. MySQL database for user profiling and hash checking
2. Bootstrap CSS framework for UI (config files in folder 'static'). DO NOT TOUCH THAT FOLDER

