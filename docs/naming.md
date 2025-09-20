# Package Naming Policy

For consistency, certain hardware adaptation / middleware plugin
packages have to be named after a certain pattern.

As in the other chapters of this guide, `$DEVICE` should be replaced
with the device codename (e.g. `mako` for Nexus 4), and the asterisk
(\*) is used as wildcard / placeholder.

## List of naming rules

Packages that are arch-specific (e.g. `aarch64`), device-specific and
contain `$DEVICE` in their name:

-   The arch-specific HAL RPMs (built from `droid-hal-device`) should be
    named **droid-hal-\$DEVICE** (e.g. `droid-hal-mako`,
    `droid-hal-mako-devel`, `droid-hal-mako-img-boot`,
    `droid-hal-mako-kernel`, `droid-hal-mako-kernel-modules`,
    `droid-hal-mako-kickstart-configuration`, `droid-hal-mako-patterns`,
    `droid-hal-mako-policy-settings` and
    `droid-hal-mako-pulseaudio-settings`)
-   The package containing kickstart files for `mic` should be named
    **ssu-kickstarts-\$DEVICE** (e.g. `ssu-kickstarts-mako`)

Package that are arch-independent (`noarch`), device-specific and
contain `$DEVICE` in their name:

-   The arch-independent HAL RPMs (built from `droid-hal-device`) should
    be named: **droid-hal-\$DEVICE-**\* (e.g.
    `droid-hal-mako-img-recovery` and `droid-hal-mako-sailfish-config`)
-   The SensorFW libhybris plugin configuration should be named
    **hybris-libsensorfw-qt5-configs**
    (`hybris-libsensorfw-qt5-configs`)

Packages that are arch-specific (e.g. `aarch64`), device-specific, but
do not contain `$DEVICE`:

-   RPMs built from libhybris should be named **libhybris-**\* (e.g.
    `libhybris-libEGL`)
-   Plugins for the non-graphic feedback daemon should be named
    **ngfd-plugin-**\* (e.g. `ngfd-plugin-droid-vibrator`); as well as
    their Qt plugin **qt5-feedback-haptics-droid-vibrator**
    (`qt5-feedback-haptics-droid-vibrator`)
-   The QPA hwcomposer plugin should be named
    **qt5-qpa-hwcomposer-plugin** (`qt5-qpa-hwcomposer-plugin`)
-   The PulseAudio support modules should be named
    **pulseaudio-modules-droid** (`pulseaudio-modules-droid`)
-   The GStreamer plugins should be named **libgstreamer0.10-**\* and/or
    **gstramer0.10-**\* (e.g. `libgstreamer0.10-gralloc`,
    `libgstreamer0.10-nativebuffer`, `gstreamer0.10-omx`,
    `gstreamer0.10-droideglsink` and `gstreamer0.10-droidcamsrc`)
-   The SensorFW libhybris plugin should be named
    **hybris-libsensorfw-qt5** (`hybris-libsensorfw-qt5`)

## List of Provides

-   **droid-hal-\$DEVICE-**\* provides **droid-hal-**\* (e.g.
    `droid-hal-$DEVICE-pulseaudio-settings` provides
    `droid-hal-pulseaudio-settings`)

## TODO

The above \"rules\" are the current state of our hardware adaptation.
Here are some things that should be improved there:

-   Some arch-specific packages contain arch-independent config files or
    binary blobs - make them arch-independent (`noarch`) instead
-   Unify the GStreamer plugin naming (either **libgstreamer0.10-**\* or
    **gstreamer0.10-**\*) to not have two naming schemes there
-   The PulseAudio settings package usually is called
    **pulseaudio-settings-\$DEVICE** (we currently have
    **droid-hal-\$DEVICE-pulseaudio-settings**, maybe this can be
    implemented as a `Provides:`?)
-   The Linux kernel modules are in
    **droid-hal-\$DEVICE-kernel-modules** at the moment, in other
    hardware adaptations we use **kmod-xyz-\$DEVICE**
-   The recovery partition in the image at the moment is
    **droid-hal-\$DEVICE-img-recovery**, but for other hardware
    adaptations we use **jolla-recovery-\$DEVICE**
