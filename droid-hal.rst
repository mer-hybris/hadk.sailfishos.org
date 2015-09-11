Packaging Droid HAL
===================

In this chapter, we will package the build results of :doc:`android`
as RPM packages and create a local RPM repository. From there, the RPM
packages can be added to a local target and used to build libhybris and the
QPA plugin. They can also be used to build the rootfs.

Creating Repositories for a New Device
-------------------------------------

If the folders ``rpm, hybris/droid-configs, hybris-droid-hal-version-$DEVICE``
do not yet exist, create them as follows (example is for Nexus 5, adjust as
appropriate and push to your GitHub home):

.. code-block:: console

 MER_SDK $

 cd $ANDROID_ROOT
 mkdir rpm
 cd rpm
 git init
 git submodule add https://github.com/mer-hybris/droid-hal-device dhd
 # Rename 'hammerhead' and other values as appropriate
 cat <<'EOF' >droid-hal-hammerhead.spec
 # These and other macros are documented in dhd/droid-hal-device.inc

 %define device hammerhead
 %define vendor lge

 %define vendor_pretty LG
 %define device_pretty Nexus 5

 %define installable_zip 1

 %include rpm/dhd/droid-hal-device.inc
 EOF
 git add .
 git commit -m "[dhd] Initial content"
 # Create this repository under your GitHub home
 git remote add myname https://github.com/myname/droid-hal-hammerhead
 git push myname master
 cd -

 mkdir hybris/droid-configs
 cd hybris/droid-configs
 git init
 git submodule add https://github.com/mer-hybris/droid-hal-configs \
     droid-configs-device
 mkdir rpm
 cat <<'EOF' >rpm/droid-config-hammerhead.spec
 # These and other macros are documented in
 # ../droid-configs-device/droid-configs.inc

 %define device hammerhead
 %define vendor lge

 %define vendor_pretty LG
 %define device_pretty Nexus 5

 %define dcd_path ./

 # Adjust this for your device
 %define pixel_ratio 2.0

 # We assume most devices will
 %define have_modem 1

 %include droid-configs-device/droid-configs.inc
 EOF
 git add .
 git commit -m "[dcd] Initial content"
 # Create this repository under your GitHub home
 git remote add myname https://github.com/myname/droid-config-hammerhead
 git push myname master
 cd -

 rpm/dhd/helpers/add_new_device.sh
 # On Nexus 5 the output of the last command is:
 # Creating the following nodes:
 # sparse/
 # patterns/
 # patterns/jolla-configuration-hammerhead.yaml
 # patterns/jolla-ui-configuration-hammerhead.yaml
 # patterns/jolla-hw-adaptation-hammerhead.yaml
 cd hybris/droid-configs
 COMPOSITOR_CFGS=sparse/var/lib/environment/compositor
 mkdir -p $COMPOSITOR_CFGS
 cat <<EOF >$COMPOSITOR_CFGS/droid-hal-device.conf
 # Config for $VENDOR/$DEVICE
 EGL_PLATFORM=hwcomposer
 QT_QPA_PLATFORM=hwcomposer
 # Determine which node is your touchscreen by checking /dev/input/event*
 LIPSTICK_OPTIONS=-plugin evdevtouch:/dev/input/event0 \
   -plugin evdevkeyboard:keymap=/usr/share/qt5/keymaps/droid.qmap
 EOF
 git add .
 git commit -m "[dcd] Patterns and compositor config"
 git push myname master
 cd -

 mkdir hybris/droid-hal-version-hammerhead
 cd hybris/droid-hal-version-hammerhead
 git init
 git submodule add https://github.com/mer-hybris/droid-hal-version
 mkdir rpm
 cat <<'EOF' >rpm/droid-hal-version-hammerhead.spec
 # rpm_device is the name of the ported device
 %define rpm_device hammerhead
 # rpm_vendor is used in the rpm space
 %define rpm_vendor lge

 # Manufacturer and device name to be shown in UI
 %define vendor_pretty LG
 %define device_pretty Nexus 5

 # See ../droid-hal-version/droid-hal-device.inc for similar macros:
 %define have_vibrator 1
 %define have_led 1

 %include droid-hal-version/droid-hal-version.inc
 EOF
 git add .
 git commit -m "[dvd] Initial content"
 # Create this repository under your GitHub home
 git remote add myname \
     https://github.com/myname/droid-hal-version-hammerhead
 git push myname master

Now to complete you local manifest, this is how it would be done for Nexus 5.
Do it for your device by renaming accordingly:

.. code-block:: console

  # add the next 3 entries into .repo/local_manifests/hammerhead.xml

  <project path="rpm/"
           name="myname/droid-hal-hammerhead" revision="master" />
  <project path="hybris/droid-configs"
           name="myname/droid-config-hammerhead" revision="master" />
  <project path="hybris/droid-hal-version-hammerhead"
           name="myname/droid-hal-version-hammerhead" revision="master" />

Once all these 3 repositories get upstreamed under https://github.com/mer-hybris
create PR into an appropriate branch of the file
``.repo/local_manifests/hammerhead.xml`` to the
 https://github.com/mer-hybris/local_manifests repository.


Packaging ``droid-hal-device``
------------------------------

The ``$ANDROID_ROOT/rpm/`` dir contains the needed ``.spec`` file to make a set
of RPM packages that form the core Droid hardware adaptation part of the
hardware adaptation. It also builds a development package (ends with -devel)
that contains libraries and headers, which are used when building middleware
components later on.

.. _build-rpms:

Building the droid-hal-device packages
``````````````````````````````````````
.. important::
 # type ``zypper ref; zypper dup`` every now and again to update your Mer SDK!

The next step has to be carried out in a Mer SDK chroot:

.. code-block:: console

    MER_SDK $

    cd $ANDROID_ROOT

    rpm/dhd/helpers/build_packages.sh

This should compile all the needed packages, patterns, middleware and put them
under local repository. If anything needs modified, just re-run this script.

Troubleshoot errors from build_packages.sh
``````````````````````````````````````````

* **Installed (but unpackaged) file(s) found**: Add those files to this section
  in your rpm/droid-hal-$DEVICE.spec before ``%include ...`` line (files sampled
  from Motorola Moto G /falcon/ build):
.. code-block:: console

 %define straggler_files \\
 /init.mmi.boot.sh\\
 /init.mmi.touch.sh\\
 /init.qcom.ssr.sh\\
 /selinux_version\\
 /service_contexts\\
 %{nil}

If it was a port of Moto G, then you'd add ``- droid-hal-falcon-detritus`` to ``droid-configs/patterns/jolla-hw-adaptation-falcon.yaml`` -- substitute as appropriate for your device. Then finally re-run ``build_packages.sh``.

* **Anything mentioning ``mesa-llvmpipe``** -- happened only few times, simply re-run
  ``build_packages.sh``.

