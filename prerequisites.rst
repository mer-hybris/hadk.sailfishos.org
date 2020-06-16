Prerequisites
=============

.. _this link: https://github.com/mer-hybris/android/branches
.. _Xperia X (Sony AOSP 6): https://sailfishos.org/wiki/Sailfish_X_Build_and_Flash
.. _Xperia XA2 (Sony AOSP 8): https://sailfishos.org/wiki/DRAFT-Sailfish_X_Xperia_XA2_Build_and_Flash
.. _Xperia 10 (Sony AOSP 9): https://sailfishos.org/wiki/Sailfish_X_Xperia_Android_9_Build_and_Flash

Mobile Device
-------------

* An Android device officially supported by LineageOS 15.1 (Android 8) and 16.0
  (Android 9) at the time of writing 2019-09-30. CyanogenMod versions (that are Sailfish
  OS-compatible) 10.1.x, 11.0, 12.1, 13.0, 14.1 will require additional
  effort because CM has become obsolete.
  For more supported Android versions also check `this link`_

 - Throughout this guide we shall use the term **Android base**, which will
   refer to the appropriate base that you are porting on: LineageOS, AOSP, CAF etc

 * We also support Sony Open Devices program, and published guidelines how to
   rebuild flashable images for:

  - `Xperia X (Sony AOSP 6)`_

  * `Xperia XA2 (Sony AOSP 8)`_

  * `Xperia 10 (Sony AOSP 9)`_

 * Starting with CM 13.0 (Android 6), support for 64bit ARM has being added
   to Sailfish OS: achieved by running a mix of 64bit Linux Kernel and Android
   HAL, whilst Sailfish OS userspace is being run in the 32bit mode

 * See https://wiki.lineageos.org/devices for a list of compatible devices

 * See https://wiki.merproject.org/wiki/Adaptations/libhybris for a status list
   of devices already ported using HADK

 * See https://wiki.merproject.org/wiki/Adaptations/libhybris/porters for a list
   of ports in early stages, and their authors to contact on the IRC

 * AOSP or CAF Android base support is also possible, but we choose LineageOS
   for a wider range of devices. It will be up to the porter to patch an AOSP/CAF
   base with hybris patches. Remaining differences in using it are minimal (e.g.
   using the ``lunch`` command instead of ``breakfast``)

* Means to do backup and restore of the device contents (e.g. SD card or USB
  cable to host computer), as well as flash recovery images to the device

Build Machine
-------------

* A 64-bit x86 machine with a 64-bit Linux kernel

* Sailfish OS Platform SDK (installation explained later)

* Sailfish OS Platform SDK Target (explained later)

* At least 30 GiB of free disk space (20 GiB source download + more for
  building) for a complete Android build; a minimal download and HADK build
  (only hardware adaptation-related components) requires slightly less space.
  The newer the Android base version, the bigger the size requirements.

* At least 4 GiB of RAM (the more the better)

