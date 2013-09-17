#!/usb/bin/env perl

=head1 NAME

csv2ads -- Convert private CSV file to ADS format

=head1 SYNOPSIS

  csv2ads ./n03.csv

=head1 DESCRIPTION

Given a CSV file for a specific Starlink bulletin, generate
a file per entry in a format suitable for ingestion by ADS.

=head1 FORMAT

CSV file should have use the pipe symbol as a separator.
Columns should be

  title|authors|startpage|endpage|affiliation|references

Authors is in "Surname,Firstname;Surname2,Firstname2" format
Affiliation is in AA() AB() format.

  AA(Affil1) AB(Affil2)

References are space-separated bibcodes. Can also use Starlink
documentation numbers such as SGP/38. Also, to internally
reference another Starlink bulletin article we use a special
syntax of "SBn/pp" where n is the bulletin number and pp the
page number. An a or b suffix can be used to indicate whether
it is the first or second article on the page. They will
probably need to be fixed up manually for the ADS file.

 BIBCODE1 SGP/38 SB4/14b

=cut

use 5.014;
use strict;
use warnings;

use Data::Dumper;

my $csv = shift(@ARGV);

die "Please specify a CSV file"
  unless defined $csv;
die "Could not find file $csv"
  unless -e $csv;

open (my $fh, "<", $csv) || die "Could not open file $csv: $!";

# Read in each line. Assign the contents to a hash and put the
# hash ito an array indexed by page number so that if we have two
# entries for a page we can work it out
my @pages;
my @header;
while (defined ( my $line = <$fh>) ) {
  $line =~ s/\s*$//;

  my @items = split(/\|/, $line, -1); # Split maximally

  if (!@header) {
    # store the header
    @header = @items;
    next;
  }

  die "Line '$line' does not have same number of items [".@items."] as header [".@header."]"
    if (@items != @header);

  # create hash
  my %article;
  for my $i (0..$#header) {
    $article{$header[$i]} = $items[$i]
      if (defined $items[$i] && length($items[$i]));
  }

  my $index = $article{startpage};
  die "Must have a startpage"
    unless defined $index;

  push(@{$pages[$index]}, \%article);


}
close($fh);

# Now make the output files
for my $page (1..$#pages) { # Note that we will have filled using 1 to N as the index
  next unless defined $pages[$page];

  my $nperpage = scalar(@{$pages[$page]});
  my $n = 0;

  for my $art (@{$pages[$page]}) {
    my $letter = ($nperpage > 1 ? chr(ord("a")+$n) : "" );
    my $filename = sprintf("page%02d%s.txt", $page, $letter);

    open( my $fh, ">", $filename ) or die "Could not open file $filename: $!";

    # do not need to be incredibly generic here
    print $fh '%T '.$art->{title} ."\n";
    print $fh '%A '.$art->{authors}."\n";
    print $fh '%P '.$art->{startpage}."\n";
    print $fh '%L '.$art->{endpage}."\n";
    print $fh '%F '.$art->{affiliation}."\n";

    if (exists $art->{references}) {
      # space-separated
      my @refs = split(/\s+/, $art->{references}, -1);
      for my $i (0..$#refs) {
        my $str = '';
        if ($i == 0) {
          $str .= "%Z ";
        } else {
          $str .= "   ";
        }
        # For now do not do anything clever with SB references
        $str .= $refs[$i]."\n";
        print $fh $str;
      }

    }

    close($fh);

    $n++;
  }


}
