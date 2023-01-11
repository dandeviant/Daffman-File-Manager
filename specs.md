# DAFFMAN: a Python-based Debian File Manager

<b>(short for Daniel's Flask File Manager)</b>

---

## About

DAFFMAN is a Python-based web application designed to interact with Network-Attached Storage (NAS) or any file servers running Network File Sharing (NFS) protocol for file sharing services. The system also utilizes multiple client-side JavaScript modules and browser APIs (Application Programming Interface) to provide client-side hashing and AES-256 CBC file encryption method and  end-to-end file encryption from the client to the web server.


This system is purely browser-based, so for client devices, the system is ready from the get-go and no additional installations or extensions are required other than up-to-date web browsers for access.

---

## When Installing...

- For MySQL installation
    - run "sudo mysql"
    - run this query:
        - ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Dane@1710'; 

- Make sure all folders in uploads directory are blank, only empty admin folder should be there.
- Change the rootpath in the main app script
- Clear all users in database, except admin
    - if deleted, add the admin row with the following details or query: 
        - user_id   : 1
        - user_name : admin
        - password  : 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918
        - full_name : System Administrator
        - Query: INSERT INTO user (user_id, user_name, password, fullname) VALUES (1, "admin", "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918", "System Administrator");
- Clear all hash stored in hash table in database 

---

## How it works

- Connection
    - The web app system is deployed in a webserver with NFS connection to the file server. 
- File Transfer/Storage
    - All files are processed through the web server for file duplication checks before stored in the file server as an encrypted file.
    - 

## System Requirements for Web Servers

