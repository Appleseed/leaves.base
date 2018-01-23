import sys
import json
import re

default_input_file = ''
default_output_file = ''

no_of_parameters = len(sys.argv)

if no_of_parameters == 1:
    f = open('awesome.param')
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
    if type(obj) not in [dict, list, map]:
        ref_url = re.findall(r'\((http.*?)\)', obj)
        if ref_url :
            url = ref_url[len(ref_url)-1].strip('[]')
        else:
            url = ''

        if acc:
            if flag == 0:
                return acc + '\n'
            else:
                return acc + url + ',' + '"' + t + '",'  + '\n'
        else:
            if flag == 0:
                return ',,"' + url +',' + t + '"'  + '\n'
            else:
                return ',' + url + ',' + '"' + t + '",'  + '\n'
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
                    if ref_url:
                        url = ref_url[len(ref_url) - 1].strip('[]')
                    else:
                        url = ''
                    if not acc:
                        sep = ','
                    else:
                        sep = ''
                    r = sep + url + ',' + '"' + t + ',' + k + '",\n'
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