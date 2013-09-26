Starlink Publications
---------------------

This repository contains a list of all Starlink publications in a format suitable
for ingesting into ADS. The hope is that we can crowd source the information from
the bulletins. References to other articles are included using %Z where appropriate.
If the bibcode is known then this is the best way of specifying a reference.

A CSV format is used to simplify the creation of the information. There is then a script
that can generate ADS format entries.

This covers

 * Enterprise Starlink Information Bulletin (#1 to #8)
 * Starlink Bulletins (#1 to #24)
 * Workshop proceedings (e.g. ADAM 1989)

Note that the Enterprise bulletins do not list an author.

Note that Starlink Bulletins 22 to 24 were foldout "brochure" style bulletins so don't
necessarily have individual authors (we list Giaretta & Currie as sole authors on the
Bulletins web site).

I've (@timj) tended not to include entries for the small editorial introductions to debate
articles. (see for example page 18 of bulletin 1).

Additionally we do include references to Starlink documents referenced by bulletin articles
as this provides a good way of linking all the documentation together.

It should be possible to generate Starlink document information automatically.
The main issue is working out how we handle the documents that are currently live (so SUN/95,
SC/21 etc).

We may have to add SUNs et al to ADS before the bulletins.

Starlink bulletins can currently be found at http://starlink.jach.hawaii.edu/starlink/Bulletins
