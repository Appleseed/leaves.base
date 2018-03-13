# coding: utf-8

# Written by Jagannath Bilgi <jsbilgi@yahoo.com>

import sys
import json
import re

"""
Program accepts *.md document and converts to csv in required format

Program parse line by line and uses recursive method to traverse from leaf to root. 
Single turn object (string, int etc) is used as point of return from recursion.


"""

default_input_file = ''
default_output_file = ''

no_of_parameters = len(sys.argv)

if no_of_parameters == 1:
    f = open('awesome-transform.param')
    for lno, fname in enumerate(f):
        if lno == 0:
           default_input_file = fname.rstrip()
        else:
           default_output_file = fname.rstrip()
    f.close()

if no_of_parameters < 2:
    input_file = default_input_file
else:
    input_file = sys.argv[1]

if no_of_parameters < 3:
    output_file = default_output_file
else:
    output_file = sys.argv[2]

with open(input_file) as f:
    json_data = json.load(f)

def obj_rec(obj, t, flag=0,acc=''):
    v_obj = type(obj)
    r = ''
    if type(obj) not in [dict, list, map]:
        ref_url = re.findall(r'\((http.*?)\)', obj)
        ref_title = re.findall(r'\[[^\[\]]*\]', obj)
        if ref_url :
            url = ref_url[len(ref_url)-1].strip('[]')
            title = ref_title[len(ref_title)-1].strip('[]')
            url_title = title + ',' + url
        else:
            url = ''
            title = ''
            url_title = title + ',' + url
            return acc

        if acc:
            if flag == 0:
                return acc + '\n'
            else:
                return acc + url_title + ',' + '"' + t + '"'  + '\n'
        else:
            if flag == 0:
                return ',,"' + url_title + ',' + t + '"' + '\n'
            else:
                return ',' + url_title + ',' + '"' + t + '"'  + '\n'
    elif v_obj == list:
            if obj :
                return obj_rec(obj[1:], t, flag, obj_rec(obj[0], t , 1, acc))
            else:
                return acc
    elif v_obj == dict:
        if bool(obj):
            for o in obj:
                k = o
                oo = obj[o]
                if type(oo) in [list,dict]:
                    r = obj_rec(oo, t + ',' + o, 1, acc)
                    acc = ""
                else:
                    ref_url = re.findall(r'\((http.*?)\)', oo)
                    ref_title = re.findall(r'\[[^\[\]]*\]', oo)
                    if ref_url:
                        url = ref_url[len(ref_url) - 1].strip('[]')
                        title = ref_title[len(ref_title)-1].strip('[]')
                        url_title = title + ',' + url
                    else:
                        url = ''
                        title = ''
                        url_title = title + ',' + url
                    if not acc:
                        sep = ','
                    else:
                        sep = ''
                    if not url:
                        r = sep + url_title + ',' + '"' + t + ',' + k + '",\n'
                break
            del obj[k]
            if not obj:
                sep = '\n'
            else:
                sep = ''
            return obj_rec(obj, t, flag, acc + r + sep)
        else:
            return acc[:-1]
itemlist = []
for o in json_data:
    itemlist.append((obj_rec(json_data[o], o.split("(",1)[0])[1:]))

with open(output_file, 'w') as outfile:
    outfile.writelines(["%s\n" % item  for item in itemlist])