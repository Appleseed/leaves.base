curl %1 -o %2.md
python html_to_markdown.py %2
md_to_json -o %2.json %2_cp.md
python transform.awesome.json.csv.py %2.json %2.csv
python Get_awesome_list.py %2.csv %2.txt
Rem cat %2.csv | tr -d ' ' | cut -d',' -f1 > awesome_list.txt
