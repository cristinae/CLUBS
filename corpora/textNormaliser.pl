#!/usr/bin/env perl
#
# This file is part of moses.  Its use is licensed under the GNU Lesser General
# Public License version 2.1 or, at your option, any later version.
# 
# Modifications to deal with CLuBS corpus. Specifically, apostrophes for French
# and Catalan are considered. Besides, several moses scripts are merged here.
# Encoding issues dealt with UTF code points
# Author: Cristina España-Bonet
# Date: 27/11/2016
#

use warnings;
use strict;
use Encode;

binmode(STDIN, ":utf8");
binmode(STDOUT, ":utf8");

my $language = "en";
my $PENN = 0;

while (@ARGV) {
    $_ = shift;
    /^-b$/ && ($| = 1, next); # not buffered (flush each line)
    /^-l$/ && ($language = shift, next);
    /^[^\-]/ && ($language = $_, next);
}

while(<STDIN>) {
    s/\r//g;

    s/’/'/g;
    s/‘/'/g;
    s/´/\'/g;
    s/\xca\xbb/'/g;
    s/\xca\xbc/'/g;
    s/\xca\xbd/'/g;
    s/\xcb\x87/'/g;
    s/\xcc\x8d/'/g;
    s/\xcc\x92/'/g;
    s/\xcc\x93/'/g;
    s/\xcc\x94/'/g;
    s/\xcc\x95/'/g;
    s/\xcd\x80/'/g;
    s/\xcd\x81/'/g;
    s/\xcd\x83/'/g;
    s/\xe2\x80\x98/'/g;
    s/\xe2\x80\x99/'/g;
    s/\xe2\x80\x9b/'/g;
    s/\xe2\x80\xb2/'/g;
        
    
    s/„/\"/g;
    s/“/\"/g;
    s/”/\"/g;
    s/''/\"/g;
    s/´´/\"/g;
    s/\xcc\x8e/\"/g;
    s/\xcc\x8f/\"/g;
    s/\xe2\x80\x9c/\"/g;
    s/\xe2\x80\x9d/\"/g;
    s/\xe2\x80\x9e/\"/g;
    s/\xe2\x80\x9f/\"/g;
    s/\xe2\x80\xb3/\"/g;

    #commas
    s/，/,/g;
    s/、/,/g; 
    s/\xcc\x96/,/g;
    s/\xcc\x97/,/g;
    s/\xcc\x98/,/g;
    s/\xcc\x99/,/g;
    s/\xe2\x80\x9a/'/g;

    s/–/-/g;
    s/—/ - /g; 
    s/\xcc\xb5/-/g;
    s/\xcc\xb6/-/g;
    s/\xe2\x80\x90/-/g;
    s/\xe2\x80\x91/-/g;
    s/\xe2\x80\x92/-/g;
    s/\xe2\x80\x93/-/g;
    s/\xe2\x80\x94/-/g;
    s/\xe2\x80\x95/-/g;
    

    s/([a-z])‘([a-z])/$1\'$2/gi;
    s/([a-z])’([a-z])/$1\'$2/gi;

    s/…/.../g;
    s/\xe2\x80\xa5/.../g;
    s/\xe2\x80\xa6/.../g;
    
    # French quotes << >>
    s/ \xc2\xab / \"/g;
    s/\xc2\xab /\"/g;
    s/\xc2\xab/\"/g;
    s/ \xc2\xbb /\" /g;
    s/ \xc2\xbb/\"/g;
    s/\xc2\xbb/\"/g;
    
    # handle pseudo-spaces
    s/ \%/\%/g;
    s/nº /nº /g;
    s/ :/:/g;
    s/ ºC/ ºC/g;
    s/ cm/ cm/g;
    s/ \?/\?/g;
    s/ \!/\!/g;
    s/ ;/;/g;
    s/, /, /g; 
    s/ +/ /g;

    # remove non-printing chars
    s/\p{C}/ /g;


    # Halfwidth and Fullwidth Forms 
    s/。 */. /g;

    s/∶/:/g;
    s/：/:/g;
    s/\xef\xbc\x9a/:/g;
    
    s/？/\?/g;
    s/\xef\xbc\x9f/\?/g;
    s/！/\!/g;
    s/\xef\xbc\x81/\!/g;

    s/《/"/g;
    s/》/"/g;
    s/\xef\xbc\x82/\"/g;
    
    s/）/\)/g;
    s/\xef\xbd\xa0/\)/g;
    s/（/\(/g;    
    s/\xef\xbd\x9f/\(/g;

    
    s/；/;/g;
    s/\xef\xbc\x9b/;/g;

    s/」/"/g;
    s/\xef\xbd\xa3/"/g;
    s/\xef\xbe\xa4/"/g;
    s/「/"/g;
    s/\xef\xbd\xa2/"/g;
    s/\xef\xbe\xa1/"/g;

    
    s/０/0/g;
    s/１/1/g;
    s/２/2/g;
    s/３/3/g;
    s/４/4/g;
    s/５/5/g;
    s/６/6/g;
    s/７/7/g;
    s/８/8/g;
    s/９/9/g;
    s/\xef\xbc\x90/0/g;
    s/\xef\xbc\x91/1/g;
    s/\xef\xbc\x92/2/g;
    s/\xef\xbc\x93/3/g;
    s/\xef\xbc\x94/4/g;
    s/\xef\xbc\x95/5/g;
    s/\xef\xbc\x96/6/g;
    s/\xef\xbc\x97/7/g;
    s/\xef\xbc\x98/8/g;
    s/\xef\xbc\x99/9/g;
    
    s/． */. /g;

    s/\xcc\xb4/\~/g;
    s/ ̸/\//g;
    s/\xcc\xb7/\//g;
    s/\xcc\xb8/\//g;    
    
    s/━/\-/g;
    s/〈/\</g;
    s/〉/\>/g;
    s/【/\[/g;
    s/】/\]/g;
    s/％/\%/g;
    s/\xef\xbc\x85/\%/g;

    # remove extra spaces
    s/\(/ \(/g;
    s/\)/\) /g; s/ +/ /g;
    s/\) ([\.\!\:\?\;\,])/\)$1/g;
    s/\( /\(/g;
    s/ \)/\)/g;
    s/(\d) \%/$1\%/g;
    s/ :/:/g;
    s/ ;/;/g;
    
 
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

    if ($language eq "fr") {
	s/c '/c'/g;
	s/d '/d'/g;
	s/l '/l'/g;
	s/n '/n'/g;
	s/s '/s'/g;
	s/j '/j'/g;
	s/qu '/qu'/g;
	s/C '/C'/g;
	s/D '/D'/g;
	s/L '/L'/g;
	s/N '/N'/g;
	s/S '/S'/g;
	s/J '/J'/g;
	s/Qu '/Qu'/g;
    }

    #if ($language eq "de" || $language eq "es" || $language eq "cz" || $language eq "cs" || $language eq "fr") {
    #s/(\d) (\d)/$1,$2/g;
    #}
    #else {
    #s/(\d) (\d)/$1.$2/g;
    #}
    print "$_\n";
}
