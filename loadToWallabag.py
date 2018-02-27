import sys
import csv
import persist_in_wallabag

#file_name = sys.argv[1]
file_name = 'sindresorhus.csv'

with open(file_name, "r") as awesome_tag_list:
        csv_file = csv.reader(awesome_tag_list)
        for row in csv_file:
            if row:
                persist_in_wallabag.createEntryWallabag(row[0],row[1],row[2])
