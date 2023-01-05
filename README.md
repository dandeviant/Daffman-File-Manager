# DAFFMAN: a Python-based Debian File Manager

<b>(short for Daniel's Flask File Manager)</b>

---

GitHub repository: https://github.com/dandeviant/Flask-file-manager

Progress so far...
---
---
- Data deduplication is completed via Python MD5, but client-side process is not possible.<br>
- Server-side AES encryption during upload is completed. Using pyAesCrypt with .aes extension
- For now, every process is server-side only.<br>
- Login and profiling is completed, only small additions are needed for better UX<br>
- Users are not allowed to modify or upload in folder not belong to them, except admin<br>
- Folders for new users will be created upon registration<br>
- Passwords for files is user's current password and will not change after user password change<br>
- Password is hashed using SHA256 algorithm, to be updated in Chapter 2 and 3<br>
- Download popup to input decrypt password, download only when password is correct, error message not in popup<br>
- Whitespaces in filename is replaced with underscore during upload
---
- change password features is completed for both admin and user
- <s>ONLY ALLOW CHANGE PASSWORD WHEN THE USER HAVE NO FILES IN THE SERVER</s>
- THIS IS BECUZ THE ENCRYPTION/DECRYPTION PASSWORD WILL NOT CHANGE<br>
- As a workaround for demos, I have put a column in hash to store rawtext password. This is temp only<br>
---
- download decryption is completed
<br>

Next task:<br>

- Complete upload page<br>
    - In the error message box, list out all file names with similar contents if found<br>
    - hash table has been altered. Debug the code for any variables using the old table column<br>
- Configure Raspberry Pi remote storage using SAMBA and connect to this PyFlask server:
- Write a markdown file for full system specifications and requirements, properlyyyyy........

https://www.circuitbasics.com/making-a-nas-with-samba-and-raspberry-pi/<br>
https://stackoverflow.com/questions/34430714/sha-256-different-result <br>
https://medium.com/@0xVaccaro/hashing-big-file-with-filereader-js-e0a5c898fc98 <br>


1. IMPORTANT: build a JavaScript code to read the file hash from client side using FileReader JS from FileAPI
    - My plan: The hash checks will be done on client side.
    - Select all hash uploaded by the user from database, but DO NOT SHOW IT YET on the upload page.
    - Perform data checks once user has selected the file
https://github.com/lvaccaro/hashfilereader.git

2. FILE SERVER CONFIGURATION
    - Use NFS and configure a shared NFS directory in the Raspberry Pi Server
    - On web server, mount the NFS shared directory and configure DAFFMAN to use that directory
https://linuxhint.com/install-and-configure-nfs-server-ubuntu-22-04/

---

1. Add User Rules page. just to explain some shit on how to use this system
    - User can upload similar files as long as the similar files has different owner user ID
2. Overall structure of the system is completed. Run some functionality testing and debugging for all features
    - Upload/Download with encrypt/decrypt and hashing
    - User profile making/removing
    - User profile change password
    
---

### About

1. DAFFMAN is a NAS file manager built on Python and built for Debian Linux system running Bash/ZSH shell
2. This project actually started as my side timekiller during COVID lockdown
3. Now I've improved this project for my final year project
4. The system is fully Debian-based/Ubuntu-based (Ubuntu, Mint OS, etc.) as far as I have tested<b>
    - DO NOT RUN ON ANY OTHER OPERATING SYSTEM UNLESS YOU KNOW WHAT YOU'RE DOING</b>

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


