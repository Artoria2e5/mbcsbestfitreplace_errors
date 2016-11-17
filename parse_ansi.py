#!/usr/bin/env python3
"""
Parse a file as specified by http://www.unicode.org/Public/MAPPINGS/VENDORS/MICSFT/WindowsBestFit/readme.txt.
"""
import sys

def parse_ansi(f):
    """Handles the outermost 'CODEPAGE'...'ENDCODEPAGE' part."""
    codepages = {}
    for l in f:
        l = l.split(';')[0]
        if l[0:8] == 'CODEPAGE':
            codepages[int(l.split()[1])] = parse_codepage(f)
    return codepages

def parse_codepage(f):
    mbtables = {}
    
    for l in f:
        l = l.split(';')[0]


if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            print(parse_ansi(f))
    else:
        print(parse_ansi(sys.stdin))
