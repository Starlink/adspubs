#!/usr/bin/env python3

"""
Convert standard input of form

BIBCODE1 BIBCODE2
BIBCODE1 STARDOC
STARDOC  BIBCODE2

to

BIBCODE1 BIBCODE2

where STARDOC will be the usually form of SUN/nnn or SGP/nnn
and not "sunnnn" or "sgpnnn".

Blank lines and lines starting with # are stripped.

  cat refs.txt | python3 expand-refs.py > newrefs.txt

"""

import fileinput
import os
import shutil
import collections

def lookslikebib(bibcode):
    if len(bibcode) != 19:
        return False
    if bibcode.startswith("1") or bibcode.startswith("2"):
        return True
    return False

mapfile = "../stardocs/star2bib.txt"

# Open the map file and get a dict
# with keys SUN/NNN and values the bibcode
starmap = {}
for line in open(mapfile):
    if line.isspace():
        continue
    line = line.strip()
    (formal, bibcode) = line.split(" ", 1)
    starmap[formal] = bibcode

# Read stdin replacing documents with bibcodes if possible
for line in fileinput.input():
    if line.isspace():
        continue
    line = line.strip()
    if line.startswith("#"):
        continue
    (bibcode1, bibcode2) = line.split(" ", 1)
    if bibcode1 in starmap:
        bibcode1 = starmap[bibcode1]
    if bibcode2 in starmap:
        bibcode2 = starmap[bibcode2]

    # Label items that do not look like they have been resolved
    # to bibcodes. Naive test for the moment
    unresolved = ""
    if not lookslikebib(bibcode1) or not lookslikebib(bibcode2):
        unresolved = " [*]"
    print("{} {}{}".format(bibcode1, bibcode2, unresolved))

