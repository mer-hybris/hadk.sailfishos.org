Creating the Sailfish OS Root Filesystem
========================================

Additional Packages for Hardware Adaptation
-------------------------------------------

Some additional packages are used to allow access to device features. These
middleware packages are usually built against droid-headers / libhybris, and
therefore need to be built separately for each target device:

+------------------------+--------------------------+--------------------------------------+
| Feature                | Source                   | Package                              |
+========================+==========================+======================================+
| Audio                  | pulseaudio-modules-droid | pulseaudio-modules-droid-$DEVICE     |
+------------------------+--------------------------+--------------------------------------+
| Sensors                | mer-packages/sensorfw    | sensorfw-qt5-hybris                  |
+------------------------+--------------------------+--------------------------------------+

Configuring the Kickstart File
------------------------------

Building the Image with MIC
---------------------------

Building a rootfs using remote repos:

  sudo mic create fs --arch armv7hl --tokenmap=RELEASE:latest,ARCH:armv7hl sfa-${DEVICE}.ks --record-pkgs=name,url
