List of Repositories
====================

**droid-hal-device**
    Contains RPM packaging and conversion scripts for converting
    the results of the Android HAL build process to RPM packages
    and systemd configuration files.

**droid-system-packager**
    Helper package for ``droid-hal-device``, installed on the
    device.

**hybris-boot**
    Script run during Android HAL build that will combine the
    kernel and a custom initrd to ``hybris-boot.img`` and
    ``hybris-recovery.img``. Those are used to boot a device into
    Sailfish OS and for development purposes.

**hybris-installer**
    Combines the ``hybris-boot`` output and the root filesystem
    into a .zip file that can be flashed via Android Recovery.

**libhybris**
    Library to allow access to Bionic-based libraries from a
    glibc-based host system (e.g. hwcomposer, EGL, GLESv2, ..).

**qt5-qpa-hwcomposer-plugin**
    Qt 5 Platform Abstraction Plugin that allows fullscreen
    rendering to the Droid-based hardware abstraction. It
    utilizes libhybris and the Android hwcomposer module.
