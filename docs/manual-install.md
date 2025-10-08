# Manual Installation and Maintenance

This assumes you are booted into the **Android base** on your device,
can `adb shell` to it to get a root shell and have your boot image and
rootfs tarball ready.

Some of these approaches also work in Android Recovery (there's an
`adbd` running).

## Extracting the rootfs via adb

Replace `sailfishos-devel-hammerhead.tar.bz2` with the name of your
rootfs tarball:

```sh title="PLATFORM SDK"

adb push sailfishos-devel-hammerhead.tar.bz2 /sdcard/
adb shell
su
mkdir -p /data/.stowaways/sailfishos
tar --numeric-owner -xvf /sdcard/sailfishos-devel-hammerhead.tar.bz2 \
    -C /data/.stowaways/sailfishos
```

## Flashing the boot image via adb

The following example is for `hammerhead`, for other devices the output
partition and filename is obviously different:

```sh title="PLATFORM SDK"

cd $ANDROID_ROOT
adb push out/target/product/hammerhead/hybris-boot.img /sdcard/
adb shell
su
dd if=/sdcard/hybris-boot.img of=/dev/block/mmcblk0p19
```

## Flashing or booting the boot image via fastboot

```sh title="PLATFORM SDK"

cd $ANDROID_ROOT
# to smoke test a boot image without flashing it:
fastboot boot out/target/product/$DEVICE/hybris-boot.img
# to permanently flash an image to boot partition:
fastboot flash boot out/target/product/$DEVICE/hybris-boot.img
adb shell
su
dd if=/sdcard/hybris-boot.img of=/dev/block/mmcblk0p19
```

## Interacting with the rootfs via adb from Android

You can interact with the Sailfish OS rootfs and carry out maintenance
(editing files, installing packages, etc..) when booted into an Android
system. You have to have your rootfs already installed/extracted. You
can use Android\'s WLAN connectivity to connect to the Internet and
download updates:

```sh title="PLATFORM_SDK"

adb shell
su
mount -o bind /dev /data/.stowaways/sailfishos/dev
mount -o bind /proc /data/.stowaways/sailfishos/proc
mount -o bind /sys /data/.stowaways/sailfishos/sys
chroot /data/.stowaways/sailfishos/ /bin/su -
echo "nameserver 8.8.8.8" >/etc/resolv.conf
...
```
