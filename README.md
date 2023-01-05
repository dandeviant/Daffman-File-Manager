# DAFFMAN: a Python-based Debian File Manager

<b>(short for Daniel's Flask File Manager)</b>

---

### Notes for progress and bug fixes are available in ```tasks-pending.md```

### About

1. DAFFMAN is a NAS file manager built on Python and built for Debian Linux system running Bash/ZSH shell
2. This project actually started as my side timekiller during COVID lockdown
3. Now I've improved this project for my final year project
4. The system is fully Debian-based/Ubuntu-based (Ubuntu, Mint OS, etc.) as far as I have tested<b>
    - DO NOT RUN ON ANY OTHER OPERATING SYSTEM UNLESS YOU KNOW WHAT YOU'RE DOING</b>
    - OR ELSE IT WON'T WORK AS INTENDED, NOTE THIS...

---

Install all requirements

```pip3 install -r requirements.txt```


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
6. pyAesCrypt
    - pyAesCrypt is a AES Crypt module integrated with Python.<br>
    - It uses AES-256-CBC encryption mode<br>
    - It can also be used directly from the terminal<br>

---

### Other Requirements:

1. MySQL database for user profiling and hash checking
2. Bootstrap CSS framework for UI (config files in folder 'static'). DO NOT TOUCH THAT FOLDER
3. SVG Source: <a href="https://www.svgrepo.com/" target="_blank">SVG Repo</a>

---

## Explanation on certain matters (FAQ)

1. Results of (hashlib.sha256(text.encode()) ) will be different from (echo 'text' | sha256sum) because the echo command add a newline to string while hashlib does not, thus resulting to different hash value

### System Preview Image

File Browser Page - Folder Section<br>
![browser-preview](https://user-images.githubusercontent.com/68473358/209222789-4dc5b62a-fab2-41e2-9a2f-f3595fc62485.png)

File Browser Page - File Section<br>
![browser-preview2](https://user-images.githubusercontent.com/68473358/209222849-b7df5633-e66b-4147-8257-9832d63d6e67.png)


