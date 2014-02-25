Porting the Android HAL
=======================

Setting up an Android Build Environment
---------------------------------------

*TODO: unpacking and ubu-chroot into a ubuntu rootfs here?*

* `Install repo`_

.. _Install repo: http://source.android.com/source/downloading.html#installing-repo

Checking out CyanogenMod Source
-------------------------------

.. code-block:: bash

    mkdir -p $ANDROID_ROOT
    cd $ANDROID_ROOT
    repo init -u git://github.com/mer-hybris/android.git -b hybris-10.1
    repo sync

This will download the source code for the subset of Android we need
to build the HAL.

The expected disk usage for the source tree after ``repo sync``
is **9.4 GB** (as of 2014-02-18).

For Supported Devices
`````````````````````

See :doc:`devices` for a list of devices supported by HADK.

For New Devices
```````````````

First, try building a full CyanogenMod build for your device and deploy it to
see if you got the right sources. Once you got that, you can try building only
the Android HAL that is used for Sailfish OS (``mka hybris-hal``).

* Ensure you got all the right mer-hybris repositories added (that includes
  the device configuration repository as well as hardware support bits)

Mer Modifications to CyanogenMod
--------------------------------

Our modifications are kept in two places:

* **repo manifest**: This tracks all hybris-specific branches of
  the Droid system that we have modified (see below)
* **Kernel repositories**: The patched kernel configuration for
  each device is kept in a modified kernel repository

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

Building Relevant Bits of CyanogenMod
-------------------------------------

Throughout the documentation we shall use $DEVICE variable denoting the code name
of your device. It can be obtained from http://wiki.cyanogenmod.org/w/Devices .

In the Android build tree, run the following in a ``bash`` shell (if you
are using e.g. ``zsh``, you need to run these commands in a ``bash`` shell):

.. code-block:: bash

    source build/envsetup.sh
    export USE_CCACHE=1

*TODO: can this bit below be automated?*

Edit ``build/core/main.mk`` and add include ``hybris/Android.mk`` to the
subdir_makefiles variable.

.. code-block:: bash

    breakfast $DEVICE

*XXX: [thp]: For i9305 the ``breakfast`` results in duplicate repos for me? Had to
use "lunch cm_$DEVICE-eng" instead (because we have modified repos for that device
in our default.xml) [sl]: There is no cm_mako among options, and I just ignored
the duplicate error - all went ahead fine. Play with roomservice is welcomed though,
thanks*

.. code-block:: bash

    mka hybris-hal

The relevant output bits will be in ``out/target/product/$DEVICE/``, in
particular:

* ``out/target/product/$DEVICE/hybris-boot.img``: Kernel and initrd
* ``out/target/product/$DEVICE/hybris-recovery.img``: Recovery boot image
* ``out/target/product/$DEVICE/system/``: HAL system libraries and binaries

The expected disk usage for the source and binaries after ``mka hybris-hal``
is **16 GB** (as of 2014-02-18).

Configuring and Compiling the Kernel
------------------------------------

For supported devices, the kernel is built as part of ``mka hybris-hal``
with the right configuration.

For new devices, you have to make sure to get the right kernel configuration
included in the repository. For this, clone the kernel repository for the
device into **mer-hybris** and configure the kernel using ``hybris/mer-kernel-check``.

*TODO: Document how to adjust ``fixup-mountpoints``*

Common Pitfalls
---------------

* If ``repo sync`` fails with a message like *fatal: duplicate path
  device/samsung/smdk4412-common in /home/nemo/android/.repo/manifest.xml*,
  remove the local manifest with ``rm .repo/local_manifests/roomservice.xml``
* In some cases (with parallel builds), the build can fail, in this case, use
``mka hybris-hal -j1`` to retry with a non-parallel build and see the error
message without output from parallel jobs. The build usually ends with:

.. code-block:: console

    ...
    Install: .../out/target/product/$DEVICE/hybris-recovery.img
    ...
    Install: .../out/target/product/$DEVICE/hybris-boot.img
    ...
    Made boot image: .../out/target/product/$DEVICE/boot.img

