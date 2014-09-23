#!/usr/bin/perl -i

# adapted from https://github.com/jmcnamara/XlsxWriter/blob/master/dev/release/modify_latex.pl

# Simple utility to modify the TeX output prior to creating a pdf file.

use strict;
use warnings;


while (<>) {

    # Convert escaped single quotes back to real single quote so that
    # the Latex upquote package has an effect.
    s/\\PYGZsq{}/'/g;


    print;

    # Modifiy the pre-amble. We could do this in the Sphinx conf.py
    # but ReadTheDocs doesn't support the fonts.
    if ( /^\\usepackage{sphinx}/ ) {
        print "\\usepackage{upquote}\n";
    }
}


__END__
