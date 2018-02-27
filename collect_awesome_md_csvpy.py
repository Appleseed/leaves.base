import os
import platform

def md_csv(p1, p2):
    param1 = p1
    param2 = p2

    file_md = param2+".md"
    file_md_cp = param2+"_cp.md"
    file_json = param2+".json"
    file_csv = param2+".csv"
    file_txt = param2+".txt"

    try:
        if platform.system() != 'Windows':
            os.system('rm s%*'(p2))
        else:
            os.system('del %s*'%(p2))
    except :
        pass

    os.system("curl %s -k -o %s"%(param1,file_md))
    os.system("'python3.6' html_to_markdown.py %s"%(param2))
    os.system("md_to_json -o %s %s"%(file_json, file_md_cp))
    os.system("'python3.6' transform.awesome.json.csv.py %s %s"%(file_json, file_csv))
    os.system("'python3.6' Get_awesome_list.py %s %s"%(file_csv, file_txt))
    if platform.system() != 'Windows':
        os.system('ls -lrt')
    else:
        os.system('dir /b %s*'%(p2))

    return "Done"

# md_csv(sys.argv[1],sys.argv[2])