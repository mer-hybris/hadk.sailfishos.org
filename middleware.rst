Middleware
==========

This chapter contains some background information about the middleware parts
that are part of the Hardware Adapation. Using this info, it should be possible
to customize and build the middleware parts for a given device.


MCE libhybris Plugin
--------------------

TODO

Non-Graphic Feedback Daemon Droid Vibrator Plugin
-------------------------------------------------

TODO

Non-Graphic Feedback Daemon PulseAudio Plugin
---------------------------------------------

TODO

PulseAudio Droid Modules
------------------------

TODO

Qt5 QtFeedback Droid Vibrator Plugin
------------------------------------

TODO

Qt5 Hardware Composer QPA
-------------------------

This Qt Platform Abstraction plugin makes use of the libhardware hwcomposer API to
send rendered frames from the Wayland Compositor to the actual framebuffer. While
for some older devices, just flipping the fbdev was enough, more recent devices
actually require using hwcomposer to request flipping and for vsync integration.

The important environment variables are:

 * ``EGL_PLATFORM`` / ``HYBRIS_EGLPLATFORM``: For the Wayland Compositor, this
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
  (``HYBRIS_EGLPLATFORM=fbdev``)

* *hwcomposer_backend_v10*: Version 1.0 of the hwcomposer API. It supports one
  display device, handles VSync explicitly and uses a single hardware layer that
  will be drawn via EGL (and not composed via hwcomposer). Swapping is done by
  waiting for VSync and uses libsync-based synchronization of posting buffers.
  Switching the screen off is also supported, and sleeping the screen disables
  VSync events. Also, the same VSync period algorithm is used (try to query from
  libhardware, fall back to 60 Hz if detection fails).
  (``HYBRIS_EGLPLATFORM=fbdev``)

* *hwcomposer_backend_v11*: Version 1.1, 1.2 and 1.3 of the hwcomposer API. Version
  1.3 only supports physical displays, whereas 1.1 and 1.2 support also virtual
  displays. This requires libsync and hwcomposer-egl from libhybris. Most of the
  hwcomposer 1.0 API properties apply, with the exception that frame posting and
  synchronization happens with the help of libhybris' hwcomposer EGL platform.
  (``HYBRIS_EGLPLATFORM=hwcomposer``)

Instead of running the Wayland Compositor (lipstick) on top of the hwcomposer QPA
plugin, one can also run all other Qt 5-based applications, but the application
can only open a single window (multiple windows are not supported, and will cause
an application abort). For multiple windows, Wayland is used. This means that for
testing, it is possible to run a simple, single-window Qt 5 application on the
framebuffer (without any Wayland Compositor in between) by setting the environment
variables ``HYBRIS_EGLPLATFORM`` and ``QT_QPA_PLATFORM`` according to the above.


SensorFW Qt 5 / libhybris Plugin
--------------------------------

TODO

.. _build-ha-pkgs:

Build HA Middleware Packages
----------------------------

Target setup
````````````

Setup to use droid headers

If not done already, as a one-off (per device-target) we need to add the local
repo to our target, as indicated in :ref:`add-local-repo`.

Now set the SDK target to use an up-to-date repo:

.. code-block:: console

  MER_SDK $

  sb2 -t $VENDOR-$DEVICE-armv7hl -R -msdk-install ssu domain sales
  sb2 -t $VENDOR-$DEVICE-armv7hl -R -msdk-install ssu dr sdk

And install the droid-hal-device headers:

.. code-block:: console

  MER_SDK $

  sb2 -t $VENDOR-$DEVICE-armv7hl -R -msdk-install zypper ref
  sb2 -t $VENDOR-$DEVICE-armv7hl -R -msdk-install \
      zypper install droid-hal-$DEVICE-devel

If you rebuild the droid-side then you'll need to repeat the two commands above.


Build Area Setup
````````````````

Setup an area to build packages

.. code-block:: console

  MER_SDK $

  mkdir -p $MER_ROOT/devel/mer-hybris
  cd $MER_ROOT/devel/mer-hybris

Packages
````````

