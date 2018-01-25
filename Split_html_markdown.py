def split_file(org_file, html_file, md_file):
    start_of_markdown = False
    with open(org_file, 'r') as html_markdown:
        for line in html_markdown:
            if line[0] == '#':
                return True
            else:
                break

    with open(org_file, 'r') as html_markdown, \
         open(html_file, 'w') as p1, \
         open(md_file, 'w') as p2:

        start_of_markdown = False
        for line in html_markdown:
            if not start_of_markdown :
                if line[0] == '#':
                    start_of_markdown = True
                    p2.write(line)
                else:
                    p1.write(line)
            else :
                p2.write(line)
    return False