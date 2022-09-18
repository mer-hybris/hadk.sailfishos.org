Publishing HADK
===============

Publishing a new version consists of the following steps.

1. Making changes
-----------------

HADK porting guide consists of several parts, which are written in
separate .rst files, using reStructuredText markup. This repository
contains an RPM spec file, so generating HTML version of the document
is as easy as `sfdk build`. The resulting document can then be found
under `_build/singlehtml` directory.

Once you are satisfied with your changes, you should commit them to
git, using commit messages with the following syntax:

    hadk: One line only short meaningful description for logs
    
    [hadk] One line only short meaningful description for logs. JB#XXXXX
    Longer description of what changed and why, in case the one line
    short description was not enough.

Once all the changes intended to be published are done, the version
number in conf.py needs to be updated. At this point it makes sense to
check all the Sailfish OS release numbers in the actual documentation
as well. Hint: grep the previous release number to find places which
potentially need updating.

After your PR has been approved, tag the merge commit using x.y.z tag.

2. Generating PDF
-----------------

As our Sailfish build environment does not contain all the necessary
tools for generating the PDF, this step needs to be done outside of
the SDK. In Debian derivatives you can install the required tools with
`apt install python3-sphinx`.

The repository contains a Makefile for generating the document in
different formats. The PDF format can be generated simply with command
`make latexpdf`. The resulting PDF can then be found under
`_build/latex` directory.

3. Publishing PDF
-----------------

The PDF is published in https://sailfishos.org/develop/hadk. The page
itself is hosted in WordPress.

4. Advertising new HADK version
-------------------------------

Once we have published a new version of HADK, we advertise it to
porters. This is done on the #sailfishos-porters IRC channel on OFTC
network. You can use e.g. the following format:

    PSA: New HADK released: https://sailfishos.org/develop/hadk
    Change log: https://paste.opensuse.org/...

You can use for example the following command to generate the
changelog:

    git diff $(git describe --tags --abbrev=0 HEAD~1)

Please note that the above command gives all changes - you need to
filter out unwanted changes, i.e. changes in conf.py or changes which
are not part of the public document. At the time of writing the public
document consists of all .rst files except factory.rst.
