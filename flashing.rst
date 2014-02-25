Flashing the rootfs image
=========================

In order to be able to use Sailfish OS on the device, the parts that we built
and assembled in the previous chapters now need to be flashed to the device.
After flashing, Sailfish OS should boot on your device on the next reboot.

Prerequisites
-------------

* Android Recovery flashed to your device

* The vanilla CM release (for your version and device)

* A SailfishOS rootfs update .zip, created by ``mic``

Flashing using Android Recovery
-------------------------------

1. Boot into Android Recovery

2. Upload the CM release: ``adb push cm-10.1.3-$DEVICE.zip /sdcard/``

3. Upload Sailfish OS: ``adb push sailfishos-$DEVICE-devel-1.2.3.4.zip /sdcard/``

4. In the Recovery on the device:

 1. Clear data and cache (factory reset)

 2. Install the CM release by picking the CM image

 3. Install Sailfish OS by picking the SFOS image

 4. Reboot the device
