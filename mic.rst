Creating the Sailfish OS Root Filesystem
========================================

Additional Packages for Hardware Adaptation
-------------------------------------------

Some additional packages are used to allow access to device features. These
middleware packages are usually built against droid-headers / libhybris, and
therefore need to be built separately for each target device. To build,
clone the repository from ``mer-hybris`` on Github.
See :doc:`middleware` for a list of all middleware components (not
all middleware components are used for all device adaptations).

Via the flexible system of patterns, you will be able to select only
working/needed functions for your device.

.. _gen-ks:

Creating and Configuring the Kickstart File
------------------------------

The kickstart file is generated using ``ssuks``, which is part of the
SSU utility.

Ensure you have done the steps to :ref:`createrepo`.

.. code-block:: console

  MER_SDK $

  cd $ANDROID_ROOT
  mkdir -p tmp

  HA_REPO="repo --name=adaptation0-$DEVICE-@RELEASE@"
  sed -e "s|^$HA_REPO.*$|$HA_REPO --baseurl=file://$ANDROID_ROOT/droid-local-repo/$DEVICE|" \
    $ANDROID_ROOT/installroot/usr/share/kickstarts/Jolla-@RELEASE@-$DEVICE-@ARCH@.ks > tmp/Jolla-@RELEASE@-$DEVICE-@ARCH@.ks

If you only want to rebuild some of the packages locally (and are confident that there are no changes that require custom rebuilds) then you can use the public build if there is one; we'll use ``sed`` to find (//) the HA_REPO and then 'a'ppend a new line with the OBS repo url:

.. code-block:: console

  HA_REPO="repo --name=adaptation0-$DEVICE-@RELEASE@"
  sed -i -e "/^$HA_REPO.*$/arepo --name=adaptation1-$DEVICE-@RELEASE@ --baseurl=http://repo.merproject.org/obs/sailfishos:/devel:/hw:/$DEVICE/sailfish_latest_@ARCH@/" \
      tmp/Jolla-@RELEASE@-$DEVICE-@ARCH@.ks

.. _patterns:

Patterns
--------

The selection of packages for each hardware adaptation has to be put into
a pattern file, so that creating the image as well as any system updates in
the future can pull in and upgrade all packages related to the hardware
adaptation.

Ensure you have done the steps to :ref:`createrepo`.

Add/update metadata about patterns using this script:

.. code-block:: console

    MER_SDK $

    hadk

    cd $ANDROID_ROOT
    rpm/helpers/process_patterns.sh

The error:

.. code-block:: console

  Exception AttributeError: "'NoneType' object has no attribute
    'px_proxy_factory_free'"...

can safely be ignored.

If you ever require to reset/update patterns, run
``rpm/helpers/add_new_device.sh``

.. _mic:

Building the Image with MIC
---------------------------

Ensure you re-generated :ref:`patterns` (needs to be run after every
``createrepo``)

Building a rootfs using RPM repositories and a kickstart file:

.. code-block:: console

  MER_SDK $

  RELEASE=1.0.7.16
  # WARNING: EXTRA_NAME currently does not support '.' dots in it!
  EXTRA_NAME=-my1
  sudo mic create fs --arch armv7hl \
      --tokenmap=ARCH:armv7hl,RELEASE:$RELEASE,EXTRA_NAME:$EXTRA_NAME \
      --record-pkgs=name,url \
      --outdir=sfa-mako-ea-$RELEASE$EXTRA_NAME \
      --pack-to=sfa-mako-ea-$RELEASE$EXTRA_NAME.tar.bz2 \
      $ANDROID_ROOT/tmp/Jolla-@RELEASE@-$DEVICE-@ARCH@.ks

If creation fails due to absence of a package required by pattern, note down
the package name and proceed to :ref:`missing-package`.

A more obscure error might look like this:

.. code-block:: console

  Warning: repo problem: pattern:jolla-configuration-$DEVICE-(version).noarch
    requires jolla-hw-adaptation-$DEVICE,
    but this requirement cannot be provided, uninstallable providers:
    pattern:jolla-hw-adaptation-$DEVICE-(version).noarch[$DEVICE]

This means a package dependency cannot be satisfied down the hierarchy of
patterns. A quick in-place solution:

* Substitute the line ``@Jolla Configuration $DEVICE`` with
  ``@jolla-hw-adaptation-$DEVICE`` in your .ks

* Rebuild .ks

* Repeat the steps above substituting respective pattern to walk down the
  patterns hierarchy -- you'll eventually discover the offending package

* If that package is provided by e.g. droid-hal-device (like
  ``droid-hal-mako-pulseaudio-settings``), it means that some of its dependencies
  are not present

 * Edit .ks file by having ``%packages`` section consisting only of single
   ``droid-hal-mako-pulseaudio-settings`` (note there is no @ at the beginning
   of the line, since it's a package, not a pattern) -- another ``mic`` run error
   will show that the offending package is actually ``pulseaudio-modules-droid``

Now you're ready to proceed to the :ref:`missing-package` section.

.. _missing-package:

Dealing with a Missing Package
``````````````````````````````
If that package is critical (e.g. ``libhybris``, ``qt5-qpa-hwcomposer-plugin`` etc.),
build and add it to the local repo as explained in :ref:`build-ha-pkgs`.
Afterwards perform:

* :ref:`patterns`
* :ref:`mic`

Otherwise if a package is not critical, and you accept to have less
functionality (or even unbootable) image, you can temporarily comment it out
from patterns in ``rpm/patterns/$DEVICE`` and orderly perform:

* :ref:`build-rpms`
* :ref:`createrepo`
* :ref:`gen-ks`
* :ref:`patterns`
* :ref:`mic`

Alternatively (or if you can't find it among patterns) add ``-NAME_OF_PACKAGE`` line
to your .ks ``%packages`` section (remember that regenerating .ks will overwrite this
modification).

