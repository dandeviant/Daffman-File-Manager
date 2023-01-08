## Notes for new things I came across in the Internet

- Try to find out more on how to use OpenMediaVault for folder sharing with web server
    - I have tried this using standard Mint VM in my Windows using NFS, but OMV has SMB/CIFS
    - Learn more about SMB/CIFS for file sharing https://linuxhint.com/install-and-configure-nfs-server-ubuntu-22-04/

- for testing, I have planned to perform hash comparison before encryption
    - Instead of saving hash of encrypted file, save the hash before encryption
    - Ignore the hash of the encrypted AES file, for real...
    - During download, users will upload the unencrypted file hash
    - Once the hash is given, compare for any similar file 
    - Then upload the file to the file server
    - Rehash the unencrypted file and compare if the hash given by user is equal to the hash generated by python
    - With what I have tested, FileReader API and hashlib produces same hash value for same unencrypted file

- file encryption password
    - make separate text input for file password
    - do not use user password for file encryption

- file deduplication
    - if user2 wants to upload a file that user1 has already uploaded in folder user1:
        1. decrypt user1's file
        2. get file password input from user2
        3. generate new hash for user2's new file
            - perform hash tests for files with same contents, but different encryption password
            - workaround for now : DO NOT HASH THE ENCRYPTED FILE, HASH ONLY UNENCRYPTED FILE
            - PLANNED WORKAROUND :
                - store hash of unencrypted file as usual in the database
                - same process, but use only hash of unencrypted file
                - all of this depends on the capability of using JS FileReader to send hash from client-side
        4. encrypt user2's file in user2 folder
        5. copy to user2 folder
        6. modify the name to make it different


- Links
    - Building Raspberry Pi OMV: https://www.raspberrypi.com/tutorials/nas-box-raspberry-pi-tutorial/
    - Mounting SMB Share from web server: https://support.zadarastorage.com/hc/en-us/articles/213024986-How-to-Mount-a-SMB-Share-in-Ubuntu
    - Some guide videos are on YouTube


- Notes
    - Hashing
        - Same filename, diff content = diff hash
        - Diff filename, same content = same hash
        - diff filename, diff content = diff hash (obviously...)
        - same filename, same content = you can guess...
---

### Progress so far...

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

- change password features is completed for both admin and user
- <s>ONLY ALLOW CHANGE PASSWORD WHEN THE USER HAVE NO FILES IN THE SERVER</s>
- THIS IS BECUZ THE ENCRYPTION/DECRYPTION PASSWORD WILL NOT CHANGE<br>
- As a workaround for demos, I have put a column in hash to store rawtext password. This is temp only<br>

- download decryption is completed


- Client-side file hashing has been completed using CryptoJS
    - more on tasks-pending.md
    
<br>

---
Next task:<br>

- Configure Raspberry Pi remote storage using SAMBA and connect to this PyFlask server:
- Write a markdown file for full system specifications and requirements, properlyyyyy........

https://www.circuitbasics.com/making-a-nas-with-samba-and-raspberry-pi/<br>
https://stackoverflow.com/questions/34430714/sha-256-different-result <br>
https://medium.com/@0xVaccaro/hashing-big-file-with-filereader-js-e0a5c898fc98 <br>


2. FILE SERVER CONFIGURATION
    - Use NFS and configure a shared NFS directory in the Raspberry Pi Server
    - On web server, mount the NFS shared directory and configure DAFFMAN to use that directory
https://linuxhint.com/install-and-configure-nfs-server-ubuntu-22-04/

3. Add User Rules page. just to explain some shit on how to use this system
    - User can upload similar files as long as the similar files has different owner user ID
4. Overall structure of the system is completed. Run some functionality testing and debugging for all features
    - Upload/Download with encrypt/decrypt and hashing
    - User profile making/removing
    - User profile change password