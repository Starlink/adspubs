#!python3

"""
Given a file in ADS format but which contains multiple entries

1. Create a file BIBCODE.txt for each entry
2. Extract out the references and write a separate
      BIBCODE1 [cites] BIBCODE2
   file.
3. Specifically for Starlink track how SUN/xxx maps to a
   specific bibcode. Write out a file with the mapping.
   This is not derivable as we do not know which year
   or author should be used so cannot trivially guess
   what SUN/95 maps into.

The reason for the references extraction is that ADS
does not reliably let you cite a bibcode that has not yet
been indexed and these files will inevitably reference
other entries in the file. The separate file allows the
references to be added later.

Author: Tim Jenness
Copyright: Tim Jenness
License: BSD 3-clause

"""

import re

filename = "adsformat.txt"
sep = "-" # separator character at start of line
inentry = 0 # Are we currently processing an entry
inabstract = 0
inrefs = 0     # Currently in references section
outfh = None
curbib = None  # Current bibcode
curfile = None # Current bibcode output file

reffile = open("starrefs.txt", "w", encoding="utf8")

ADS2STAR = {
    "StaUN": "SUN",
    "StaGP": "SGP",
    "StaSN": "SSN",
    "StarG": "SG",
    "StarC": "SC"
    }

star2bib = { }
starcodes = { }

for line in open(filename):
    #print (line)
    if line.isspace():
        if inabstract:
            print(file=curfile)
        continue
    if line.startswith(sep):
        inentry = 0
        inabstract = 0
        inrefs = 0
        curbib = None
        if curfile:
            curfile.close()
            curfile = None
        continue
    if line.startswith("%R"):
        # Definitely new entry
        inentry = 1
        inrefs = 0
        inabstract = 0

    line = line.rstrip()
    (key,value) = line.split(" ", 1)

    # Need to open the output file for each individual entry
    # and also need to determine the short code "SUN/??" for the
    # bibcode to short code mapping
    if key == "%R":
        # StaUN / StaGP / StarG / StaSN / StarC .NNN ..NN ...N
        match = re.search(r"\d\d\d\d(Sta\w\w)\.+(\d+)", value)
        if match:
            starclass = match.group(1)
            number = match.group(2)
            if starclass in ADS2STAR:
                # we store an additional set as tuples
                # so that we can sort them properly for output
                starcode = ADS2STAR[starclass] + "/" + number
                star2bib[starcode] = value
                starcodes[starcode] = ( ADS2STAR[starclass], int(number) )
        else:
            raise RuntimeError("String "+value+" does not look like Starlink bibcode")
        # Need to open the output file
        curbib = value
        print("Processing entry", value)
        curfile = open("bibcodes/"+curbib+".txt", "w", encoding="utf8")

    if key == "%B":
        inabstract = 1
    elif key.startswith("%"):
        inabstract = 0

    if key == "%Z":
        inrefs = 1

    # References all go to a single output file
    if inrefs:
        value = value.lstrip()
        print(curbib,value, file=reffile)
        continue

    print(key,value,file=curfile)

# Now that we've scanned through the whole file we can
# now write out the mapping file to go from Starlink code
# to ADS bibcode. Sort them for output.
mapfile = open("star2bib.txt", "w", encoding="utf8")

sorteddocs = sorted(starcodes.values())
for codetuple in sorteddocs:
    starcode = codetuple[0] + "/" + str(codetuple[1])
    print(starcode, star2bib[starcode], file=mapfile)


# Tidy up
mapfile.close()
reffile.close()

