Manual Installation and Maintenance
===================================

This assumes you are booted into CyanogenMod on your device, can ``adb shell``
to it to get a root shell and have your boot image and rootfs tarball ready.

Some of these approaches also work in Android Recovery (there's an ``adbd``
running), but you obviously won't have network connectivity for downloading
updates.

Extracting the rootfs via adb
-----------------------------

Replace ``i9305-devel.tar.gz`` with the name of your rootfs tarball:

.. code-block:: bash

    adb push i9305-devel.tar.gz /sdcard/
    adb shell
    su
    mkdir -p /data/.stowaways/sailfishos
    tar --numeric-owner -xvzf /sdcard/i9305-devel.tar.gz \
        -C /data/.stowaways/sailfishos

Flashing the boot image via adb
-------------------------------

The following example is for ``i9305``, for other devices the output
partition and filename is obviously different:

.. code-block:: bash

    adb push out/target/product/i9305/hybris-boot.img /sdcard/
    adb shell
    su
    dd if=/sdcard/hybris-boot.img of=/dev/block/mmcblk0p8

Interacting with the rootfs via adb from Android
------------------------------------------------

You can interact with the Sailfish OS rootfs and carry out maintenance (editing
files, installing packages, etc..) when booted into an Android system. You have
to have your rootfs already installed/extracted. You can use Android's WIFI
connectivity to connect to the Internet and download updates:

.. code-block:: bash

    adb shell
    su
    mount -o bind /dev /data/.stowaways/sailfishos/dev
    mount -o bind /proc /data/.stowaways/sailfishos/proc
    mount -o bind /sys /data/.stowaways/sailfishos/sys
    chroot /data/.stowaways/sailfishos/ /bin/sh
    export PATH=/bin:/sbin:/usr/bin:/usr/sbin
    export HOME=/root/
    echo "nameserver 8.8.8.8" >/etc/resolv.conf
    ...

