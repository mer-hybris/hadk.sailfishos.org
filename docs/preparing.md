# Preparing Your Device

Verify that you can backup and restore your device and that you
understand device recovery options. This is not only useful when
flashing images you build with this guide, but also in case you want to
reset your device to its factory state with stock Android (note that not
all Android vendors provide factory images for download, so you might
need to create a full backup of your running Android system and store it
in a safe place before starting to erase and reflash the device with
your custom builds).

## Backup and Verify Your Device

As mentioned above, it might be helpful to backup the existing stock
Android image before flashing the **Android base** release for the first
time, as obtaining the stock image might be hard for some vendors (e.g.
some stock images are only available as self-extracting .exe package for
Windows) or impossible (some vendors do not provide stock images for
download).

Use Android Recovery (e.g. TWRP or ClockworkMod) to:

1.  Backup to SD card: system, data, boot and recovery partitions
2.  Test restoring the backup (important)

::: warning
::: title
Warning
:::

While backing up to internal device storage is possible for some
devices, if during porting you end up overwriting that partition, your
backups will be gone. In that case (and in case of devices without SD
card slots), it\'s better to also copy the backup data to your
development machine (e.g. via `adb pull` in recovery). Recent versions
of `adb` support full-device backups to a host computer using the
`adb backup` feature.
:::

See the [ClockworkMod
Instructions](https://forum.xda-developers.com/wiki/ClockworkMod_Recovery)
for additional help.

## Flash and Test your Android base image

Flash an image that you built or obtained of your **Android base**,
whether it\'s LineageOS, CAF, AOSP, or another.

The official LineageOS flashing instructions can be found on this
[LineageOS wiki page](https://wiki.lineageos.org/devices).

You may also want to verify that the **Android base** build for your
device is fully functional, to avoid wasting time with hardware
adaptations that have known issues. Also, your device might have some
hardware defects - testing in Android verifies that all components are
working correctly, so you have a functionality baseline to compare your
Sailfish OS build results with.

You should at least check the following features:

-   **OpenGL ES 2.0**: Use e.g. [Gears for
    Android](http://www.jeffboody.net/gears4android.php) to test (the hz
    you will get there will be max refresh rate).
-   **WLAN connectivity**: Connect to an AP, ad-hoc or set up a mobile
    access point with your device.
-   **Audio**: Headset detection, earpiece speaker, loudspeakers, etc.
-   **Bluetooth**: Connect to bluetooth headsets, verify
    discoverability, send files.
-   **NFC**: Check if NFC tags can be detected, read and/or written by
    the device.
-   **SD/MicroSD**: Use a file manager app to see if inserted SD cards
    can be detected.
-   **USB**: MTP, mass storage (if available) and `adb` access.
-   **Telephony**: 2G/3G/LTE calls + data connectivity.
-   **GPS**: Using [GPS
    Test](https://play.google.com/store/apps/details?id=com.chartcross.gpstest),
    check GLONASS too; typical time to fix; AGPS.
-   **Sensors**: Using
    [AndroSensor](https://play.google.com/store/apps/details?id=com.fivasim.androsenso):
    Accelerometer, Proximity Sensor, Ambient Light Sensor, Gyroscope,
    Magnetometer (Compass), Hall (flip case), \...
-   **LEDs**: If your device has notification LEDs or keypad backlights.
-   **Camera** (front and back): Also test functionality of zoom, flash,
    etc..
-   **Buttons**: Volume up, volume down, power, camera shutter, etc..
-   **Video out**: HDMI / MHL connectivity if you have the necessary
    adapters. TV out.
-   **Screen backlight**: Suspend and backlight control, minimum and
    maximum brightness.
-   **Battery meter**: Charge level, battery health, charging via USB
    (wall charger and host PC).
-   **Vibration motor**: Intensity, patterns.
-   **HW composer version**: check `dumpsys SurfaceFlinger` through ADB
    (see [SF Layer
    Debugging](http://bamboopuppy.com/dumpsys-surfaceflinger-layer-debugging/)).
-   **Fingerprint sensor**
-   **FM Radio**

We recommend that you write down the results of these tests, so you can
always remember them.
