Middleware
==========

This chapter contains some background information about the middleware parts
that are part of the Hardware Adapation. Using this info, it should be possible
to customize and build the middleware parts for a given device.


MCE libhybris Plugin
--------------------

TODO

.. _mceconfiguration:

MCE configuration
-----------------

**/etc/mce/60-doubletap-jolla.ini**

Configures the touchscreen kernel driver sysfs that can be used to disable
and enable double tap to wake up feature. Example of its content:

.. code-block:: ini

    # Configuration for doubletap wakeup plugin
    [DoubleTap]
    # Path to doubletap wakeup control file
    ControlPath=/sys/bus/i2c/drivers/touch_synaptics/3-0020/double_tap_enable
    # Value to write when enabling doubletap wakeups
    EnableValue=1
    # Value to write when Disabling doubletap wakeups
    DisableValue=0

TODO:

**/etc/mce/60-mce-cpu-scaling-governor.ini**

**/etc/mce/60-mce-display-blank-timeout.conf**

**/etc/mce/60-mce-display-brightness.conf**

**/etc/mce/60-mce-possible-display-dim-timeouts.conf**

**/etc/mce/60-memnotify-jolla.conf**


.. _hapticconfiguration:

Non-Graphical Feedback Daemon (NGFD)
------------------------------------

The `Non-Graphical Feedback Daemon <https://github.com/sailfishos/ngfd>` provides combined audio, haptic, and LED
feedback for system events and alarms. These events include such things as
ring tones, message tones, clock alarms, email notifications, etc.

From here on shortened to NGFD.

TODO: add more detail about configuring NGFD.

Configuring Haptics
^^^^^^^^^^^^^^^^^^^

Sailfish OS uses **NGFD** to provide haptic feedback. We use a **QtFeedback**
plugin to bridge it with NGFD.
The NGFD plugin is for providing feedback for events and alarms, it interfaces directly
with QtFeedback that can be used by 3rd-party applications.

When configuring haptics it is important to know if your device uses
ffmemless or the LED/Droid based vibrator interface.

To determine if your device uses the LED/native interface check for
`/sys/class/timed_output/vibrator/enable` or `/sys/class/leds/vibrator/activate`.
The exact path for these might be a little different in some cases, e.g. instead of
`vibrator` the path could contain `foobar`, `foobar` being the device name in this case.
Check for down below :ref:`Non-Graphic Feedback Daemon Native Vibrator Plugin<non-graphic-feedback-daemon-native-vibrator-plugin>` for more.

If these files are not present it is very likely that your device uses
ffmemless to control haptics. To verify if your device uses ffmemless
install the `mce-tools` package and run `evdev\_trace -i`.
If the listing contains a device with the type `EV_FF` then your device
uses ffmemless.

The **qt5-feedback-haptics-ffmemless** used before **Sailfish OS 4.3** is deprecated in favor of the before mentioned QtFeedback plugin.

When migrating away from **qt5-feedback-haptics-ffmemless** /usr/lib/qt5/plugins/feedback/ffmemless.ini
can be removed without further intervention.

You can copy the Configuration file of the specific plugin used by your
device to tune it fit better to your device.

The reason we have possibility for device specific effects is that hardware
mechanics and the vibra engines differ greatly device-by-device, and single
settings will not give good effect on all devices.

Good guideline for VKB haptic is that it should be as short as possible, and
vibrate at the resonance frequency of the device mechanics when vibra engine
reaches top magnitude of the vibra effect. It should not feel like vibration,
but like a single kick.

NGFD PulseAudio Plugin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

TODO

NGFD ffmemless Plugin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the main plugin handling vibra feedback for Sailfish OS for devices that use the ffmemless interface.

The default configuration file can be found in `/usr/share/ngfd/plugins.d/50-ffmemless.ini <https://github.com/sailfishos/ngfd/blob/master/data/plugins.d/50-ffmemless.ini>`.

The default configuration files can be over-ridden with setting environment
variable `NGF_FFMEMLESS_SETTINGS`.

To set the environment variables add environment config file to your config
package that installs to. Replace with your `<device>` with the name
of your device. E.g. mako, hammerhead etc.

 /var/lib/environment/nemo/60-<device>-vibra.conf

And that file should look like below:


.. code-block:: sh

   NGF_FFMEMLESS_SETTINGS=/usr/share/ngfd/plugins.d/ngf-vibra-<device>.ini

Now you can use the file to tune force feedback effects suitable
specifically for your device. For template to start making your own
configuration files, just copy-paste the ngfd `50-ffmemless.ini <https://github.com/sailfishos/ngfd/blob/master/data/plugins.d/50-ffmemless.ini>`
default config files as the device specific files and then edit only needed
bits.

An alternative instead of using the environment variable is duplicating
the `50-ffmemless.ini` in the same folder with a different name such
as `51-ffmemless.ini`, NGFD will now pickup your configuration file
instead of the stock configuration file.

This especially affects those devices using ffmemless CUSTOM vibration patterns,
read the default 50-ffmemless.ini.
To check if the device uses ffmemless custom vibration patterns check
if `evdev\_trace` contains a device that contains `FF_CUSTOM`.

.. _non-graphic-feedback-daemon-native-vibrator-plugin:

Non-Graphic Feedback Daemon Native Vibrator Plugin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This plugin uses the native kernel interface from the timed output driver or the
led vibrator interface. The native plugin doesn't require any configuration normally.

It is possible to set the path of the activation and duration controls as shown
below if the plugin can't find these on its own:

