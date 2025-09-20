# Flashing the rootfs image

In order to be able to use Sailfish OS on the device, the parts that we
built and assembled in the previous chapters now need to be flashed to
the device. After flashing, Sailfish OS should boot on your device on
the next reboot.

## Prerequisites

-   Android Recovery flashed to your device
-   The stock firmware image (for your version and device)
-   The **Android base** release (for your version and device)
-   A Sailfish OS rootfs update .zip, created by `mic`

## Flashing back to Stock Android

It is important that you start with a fresh stock image that matches the
**Android base** release version you are going to flash (which in turn
is dictated by the Sailfish OS image you are going to flash).

While the **Android base** (e.g. CyanogenMod) .zip contains all files in
`/system/` (e.g. libraries and libhardware modules), the stock image
also contains firmware parts and flashables for partitions that are not
included in the **Android base** .zip.

For example, if you are running stock 4.4.2 on a Nexus 4 (mako), and you
are going to flash CM 10.1.3 and Sailfish OS to it, you have to first
flash the stock 4.2.2 (note that this is 4.2, not 4.4) first, so that
the firmware bits are matching the CM version.

If you do not flash the right stock version (and therefore firmware),
there might be some issues when booting into Sailfish OS:

-   Problems accessing `/sdcard/` in recovery (e.g. `adb push` does not
    work)
-   WLAN, sensors, audio and other hardware not working

If you experience such issues, please make sure you first flash the
stock system, ROM, followed by the **Android base** image, and finally
the Sailfish OS update. Please also note that you can\'t just take the
latest stock ROM and/or **Android base** ROM - both versions have to
match the Android version against which the Sailfish OS adaptation was
built.

## Flashing using Android Recovery

1.  Boot into Android Recovery
2.  Upload the CM release: `adb push cm-10.1.3-$DEVICE.zip /sdcard/`
3.  Upload Sailfish OS:
    `adb push sailfishos-$DEVICE-devel-1.2.3.4.zip /sdcard/`
4.  In the Recovery on the device:

> 1.  Clear data and cache (factory reset)
> 2.  Install the CM release by picking the CM image
> 3.  Install Sailfish OS by picking the SFOS image
> 4.  Reboot the device
