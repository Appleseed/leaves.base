curl %1 -o %2.md
md_to_json -o %2.json %2.md
python transform.awesome.json.csv.py %2.json %2.csv
Rem cat %2.csv | tr -d ' ' | cut -d',' -f1 > awesome_list.txt
