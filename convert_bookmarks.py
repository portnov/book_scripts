#!/usr/bin/python3

import sys
import re
import argparse
from collections import defaultdict

line_re = re.compile(r"^([ ]*)([^#]+)\s+#{0,1}([0-9]+)$")

EPILOG = """
Input format:

1 first chapter #10
  1.1 first section #11
    1.1.1 first subsection #12
  1.2 second section #13
2 second chapter #14
  2.1 first section #16
  2.2 second section #17

Hierarchy is defined by indents. Page numbers are placed after `#` sign.
"""

def parse_cmdline():
    parser = argparse.ArgumentParser(
                formatter_class=argparse.RawDescriptionHelpFormatter,
                description="Prepare bookmarks for DJVU or PDF document",
                epilog=EPILOG)
    parser.add_argument('-f', '--from', nargs=1, metavar='INDENTS|PDF', help='Input format of bookmarks', default=['INDENTS'])
    parser.add_argument('-t', '--to', nargs=1, metavar='DJVU|PDF|INDENTS', help='Output format of bookmarks: DJVU for Djvulibre format, or PDF for Pdftk format.', default=['DJVU'])
    parser.add_argument('-o', '--offset', nargs=1, metavar='OFFSET', type=int, help="Offset for page numbers", default=[0])
    parser.add_argument('input', metavar='INPUT.TXT', help='Path to input file')
    return parser.parse_args()

class Bookmark(object):
    def __init__(self, input_indent, name, page):
        self.input_indent = input_indent
        self.name = name
        self.page = int(page)
        self.children = []
        self.parent = None
        self.level = 0

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def apply_offset(self, offset):
        self.page = self.page + offset
        for child in self.children:
            child.apply_offset(offset)

    def __str__(self):
        return f"<[{self.level}] {self.name} - {self.page}>"

    def __repr__(self):
        return f"<Bookmark: {self.name}>"

    def calc_level(self):
        if self.parent is None:
            return 0
        else:
            return 1 + self.parent.level()

    def to_djvlibre(self, indent=0):
        prefix = "  " * indent
        if self.parent is None:
            start = "(bookmarks"
        else:
            start = prefix + f"(\"{self.name}\" \"#{self.page}\""
        if not self.children:
            return start + ")"
        children = [child.to_djvlibre(indent+1) for child in self.children]
        end = [prefix + ")"]
        lines = [start] + children + end
        return "\n".join(lines)

    def to_pdftk(self, level=0):
        if self.parent is not None:
            self_lines = []
            self_lines.append("BookmarkBegin")
            self_lines.append(f"BookmarkTitle: {self.name}")
            self_lines.append(f"BookmarkLevel: {level}")
            self_lines.append(f"BookmarkPageNumber: {self.page}")
        else:
            self_lines = []

        child_lines = [child.to_pdftk(level+1) for child in self.children]

        lines = self_lines + child_lines
        return "\n".join(lines)

    def to_indents(self, indent=0):
        prefix = "  " * indent
        if self.parent is not None:
            start = [prefix + f"{self.name}        #{self.page}"]
        else:
            start = []
        children = [child.to_indents(indent+1) for child in self.children]
        lines = start + children
        return "\n".join(lines)

    @staticmethod
    def parse_indents(path):

        def parse_line(line):
            m = line_re.match(line)
            if not m:
                raise Exception("Can not parse line:\n" + line)
            prefix, name, page = m.groups()
            return Bookmark(len(prefix), name.strip(), page)

        root = Bookmark(-1, "Root", 0)
        prev_bookmark = root

        for line in open(path):
            line = line.rstrip()
            if not line:
                continue

            bookmark = parse_line(line)

            if bookmark.input_indent > prev_bookmark.input_indent:
                prev_bookmark.add_child(bookmark)
            elif bookmark.input_indent == prev_bookmark.input_indent:
                prev_bookmark.parent.add_child(bookmark)
            else: # bookmark.input_indent < prev_bookmark.input_indent
                parent = prev_bookmark.parent.parent
                while bookmark.input_indent <= parent.input_indent:
                    parent = parent.parent
                parent.add_child(bookmark)
            
            prev_bookmark = bookmark
        
        return root

    @staticmethod
    def parse_pdftk(path):

        header_re = re.compile(r"^(\w+):\s+(.+)$")
        
        def parse_line(line):
            if line == 'BookmarkBegin':
                return line

            m = header_re.match(line)
            if not m:
                return None

            name, value = m.groups()
            return name, value

        root = Bookmark(0, "Root", 0)
        by_level = {0: root}
        bookmark = None

        def remember(b):
            item = by_level.get(b.level-1)
            if item:
                item.add_child(b)
                by_level[b.level] = b
            else:
                by_level[b.level-2].add_child(b)
                by_level[b.level-1] = b

        for line in open(path):
            line = line.rstrip()
            if not line:
                continue
            r = parse_line(line)
            if not r:
                continue
            if r == 'BookmarkBegin':
                if bookmark is not None:
                    remember(bookmark)
                bookmark = Bookmark(0, "Untitled", 0)
            else:
                name, value = r
                if name == 'BookmarkTitle':
                    bookmark.name = value
                elif name == 'BookmarkLevel':
                    bookmark.level = int(value)
                elif name == 'BookmarkPageNumber':
                    bookmark.page = int(value)

        remember(bookmark)
        
        return root

args = parse_cmdline()
from_format = getattr(args, 'from')[0].upper()
to_format = args.to[0].upper()

if from_format == 'INDENTS':
    bookmarks = Bookmark.parse_indents(args.input)
elif from_format == 'PDF':
    bookmarks = Bookmark.parse_pdftk(args.input)
else:
    sys.sterr.write("Unsupported input format: " + from_format + "\n")
    sys.exit(1)

bookmarks.apply_offset(args.offset[0])

if to_format == 'DJVU':
    print(bookmarks.to_djvlibre())
elif to_format == 'PDF':
    print(bookmarks.to_pdftk())
elif to_format == 'INDENTS':
    print(bookmarks.to_indents())
else:
    sys.sterr.write("Unsupported output format: " + args.to[0] + "\n")
    
