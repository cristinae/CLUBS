#!/usr/bin/env perl
#
# This file is part of moses.  Its use is licensed under the GNU Lesser General
# Public License version 2.1 or, at your option, any later version.
# 
# Modifications to deal with CLuBS corpus. Specifically, apostrophes for French
# and Catalan are considered. Besides, several moses scripts are merged here.
# Author: Cristina España-Bonet
# Date: 27/11/2016
#

use warnings;
use strict;

binmode(STDIN, ":utf8");
binmode(STDOUT, ":utf8");

my $language = "en";
my $PENN = 0;

while (@ARGV) {
    $_ = shift;
    /^-b$/ && ($| = 1, next); # not buffered (flush each line)
    /^-l$/ && ($language = shift, next);
    /^[^\-]/ && ($language = $_, next);
  	/^-penn$/ && ($PENN = 1, next);
}

while(<STDIN>) {
    s/\r//g;
    # remove extra spaces
    s/\(/ \(/g;
    s/\)/\) /g; s/ +/ /g;
    s/\) ([\.\!\:\?\;\,])/\)$1/g;
    s/\( /\(/g;
    s/ \)/\)/g;
    s/(\d) \%/$1\%/g;
    s/ :/:/g;
    s/ ;/;/g;
    # normalize unicode punctuation
    if ($PENN == 0) {
      s/\`/\'/g;
      s/\'\'/ \" /g;
    }

    s/„/\"/g;
    s/“/\"/g;
    s/”/\"/g;
    s/–/-/g;
    s/—/ - /g; s/ +/ /g;
    s/´/\'/g;
    s/([a-z])‘([a-z])/$1\'$2/gi;
    s/([a-z])’([a-z])/$1\'$2/gi;
    s/‘/\"/g;
    s/‚/\"/g;
    s/’/\"/g;
    s/''/\"/g;
    s/´´/\"/g;
    s/…/.../g;
    # French quotes
    s/ « / \"/g;
    s/« /\"/g;
    s/«/\"/g;
    s/ » /\" /g;
    s/ »/\"/g;
    s/»/\"/g;
    # handle pseudo-spaces
    s/ \%/\%/g;
    s/nº /nº /g;
    s/ :/:/g;
    s/ ºC/ ºC/g;
    s/ cm/ cm/g;
    s/ \?/\?/g;
    s/ \!/\!/g;
    s/ ;/;/g;
    s/, /, /g; s/ +/ /g;
    # remove non-printing chars
    s/\p{C}/ /g;
    # replace unicode punctuation
    s/，/,/g;
    s/。 */. /g;
    s/、/,/g;
    s/”/"/g;
    s/“/"/g;
    s/∶/:/g;
    s/：/:/g;
    s/？/\?/g;
    s/《/"/g;
    s/》/"/g;
    s/）/\)/g;
    s/！/\!/g;
    s/（/\(/g;
    s/；/;/g;
    s/１/"/g;
    s/」/"/g;
    s/「/"/g;
    s/０/0/g;
    s/３/3/g;
    s/２/2/g;
    s/５/5/g;
    s/６/6/g;
    s/９/9/g;
    s/７/7/g;
    s/８/8/g;
    s/４/4/g;
    s/． */. /g;
    s/～/\~/g;
    s/’/\'/g;
    s/…/\.\.\./g;
    s/━/\-/g;
    s/〈/\</g;
    s/〉/\>/g;
    s/【/\[/g;
    s/】/\]/g;
    s/％/\%/g;
 
    # English "quotation," followed by comma, style
    if ($language eq "en") {
	s/\"([,\.]+)/$1\"/g;
    }
    # Czech is confused
    elsif ($language eq "cs" || $language eq "cz") {
    }
    # German/Spanish/French "quotation", followed by comma, style
    else {
	s/,\"/\",/g;	
	s/(\.+)\"(\s*[^<])/\"$1$2/g; # don't fix period at end of sentence
    }

    # French apostrophes are separated in some corpora
    if ($language eq "fr") {
	s/c '/c'/g;
	s/d '/d'/g;
	s/j '/j'/g;
	s/l '/l'/g;
 	s/n '/n'/g;
 	s/s '/s'/g;
 	s/qu '/qu'/g;
 	s/C '/C'/g;
	s/D '/D'/g;
	s/J '/J'/g;
	s/L '/L'/g;
 	s/N '/N'/g;
 	s/S '/S'/g;
 	s/Qu '/Qu'/g;
    }

    #if ($language eq "de" || $language eq "es" || $language eq "cz" || $language eq "cs" || $language eq "fr") {
    #	s/(\d) (\d)/$1,$2/g;
    #}
    #else {
    #	s/(\d) (\d)/$1.$2/g;
    #}
    print "$_\n";
}
