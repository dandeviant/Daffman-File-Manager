import subprocess
import os

FAIL = '\033[91m'
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

# check for root privileges
if os.geteuid() != 0:
    exit(""" 
    ========================================================
        DAFFMAN - A Flask File Manager for Debian/Ubuntu
    ========================================================
    The system requires multiple Python modules installed
    through "pip3". Root privileges is required.

    Please rerun the script with sudo. 
    """)

print("""

========================================================
    DAFFMAN - A Flask File Manager for Debian/Ubuntu
========================================================
DAFFMAN is a Python-based NAS Web File Manager System
built for Debian-based Linux running Bash/ZSH.

These modules will be installed using pip3. 

- flask - Python Flask Framework
- python-mysql-connector - Python MySQL Connector
- werkzeug
- hashlib 
- pyaescrypt - PyAesCrypt AES256-CBC Encryption module


""")
print("===================================================")
print("Running installation process...")
print("===================================================")
print("")
print(OKCYAN + "[+] Checking for pip3 package" + ENDC)

output = subprocess.check_output('sudo dpkg -l | grep python3-pip', shell=True).decode('utf-8').split('\n')
if output == '':
    print("""
    [-] pip3 package missing
    [+] Installing pip3...
    """)


print(OKGREEN + "[+] pip3 package is installed"+ ENDC)
print("===================================================")
print(OKCYAN + "[+] Installing required Python modules via pip3" )



print(FAIL + "[+] INSTALLATION FAILED")
print(WARNING + "[+] WARNING")
print(OKCYAN + "[+] OKCYAN")
print(OKGREEN + "[+] OKGREEN")

