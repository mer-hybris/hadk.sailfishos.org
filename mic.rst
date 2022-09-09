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

   Ensure you pick the same release as your target was in :doc:`build-env`.
   E.g., if target's ``ssu lr`` versions begin with ``4.4.0.``, build Sailfish OS update
   4.4.0.68 (check for the latest, non "Early Access" `Sailfish OS version`_)

Build a rootfs using RPM repositories and a kickstart file (NB: all errors are
non-critical as long as you end up with a generated .zip image):

.. _Sailfish OS version: http://en.wikipedia.org/wiki/Sailfish_OS#Version_history

.. code-block:: console

  PLATFORM_SDK $

  # Set the version of your choosing, latest is strongly preferred
  # (check with "Sailfish OS version" link above)
  export RELEASE=4.4.0.68
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
---------------

/dev/null - Permission denied (while using `mic`)
`````````````````````````````````````````````````

Most likely the partition your Platform SDK resides in, is mounted with ``nodev`` option.
Remove that option from mount rules.

Executing commands in the build environment
```````````````````````````````````````````

You can execute commands to build and install packages under the build
environment, inspect and debug any issues. The syntax is shown in
:doc:`build-env`.

Note that ``mb2`` uses a working copy of your original build target, which
means you can experiment with ``mb2 build-shell`` at will, but once you have
found a desired fix, make it permanent by recording the changes in your
source code (e.g. do not leave installed packages with ``zypper in`` lying
around, but add them to your .spec's ``BuildRequires``).

If you break your build environment via ``mb2 build-shell``, you can reset
it back to its clean state via ``mb2 -t $VENDOR-$DEVICE-$PORT_ARCH
build-requires reset``. This happens implicitly after re-running
``build_packages.sh`` [#]_.

Use ``mb2 ... build-requires diff`` if you want to know what you have done
to your build environment with ``mb2`` in terms of installed/removed
packages [#]_.

``mb2 ... build-shell`` is limited to launch only from directories where
you previously ran commands like ``mb2 ... build`` or ``mb2 ...
build-init`` [#]_. Such commands are run under ``$ANDROID_ROOT`` during the
build of dhd, so you can run ``mb2 build-shell`` from ``$ANDROID_ROOT`` if
you find no better place.


.. rubric:: Footnotes

.. [#] As long as your original build target does not change, ``mb2`` keeps
   using the same working copy ("snapshot" in mb2's speech) of your build
   target in subsequent executions, preserving any changes you make to it.
   When your original build target changes, ``mb2`` will reset the working copy
   to match the updated state of your original target next time it is invoked.
   This happens e.g. when you use ``build_packages.sh``, which intentionally
   works directly on your original build target. Factors that are regarded as
   a change in the original build target are: RPM DB change, SSU configuration,
   and few other things.

.. [#] If you need to make permanent changes to the original build environment
   (not recommended), add ``--no-snapshot=force`` option at the beginning of
   ``mb2`` command line (it is a global option).

.. [#] ``mb2`` looks for a directory named ``.mb2``, where it stores some of
   its state. It is created implicitly by ``mb2 ... build`` and you can also
   create it explicitly with ``mb2 -t $VENDOR-$DEVICE-$PORT_ARCH build-init``.
