#!/usr/bin/python
# EASY-INSTALL-ENTRY-SCRIPT: 'markdown-to-json==1.0.0','console_scripts','md_to_json'
__requires__ = 'markdown-to-json==1.0.0'
import sys
from pkg_resources import load_entry_point

#included 2 lines below to address ascii codec issue
reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == '__main__':
    sys.exit(
        load_entry_point('markdown-to-json==1.0.0', 'console_scripts', 'md_to_json')()
    )
