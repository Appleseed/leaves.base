# Written by Jagannath Bilgi <jsbilgi@yahoo.com>

"""
    Converts markdown file to json format.

    Process fails in case file is noncombatant with utf-8 character set.
    Process also fails if markdown contains mix lists and other content. example

    # Books
    TODO : Need to get more books, and then order by reading level.
     - [Apache Solr Enterprise Search Server, 3rd Edition](https://www.amazon.com/Apache-Solr-Enterprise-Search-Server/dp/1782161368/)

    However process succeeds after editing content as below
    # Books
     - TODO : Need to get more books, and then order by reading level.
     - [Apache Solr Enterprise Search Server, 3rd Edition](https://www.amazon.com/Apache-Solr-Enterprise-Search-Server/dp/1782161368/)

"""
import os

def convert(file_json, file_md_cp):
    os.system("md_to_json -o %s %s"%(file_json, file_md_cp))

