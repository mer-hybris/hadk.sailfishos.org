Overview
--------

Goal
====

By following this guide you can set up a Sailfish OS (or another Sailfish Core based)
Linux system that will run on an Android device, on top of an existing Android
Hardware Adaptation kernel and drivers.

This consists of:

* **Sailfish Core**: the GNU/Linux userspace core
* **Android Hardware Adaptation** (HA/HAL), consisting of:
 - Device-specific **Android Kernel**
 * **Android base** which can be:
  - LineageOS - https://wiki.lineageos.org
  * AOSP - Android Open Source Project - https://source.android.com
  * CAF - Code Aurora Forum - https://www.codeaurora.org
  * Sony Open Devices program - https://developer.sony.com/develop/open-devices
  * Vendor-specific Android base
 * **Binary device drivers** taken from an **Android base**
 * Hybris patches to the **Android base**
 * The **libhybris interface** built against the binary drivers
 * **Middleware packages** depending on hardware-specific plugins
 * A Qt/Wayland **QPA plugin** utilizing the Android ``hwcomposer``
* **Sailfish OS** components


Development
===========

Requirements
````````````

The development environment uses the Platform SDK, with:

* one or more device specific **targets** (a rootfs with device-specific
  headers and libraries)

* a HA build SDK (a minimal Ubuntu chroot required to build
  the Android sources)

During the HA development you'll typically have one window/terminal using the
HA build SDK where you build and work on Android code and another session
using the Platform SDK where you build RPMs for the hardware adaptation.

Setting up the Platform SDK, as well as the device-specific targets
and the Ubuntu HA build chroot is described in :doc:`setupsdk`.

Commands and output from the Platform SDK session are indicated using
``PLATFORM_SDK $`` at the top of the code block, like this:

.. code-block:: console

  PLATFORM_SDK $

  echo "run this command in the Platform SDK terminal"

How to enter ``PLATFORM_SDK $`` is explained in :ref:`enter-sfos-sdk`.

Commands and output from the HA build session are indicated using
``HABUILD_SDK $`` at the top of the code block, like this:

.. code-block:: console

  HABUILD_SDK $

  echo "run this command in the Ubuntu HA build SDK terminal"

How to enter ``HABUILD_SDK $`` is explained in :ref:`enter-ubu-chroot`.

.. _mer-root:

The build area root directory
`````````````````````````````

In this guide, we refer to the SDK directory hosting Platform SDK, Targets, and
Ubuntu chroot with the environment variable ``$PLATFORM_SDK_ROOT``. With one SDK target
spanning 0.5-1GB, you need around 3GB of space in total.

Build components
````````````````
There are a number of components to build; the lower level and Android related
components are built in the HA build SDK; the rest are built in the Platform SDK.

* In the **HA build SDK**
 - a kernel
 * a hacking friendly initrd which supports various boot options
 * ``hybris-boot.img`` and ``hybris-recovery.img`` (for booting and debugging)
 * a minimal Android ``/system/`` tree
 * modified Android parts for compatibility with libhybris and Sailfish OS
   (e.g. Bionic libc, ``logcat``, ``init``, ...)

* In the **Platform SDK**
 - RPM packages containing all the built binaries and extracted configs
 * Hardware-specific middleware and plugins (e.g. Qt QPA plugins, PulseAudio)

For distribution, RPM packages are uploaded to a HA-specific repository. With
this repository, full system images using the ``mic`` utility. The ``mic``
utility is usually also run inside the Platform SDK.

Deployment
==========

The ``hybris-boot.img`` (containing both the kernel and our custom initrd) is flashed
to the device, while the Sailfish OS rootfs is placed in a subdirectory of
the ``/data/`` partition alongside an existing, unmodified Android system.

The Sailfish OS rootfs is then used as a switchroot target with /data bind-mounted inside it for shared access to any user data.

