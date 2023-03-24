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

### Python Modules (installed thru pip3, just run the install script wit python3):

1. Python Flask framework
2. Flask Markdown
3. werkzeug.utils (secure_filename)
4. mysql-connector-python (import mysql.connector)


---

### Other Requirements:

1. MySQL database for user profiling and hash checking
2. Bootstrap CSS framework for UI (config files in folder 'static'). DO NOT TOUCH THAT FOLDER
3. SVG Source: https://www.svgrepo.com/

---

## Explanation on certain matters (FAQ)

1. Results of (hashlib.sha256(text.encode()) ) will be different from (echo 'text' | sha256sum) because the echo command add a newline to string while hashlib does not, thus resulting to different hash value


