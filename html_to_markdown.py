import sys
import os
import platform
import tomd
from tomd import Tomd
from HTMLParser import HTMLParser
import Split_html_markdown

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

only_md = Split_html_markdown.split_file(d_file, html_file, md_file)

if not only_md :
    with open(html_file, 'r') as f:
        html = f.read()

    td = TagDropper(['img','br'])
    td.feed(html)

    with open(final_file, 'w') as w, \
            open(md_file, 'r') as p2:
        w.write(tomd.Tomd(td.get_text()).markdown)
        w.write(p2.read())
else:
    if platform.system() != 'Windows':
	os.system("mv %s %s"%(d_file,final_file))
    else:
	os.system("rename %s %s"%(d_file,final_file))