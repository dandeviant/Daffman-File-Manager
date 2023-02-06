### Progress so far...

OVERALL CODING IS 100% COMPLETED. 
WOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOPPPP...
TIME FOR BUG FUCKIN HUNTING FOR DEMO

Next Tasks (not important)
1. Write a markdown file for full system specifications and requirements, properlyyyyy........
2. Add User Rules page. just to explain some shit on how to use this system
    - User can upload similar files as long as the similar files has different owner user ID
3. Overall structure of the system is completed. Run some functionality testing and debugging for all features
    - Upload/Download with encrypt/decrypt and hashing
    - User profile making/removing
    - User profile change password


## Notes for new things I came across in the Internet

- CryptoJS
    - https://stackoverflow.com/questions/60520526/aes-encryption-and-decryption-of-files-using-crypto-js


- NFS File Sharing
    - https://linuxhint.com/install-and-configure-nfs-server-ubuntu-22-04/


- Links
    - Building Raspberry Pi OMV: https://www.raspberrypi.com/tutorials/nas-box-raspberry-pi-tutorial/
    - Mounting SMB Share from web server: https://support.zadarastorage.com/hc/en-us/articles/213024986-How-to-Mount-a-SMB-Share-in-Ubuntu
    - Some guide videos are on YouTube
    - NFS configuration: https://linuxhint.com/install-and-configure-nfs-server-ubuntu-22-04/
    - https://www.circuitbasics.com/making-a-nas-with-samba-and-raspberry-pi/<br>
    - https://stackoverflow.com/questions/34430714/sha-256-different-result <br>
    - https://medium.com/@0xVaccaro/hashing-big-file-with-filereader-js-e0a5c898fc98 <br>

- Notes
    - Hashing of two files with...
        - Same filename, diff content = diff hash
        - Diff filename, same content = same hash
        - diff filename, diff content = diff hash (obviously...)
        - same filename, same content = you can guess...
---