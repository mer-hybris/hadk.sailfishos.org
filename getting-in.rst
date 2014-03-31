Getting In
==========

Boot and Flashing Process
-------------------------

This varies from device to device. There are a few different boot loaders and
flashing mechanisms used for Android devices:

* **fastboot**: Used by most Nexus devices

* **odin**: Used by most Samsung devices

For flashing fastboot-based devices, use ``fastboot`` (available in the
Mer SDK), for odin-based devices, use `Heimdall`_.

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

The init system in the initrd will attempt to write information via
the usb device serial number and model. So 'dmesg' on the host could
produce::

 [1094634.238136] usb 2-2: Manufacturer: Mer Boat Loader
 [1094634.238143] usb 2-2: SerialNumber: Mer Debug setting up (DONE_SWITCH=no)

However dmesg doesn't report all changes in the usb subsystem and the init script will attempt to update the iSerial field with information so also do::

  $ lsusb -v | grep iSerial
   iSerial    3 Mer Debug telnet on port 23 on rndis0 192.168.2.1 - also running udhcpd

Splitting and Re-Assembling Boot Images
---------------------------------------

A **boot.img** file is basically a combination of a Linux kernel and an
initramfs as ``cpio`` archive. The Mer SDK offer the ``mkbootimg``
to build a boot image from a kernel and cpio archive. To split a boot
image, use ``split_bootimg`` in the SDK.

In the CyanogenMod-based Sailfish OS port, a boot image with Sailfish OS-
specific scripts will be built automatically. These boot images are then
available as **hybris-boot.img** (for booting into Sailfish OS) and
**hybris-recovery.img** (for debugging via telnet and test-booting).
