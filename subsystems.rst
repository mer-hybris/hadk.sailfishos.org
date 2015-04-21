Detailed subsystem adaptation guides
####################################

Mer / Sailfish OS uses some kernel interfaces directly, bypassing the android
HAL. Mainly this is used in places where the kernel API is stable enough and
also used by Android. The other reasons for using kernel APIs directly include
better features offered by standard kernel frameworks, differing middleware
between Mer / Sailfish OS linux and Android, and lastly special features of
Sailfish OS.

Vibration / force feedback
**************************

The default vibra framework that is used in full featured productized Sailfish
OS devices is the force feedback API in kernel input framework. The kernel
drivers should either use the ffmemless framework OR provide FF_PERIODIC and
FF_RUMBLE support via as a normal input driver. In this chapter we go through
the ff-memless aproach of adapting your kernel for Mer/Sailfish OS

This is a different method than what is used in community Sailfish OS ports,
which utilize the android vibrator / timed-output API. The android vibrator
plugins in Mer/Sailfish OS middleware have very reduced feature set, and are
not recommended for commercial products.

In order to utilize the standard input framework force feedback features of
Sailfish OS, the android timed output vibrator kernel driver needs to be
converted to a ffmemless driver. The main tasks for this are:

* Enable CONFIG_INPUT_FF_MEMLESS kernel config option
* Disable CONFIG_ANDROID_TIMED_OUTPUT kernel config option
* Change maximum amount of ffmemless effects to **64** by patching ff-memless.c:
 * http://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/tree/drivers/input/ff-memless.c#n41

.. code-block:: c

 diff --git a/drivers/input/ff-memless.c b/drivers/input/ff-memless.c
 index 117a59a..fa53611 100644
 --- a/drivers/input/ff-memless.c
 +++ b/drivers/input/ff-memless.c
 @@ -39,7 +39,7 @@ MODULE_AUTHOR("Anssi Hannula <anssi.hannula@gmail.com>");
  MODULE_DESCRIPTION("Force feedback support for memoryless devices");
  
  /* Number of effects handled with memoryless devices */
 -#define FF_MEMLESS_EFFECTS     16
 +#define FF_MEMLESS_EFFECTS     64
  
  /* Envelope update interval in ms */
  #define FF_ENVELOPE_INTERVAL   50


* If your platform happens to already support a ffmemless based vibra driver,
  just enable it and fix any issues that you see. Otherwise go through the rest
  of the points below.
* Convert the android timed output vibra driver to support to ffmemless
 * add "#include <linux/input.h>"
 * Create a ffmemless play function.
 * Examples of ffmemless play functions / ffmemless drivers:
  * http://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/tree/drivers/input/misc/arizona-haptics.c#n110
  * http://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/tree/drivers/input/misc/max8997_haptic.c#n231
  * http://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/tree/drivers/input/misc/pm8xxx-vibrator.c#n130
 * At probe, create a ffmemless device with **input_ff_create_memless**
  * http://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/tree/include/linux/input.h#n531
 * And register the resulting device with input_device_register.
 * Remeber to clean up the input device structure at driver exit
 * The example ffmemless drivers above can be used for reference

The userspace configuration haptic feedback and effects is handled with ngfd
configuration files, see more details in

* :ref:`hapticconfiguration`

Camera
******

TODO

Cellular modem
**************

TODO

Bluetooth
*********

For bluetooth Sailfish OS uses BlueZ stack from linux.

TODO: bluetooth adaptation guide.

TODO: add detail about audio routing.


WLAN
****

Typically WLAN drivers are external kernel modules in android adaptations. To
set up WLAN for such devices, a systemd service file needs to be created
that loads the kernel module at boot. In addition to this you need to check that
firmware files and possible HW tuning files are installed in correct locations
on the filesystem.

Mer / Sailfish OS WLAN adaptation assumes the driver is compatible with WPA
supplicant. This means the WLAN device driver has to support cfg80211 interface.
In some cases connman (the higher level connection manager in Mer/Sailfish)
accesses directly the WLAN driver bypassing wpa_supplicant.

The version of currently used wpa_supplicant can be checked from here:

 https://github.com/mer-packages/wpa_supplicant

The version of used connman can be checked from here:

 https://github.com/mer-packages/connman

Special quirks: WLAN hotspot
============================

On some android WLAN drivers, the whole connectivity stack needs to be reset
after WLAN hotspot use. For that purpose there is reset service in dsme, please
see details how to set that up for your adaptation project in here:

 https://github.com/nemomobile/dsme/commit/c377c349079b470db38ba6394121b6d899004963

NFC
***

Currently there is no NFC middleware in Sailfish OS. Android HAL API support
should be enough for future compatibility.

GPS
***

TODO

Audio
*****

For audio, Mer / Sailfish OS uses pulse audio as the main mixer. For audio
routing ohmd is used.

TODO: Add info about audio routing configuration
TODO: Add more info in general.

Sensors
*******

TODO

Power management
****************

Under the hood, Sailfish OS uses the android wake locks. Typically there is
no need to change anything in the kernel side (assuming it works fine with
android) for the power management to work, as long as all the device drivers
are working normally.

The userspace API's for platform applications is exposed via nemo-keepalive
package. See more details here:

 https://github.com/nemomobile/nemo-keepalive

Watchdog
********

A standard linux kernel `watchdog core driver <http://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/tree/Documentation/watchdog/watchdog-kernel-api.txt>`_ support is expected. The
device node should be in /dev/watchdog. It should be configured with following
kernel options:

.. code-block:: console

   CONFIG_WATCHDOG=y
   CONFIG_WATCHDOG_CORE=y
   CONFIG_WATCHDOG_NOWAYOUT=y

* **NOTE 1**: Please note that watchdog driver should disable itself during suspend.

* **NOTE 2**: Normally the watchdog period is programmed automatically, but if your driver does not support programming the period, the default kicking period is 20 seconds.

Touch
*****

Sailfish OS is compatible with standard kernel multitouch input framework
drivers. Protocol A is preferred. The main configuration needed is to symlink
the correct event device node to /dev/touchscreen. To do this the best way is
to set up a udev rule that checks the devices with evcap script and creates the
link once first valid one is found. See more details for evcap here:

 https://github.com/mer-hybris/evcap

The udev rule can be put to file

 /lib/udev/rules.d/61-touchscreen.rules

The reason this is not done by default is that typically driver authors
mark bit varying capabilities as supported and there could be multiple
touch controllers on a device, so the final rule is best to be written
in a device specific configs package.

NOTE: if you still have problems with touch, please check that lipstick
environment has correct touch device parameter:

 cat /var/lib/environment/compositor/droid-hal-device.conf

* **LIPSTICK_OPTIONS** should have **"-plugin evdevtouch:/dev/touchscreen"**

Special feature: double tap to wake up
======================================

Sailfish OS supports waking up the device from suspend (unblanking the screen)
via double tap gesture to the touchscreen. The touchscreen driver should either
emulate KEY_POWER press / release or post a EV_MSC/MSC_GESTURE event with value
0x4 when double tap gesture is detected when waking up from suspend.

In order to avoid excess power drain when device is in pocket facing users
skin, some sysfs should be exported to allow disabling the touch screen. The
feature requires that the device has a working proximity sensor that can
wake up the system when it is suspended (to be able to update touch screen
state according to need). To configure MCE that handles this see
:ref:`mceconfiguration`

