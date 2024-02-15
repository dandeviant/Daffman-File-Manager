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
3. SVG Source: https://www.svgrepo.com/

---

## Explanation on certain matters (FAQ)

1. Results of (hashlib.sha256(text.encode()) ) will be different from (echo 'text' | sha256sum) because the echo command add a newline to string while hashlib does not, thus resulting to different hash value

### System Preview Image

File Browser Page - Folder Section<br>
![image](https://github.com/dandeviant/Daffman-NAS-System/assets/68473358/7fa32cd2-a815-4087-8823-4fb316158aa8)

![image](https://github.com/dandeviant/Daffman-NAS-System/assets/68473358/a738d840-174b-4d9f-b451-f15f83977de9)
<br>
![image](https://github.com/dandeviant/Daffman-NAS-System/assets/68473358/5e542ce9-f59a-4ce9-9e1c-87eea50f44d9)
<br>
File Download Popup<br>
![image](https://github.com/dandeviant/Daffman-NAS-System/assets/68473358/5b2f9eae-4257-4e42-892a-dc2892be33bb)
<br>
File Browser Page - File Section<br>
![browser-preview2](https://user-images.githubusercontent.com/68473358/209222849-b7df5633-e66b-4147-8257-9832d63d6e67.png)
<br>
File Upload Page<br>
![image](https://github.com/dandeviant/Daffman-NAS-System/assets/68473358/4b63163f-1ffe-4af0-a9ac-c6af8b548072)
<br>
File Decryption Page<br>
![image](https://github.com/dandeviant/Daffman-NAS-System/assets/68473358/fcd05b74-2a3f-479a-ba41-3ded46d983bb)
<br>
User Profile Page<br>
![image](https://github.com/dandeviant/Daffman-NAS-System/assets/68473358/cd732225-4386-4533-87a8-4db1b1c8b772)
![image](https://github.com/dandeviant/Daffman-NAS-System/assets/68473358/48b45c01-f9e7-4a32-a10a-daa742cc67de)
<br>
Admin Page<br>
![image](https://github.com/dandeviant/Daffman-NAS-System/assets/68473358/726c54da-2c88-4404-b959-cbf80e56d1c0)
![image](https://github.com/dandeviant/Daffman-NAS-System/assets/68473358/e59dcc1f-f16f-4b95-806c-2e3920d9086e)




