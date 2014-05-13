List of Supported Devices
=========================

.. devices:

Devices currently supported by HADK (with $DEVICE/$VENDOR in brackets)

* **Nexus 4** (mako/lge)

* **Nexus 7 2012 GSM** (tilapia/asus)

* **Nexus 7 2012 WIFI** (grouper/asus)

* **Samsung Galaxy SIII LTE** (i9305/samsung)

For an up-to-date list of supported features for each device, see
`Adaptations/libhybris`_ in the Mer Wiki.

.. _Adaptations/libhybris: https://wiki.merproject.org/wiki/Adaptations/libhybris

Devices: $DEVICE and $VENDOR
---------------------------------

To get this information find your device here: `CyanogenMod Devices`_,
note down the "*Manufacturer*" and "*Codename*" values, which are
displayed in the side bar on the right. The Codename is the DEVICE and
the Manufacturer is the VENDOR.

.. _CyanogenMod Devices: http://wiki.cyanogenmod.org/w/Devices

For New Devices
---------------

First, try building a full CyanogenMod build for your device and deploy it to
see if you got the right sources. Once you got that, you can try building only
the Android HAL that is used for Sailfish OS (``mka hybris-hal``).

* Ensure you got all the right mer-hybris repositories added (that includes
  the device configuration repository as well as hardware support bits)


