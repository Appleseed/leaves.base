# Written by Jagannath Bilgi <jsbilgi@yahoo.com>

import sys
import tomd
from html.parser import HTMLParser
import Split_HTML_MD

"""
    "md_to_json" program needs input document to be purely in mmarkdown format. However markdown support mix of html and markdown.
    This program converts input document to pure markdown document by splitting html section (*_p1.html) and markdown section (*_p2.md).
    It removes images from html and converts to markdown using TagDropper.
    
    Special characters are removed using encode and decode function
    
    Finally merged *_Cp.md file is created 
"""

class TagDropper(HTMLParser):
    def __init__(self, tags_to_drop, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)
        self._text = []
        self._tags_to_drop = set(tags_to_drop)
    def clear_text(self):
        self._text = []
    def get_text(self):
        return ''.join(self._text)
    def handle_starttag(self, tag, attrs):
        if tag not in self._tags_to_drop:
            self._text.append(self.get_starttag_text())
    def handle_endtag(self, tag):
        self._text.append('</{0}>'.format(tag))
    def handle_data(self, data):
        self._text.append(data)

file1 = sys.argv[1]
d_file = file1 + ".md"
html_file = file1 + "_p1.html"
md_file = file1 + "_p2.md"
final_file = file1 + "_cp.md"


only_md = Split_HTML_MD.split_file(d_file, html_file, md_file)

if not only_md :
    with open(html_file, 'r') as f:
        html = f.read()

    td = TagDropper(['img','br'])
    td.feed(html)

    with open(final_file, 'w') as w, \
            open(md_file, 'r') as p2:
        w.write((tomd.Tomd(td.get_text()).markdown).encode('ascii', 'ignore').decode('ascii').replace("# ", "# " + file1).strip())
        w.write((p2.read()).encode('ascii', 'ignore').decode('ascii'))
else:
    with open(final_file, 'wb') as w, \
            open(d_file, 'rb') as p2:
        w.write((p2.read()).decode('ascii', 'ignore').encode('utf-8'))
