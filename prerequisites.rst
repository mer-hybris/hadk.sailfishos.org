Prerequisites
=============

.. _this link: https://github.com/mer-hybris/android/branches

Mobile Device
-------------

* An ARM Android device officially supported by CyanogenMod 10.1.x, 11.0,
  12.1, 13.0 (at the time of writing 2017-02-02). Also check `this link`_

 - Starting with CM 13.0 (Android 6), support for 64bit ARM is also being added
   to Sailfish OS: firstly by running a mix of 64bit Linux Kernel and Android
   HAL, whilst Sailfish OS userspace is being run in 32bit mode

 * We will gradually transition from CyanogenMod to Lineage OS, in the meantime
   please use https://archive.org for CM and the mirror for their ZIP downloads:
   https://www.reddit.com/r/Android/comments/5kfm8x/the_cyanogenmod_archives_full_downloads

 * See http://wiki.lineageos.org/devices.html for a list of compatible devices,
   as well as the exhaustive list:
   http://web.archive.org/web/20161225121104/https://wiki.cyanogenmod.org/w/Devices

 * See https://wiki.merproject.org/wiki/Adaptations/libhybris for a status list
   of devices already ported using HADK

 * See https://wiki.merproject.org/wiki/Adaptations/libhybris/porters for a list
   of ports in early stages, and their authors to contact on IRC

 * AOSP or CAF Android base support is also possible, but we chose CM/LineageOS
   for a wider range of devices. It will be up to the porter to patch an AOSP/CAF
   base with hybris patches. Remaining differences in using it are minimal (e.g.
   using the ``lunch`` command instead of ``breakfast``)

* Means to do backup and restore of the device contents (e.g. SD card or USB
  cable to host computer), as well as flash recovery images to the device

Build Machine
-------------

* A 64-bit x86 machine with a 64-bit Linux kernel

* Sailfish OS Platform SDK (installation explained later)

* Sailfish OS Target (explained later)

* At least 16 GiB of free disk space (10 GiB source download + more for
  building) for a complete Android build; a minimal download and HADK build
  (only hardware adaptation-related components) requires slightly less space

* At least 4 GiB of RAM (the more the better)

