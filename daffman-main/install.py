import subprocess

def prRed(text): print("\033[91m{}\033[00m" .format(text))
def prCyan(text): print("\033[96m{}\033[00m" .format(text))
def prGreen(text): print("\033[92m{}\033[00m" .format(text))
def prLightGray(text): print("\033[97m{}\033[00m" .format(text))
def prYellow(text): print("\033[93m{}\033[00m" .format(text))
def prLightPurple(text): print("\033[94m{}\033[00m" .format(text))
def prBlack(text): print("\033[98m{}\033[00m" .format(text))
def prPurple(text): print("\033[95m{}\033[00m" .format(text))



def listpackage():
    
    listoutput = subprocess.check_output(['pip3', 'list'], universal_newlines=True, text=True)
    listoutput = listoutput.replace("\n", " ")
    listoutput = listoutput.split(" ")
    # print(listoutput)
    
    package = ["Markdown", 
    "Flask",
    "Flask-Bootstrap",
    "Jinja2",
    "Werkzeug", 
    # "hashlib", 
    "mysql-connector-python",
    "pyAesCrypt",
    "gunicorn"
    ]
    print("pip3 modules needed: ")
    for x in package:
        print("       [-] %s" %(x))
    print("\n")
    prYellow("Scanning for installed modules")
    prCyan("=================================")

    # print("Package: " + str(package))
    
    for pkg in package:
        # print("pkg = " + pkg)
        for item in listoutput:
            # print("Item = " + item)
            if item == pkg:
                installed = True
                break
            else:
                installed = False
            # print("Installed = " + str(installed))
        if installed == True:
            prGreen("[INSTALLED] " + pkg)
        else:
            prRed("[MISSING] " + pkg)
            install(pkg)

def install(pkg):
    prCyan("=================================")
    prYellow("Installing %s" %(pkg))
    output = subprocess.check_output(['pip3', 'install', pkg], universal_newlines=True)
    prCyan("=================================")
    

if __name__ == '__main__':
    prPurple("DAFFMAN Installer")
    prCyan("=================================")
    listpackage()
    # install('flask')
    print("\nBye\n")