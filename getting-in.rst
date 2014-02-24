Getting In
==========

Boot and Flashing Process
-------------------------

This varies from device to device. There are a few different boot loaders and
flashing mechanisms used for Android devices:

* **fastboot**: Used by most Nexus devices

* **odin**: Used by most Samsung devices

For flashing fastboot-based devices, use ``fastboot`` (available in the
Android SDK Tools package), for odin-based devices, use `Heimdall`_.

.. _Heimdall: http://glassechidna.com.au/heimdall/

Operating Blind on an Existing Device
-------------------------------------

Long story short, you will have to assume that you cannot:

* See any framebuffer console

* See any error messages of any kind during bootup

* Get any information relayed from your startup process

* Set any kind of modified kernel command lines

Hence, we have to learn how to operate blind on a device. The good news is that
when you have a working kernel, you can combine it with a init ramdisk and that
Android's USB gadget is built in to most kernel configurations. It is possible
then for the ramdisk to set up working USB networking on most devices and then
open up a telnet daemon.

The **hybris-boot** repository contains such a initrd with convenient
USB networking, DHCP and telnet server, plus the ability to boot into
a Sailfish OS system.

Splitting and Re-Assembling Boot Images
---------------------------------------

A **boot.img** file is basically a combination of a Linux kernel and an
initramfs as ``cpio`` archive. The Android SDK Tools offer the ``mkbootimg``
to build a boot image from a kernel and cpio archive. To split the boot
image, use `split_bootimg.pl`_.

.. _split_bootimg.pl: http://www.enck.org/tools/split_bootimg_pl.txt

In the CyanogenMod-based Sailfish OS port, a boot image with Sailfish OS-
specific scripts will be built automatically. These boot images are then
available as ``hybris-boot.img`` (for booting into Sailfish OS) and
``hybris-recovery.img`` (for debugging via telnet and test-booting).
