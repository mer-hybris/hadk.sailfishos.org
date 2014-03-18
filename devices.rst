List of Supported Devices
=========================

.. devices:

Devices currently supported by HADK:

* **Nexus 4** (mako)

* **Nexus 7 2012 GSM** (tilapia)

* **Nexus 7 2012 WIFI** (grouper)

* **Sony Xperia Z** (yuga)

* **Samsung Galaxy SIII LTE** (i9305)

For an up-to-date list of supported features for each device, see
`Adaptations/libhybris`_ in the Mer Wiki.

.. _Adaptations/libhybris: https://wiki.merproject.org/wiki/Adaptations/libhybris

For New Devices
```````````````

First, try building a full CyanogenMod build for your device and deploy it to
see if you got the right sources. Once you got that, you can try building only
the Android HAL that is used for Sailfish OS (``mka hybris-hal``).

* Ensure you got all the right mer-hybris repositories added (that includes
  the device configuration repository as well as hardware support bits)
