Packaging Droid HAL
===================

In this chapter, we will package the build results of :doc:`android`
as RPM packages and create a local rpm repository. From there, they
can be added to a local target and used to build libhybris and the QPA
plugin. They can also be used to build the rootfs.

Packaging ``droid-hal-device``
------------------------------

This step requires:

* A populated ``$ANDROID_ROOT`` from :doc:`android`
* A Mer Platform SDK installation (chroot) for RPM building

Inside your ``$ANDROID_ROOT``, there is a copy of ``droid-hal-device``
in the ``rpm/`` directory (since it appears in the manifest). 

The master git repo for the packaging is here:  https://github.com/mer-hybris/droid-hal-device

This rpm/ dir contains some rather spooky spec file packaging to make
a set of rpms.

Create the rpms
```````````````

The next step has to be carried out in a Mer SDK chroot:

.. code-block:: console

    MER_SDK $

    cd $ANDROID_ROOT
    #FIXME: this revolting workaround is needed since mb2 doesn't parse %include and
    #       rpmspec --query --buildrequires fails since some macros provided by the BRs
    #       aren't present ... catch22
    mb2 -t $VENDOR-$DEVICE-armv7hl -s rpm/droid-hal-device.inc build

    mb2 -t $VENDOR-$DEVICE-armv7hl -s rpm/droid-hal-$DEVICE.spec build

This should leave you with several RPM packages in ``$ANDROID_ROOT/RPMS/``.

Create a local repo
```````````````````

Now we create a local repository that can be used to make images or to
update Targets with the devel headers to enable device specific
packages to be built (like libhybris or pulseaudio)

.. code-block:: console

    MER_SDK $

    mkdir -p $ANDROID_ROOT/droid-local-repo/$DEVICE

    rm -f $ANDROID_ROOT/droid-local-repo/$DEVICE/droid-hal-*rpm
    mv RPMS/*${DEVICE}* $ANDROID_ROOT/droid-local-repo/$DEVICE

    createrepo  $ANDROID_ROOT/droid-local-repo/$DEVICE
