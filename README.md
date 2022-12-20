# Flask File Manager

<br>GitHub repository: https://github.com/dandeviant/Flask-file-manager
<br><br>
File Manager using Python Flask<br>
This project actually started as my side timekiller during COVID lockdown<br>
Now I've improved this project for my final year project<br>
The system is fully Linux Debian-based. <b>DO NOT RUN ON ANY WINDOWS OS</b>
---


### How to run the app in development env
<br> $ python3 flask-manager.py
<br> $ flask --app flask-manager.py run 

Gonna look into gunicorn to deploy this app locally from my Raspberry Pi server

---

## Added/Planned features:

1. File download/upload (completed)
2. User profiling with session login (incomplete)
3. MD5 file deduplication  (incomplete)
4. AES encryption using Python modules (incomplete)

---

## Python Modules (installed thru pip3):

1. Python Flask framework
2. werkzeug.utils (secure_filename)
3. hashlib

---

## Extra Requirements:

1. MySQL database for user profiling
2. Bootstrap CSS framework for UI (config files in folder 'static'). DO NOT TOUCH THAT FOLDER

