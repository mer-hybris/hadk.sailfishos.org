Prerequisites
=============

.. _this link: https://github.com/mer-hybris/android/branches

Mobile Device
-------------

* An ARMv7 Android device officially supported by CyanogenMod 10.1.x, 11.0, or
  12.1 (at the time of writing 2015-09-11). Also check `this link`_

 - See http://wiki.cyanogenmod.org/w/Devices for a list of compatible devices

 * See https://wiki.merproject.org/wiki/Adaptations/libhybris for a status list
   of devices already ported using HADK

 * AOSP5 support (**hybris-aosp-5.1.0_r5**) is also available, however certain
   AOSP build aspects differ, and are left for porters to discover themselves

* Means to do backup and restore of the device contents (e.g. SD card or USB
  cable to host computer), as well as flash recovery images to the device

Build Machine
-------------

* A 64-bit x86 machine with a 64-bit Linux kernel

* Mer Platform SDK (installation explained later)

* Sailfish OS Target (explained later)

* At least 16 GiB of free disk space (10 GiB source download + more for
  building) for a complete Android build; a minimal download and HADK build
  (only hardware adaptation-related components) requires slightly less space

* At least 4 GiB of RAM (the more the better)

