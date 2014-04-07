Preparing Your Device
=====================

Verify that you can restore your device and that you understand device
recovery options. This may be useful for deciding how to transfer WiP
images to your device.


Backup and Verify Your Device
-----------------------------

For some devices, it might be helpful to backup the stock image before flashing
the CM release for the first time, as getting the stock image might be hard for
some vendors (e.g. having to extract it from some windows .exe, or it simply
does not exist at all).

Use an Android/CyanogenMod Recovery to:

1. Backup to SD card: system, data, boot and recovery partitions

2. Test restoring the backup (important)

.. warning::

    While backing up to internal device storage is possible for some
    devices, if during porting you end up overwriting that partition,
    your backups will be gone. In that case (and in case of devices
    without SD card slots), it's better to also copy the backup data to
    your development machine (e.g. via ``adb pull`` in recovery).

See the `ClockworkMod Instructions`_ for additional instructions.

.. _ClockworkMod Instructions: http://wiki.cyanogenmod.org/w/ClockWorkMod_Instructions

Flash and Test CyanogenMod
--------------------------

Official flashing instructions can be found on this `CyanogenMod wiki page`_.

.. _CyanogenMod wiki page: http://wiki.cyanogenmod.org/w/Devices

You may also want to verify that the CM build for your device is fully
functional, to avoid wasting time with known not working hardware
adaptations. Also, the device you have might have some hardware
defects - testing in Android verifies that all components are
working correctly.

You should at least check the following features:

* **OpenGL ES 2.0**:
  Use e.g. `Gears4Android`_ to test
  (the hz you will get there will be max refresh rate).

* **WLAN connectivity**:
  Connect to an AP, ad-hoc or set up a mobile access point
  with your device.

* **Audio**:
  Headset detection, earpiece speaker, loudspeakers, etc.

* **Bluetooth**

* **NFC**

* **SD/MicroSD**

* **USB**:
  MTP, mass storage (if available) and ADB access.

* **Telephony**:
  2G/3G/LTE calls + data connectivity.

* **GPS**:
  Using `GPSTest`_, check GLONASS too; typical time to fix; AGPS.

* **Sensors**:
  Using `AndroSensor`_: Accelerometer, Proximeter, ALS, Gyroscope, Compass.

* **LEDs**

* **Camera** (front and back):
  Also test functionality of zoom, flash, etc..

* **Buttons**
  Volume up, volume down, power, camera shutter, etc..

* **Video out** (HDMI, S-Video)

* **Screen blanking**:
  Suspend and backlight control

* **Battery meter**:
  Charge level, battery health, charging via USB

* **Vibrator**

* **HW composer version**:
  check ``dumpsys surfaceflinger`` through ADB (see `SF Layer Debugging`_).

.. _Gears4Android: http://www.jeffboody.net/gears4android.php
.. _GPSTest: https://play.google.com/store/apps/details?id=com.chartcross.gpstest
.. _AndroSensor: https://play.google.com/store/apps/details?id=com.fivasim.androsenso
.. _SF Layer Debugging: http://bamboopuppy.com/dumpsys-surfaceflinger-layer-debugging/
