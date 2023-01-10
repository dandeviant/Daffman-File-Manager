# DAFFMAN: a Python-based Debian File Manager

<b>(short for Daniel's Flask File Manager)</b>

---

## About

DAFFMAN is a Python-based web application designed to interact with Network-Attached Storage (NAS) or any file servers running Network File Sharing (NFS) protocol for file sharing services. The system also utilizes multiple client-side JavaScript modules and browser APIs (Application Programming Interface) to provide client-side hashing and AES-256 CBC file encryption method and  end-to-end file encryption from the client to the web server.


This system is purely browser-based, so for client devices, the system is ready from the get-go and no additional installations or extensions are required other than up-to-date web browsers for access.

---

## How it works

- Connection
    - The web app system is deployed in a webserver with NFS connection to the file server. 
- File Transfer/Storage
    - All files are processed through the web server for file duplication checks before stored in the file server as an encrypted file.
    - 

## System Requirements for Web Servers

