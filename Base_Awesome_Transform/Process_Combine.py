# Written by Jagannath Bilgi <jsbilgi@yahoo.com>

import os
import platform
import Process_MD_to_JSON
"""

Program downloads and converts makrdown document to csv file.

Example :
Markdown file

    # Platforms
    
    - [Node.js](https://github.com/sindresorhus/awesome-nodejs) - JavaScript runtime built on Chrome's V8 JavaScript engine.
    - [Frontend Development](https://github.com/dypsilon/frontend-dev-bookmarks)
    - [Linux](https://github.com/aleksandar-todorovic/awesome-linux)
        - [Containers](https://github.com/Friz-zy/awesome-linux-containers)
    - [macOS](https://github.com/iCHAIT/awesome-macOS)
        - [Command-Line](https://github.com/herrbischoff/awesome-osx-command-line)
        - [Screensavers](https://github.com/aharris88/awesome-macos-screensavers)
csv file
    Title                   Url                                                         Tags
    Node.js,                 https://github.com/sindresorhus/awesome-nodejs,              "Platforms"              
    Frontend Development,    https://github.com/dypsilon/frontend-dev-bookmarks,          "Platforms"
    Linux,                   https://github.com/aleksandar-todorovic/awesome-linux,       "Platforms"
    Containers,              https://github.com/Friz-zy/awesome-linux-containers,         "Platforms,Linux"
    macOS,                   https://github.com/iCHAIT/awesome-macOS,                     "Platforms"
    Command-Line,            https://github.com/herrbischoff/awesome-osx-command-line,    "Platforms,macOS"
    Screensavers,            https://github.com/aharris88/awesome-macos-screensavers,     "Platforms,macOS"

"""

def md_to_csv(p1, p2):
    param1 = p1
    param2 = p2

    file_md = param2+".md"
    file_md_cp = param2+"_cp.md"
    file_json = param2+".json"
    file_csv = param2+".csv"

    try:
        if platform.system() != 'Windows':
            os.system('rm s%*'(p2))
        else:
            os.system('del %s*'%(p2))
    except :
        pass

    os.system("curl %s -k -o %s"%(param1,file_md))
    os.system("'python3.6' Process_HTML_to_MD.py %s"%(param2))
    Process_MD_to_JSON.convert(file_json, file_md_cp)
    os.system("'python3.6' Process_JSON_to_CSV.py %s %s"%(file_json, file_csv))
    if platform.system() != 'Windows':
        os.system('ls -lrt')
        os.system("mv %s /var/awesome"%(file_csv))
        os.system("rm %s*"%p2)
    else:
        os.system('dir /b %s*'%(p2))
    return "Done"

