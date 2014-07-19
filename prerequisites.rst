Prerequisites
=============

.. _supported_devices:
 
Mobile Device
-------------

* An ARMv7 Android device officially supported by CyanogenMod 10.1.x

 - See http://wiki.cyanogenmod.org/w/Devices for a list of compatible devices

 * See :doc:`devices` for a list of devices already supported by HADK

* Means to do backup and restore of the device contents (e.g. SD card or USB
  cable to host computer), as well as flash recovery images to the device

Build Machine
-------------

* A 64-bit X86 machine with a 64-bit Linux kernel

* `Mer Platform SDK`_

* `Sailfish OS Target`_

* At least 16 GiB of free disk space (10 GiB source download + more for
  building) for a complete Android build; a minimal download and HADK build
  (only hardware adaptation-related components) requires slightly less space

* At least 4 GiB of RAM (the more the better)

.. _Mer Platform SDK: http://wiki.merproject.org/wiki/Platform_SDK

.. _Sailfish OS Target: http://releases.sailfishos.org/sdk/latest/targets/
