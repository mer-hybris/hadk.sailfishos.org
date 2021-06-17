Creating the Sailfish OS Root Filesystem
========================================

.. _extra-mw:
Additional Packages for Hardware Adaptation
-------------------------------------------

See :doc:`middleware` for a list of all middleware components (not all
middleware components are used by every device adaptation). Most of them will
have already been built by the ``build_packages.sh --mw`` script, but if you
need an extra one, rebuild with
``rpm/dhd/helpers/build_packages.sh --mw=GIT_URL``.

Via the flexible system of patterns, you will be able to select only
working/needed functions for your device.

Allowed Content in Your Sailfish OS Image
-----------------------------------------

The default set of packages results in a minimal and functional root filesystem.

It is forbidden to add proprietary/commercial packages to your image, because
royalty fees need to be paid or licence constraints are not allowing to
redistribute them. Examples:

* jolla-xt9 (predictive text input)
* sailfish-eas (Microsoft Exchange support)
* aliendalvik (Android™ App Support)
* sailfish-maps
* Any non-free audio/video codecs, etc.

Patterns
--------

The selection of packages for each hardware adaptation has to be put into
a pattern file, so that creating the image as well as any system updates in
the future can pull in and upgrade all packages related to the hardware
adaptation.

.. _patterns:

Modifying a pattern
```````````````````

To make an extra modification to a pattern, edit its respective file under
``hybris/droid-configs/patterns/``. Take care and always use ``git status/stash``
commands. Once happy, commit to your GitHub home and eventually PR upstream.

For patterns to take effect on the image, run the following:

.. code-block:: console

    PLATFORM_SDK $

    cd $ANDROID_ROOT
    rpm/dhd/helpers/build_packages.sh --configs

.. _mic:

Building the Image with MIC
---------------------------

You need to choose a `Sailfish OS version`_ you want to build.

.. important::
   Avoid building older releases unless you know what you're doing - we do not
   guarantee backwards compatibility for old Sailfish OS versions! E.g., expect
   patterns to break as new HA packages get introduced etc.

   Ensure you pick the same release as your target was in    :doc:`scratchbox2`.
   E.g., if target's ``ssu lr`` versions begin with ``4.0.1.``, build Sailfish OS update
   4.0.1.48 (check for the latest, non "Early Access" `Sailfish OS version`_)

Build a rootfs using RPM repositories and a kickstart file (NB: all errors are
non-critical as long as you end up with a generated .zip image):

.. _Sailfish OS version: http://en.wikipedia.org/wiki/Sailfish_OS#Version_history

.. code-block:: console

  PLATFORM_SDK $

  # Set the version of your choosing, latest is strongly preferred
  # (check with "Sailfish OS version" link above)
  export RELEASE=4.0.1.48
  # EXTRA_NAME adds your custom tag. It doesn't support '.' dots in it!
  export EXTRA_NAME=-my1
  rpm/dhd/helpers/build_packages.sh --mic

Once obtained the ``.zip`` file, sideload via your device's recovery mode,
or examine other particular ways of deploying to your device.

Jolla Store functionality can be enabled only if your device identifies itself
uniquely - either via IMEI or (for non-cellular devices) WLAN/BT MAC address.
Consult us on #sailfishos-porters IRC channel on oftc.net about details.

If creation fails due to absence of a package required by pattern, note down
the package name.

If that package is critical (e.g. ``libhybris``, ``qt5-qpa-hwcomposer-plugin`` etc.),
build and add it to the local repo as explained in :ref:`extra-mw`.
Afterwards perform:

* :ref:`patterns`
* :ref:`mic`

Otherwise if a package is not critical, and you accept to have less
functionality (or even unbootable) image, you can temporarily comment it out
from patterns in ``hybris/droid-configs/patterns`` and orderly perform:

* :ref:`patterns`
* :ref:`mic`

Alternatively (or if you can't find it among patterns) provide a line beginning
with dash (e.g. ``-jolla-camera``) indicating explicit removal of package,
to your .ks ``%packages`` section (remember that regenerating .ks will overwrite this
modification).

Troubleshooting
```````````````

/dev/null - Permission denied
'''''''''''''''''''''''''''''

Most likely the partition your Platform SDK resides in, is mounted with ``nodev`` option.
Remove that option from mount rules.

