#!/usr/bin/python3

import sys
import re

line_re = re.compile(r"^([ ]*)([^#]+)#([0-9]+)")

class Bookmark(object):
    def __init__(self, input_indent, name, page):
        self.input_indent = input_indent
        self.name = name
        self.page = page
        self.children = []
        self.parent = None

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def __str__(self):
        return f"<{self.name} - {self.page}>"

    def format(self, indent=0):
        prefix = "  " * indent
        if self.parent is None:
            start = "(bookmarks"
        else:
            start = prefix + f"(\"{self.name}\" \"#{self.page}\""
        if not self.children:
            return start + ")"
        children = [child.format(indent+1) for child in self.children]
        end = [prefix + ")"]
        lines = [start] + children + end
        return "\n".join(lines)

    @staticmethod
    def parse(line):
        m = line_re.match(line)
        if not m:
            raise Exception("Can not parse line:\n" + line)
        prefix, name, page = m.groups()
        return Bookmark(len(prefix), name.strip(), page)

INPUT=sys.argv[1]

root = Bookmark(-1, "Root", 0)
current_parent = root
prev_bookmark = root

for line in open(INPUT):
    line = line.rstrip()
    if not line:
        continue

    bookmark = Bookmark.parse(line)

    if bookmark.input_indent > prev_bookmark.input_indent:
        prev_bookmark.add_child(bookmark)
    elif bookmark.input_indent == prev_bookmark.input_indent:
        prev_bookmark.parent.add_child(bookmark)
    else: # bookmark.input_indent < prev_bookmark.input_indent
        prev_bookmark.parent.parent.add_child(bookmark)
    
    prev_bookmark = bookmark

print(root.format())

