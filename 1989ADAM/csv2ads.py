#!python

"""
Read a CSV format file (but using a | separator), and output it
in ADS format with all content in a single file.

Columns are:

title|authors|startpage|endpage|affiliation|references

affiliation and authors are already in ADS format.
References are space-separated.

We do attempt to generate a bibcode and
for the 1989 ADAM workshop it will be something like

1990adam.proc...nnI

Noting that the proceedings were published in January 1990.

"nn" is the first page number and "I" is the first letter of the first
author surname.

Author: Tim Jenness
Copyright: Tim Jenness
License: BSD 3-clause

"""

filename = "index.csv"
sep = "---sep---"

# Start by dumping the table of contents record
print("""
%R 1990adam.proc.....C
%T Proceedings of the 1989 ADAM Workshop
%A Chipperfield, Alan
%J Proceedings of the 1989 ADAM Workshop,
   held in Cosener's House, Abingdon from 3rd to 7th July 1989.
   Ed: A. Chipperfield,
   Starlink Project.
%C Science and Technology Facilities Council
%D 01/1990

""")

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

    # Determine the bib code as we want that to go first
    extradot = ""
    if int(startpage) < 10:
        extradot = "."
    bibcode = "1990adam.proc..." + extradot + startpage + authors[0]
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
