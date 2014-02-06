Porting the Android HAL
=======================

Setting up an Android Build Environment
---------------------------------------

Checking out CyanogenMod Source
-------------------------------

For Existing Devices
````````````````````

For New Devices
```````````````

Mer Modifications to CyanogenMod
--------------------------------

Our modifications are kept in two places:

* **repo manifest**: This tracks all hybris-specific branches of
  the Droid system that we have modified (see below).
* **Kernel repositories**: The patched kernel configuration for
  each device is kept in a modified kernel repository.

Droid System
````````````

In order to work with ``libhybris``, some parts of the lower levels of
Android need to be modified:

* **bionic/**
 * Pass ``errno`` from bionic to libhybris (``libdsyscalls.so``)
 * ``/dev/log/`` to ``/dev/alog/`` renaming
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

All these modifications are already done in the **mer-hybris** Git
repository forks from the original CyanogenMod sources. If the hybris
repo manifest is used, these changes will be included automatically.

In addition to these generic modifications, for some devices and SoCs
we also maintain a set of patches on top of CyanogenMod to fix issues
with drivers that only happen in Sailfish OS:

* **hardware/samsung/**
 * SEC hwcomposer: Avoid segfault if ``registerProcs`` was never called

Kernel
``````

For the Kernel, some configuration options must be enabled to support
``systemd`` features, and some configuration options must be disabled,
because they conflict or block some features of Sailfish OS.

* **Required Configuration Options**
 * TODO
 * TODO2
 * ...
* **Conflicting Configuration Options**
 * **CONFIG_ANDROID_PARANOID_NETWORK**:
   This would make all network connections fail if the user is not
   in the group with ID 3003.
 * ...

See ``mer-kernel-check`` for a tool that can be used to verify the kernel
configuration.

Building Relevant Bits of CyanogenMod
-------------------------------------

Configuring and Compiling the Kernel
------------------------------------

Packaging ``hybris-boot`` and the Kernel
----------------------------------------

