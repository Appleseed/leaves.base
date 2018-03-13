# Written by Jagannath Bilgi <jsbilgi@yahoo.com>

"""
    Program return true if file content starts with '#'
    else creates 2 files. *_p1.html with HTML and *_p2.md with markdown
"""


def split_file(org_file, html_file, md_file):
    start_of_markdown = False
    with open(org_file, 'rb') as html_markdown:
        for line in html_markdown:
            if line.decode('ascii', errors='ignore')[0] == '#':
                return True
            else:
                break

    with open(org_file, 'rb') as html_markdown, \
         open(html_file, 'w') as p1, \
         open(md_file, 'w') as p2:

        start_of_markdown = False
        for line in html_markdown:
            if not start_of_markdown :
                if line.decode('ascii', errors='ignore')[0] == '#':
                    start_of_markdown = True
                    p2.write(line.decode('ascii', errors='ignore'))
                else:
                    p1.write(line.decode('ascii', errors='ignore'))
            else :
                p2.write(line.decode('ascii', errors='ignore'))
    return False