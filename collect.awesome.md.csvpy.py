import sys
import os

param1 = sys.argv[1]
param2 = sys.argv[2]

file_md = param2+".md"
file_md_cp = param2+"_cp.md"
file_json = param2+".json"
file_csv = param2+".csv"
file_txt = param2+".txt"

os.system("curl %s -k -o %s"%(param1,file_md))
os.system("python html_to_markdown.py %s"%(param2))
os.system("md_to_json -o %s %s"%(file_json, file_md_cp))
os.system("python transform.awesome.json.csv.py %s %s"%(file_json, file_csv))
os.system("python Get_awesome_list.py %s %s"%(file_csv, file_txt))

