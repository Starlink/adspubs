#!python

"""
Starlink Bulletin ADS entry generator

  python3 csv2ads.py n01.csv

Read a CSV format file (but using a | separator), and output it
in ADS format with all content in a single file.

Columns are:

title|authors|startpage|endpage|affiliation|references

affiliation and authors are already in ADS format.
References are space-separated.

We do attempt to generate a bibcode and
for the Starlink bulletins it will be something like:

1989StarB...3....2X
1989StarB...3G...2X

Where "G" is used for the supplement pages.

Program assumes that article information is found in
file "index.csv" volume information is found in "info.txt".

Author: Tim Jenness
Copyright: Tim Jenness
License: BSD 3-clause

"""

import sys

if len(sys.argv) != 2:
    print("Must supply a CSV file as argument")
    exit()


volfile = "info.txt"
filename = sys.argv[1]

sep = "---sep---"

bibroot = None

print("-*-Text-*-")
print()

# Start by dumping the table of contents record
for line in open(volfile):
    line = line.rstrip()
    if line.startswith("%R"):
        (key,bibroot) = line.split(" ")
        bibroot = bibroot[0:-6]
    print(line)

if bibroot is None:
    print("Failed to find bibcode in "+volfile)
    exit()

print(sep)

# Now read each line
for line in open(filename):
    if line.isspace():
        continue
    if line.startswith("title|"):
        continue
    print()
    line = line.rstrip()
    (title, authors, startpage, endpage, affil, refs) = line.split("|")

    # Handle supplement pages
    supp = "."
    bibpage = startpage
    if bibpage.startswith("G"):
        bibpage = bibpage[1:]
        supp = "G"

    # Determine the bib code as we want that to go first
    extradot = ""
    if int(bibpage) < 10:
        extradot = "."
    bibcode = bibroot + supp + ".." + extradot + bibpage + authors[0]
    print("%R "+bibcode)

    # From file
    print("%T "+title)
    print("%A "+authors)
    print("%P "+startpage)
    print("%L "+endpage)
    print("%F "+affil)

    refs.rstrip()
    if len(refs):
        allrefs = refs.split(" ")
        prefix = "%Z "
        for r in allrefs:
            print(prefix+r)
            prefix = "   "
    print()
    print(sep)
