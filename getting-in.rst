Getting In
==========

Boot and Flashing Process
-------------------------

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

Telnet Boot Image
-----------------

