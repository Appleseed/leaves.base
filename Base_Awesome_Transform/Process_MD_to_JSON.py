# coding: utf-8

# Written by Jagannath Bilgi <jsbilgi@yahoo.com>

"""
    Converts markdown file to json format.

    Process fails in case file is no compliant with utf-8 character set.
    Process also fails if markdown contains mix lists and other content. example

    # Books
    TODO : Need to get more books, and then order by reading level.
     - [Apache Solr Enterprise Search Server, 3rd Edition](https://www.amazon.com/Apache-Solr-Enterprise-Search-Server/dp/1782161368/)

    However process succeeds after editing content as below
    # Books
     - TODO : Need to get more books, and then order by reading level.
     - [Apache Solr Enterprise Search Server, 3rd Edition](https://www.amazon.com/Apache-Solr-Enterprise-Search-Server/dp/1782161368/)

"""
import sys
import os

file_json = sys.argv[1]
file_md_cp = sys.argv[1]

os.system("md_to_json -o %s %s"%(file_json, file_md_cp))