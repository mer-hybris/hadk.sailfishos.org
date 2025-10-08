# Modifications and Patches

Running Sailfish OS on top of a Mer Hybris adaptation requires a few
modifications to the underlying **Android base**. We maintain forks of
some repos with those patches applied.

## Hybris Modifications to an Android base

Our modifications are tracked by our own Hybris-specific repo manifest
file. The below sections outline our modifications to these sources.

### Droid System

In order to work with `libhybris`, some parts of the lower levels of
Android need to be modified:

**bionic/**
:   - Pass `errno` from bionic to libhybris (`libdsyscalls.so`)
    - Rename `/dev/log/` to `/dev/alog/`
    - TLS slots need to be re-assigned to not conflict with glibc
    - Support for `HYBRIS_LD_LIBRARY_PATH` in the linker
    - Add `/usr/libexec/droid-hybris/system/lib` to the linker search path

**external/busybox/**
:   - Busybox is used in the normal and recovery boot images. We need
      some additional features like `mdev` and `udhcpd`

**system/core/**
:   - Make `cutils` and `logcat` aware of the new log location (`/dev/alog/`)
    - Add `/usr/libexec/droid-hybris/lib-dev-alog/` to the `LD_LIBRARY_PATH`
    - Force SELinux OFF since hybris does not utilise the relevant Android
      parts, and leaving SELinux support ON would then cause device to reboot
      to recovery
    - Remove various `init` and `init.rc` settings and operations that are
      handled by `systemd` and/or Hybris on a Sailfish OS system

**frameworks/base/**
:   - Only build `servicemanager`, `bootanimation` and `androidfw` to make
      the minimal Droid HAL build smaller (no Java content)

**libcore/**
:   - Don't include `JavaLibrary.mk`, as Java won't be available

All these modifications have already been done in the **mer-hybris**
GitHub organisation of forks from various Android sources. If its
`android` [manifest is used](https://github.com/mer-hybris/android/),
these patches will be included automatically.

In addition to these generic modifications, for some devices and SoCs we
also maintain a set of patches to fix issues with drivers that only
happen in Sailfish OS, for example:

- **hardware/samsung/**: SEC hwcomposer: Avoid segfault if `registerProcs` was
  never called

### Kernel

For the Kernel, some configuration options must be enabled to support
`systemd` features, and some configuration options must be disabled,
because they conflict or block certain features of Sailfish OS.

**Required Configuration Options**

See `$ANDROID_ROOT/hybris/hybris-boot/init-script` function
`check_kernel_config()` for a list of required kernel options.

**Conflicting Configuration Options**

`CONFIG_ANDROID_PARANOID_NETWORK`
:   This would make all network connections fail if the user is not
    in the group with ID 3003.

As an alternative to checking the kernel options in the initramfs, the
script `$ANDROID_ROOT/hybris/mer-kernel-check` can also be used to
verify if all required configuration options have been enabled.

## Configuring and Compiling the Kernel

For supported devices, the kernel is built as part of `mka hybris-hal`
with the right configuration.

For new devices, you have to make sure to get the right kernel
configuration included in the repository. For this, clone the kernel
repository for the device into **mer-hybris** and configure the kernel
using `hybris/mer-kernel-check`.
