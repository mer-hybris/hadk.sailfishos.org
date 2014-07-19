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

Want to Port to a New Device?
-----------------------------

If you cannot find your gadget among the :doc:`devices`, from now on please
scrupuluosly follow :doc:`new-device-build`, clicking on all referenced chapters
as you go, and backtracking to where you left off when each chapter is finished.

The guide you are reading is supported-device-centric, hence its layout. We kindly
ask our pioneer porters of new devices to be patient and use sophisticated PDF
readers, which back/forward ability.

