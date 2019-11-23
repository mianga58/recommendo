#!C:\Users\FANTAMA\Documents\untitled2\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'ZEO==5.2.1','console_scripts','runzeo'
__requires__ = 'ZEO==5.2.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('ZEO==5.2.1', 'console_scripts', 'runzeo')()
    )
