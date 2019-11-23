#!C:\Users\FANTAMA\Documents\untitled2\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'zdaemon==4.3','console_scripts','zdaemon'
__requires__ = 'zdaemon==4.3'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('zdaemon==4.3', 'console_scripts', 'zdaemon')()
    )
