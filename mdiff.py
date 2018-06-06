#!/usr/bin/env python3
import sys
import re
import collections


class Markdown:
    def __init__(self, lines):
        self.lines = lines

    def parse_diff(self):
        self.diff_statuses = [0 for i in range(len(self.lines))]
        nr = -1
        for line in self.lines:
            nr += 1
            ret = re.search('^@@ ', line)
            if ret is not None:
                self.diff_statuses[nr] = None
                self.lines[nr] = ''
                continue
            ret = re.search('^---', line)
            if ret is not None:
                self.diff_statuses[nr] = None
                self.lines[nr] = ''
                continue
            ret = re.search('^\+\+\+', line)
            if ret is not None:
                self.diff_statuses[nr] = None
                self.lines[nr] = ''
                continue

            ret = re.search('^-', line)
            if ret is not None:
                self.diff_statuses[nr] = '-'
                self.lines[nr] = line.split("-", 1)[-1]
                continue
            ret = re.search('^\+', line)
            if ret is not None:
                self.diff_statuses[nr] = '+'
                self.lines[nr] = line.split("+", 1)[-1]
                continue
            ret = re.search('^@@ ', line)
            if ret is not None:
                self.diff_statuses[nr] = None
                self.lines[nr] = ''
                continue
            self.diff_statuses[nr] = ''
            self.lines[nr] = line.split(" ", 1)[-1]
        for i, line in enumerate(self.lines):
            self.lines[i] = re.compile(
                '\n$').sub('', line)

    def analyze_heading(self):
        self.headings = [0 for i in range(len(self.lines))]
        od_headings = collections.OrderedDict()
        # NOTE: 想定される#の数を最初に確保
        for i in range(0, 4):
            od_headings[i] = ''
        headeing_level = 0
        for i, line in enumerate(self.lines):
            ret = re.search('^#+', line)
            if ret != None:
                headeing_level = len(ret.group())
                od_headings[headeing_level] = re.compile(
                    '^#+\s*').sub('', line)
            self.headings[i] = '-'.join([od_headings[x]
                                         for x in range(1, headeing_level+1)]) if headeing_level > 0 else ''
        for i, line in enumerate(self.lines):
            print(self.headings[i])

    def analyze_output(self):
        for i, status in enumerate(self.diff_statuses):
            if status == '+':
                opening_tag = "<span style='color: #00aa00'>"
                closing_tag = "</span>"
                line = self.lines[i]
                line = self.diff_replace(line, opening_tag, closing_tag)
#                 line = set_link_src(line, label, "[" get_joined_heading() "]の変更")

    def diff_replace(self, line, opening_tag, closing_tag):
        # TODO
        pass

    def print_output(self):
        for i, j in zip(self.lines, self.diff_statuses):
            if j in {'+', ''}:
                print("{0}".format(i))


code_flag = False
lines = sys.stdin.readlines()
md = Markdown(lines)
md.parse_diff()
md.print_output()
md.analyze_heading()
md.analyze_output()
sys.exit(0)
# print(lines)
for line in lines:
    ret = re.search('^#+', line)
    if ret is not None:
        headeing_level = len(ret.group())
        print(headeing_level)
        print("ok" + ret.group() + line)
    ret = re.search(r'^\s*\*\s*', line)
    if ret is not None:
        print('list * ')
    ret = re.search('^```', line)
    if ret is not None:
        code_flag = not code_flag
        print("code"+str(code_flag))
