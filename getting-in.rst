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

The **hybris-boot** repository contains such an initrd with convenient USB
networking, DHCP and telnet server, plus the ability to boot into a Sailfish
OS system. The init system in the hybris-boot initrd will attempt to write
information via the USB device serial number and model. So ``dmesg`` on the
host could produce::

 [1094634.238136] usb 2-2: Manufacturer: Mer Boat Loader
 [1094634.238143] usb 2-2: SerialNumber: Mer Debug setting up (DONE_SWITCH=no)

However ``dmesg`` doesn't report all changes in the USB subsystem and the init script will attempt to update the iSerial field with information so also do::

  $ lsusb -v | grep iSerial
   iSerial    3 Mer Debug telnet on port 23 on rndis0 192.168.2.15 - also running udhcpd

However, if it says something like::

 [1094634.238143] usb 2-2: SerialNumber: Mer Debug setting up (DONE_SWITCH=yes)

connectivity will be available via ``telnet 192.168.2.15 2323`` port.

Bootloops
`````````

If device bootloops, there might be several reasons:

* If it immediately reboots (and especially if it later boots to recovery mode),
  SELinux is enabled, and all ports based on Android 4.4 or newer need to disable
  it. Add ``CONFIG_SECURITY_SELINUX_BOOTPARAM=y`` to your kernel defconfig, and
  ``selinux=0`` to your kernel command line (usually in ``BOARD_KERNEL_CMDLINE``
  under $ANDROID_ROOT/device/$VENDOR/\*/BoardConfig\*.mk)
* If it reboots after a minute or so, be quick and telnet into device, then do::
 ln -s /dev/null /etc/systemd/system/ofono.service
* Check if your /system is mounted by systemd (system.mount unit)

Tips
````

To ease debugging in unstable/halting/logs spamming early ports::
 systemctl mask droid-hal-init
 systemctl mask user@100000

Get connected
`````````````
Use USB networking to connect to the Internet from your Sailfish OS

Execute on your host as root. Use the interface which your host uses
to connect to the Internet. It's wlan0 in this example::
 HOST $

 iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
 echo 1 > /proc/sys/net/ipv4/ip_forward

Execute on the device::
 TARGET $

 route add default gw 192.168.2.X (<- host's usb0 IP)
 echo 'nameserver 208.67.222.222' > /etc/resolv.conf


Splitting and Re-Assembling Boot Images
---------------------------------------

A **boot.img** file is basically a combination of a Linux kernel and an
initramfs as ``cpio`` archive. The Mer SDK offer the ``mkbootimg``
to build a boot image from a kernel and cpio archive. To split a boot
image, use ``split_bootimg`` in Mer SDK.

In the CyanogenMod-based Sailfish OS port, a boot image with Sailfish OS-
specific scripts will be built automatically. These boot images are then
available as **hybris-boot.img** (for booting into Sailfish OS) and
**hybris-recovery.img** (for debugging via telnet and test-booting).
