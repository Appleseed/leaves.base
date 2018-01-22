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
    data = json.load(f)

output_line = ''
site_url = ''
for title in data:
    title_content = title.split("[",1)[0]
    for subTitle in data[title]:
        if subTitle[0] == '[':
            site_url = re.findall(r'\((http.*?)\)', subTitle)
            if site_url != []:
                output_line = output_line + " ".join(site_url) + ',' + '"' + title_content + '"' + "\n"
#                output_line = output_line + " ".join(site_url) + ',' + '"' + title + '"' + "\n"
        else:
            l = data[title][subTitle]
            if (type(data[title][subTitle]) is list) or (type(data[title][subTitle]) is dict):
                for subsubTitle in data[title][subTitle]:
                    if type(subsubTitle) is list:
                        for subsubdetails in subsubTitle:
                            site_url = re.findall(r'\((http.*?)\)', subsubdetails)
                            if len(site_url) > 0:
                                output_line = output_line + site_url[0].strip('[]') + ',' + '"' + title_content + ',' + subTitle + ',' + '"' + "\n"
    #                            output_line = output_line + site_url[0].strip('[]') + ',' + '"' + title + ',' + subTitle + ',' + '"' + "\n"
                            else:
                                tempvar2 = re.findall(r'\[.*?\]',subsubdetails)[0].strip('[]')
                                output_line = output_line + tempvar2 + ',' + '"' + title_content + ',' + subTitle + ',' + tempvar1 + '"' + "\n"
    #                            output_line = output_line + ',' + '"' + title + ',' + subTitle + ',' + '"' + "\n"
                    elif subsubTitle[0] == '[':
                        site_url = re.findall(r'\((http.*?)\)', subsubTitle)
                        if site_url != []:
                            ref_url = site_url[len(site_url)-1]
                            output_line = output_line + ref_url + ',' + '"' + title_content + ',' + subTitle + '"' + "\n"
    #                        output_line = output_line + " ".join(site_url) + ',' + '"' + title + ',' + subTitle + '"' + "\n"
                        else:
                            tempvar1 = re.findall(r'\[.*?\]',subsubTitle)[0].strip('[]')
                            output_line = output_line + tempvar1 + ',' + '"' + title_content + ',' + subTitle + ',' + '"' + "\n"
                    else:
                        err = 0
                        try:
                            l = data[title][subTitle][subsubTitle]
                        except TypeError:
                            err = 1

                        if err == 0:
                            for details in data[title][subTitle][subsubTitle]:
                                site_url = re.findall(r'\((http.*?)\)', details)
                                if site_url != []:
                                    output_line = output_line + " ".join(site_url) + ',' + '"' + title_content + ',' + subTitle + ',' + subsubTitle + '"' + "\n"
    #                               output_line = output_line + " ".join(site_url) + ',' + '"' + title + ',' + subTitle + ',' + subsubTitle + '"' + "\n"
                        else:
                            l = re.findall(r'\[.*?\]',subsubTitle)[0].strip('[]')
                            ref_url = re.findall(r'\((http.*?)\)', subsubTitle)[0].strip('[]')
                            output_line = output_line + ref_url + ',' + '"' + title_content + ',' + subTitle + ',' + l + '"' + "\n"
            else:
                ref_url = re.findall(r'\((http.*?)\)', l)
                if ref_url != []:
                    output_line = output_line + ref_url[len(ref_url)-1].strip('[]') + ',' + '"' + title_content + ',' + subTitle + '"' + "\n"
                else:
                    output_line = output_line + ',' + '"' + title_content + ',' + subTitle + '"' + "\n"

#print output_line
with open(output_file, 'w') as o:
     o.write(output_line)

