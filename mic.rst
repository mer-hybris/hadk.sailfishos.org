Creating the Sailfish OS Root Filesystem
========================================

Additional Packages for Hardware Adaptation
-------------------------------------------

Some additional packages are used to allow access to device features. These
middleware packages are usually built against droid-headers / libhybris, and
therefore need to be built separately for each target device. To build,
clone the repository via Git from either ``nemomobile`` or ``mer-hybris`` on
Github. See :doc:`middleware` for a list of all middleware components (not
all middleware components are used for all device adaptations).

Configuring the Kickstart File
------------------------------

The kickstart file is generated using ``ssuks``, which is part of the
SSU utility.

Patterns
--------

The selection of packages for each hardware adaptation has to be put into
a pattern file, so that the image build as well as any system updates in
the future can pull in and upgrade all packages related to the hardware
adaptation.

Building the Image with MIC
---------------------------

Building a rootfs using remote RPM repositories and a kickstart file:

.. code-block:: console

  MER_SDK $

  sudo mic create fs --arch armv7hl \
      --tokenmap=RELEASE:latest,ARCH:armv7hl sfa-${DEVICE}.ks \
      --record-pkgs=name,url

  sudo mic create fs --arch armv7hl \
      --tokenmap=RNDPATTERN:,RNDRELEASE:latest,ARCH:armv7hl,RELEASE:1.0.4.20 \
      --record-pkgs=name,url \
      --outdir=sfa-mako-ea \
      --pack-to=sfa-mako-ea.tar.gz \
      git/ks/sfa-mako-ea.ks
