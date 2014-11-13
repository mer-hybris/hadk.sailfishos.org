Preparing Your Device
=====================

Verify that you can backup and restore your device and that you understand
device recovery options. This is not only useful when flashing images you
build with this guide, but also in case you want to reset your device to
its factory state with stock Android (note that not all Android vendors
provide factory images for download, so you might need to create a full
backup of your running Android system and store it in a safe place before
starting to erase and reflash the device with your custom builds).


Backup and Verify Your Device
-----------------------------

As mentioned above, it might be helpful to backup the stock image before
flashing the CM release for the first time, as getting the stock image might
be hard for some vendors (e.g. some stock images are only available as
self-extracting .exe package for Windows) or impossible (some vendors do not
provide stock images for download).

Use an Android/CyanogenMod Recovery to:

1. Backup to SD card: system, data, boot and recovery partitions

2. Test restoring the backup (important)

.. warning::

    While backing up to internal device storage is possible for some
    devices, if during porting you end up overwriting that partition,
    your backups will be gone. In that case (and in case of devices
    without SD card slots), it's better to also copy the backup data to
    your development machine (e.g. via ``adb pull`` in recovery). Recent
    versions of ``adb`` support full-device backups to a host computer
    using the ``adb backup`` feature.

See the `ClockworkMod Instructions`_ for additional help.

.. _ClockworkMod Instructions: http://wiki.cyanogenmod.org/w/ClockWorkMod_Instructions

Flash and Test CyanogenMod
--------------------------

The official CyanogenMod flashing instructions can be found on this `CyanogenMod wiki page`_.

.. _CyanogenMod wiki page: http://wiki.cyanogenmod.org/w/Devices

You may also want to verify that the CM build for your device is fully
functional, to avoid wasting time with hardware adaptations that have
known issues. Also, your device might have some hardware defects - testing
in Android verifies that all components are working correctly, so you have
a functionality baseline to compare your build results with.

You should at least check the following features:

* **OpenGL ES 2.0**:
  Use e.g. `Gears4Android`_ to test
  (the hz you will get there will be max refresh rate).

* **WLAN connectivity**:
  Connect to an AP, ad-hoc or set up a mobile access point
  with your device.

* **Audio**:
  Headset detection, earpiece speaker, loudspeakers, etc.

* **Bluetooth**:
  Connect to bluetooth headsets, verify discoverability, send files.

* **NFC**:
  Check if NFC tags can be detected, read and/or written by the device.

* **SD/MicroSD**:
  Use a file manager app to see if inserted SD cards can be detected.

* **USB**:
  MTP, mass storage (if available) and ``adb`` access.

* **Telephony**:
  2G/3G/LTE calls + data connectivity.

* **GPS**:
  Using `GPSTest`_, check GLONASS too; typical time to fix; AGPS.

* **Sensors**:
  Using `AndroSensor`_: Accelerometer, Proximity Sensor, Ambient Light
  Sensor, Gyroscope, Magnetometer (Compass).

* **LEDs**:
  If your device has notification LEDs or keypad backlights.

* **Camera** (front and back):
  Also test functionality of zoom, flash, etc..

* **Buttons**:
  Volume up, volume down, power, camera shutter, etc..

* **Video out**:
  HDMI / MHL connectivity if you have the necessary adapters. TV out.

* **Screen backlight**:
  Suspend and backlight control, minimum and maximum brightness.

* **Battery meter**:
  Charge level, battery health, charging via USB (wall charger and host PC).

* **Vibration motor**:
  Intensity, patterns.

* **HW composer version**:
  check ``dumpsys SurfaceFlinger`` through ADB (see `SF Layer Debugging`_).

.. _Gears4Android: http://www.jeffboody.net/gears4android.php
.. _GPSTest: https://play.google.com/store/apps/details?id=com.chartcross.gpstest
.. _AndroSensor: https://play.google.com/store/apps/details?id=com.fivasim.androsenso
.. _SF Layer Debugging: http://bamboopuppy.com/dumpsys-surfaceflinger-layer-debugging/

We recommend that you write down the results of these tests, so you can always remember them.
