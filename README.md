Starlink Publications
---------------------

This repository contains a list of all Starlink publications in a format suitable
for ingesting into ADS. The hope is that we can crowd source the information from
the bulletins. References to other articles are included using %Z where appropriate.
If the bibcode is known then this is the best way of specifying a reference.

This covers

 * Enterprise Starlink Information Bulletin (#1 to #8)
 * Starlink Bulletins (#1 to #24)

Note that the Enterprise bulletins do not list an author.

Note that Starlink Bulletins 22 to 24 were foldout "brochure" style bulletins so don't
necessarily have individual authors (we list Giaretta & Currie as sole authors on the
Bulletins web site).

I've (@timj) tended not to include entries for the small editorial introductions to debate
articles. (see for example page 18 of bulletin 1).

Additionally we can include the standard Starlink documentation. It should be possible to generate
this information automatically from the `document.xml` entries in the main Starlink repository.
The main issue is working out how we handle the documents that are currently live (so SUN/95,
SC/21 etc).

Ideally bulletin articles that reference SUNs and SGPs (etc) should reference them using %Z entries
but it will probably be easiest to defer that until we know if SUNs et al are to be included in
ADS.

Starlink bulletins can currently be found at http://starlink.jach.hawaii.edu/starlink/Bulletins
