Overview
--------

Goal
====

What we're aiming for is a Mer-core based Linux system that will run on an android device.

This consists of:

* Mer core : The Linux userspace core
* Android Hardware Adaptation : (also called an HA) this consists of

 * a device specific Android kernel
 * binary device drivers taken from an Android or CM distribution
 * the libhybris interface built for the device
 * Mer HA dependent packages built for the device

* Qt/Wayland (using a suitable platform plugin such as eglfs or hwcomposer)
* Sailfish (or a.n.other UI)


Development
===========

The development environment uses:

* Mer Platform SDK with

 * Architecture specific 'target' (typically a rootfs with non-x86 headers/libs)

* Android build chroot (a minimal Ubuntu chroot required to build the Android src)

During the HA development you'll typically have one window where you build/hack on Android code and another where you assemble the Mer glue packages.

The approach is to build the following components in the Android build chroot:

* a kernel
* a hacking friendly initrd which supports various boot options
* boot and recovery images
* a minimal 'standard' /system
* some 'libhybris-ised' packages for /system (like bionic, logcat and Android's init)

Then in the Mer SDK we build:

* rpms containing all the built binaries and extracted configs
* hardware specific packages or plugins eg: Qt/Wayland, Pulseaudio

The rpms are then put into an HA specific repository and we can make full system images using mic or IMG. This is also done in the Mer SDK.

Deployment 
==========

The kernel and initrd are flashed to the device and the rootfs is placed in the data partition alongside the unmodified Android system.