libhybris
'''''''''

Check out the libhybris source code from Git:

.. code-block:: console

  MER_SDK $

  PKG=libhybris
  cd $MER_ROOT/devel/mer-hybris
  git clone https://github.com/mer-hybris/libhybris.git
  cd libhybris

Some packages will use submodules:

.. code-block:: console

  MER_SDK $

  git submodule update
  cd libhybris

Now use ``mb2`` to build the package. This essentially runs a slightly
modified ``rpmbuild`` using the Scratchbox2 target. It also pulls in
build requirements into the target. Note that this makes the target
'dirty' and you may miss build dependencies. This should be caught during
clean builds.

.. code-block:: console

  MER_SDK $

  mb2 -s ../rpm/libhybris.spec -t $VENDOR-$DEVICE-armv7hl build

Now add the packages you just built to the local repo and refresh the repo cache:

.. code-block:: console

  MER_SDK $

  mkdir -p $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG/
  rm -f $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG/*.rpm
  mv RPMS/*.rpm $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG
  createrepo $ANDROID_ROOT/droid-local-repo/$DEVICE
  sb2 -t $VENDOR-$DEVICE-armv7hl -R -msdk-install zypper ref

Note that all repositories that are in ``tar_git`` format (for use with OBS)
will have their RPM packages built locally might not always have the right
release and version set.

At this point, and for the libhybris package only, you can remove the mesa-llvmpipe packages from the target:

.. code-block:: console

  MER_SDK $

  sb2 -t $VENDOR-$DEVICE-armv7hl -R -msdk-build zypper rm mesa-llvmpipe

Failure to do this will cause problems pulling in build requirements for other packages.


qt5-qpa-hwcomposer-plugin
'''''''''''''''''''''''''

.. code-block:: console

  MER_SDK $

  PKG=qt5-qpa-hwcomposer-plugin
  cd $MER_ROOT/devel/mer-hybris
  git clone https://github.com/mer-hybris/$PKG.git
  cd $PKG
  mb2 -s rpm/$PKG.spec -t $VENDOR-$DEVICE-armv7hl build
  mkdir -p $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG/
  rm -f $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG/*.rpm
  mv RPMS/*.rpm $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG
  createrepo $ANDROID_ROOT/droid-local-repo/$DEVICE
  sb2 -t $VENDOR-$DEVICE-armv7hl -R -msdk-install zypper ref

sensorfw
''''''''

.. code-block:: console

  MER_SDK $

  PKG=sensorfw
  SPEC=sensorfw-qt5-hybris
  OTHER_RANDOM_NAME=hybris-libsensorfw-qt5

  cd $MER_ROOT/devel/mer-hybris
  git clone https://github.com/mer-hybris/$PKG.git
  cd $PKG
  mb2 -s rpm/$SPEC.spec -t $VENDOR-$DEVICE-armv7hl build
  mkdir -p $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG/
  rm -f $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG/*.rpm
  mv RPMS/*.rpm $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG
  createrepo $ANDROID_ROOT/droid-local-repo/$DEVICE
  sb2 -t $VENDOR-$DEVICE-armv7hl -R -msdk-install zypper ref

ngfd-plugin-droid-vibrator
''''''''''''''''''''''''''
.. code-block:: console

  MER_SDK $

  PKG=ngfd-plugin-droid-vibrator
  SPEC=$PKG

  cd $MER_ROOT/devel/mer-hybris
  git clone https://github.com/mer-hybris/$PKG.git
  cd $PKG
  mb2 -s rpm/$SPEC.spec -t $VENDOR-$DEVICE-armv7hl build
  mkdir -p $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG/
  rm -f $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG/*.rpm
  mv RPMS/*.rpm $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG
  createrepo $ANDROID_ROOT/droid-local-repo/$DEVICE
  sb2 -t $VENDOR-$DEVICE-armv7hl -R -msdk-install zypper ref

qt5-feedback-haptics-droid-vibrator
'''''''''''''''''''''''''''''''''''
.. code-block:: console

  MER_SDK $

  PKG=qt5-feedback-haptics-droid-vibrator
  SPEC=$PKG

  cd $MER_ROOT/devel/mer-hybris
  git clone https://github.com/mer-hybris/$PKG.git
  cd $PKG
  mb2 -s rpm/$SPEC.spec -t $VENDOR-$DEVICE-armv7hl build
  mkdir -p $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG/
  rm -f $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG/*.rpm
  mv RPMS/*.rpm $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG
  createrepo $ANDROID_ROOT/droid-local-repo/$DEVICE
  sb2 -t $VENDOR-$DEVICE-armv7hl -R -msdk-install zypper ref

pulseaudio-modules-droid
''''''''''''''''''''''''
.. code-block:: console

  MER_SDK $

  PKG=pulseaudio-modules-droid
  SPEC=$PKG

  cd $MER_ROOT/devel/mer-hybris
  git clone https://github.com/mer-hybris/$PKG.git
  cd $PKG
  mb2 -s rpm/$SPEC.spec -t $VENDOR-$DEVICE-armv7hl build
  mkdir -p $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG/
  rm -f $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG/*.rpm
  mv RPMS/*.rpm $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG
  createrepo $ANDROID_ROOT/droid-local-repo/$DEVICE
  sb2 -t $VENDOR-$DEVICE-armv7hl -R -msdk-install zypper ref

