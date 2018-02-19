# coding: utf-8
import sys
import csv
import re
import persist_in_wallabag

with open('sindresorhus.csv', "r") as awesome_tag_list:
        csv_file = csv.reader(awesome_tag_list)
        for row in csv_file:
            if row:
                persist_in_wallabag.callWallabag(row[0],row[1],row[2])
