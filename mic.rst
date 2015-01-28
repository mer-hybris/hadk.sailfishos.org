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

  hadk $DEVICE

  cd $ANDROID_ROOT
  mkdir -p tmp

  HA_REPO="repo --name=adaptation0-$DEVICE-@RELEASE@"
  sed -e \
   "s|^$HA_REPO.*$|$HA_REPO --baseurl=file://$ANDROID_ROOT/droid-local-repo/$DEVICE|" \
   $ANDROID_ROOT/installroot/usr/share/kickstarts/Jolla-@RELEASE@-$DEVICE-@ARCH@.ks \
   > tmp/Jolla-@RELEASE@-$DEVICE-@ARCH@.ks

.. warning::
    THIS IS IMPORTANT: Do not execute the code below this box if you are not
    aware what OBS is, or if the packages for your device are not available on
    the Mer OBS -- OpenSUSE Build Serice is out of scope for this guide.

    If however, on OBS your device's hardware adaptation repository exists,
    consider the steps below.
Feel free to replace ``nemo:/devel:/hw:`` with path to your HA repo within the
Mer OBS:

.. code-block:: console

  MOBS_URI="http://repo.merproject.org/obs"
  HA_REPO="repo --name=adaptation0-$DEVICE-@RELEASE@"
  HA_REPO1="repo --name=adaptation1-$DEVICE-@RELEASE@ \
  --baseurl=$MOBS_URI/nemo:/devel:/hw:/$VENDOR:/$DEVICE/sailfish_latest_@ARCH@/"
  sed -i -e "/^$HA_REPO.*$/a$HA_REPO1" tmp/Jolla-@RELEASE@-$DEVICE-@ARCH@.ks


.. _patterns:

Patterns
--------

The selection of packages for each hardware adaptation has to be put into
a pattern file, so that creating the image as well as any system updates in
the future can pull in and upgrade all packages related to the hardware
adaptation.

Ensure you have done the steps to :ref:`createrepo`.

Add/update metadata about patterns using this script (NB: it will fail with a
non-critical ``Exception AttributeError: "'NoneType...`` error):

.. code-block:: console

    MER_SDK $

    hadk

    cd $ANDROID_ROOT
    rpm/helpers/process_patterns.sh

To modify a pattern, edit its respective template under ``rpm/patterns/{common,hybris,templates}``
and then run ``rpm/helpers/add_new_device.sh``. Take care and always use ``git status/stash`` commands.

.. _mic:

Building the Image with MIC
---------------------------

Ensure you re-generated :ref:`patterns` (needs to be run after every
``createrepo``)

In the script below choose a `Sailfish OS version`_ you want to build.

.. important::
   Avoid building older releases unless you know what you're doing (expect
   patterns to break as new HA packages get introduced).

   Ensure you pick the same release as your target was in    :doc:`scratchbox2`.
   E.g., if target said ``Jolla...Update9...tar.bz2``, build the 10th SailfishOS
   update 1.1.0.39 (check with `Sailfish OS version`_)

Build a rootfs using RPM repositories and a kickstart file (NB: all errors are
non-critical as long as you end up with a generated .zip image):

.. _Sailfish OS version: http://en.wikipedia.org/wiki/Sailfish_OS#Software_version

.. code-block:: console

  MER_SDK $

  # Set the version of your choosing, latest is strongly preferred
  # (check with "Sailfish OS version" link above)
  RELEASE=1.1.0.39
  # EXTRA_NAME adds your custom tag. It doesn't support '.' dots in it!
  EXTRA_NAME=-my1
  sudo mic create fs --arch armv7hl \
      --tokenmap=ARCH:armv7hl,RELEASE:$RELEASE,EXTRA_NAME:$EXTRA_NAME \
      --record-pkgs=name,url \
      --outdir=sfe-$DEVICE-$RELEASE$EXTRA_NAME \
      --pack-to=sfe-$DEVICE-$RELEASE$EXTRA_NAME.tar.bz2 \
      $ANDROID_ROOT/tmp/Jolla-@RELEASE@-$DEVICE-@ARCH@.ks

Once obtained the ``.zip`` file, sideload via your device's recovery mode,
or examine other particular ways of deploying to your device.

Currently HADK does not support creating images with Jolla Store functionality.

If creation fails due to absence of a package required by pattern, note down
the package name and proceed to :ref:`missing-package`.

A more obscure error might look like this:

.. code-block:: console

  Warning: repo problem: pattern:jolla-configuration-$DEVICE-(version).noarch
    requires jolla-hw-adaptation-$DEVICE,
    but this requirement cannot be provided, uninstallable providers:
    pattern:jolla-hw-adaptation-$DEVICE-(version).noarch[$DEVICE]

This means a package dependency cannot be satisfied down the hierarchy of
patterns. A quick in-place solution (NB: expand @DEVICE@ occurrences manually):

* Substitute the line ``@Jolla Configuration @DEVICE@`` with
  ``@jolla-hw-adaptation-@DEVICE@`` in your .ks

* Rebuild .ks

* Repeat the steps above substituting respective pattern to walk down the
  patterns hierarchy -- you'll eventually discover the offending package

* If that package is provided by e.g. droid-hal-device (like
  ``droid-hal-mako-pulseaudio-settings``), it means that some of its dependencies
  are not present:

 - Edit .ks file by having ``%packages`` section consisting only of single
   ``droid-hal-mako-pulseaudio-settings`` (note there is no @ at the beginning
   of the line, since it's a package, not a pattern) -- another ``mic`` run error
   will show that the offending package is actually ``pulseaudio-modules-droid``

.. important:: When found and fixed culprit in next sections, restore your .ks
   %packages section to ``@Jolla Configuration @DEVICE@``! Then rebuild .ks with
   ``mic``

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

Troubleshooting
```````````````

/dev/null - Permission denied
'''''''''''''''''''''''''''''

Most likely the partition your MerSDK resides in, is mounted with ``nodev`` option.
Remove that option from mount rules.

