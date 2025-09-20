# Hardware Adaptation Checklist

Before publishing the adaptation, at least the following features should
be checked.

-   **Thermal sensor configuration for dsme**
    -   Even if we do not enforce any limits, CSD[^1] gets temperature
        info from dsme

    -   Quick test:

            dbus-send --system --print-reply --dest=com.nokia.thermalmanager \
                /com/nokia/thermalmanager com.nokia.thermalmanager.battery_temperature
-   **memnotify patch to kernel + config for mce**
    -   Memory pressure normalcritical affects for example browser

    -   Quick test:

            ls /etc/mce/*memnot*
-   **Watchdog driver in kernel + verify it works with dsme**
    -   We want the device to reboot if userspace gets hopelessly stuck

    -   Some android kernels use hardware watchdog for kernel stuck
        detection

    -   Quick test:

            journalctl -b | grep 'dsme.*watchdog'
-   **usb-moded works**
    -   Detects charger and PC correctly
-   **USB diag mode works (optional)**
    -   Only needed for factory releases, and not even always for those
-   **USB gadget driver in kernel + verify it works with buteo-mtp**
    -   Android has some MTP logic imlemented at kernel and thus some
        FFS stuff we need is typically missing
-   **ssu config files**
    -   Verify ssu & ssu-sysinfo agree on results
-   **Vibra driver in kernel**
    -   Patterns choose android vibra, LED vibra or ff-memless
        (memoryless force-feedback devices)
    -   ff-memless needs adding kernel driver
-   **Suspend works**
    -   If the device does not suspend, standby time will drop
        considerably
    -   There is a CSD test for this (Hardware tests-\>All
        tests-\>System state)
-   **Resume via iphb works**
    -   Only \"official\" way we have for scheduled wakeups from suspend
-   **Volume key probing & policy works**
    -   Display off -\> no ringing volume change should happen
    -   Display off -\> audio playback volume should change
    -   Both vol keys down -\> UI snapshot should happen
-   **Power key works**
    -   Long press power key menu
    -   Double presses
    -   Loooong press shutdown in dsme
    -   False double press reporting from a single press
-   **Proximity sensor works in suspend**
    -   We have built in assumption of having up-to-date p-sensor state
    -   NB: If device does not have PS -\> that must be configured
-   **Ambient light sensor works**
    -   Long sensor power up time -\> can break display power on
        brightness
    -   Kernel side filtering / odd delta reporting -\> breaks auto
        adjustments
    -   Total darkness should report \"zero lux\"
-   **LED works**
    -   Check the accuracy of colours and brightness
    -   Blocking at sysfs write can make mce unresponsive
    -   All but RGB LEDs probably require custom pattern config
-   **Proximity blanking during active call works**
    -   Some ports have weird problems here
-   **CSD config**
    -   HW features
    -   Factory test set
    -   Run-in test set
    -   Masked/blacklisted tests
-   **abootsettings etc. when applicable**
-   **Double tap works**
    -   There has been many devices where gestures are supported but
        touch driver uses odd concepts
-   **zram in kernel**
-   **Look out for suspicious logging during bootup / shutdown**
    -   Faster/slower/just different -\> odd things can/will happen
-   **usb-moded vs Android USB stuff in /\*.rc**
    -   Device serial number is assumed to come from Android side logic
    -   Otherwise Android stuff should preferably not touch USB in any
        way
-   **Touch reporting**
    -   Seems many Android kernels have issues around display power
        cycling & finger on screen
-   **Act dead mode**
    -   What Android services are needed varies from one device to
        another
    -   Act dead alarms need to be verified too
-   **Extra filesystems enabled in kernel where possible**
    -   BTRFS, F2FS, UDF, NFS, CIFS etc.

**Footnotes**

[^1]: You can start the CSD tool either via command line (`csd`) or via
    Settings app: Go to \"About Product\" and tap five times on the
    Build entry
