import os

'''
prefs.py
This files handles:
    1. Setting prefs
    2. Getting prefs
    3. Dropping prefs
'''

PAIRING_KEY = "PAIRING_KEY"

destfolder = "prefs/"
if not os.path.exists(destfolder):
    os.makedirs(destfolder)

# Returns value of pref p in string format
def get_pref(p):
    stick_config = destfolder + p + ".txt"
    file_exists = os.path.isfile(stick_config) 

    if not file_exists:
        f=open(stick_config, "w")
        f.write("")
        f.close()
        return ""

    f=open(stick_config, "r")

    if f.mode == 'r':
        return f.read()
    else:
        print("Permission Error : "+ stick_config)
        exit(1)

# Sets value of pref p as val
def set_pref(p, val):
    stick_config = destfolder + p + ".txt"
    f=open(stick_config, "w")
    f.write(val)
    f.close()

# Deletes value of pref p
def drop_pref(p):
    stick_config = destfolder + p + ".txt"
    f=open(stick_config, "w")
    f.write("")
    f.close()