.. code-block:: ini

   [droid-vibrator]
   native.path          = /sys/class/leds/<device>/duration
   native.activate_path = /sys/class/leds/<device>/activate

Replace `<device>` with the name of device directory for your vibration
device.

It is the preferred method if the ffmemless plugin isn't used.

NGFD Droid Vibrator Plugin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is a secondary vibra plugin for demoing and quick ports. It works out
of the box with android timed output drivers. The feature set is reduced
compared to ffmemless plugin.

TODO

PulseAudio Droid Modules
------------------------

TODO - more information about how PA works


Qt5 Hardware Composer QPA
-------------------------

This Qt Platform Abstraction plugin makes use of the libhardware hwcomposer API to
send rendered frames from the Wayland Compositor to the actual framebuffer. While
for some older devices, just flipping the fbdev was enough, more recent devices
actually require using hwcomposer to request flipping and for vsync integration.

The important environment variables are:

 * ``EGL_PLATFORM``: For the Wayland Compositor, this
   needs to be set to ``fbdev`` on devices with older hwcomposer versions, and
   to ``hwcomposer`` for hwcomposer version 1.1 and newer. For best results,
   first try ``fbdev``, and if it doesn't work, try ``hwcomposer`` instead.
   For the Wayland Clients, this always needs to be set to ``wayland``.
 * ``QT_QPA_PLATFORM``: For the Wayland Compositor, this needs to be set to
   ``hwcomposer`` to use the plugin. Previously, ``eglfs`` was used, but the
   ``hwcomposer`` module replaces the old plugin on Sailfish OS on Droid. For
   Wayland Clients, this always needs to be set to ``wayland``.

When starting up an application (e.g. the Wayland Compositor, ``lipstick``), the
systemd journal (``journalctl -fa`` as user root) will show some details about
the detected screen metrics, which will come from the framebuffer device:

.. code-block:: console

    HwComposerScreenInfo:251 - EGLFS: Screen Info
    HwComposerScreenInfo:252 -  - Physical size: QSizeF(57, 100)
    HwComposerScreenInfo:253 -  - Screen size: QSize(540, 960)
    HwComposerScreenInfo:254 -  - Screen depth: 32

Also, it will print information about the hwcomposer module and the device. In
this specific case, the hwcomposer version is 0.3:

.. code-block:: console

    == hwcomposer module ==
    * Address: 0x40132000
    * Module API Version: 2
    * HAL API Version: 0
    * Identifier: hwcomposer
    * Name: Qualcomm Hardware Composer Module
    * Author: CodeAurora Forum
    == hwcomposer module ==
    == hwcomposer device ==
    * Version: 3 (interpreted as 30001)
    * Module: 0x40132000
    == hwcomposer device ==

The source tree contains different implementations of hwcomposer backends, each
one for a different hwcomposer API version (see
``hwcomposer/hwcomposer_backend.cpp``). Based on that detection, one of the
existing implementations is used. Right now, the following implementations exist:

* *hwcomposer_backend_v0*: Version 0.x (e.g. 0.3) of the hwcomposer API. It can
  handle swapping of an EGL surface to the display, doesn't use any additional
  hardware layers at the moment and can support switching the screen off. The VSync
  period is queried from the hwcomposer device, but it will fall back to 60 Hz if
  the information cannot be determined via the libhardware APIs.
  (``EGL_PLATFORM=fbdev``)

* *hwcomposer_backend_v10*: Version 1.0 of the hwcomposer API. It supports one
  display device, handles VSync explicitly and uses a single hardware layer that
  will be drawn via EGL (and not composed via hwcomposer). Swapping is done by
  waiting for VSync and uses libsync-based synchronization of posting buffers.
  Switching the screen off is also supported, and sleeping the screen disables
  VSync events. Also, the same VSync period algorithm is used (try to query from
  libhardware, fall back to 60 Hz if detection fails).
  (``EGL_PLATFORM=fbdev``)

* *hwcomposer_backend_v11*: Version 1.1, 1.2, 1.3, 1.4, and 1.5
  of the hwcomposer API. Versions higher or equal than
  1.3 only support physical displays, whereas 1.1 and 1.2 support also virtual
  displays. This requires libsync and hwcomposer-egl from libhybris. Most of the
  hwcomposer 1.0 API properties apply, with the exception that frame posting and
  synchronization happens with the help of libhybris' hwcomposer EGL platform.
  (``EGL_PLATFORM=hwcomposer``)

Instead of running the Wayland Compositor (lipstick) on top of the hwcomposer QPA
plugin, one can also run all other Qt 5-based applications, but the application
can only open a single window (multiple windows are not supported, and will cause
an application abort). For multiple windows, Wayland is used. This means that for
testing, it is possible to run a simple, single-window Qt 5 application on the
framebuffer (without any Wayland Compositor in between) by setting the environment
variables ``EGL_PLATFORM`` and ``QT_QPA_PLATFORM`` according to the above.


SensorFW Qt 5 / libhybris Plugin
--------------------------------

TODO

.. _build-ha-pkgs:

Build HA Middleware Packages
----------------------------

``rpm/dhd/helpers/build_packages.sh`` now is taking care of builds/rebuilds/local
repo preparation and patterns.

All other packages
''''''''''''''''''
Please compile any other required packages should a build/mic process
indicate a dependency on them. Feel free to add/remove those packages
to/from patterns to suit your port's needs.

Follow the exact same compilation approach as with above packages. Known
packages are:

* https://github.com/mer-hybris/unblank-restart-sensors - needed only by mako

