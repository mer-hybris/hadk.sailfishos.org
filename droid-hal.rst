Packaging Droid HAL
===================

In this chapter, we will package the build results of :doc:`android`
as RPM packages and upload them to OBS. From there, it can be
used to build libhybris and the QPA plugin.

Packaging ``droid-hal-device``
------------------------------

This step requires:

* A populated ``$ANDROID_ROOT`` from :doc:`android`
* A Mer Platform SDK installation (chroot) for RPM building

Inside your ``$ANDROID_ROOT``, clone ``droid-hal-device`` into ``rpm/``:

.. code-block:: bash

    cd $ANDROID_ROOT
    git clone git://example.com/droid-hal-device.git rpm

For Supported Devices
`````````````````````

The next step has to be carried out in a Mer SDK chroot:

.. code-block:: bash

    cd $ANDROID_ROOT
    mb2 -t $VENDOR-$DEVICE-armv7hl -s rpm/droid-hal-$DEVICE.spec build

This should leave you with several RPM packages in ``$ANDROID_ROOT/RPMS/``.

For New Devices
```````````````

1. Create ``rpm/droid-hal-$DEVICE.spec`` and fill in the metadata:

.. code-block:: bash

    $ cat > rpm/droid-hal-$DEVICE.spec << EOF
    %define device $DEVICE
    %define vendor $VENDOR

    %include rpm/droid-hal-device.inc
    EOF

2. Create ``rpm/device-$VENDOR-$DEVICE-configs``:

.. code-block:: bash

    $ mkdir rpm/device-$VENDOR-$DEVICE-configs

3. Customize device configs

.. code-block:: bash

    $ cd rpm/droid-$VENDOR-$DEVICE-configs
    $ mkdir -p var/lib/environment/compositor
    $ cat > var/lib/environment/compositor/droid-hal-device.conf << EOF
    HYBRIS_EGLPLATFORM=fbdev
    QT_QPA_PLATFORM=hwcomposer
    LIPSTICK_OPTIONS=-plugin evdevtouch:/dev/input/event0
    EOF

Uploading ``droid-hal-device`` to OBS
-------------------------------------

For now, we upload the locally-built ``droid-hal-device`` packages to
OBS as binary packages:

.. code-block:: bash

    cd $ANDROID_ROOT/rpm/obs-upload
    make

Packaging and Building ``libhybris`` in OBS
-------------------------------------------

Packaging and Building ``qt5-qpa-hwcomposer-plugin`` in OBS
------------------------------------------------------------

