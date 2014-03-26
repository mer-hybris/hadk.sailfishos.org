Tweaks and Patches
==================

Running SailfishOS using libhybris and Mer requires a few
modifications to a standard Android/CM system. We maintain forks of
some repos with those patches aplied.

For Supported Devices
`````````````````````

See :doc:`devices` for a list of devices supported by HADK. Supported
devices are automatically downloaded as part of the HADK android build
environment.


Mer Modifications to CyanogenMod
--------------------------------

Our modifications are tracked by our own hybris-specific repo manifest
file, currently at version *hybris-10.1* which is based on the
*CyanogenMod* 10.1.x releases. The below sections outline our
modifications to these sources for developing *libhybris* based
adaptations.

Droid System
````````````

In order to work with ``libhybris``, some parts of the lower levels of
Android need to be modified:

* **bionic/**
 * Pass ``errno`` from bionic to libhybris (``libdsyscalls.so``)
 * Rename ``/dev/log/`` to ``/dev/alog/``
 * TLS slots need to be re-assigned to not conflict with glibc
 * Support for ``HYBRIS_LD_LIBRARY_PATH`` in the linker
 * Add ``/usr/libexec/droid-hybris/system/lib`` to the linker search path
* **external/busybox/**
 * Busybox is used in the normal and recovery boot images. We need
   some additional features like ``mdev`` and ``udhcpd``.
* **system/core/**
 * Make ``cutils`` and ``logcat`` aware of the new log location
   (``/dev/alog/``)
 * Add ``/usr/libexec/droid-hybris/lib-dev-alog/``
   to the ``LD_LIBRARY_PATH``
 * Force SELINUX off since mer doesn't support it
 * Remove various ``init`` and ``init.rc`` settings and operations that
   are handled by ``systemd`` / Mer on a Sailfish OS system.
* **frameworks/base/**
 * Only build ``servicemanager``, ``bootanimation`` and ``androidfw``
   to make the minimal Droid HAL build smaller (no Java content)
* **libcore/**
 * Don't include ``JavaLibrary.mk``, as Java won't be available

All these modifications have already been done in the **mer-hybris** Git
collection of forks from the original CyanogenMod sources. If the hybris
repo manifest is used, these changes will be included automatically.

In addition to these generic modifications, for some devices and SoCs
we also maintain a set of patches on top of CyanogenMod to fix issues
with drivers that only happen in Sailfish OS, for example:

* **hardware/samsung/**
 * SEC hwcomposer: Avoid segfault if ``registerProcs`` was never called

Kernel
``````

For the Kernel, some configuration options must be enabled to support
``systemd`` features, and some configuration options must be disabled,
because they conflict or block certain features of Sailfish OS.

*FIXME: CONFIGS_ are in two other places: kernel checker and ``initramfs/init``.
I suggest we direct them to one of those*

* **Required Configuration Options**
 * TODO
 * TODO2
 * ...
* **Conflicting Configuration Options**
 * **CONFIG_ANDROID_PARANOID_NETWORK**:
   This would make all network connections fail if the user is not
   in the group with ID 3003.
 * ...

See ``$ANDROID_ROOT/hybris/mer-kernel-check`` for a tool that can be used to
verify the kernel configuration.


Configuring and Compiling the Kernel
------------------------------------

For supported devices, the kernel is built as part of ``mka hybris-hal``
with the right configuration.

For new devices, you have to make sure to get the right kernel configuration
included in the repository. For this, clone the kernel repository for the
device into **mer-hybris** and configure the kernel using ``hybris/mer-kernel-check``.

*TODO: Document how to adjust ``fixup-mountpoints``*


Packaging Droid HAL
-------------------

Following on ...

For New Devices
```````````````

1. Create ``rpm/droid-hal-$DEVICE.spec`` and fill in the metadata:

.. code-block:: console

  MER_SDK $

  cat > rpm/droid-hal-$DEVICE.spec << EOF
  %define device $DEVICE
  %define vendor $VENDOR

  %include rpm/droid-hal-device.inc
  EOF

2. Create ``rpm/device-$VENDOR-$DEVICE-configs``:

.. code-block:: console

  MER_SDK $

  mkdir rpm/device-$VENDOR-$DEVICE-configs

3. Customize device configs

.. code-block:: console

  MER_SDK $

  cd rpm/droid-$VENDOR-$DEVICE-configs
  mkdir -p var/lib/environment/compositor
  cat > var/lib/environment/compositor/droid-hal-device.conf << EOF
  HYBRIS_EGLPLATFORM=fbdev
  QT_QPA_PLATFORM=hwcomposer
  LIPSTICK_OPTIONS=-plugin evdevtouch:/dev/input/event0
  EOF
