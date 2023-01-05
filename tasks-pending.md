## Notes for new things I came across in the Internet

- Try to find out more on how to use OpenMediaVault for folder sharing with web server
    - I have tried this using standard Mint VM in my Windows using NFS, but OMV has SMB/CIFS
    - Learn more about SMB/CIFS for file sharing https://linuxhint.com/install-and-configure-nfs-server-ubuntu-22-04/

- Links
    - Building Raspberry Pi OMV: https://www.raspberrypi.com/tutorials/nas-box-raspberry-pi-tutorial/
    - Mounting SMB Share from web server: https://support.zadarastorage.com/hc/en-us/articles/213024986-How-to-Mount-a-SMB-Share-in-Ubuntu
    - Some guide videos are on YouTube
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
<br>

---
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

3. Add User Rules page. just to explain some shit on how to use this system
    - User can upload similar files as long as the similar files has different owner user ID
4. Overall structure of the system is completed. Run some functionality testing and debugging for all features
    - Upload/Download with encrypt/decrypt and hashing
    - User profile making/removing
    - User profile change password
    
---