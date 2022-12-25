# DAFFMAN: a Python-based Debian File Manager

<b>(short for Daniel's Flask File Manager)</b>

---

GitHub repository: https://github.com/dandeviant/Flask-file-manager

Progress Reminder:<br>
- Data deduplication is completed via Python MD5, but client-side process is not possible.<br>
- For now, every process is server-side only.<br>
- Login and profiling 70% done
<br>

Next task:<br>
- Write the code for AES encryption using PyAesCrypt
- Extension used is .enc or .aes
- Add change password
- Add
<br>

Later:<br>
- add change password features
- for admin, add new user page in Administration section
<br>

- Do not allow files with same contents for storage, even for files with different names.
- The process happens during upload process
- If file has different name, but same contents with files in database, ABORT UPLOAD and display error message.
- SELECT * FROM hash where md5=" " - to list all files with same content
- In the error message box, list out all file names with similar contents if found
<br>

- If you are to use client-side MD5 checking, create another page for file upload
- Display errors of fileexist in the page, not in browser page
<br>

---

### About

DAFFMAN is a NAS file manager built on Python and built for Debian Linux system running Bash/ZSH shell<br>
This project actually started as my side timekiller during COVID lockdown<br>
Now I've improved this project for my final year project<br>
The system is fully Debian-based. <b>DO NOT RUN ON ANY OTHER OPERATING SYSTEM UNLESS YOU KNOW WHAT YOU'RE DOING</b>

---

### System Preview Image

File Browser Page - Folder Section
![browser-preview](https://user-images.githubusercontent.com/68473358/209222789-4dc5b62a-fab2-41e2-9a2f-f3595fc62485.png)

File Browser Page - File Section
![browser-preview2](https://user-images.githubusercontent.com/68473358/209222849-b7df5633-e66b-4147-8257-9832d63d6e67.png)

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
3. SVG Source: <a href="https://www.svgrepo.com/" target="_blank">SVG Repo</a>

