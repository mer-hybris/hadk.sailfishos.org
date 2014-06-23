Porting Sailfish OS to a New Device
===================================

Find Device Info
----------------

See :doc:`prerequisites` for sourcing information about your device.

This example has snippets based on the Encore_. The CyanogenMod base
ROM has been downloaded using:

.. _Encore: http://wiki.cyanogenmod.org/w/Encore_Info

.. code-block:: console

  MER_SDK $

  curl -L -O http://download.cyanogenmod.org/get/jenkins/51847/cm-10.1.3.2-encore.zip

Installation of the ROM is described in the `Encore install guide`_.

.. _`Encore install guide`: http://wiki.cyanogenmod.org/w/Install_CM_for_encore

Prepare Environment
-------------------

Make sure all the commands use the correct ``$DEVICE`` and ``$VENDOR`` by
updating your ``~/.hadk.env`` (in this example, ``DEVICE=encore`` and
``VENDOR=bn``).

Build Android
-------------

Building Android is done inside the Android SDK. Ensure the environment
variables are set up correctly by executing ``hadk`` inside the Android SDK:

.. code-block:: console

  HABUILD_SDK $

  hadk

Device Repos
````````````

You'll need a new local manifest. The example given below is for encore. Modify it appropriately.

The entries will vary per-device but you'll need the device and kernel repos
as a minimum. Depending on any build issues that arise you may need additional
``hardware/`` and/or ``external/`` repositories (the example ones probably
won't be needed for your device). You'll need to fork the kernel repository in
order to update the default config:

.. FIXME: Avoid forking the kernel repo by adding support for a 'local config'

* ``device/$VENDOR/$DEVICE``
* ``kernel/$VENDOR/$DEVICE``

.. code-block:: console

  HABUILD_SDK $

  mkdir .repo/local_manifests/
  cat <<EOF > .repo/local_manifests/encore.xml
  <?xml version="1.0" encoding="UTF-8"?>
  <manifest>
    <project path="device/bn/encore" name="CyanogenMod/android_device_bn_encore" revision="cm-10.1" />
    <project path="kernel/bn/encore" name="lbt/android_kernel_bn_encore" revision="cm-10.1-staging" />
    <project path="hardware/ti/wlan" name="CyanogenMod/android_hardware_ti_wlan" revision="cm-10.1" />
    <project path="external/wpa_supplicant_8" name="CyanogenMod/android_external_wpa_supplicant_8" revision="cm-10.1" />
  </manifest>
  EOF

Once you have a local manifest you can sync the Git repositories:

.. code-block:: console

  HABUILD_SDK $

  repo sync
  breakfast $DEVICE

If you get errors about duplicate repositories, see the "Common Pitfalls"
section in :doc:`android`.

Configure Mountpoint informatiion
`````````````````````````````````

Until ``systemd`` is updated we need to patch
``hybris/hybris-boot/fixup-mountpoints`` for the device. The idea here is to
ensure the udev-less initrd mounts the correct ``/boot`` and ``/data``
partition. If you're lucky the device will simply use
``/dev/block/<somedev>`` and you can use the i9305 approach.
If not then look in the recovery ``fstab`` for the
right mapping. The build log will have provided feedback like:

.. code-block:: console

  HABUILD_SDK $

  hybris/hybris-boot/Android.mk:48: ********************* /boot should live on /dev/block/platform/msm_sdcc.1/by-name/boot
  hybris/hybris-boot/Android.mk:49: ********************* /data should live on /dev/block/platform/msm_sdcc.1/by-name/userdata


Note that a subsequent ``repo sync`` will reset this unless you update your
``.repo/local_manifests/encore.xml`` to point to a fork of the hybris-boot
repo.

Additional packages
```````````````````

Additional tools can be downloaded inside the Android Ubuntu chroot. For
example, devices based on the U-Boot bootloader require the ``mkimage``
utility, which can be installed with the following command:

.. code-block:: console

  HABUILD_SDK $

  sudo apt-get install uboot-mkimage


Do a build
``````````

You'll probably need to iterate this a few times to spot missing repositories,
tools, configuration files and others:

.. code-block:: console

  HABUILD_SDK $

  mka hybris-hal

For example, an error about ``hardware/ti/wlan/mac80211/compat_wl12xx`` leads
us to check ``.repo/manifests/cm-10.1.3.xml`` and find a likely looking
project; you can see in the example above it was added to
``.repo/local_manifests/encore.xml``.

If you're building for encore, try removing it from the local manifest and
removing the ``hardware/ti`` directory to see the errors. Repeat this for
other local projects you may find. Also note that you may have to run ``mka
hybris-hal`` multiple times; please report a bug if that happens as something
will be wrong with dependencies.

If you hit any other issues then please report them too.

Kernel Config
`````````````

Once the kernel has built you can check the kernel config. You can use the Mer kernel config checker:

.. code-block:: console

  HABUILD_SDK $

  tmp/mer_verify_kernel_config ./out/target/product/$DEVICE/obj/KERNEL_OBJ/.config

Look for a file like: ``arch/arm/configs/$DEVICE_cm10.1_defconfig`` in ``kernel/$VENDOR/$DEVICE/`` and modify it in your kernel repo fork.


Success
```````

You've finished this section when your build finishes with:

.. code-block:: console

  HABUILD_SDK $

  Install: $ANDROID_ROOT/out/target/product/$DEVICE/hybris-recovery.img
  Install: $ANDROID_ROOT/out/target/product/$DEVICE/hybris-boot.img


Mer-side package building
-------------------------

As you may expect this section is done in the Mer SDK. Again, ensure the environment is correct:

.. code-block:: console

  MER_SDK $

  hadk

Device Specific Target
``````````````````````

Setup a device-specific target. This step is generally only needed when working with the HA layer because the target will contain device-specific information that is not usually needed in a target.

Setup a device target: :doc:`scratchbox2`

Create a simple ``.spec`` file that sets the correct variables and then
includes ``droid-hal-device.inc``, which contains the RPM building logic:

.. code-block:: console

  MER_SDK $

  cd $ANDROID_ROOT
  cat <<EOF > rpm/droid-hal-$DEVICE.spec
  # device is the cyanogenmod codename for the device
  # eg mako = Nexus 4
  %define device $DEVICE
  # vendor is used in device/%vendor/%device/
  %define vendor $VENDOR

  %include rpm/droid-hal-device.inc
  EOF

Device Specific Config
``````````````````````

You'll need as a minimum:

.. code-block:: console

  MER_SDK $

  COMPOSITOR_CONFIGS_DIR=rpm/device-$VENDOR-$DEVICE-configs/var/lib/environment/compositor
  mkdir -p $COMPOSITOR_CONFIGS_DIR
  cat <<EOF >$COMPOSITOR_CONFIGS/droid-hal-device.conf
  # Config for $VENDOR/$DEVICE
  HYBRIS_EGLPLATFORM=fbdev
  QT_QPA_PLATFORM=hwcomposer
  LIPSTICK_OPTIONS=-plugin evdevtouch:/dev/input/event0 -plugin evdevkeyboard:keymap=/usr/share/qt5/keymaps/droid.qmap
  EOF


Build the HAL
`````````````

See :doc:`droid-hal`. To build a local repository for installing packages:

.. code-block:: console

  MER_SDK $

  PKG=droid-hal-device
  rm RPMS/*
  mb2 -t $VENDOR-$DEVICE-armv7hl -s rpm/droid-hal-$DEVICE.spec build
  mkdir -p $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG/
  rm -f $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG/*.rpm
  mv RPMS/*${DEVICE}* $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG
  createrepo  $ANDROID_ROOT/droid-local-repo/$DEVICE

You will need to update the target every time to build new RPMs.


HAL specific packages
`````````````````````

Target setup
''''''''''''

Setup to use droid headers

As a one off (per device-target) we need to add the local repo to our target:

.. code-block:: console

  MER_SDK $

  sb2 -t $VENDOR-$DEVICE-armv7hl -R -msdk-install \
      ssu ar local file://$ANDROID_ROOT/droid-local-repo/$DEVICE

Check it's there:

.. code-block:: console

  MER_SDK $

  sb2 -t $VENDOR-$DEVICE-armv7hl -R -msdk-install ssu lr

Now set the SDK target to use an up-to-date repo:

.. code-block:: console

  MER_SDK $

  sb2 -t $VENDOR-$DEVICE-armv7hl -R -msdk-install ssu domain sales
  sb2 -t $VENDOR-$DEVICE-armv7hl -R -msdk-install ssu dr sdk

And install the droid-hal-device headers:

.. code-block:: console

  MER_SDK $

  sb2 -t $VENDOR-$DEVICE-armv7hl -R -msdk-install zypper ref
  sb2 -t $VENDOR-$DEVICE-armv7hl -R -msdk-install \
      zypper install droid-hal-$DEVICE-devel

If you rebuild the droid-side then you'll need to repeat the two commands above.


Build Area Setup
''''''''''''''''

Setup an area to build packages

.. code-block:: console

  MER_SDK $

  mkdir -p $MER_ROOT/devel/mer-hybris
  cd $MER_ROOT/devel/mer-hybris

Packages
''''''''

libhybris
~~~~~~~~~

Check out the libhybris source code from Git:

.. code-block:: console

  MER_SDK $

  PKG=libhybris
  cd $MER_ROOT/devel/mer-hybris
  git clone https://github.com/mer-hybris/libhybris.git
  cd libhybris

Some packages will use submodules:

.. code-block:: console

  MER_SDK $

  git submodule update  
  cd libhybris

Now use ``mb2`` to build the package. This essentially runs a slightly
modified ``rpmbuild`` using the Scratchbox2 target. It also pulls in
build requirements into the target. Note that this makes the target
'dirty' and you may miss build dependencies. This should be caught during
clean builds.

.. code-block:: console

  MER_SDK $

  mb2 -s ../rpm/libhybris.spec -t  $VENDOR-$DEVICE-armv7hl build

Now add the packages you just built to the local repo and refresh the repo cache:

.. code-block:: console

  MER_SDK $

  mkdir -p $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG/
  rm -f $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG/*.rpm
  mv RPMS/*.rpm $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG
  createrepo  $ANDROID_ROOT/droid-local-repo/$DEVICE
  sb2 -t  $VENDOR-$DEVICE-armv7hl -R -msdk-install zypper ref

Note that all repositories that are in ``tar_git`` format (for use with OBS)
will have their RPM packages built locally might not always have the right
release and version set.

At this point, and for the libhybris package only, you can remove the mesa-llvmpipe packages from the target:

.. code-block:: console

  MER_SDK $

  sb2 -t  $VENDOR-$DEVICE-armv7hl -R -msdk-build zypper rm mesa-llvmpipe

Failure to do this will cause problems pulling in build requirements for other packages.


qt5-qpa-hwcomposer-plugin
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

  MER_SDK $

  PKG=qt5-qpa-hwcomposer-plugin
  cd $MER_ROOT/devel/mer-hybris
  git clone https://github.com/mer-hybris/$PKG.git
  cd $PKG
  mb2 -s rpm/$PKG.spec -t  $VENDOR-$DEVICE-armv7hl build
  mkdir -p $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG/
  rm -f $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG/*.rpm
  mv RPMS/*.rpm $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG
  createrepo  $ANDROID_ROOT/droid-local-repo/$DEVICE
  sb2 -t  $VENDOR-$DEVICE-armv7hl -R -msdk-install zypper ref

sensorfw
~~~~~~~~

.. code-block:: console

  MER_SDK $

  PKG=sensorfw
  SPEC=sensorfw-qt5-hybris
  OTHER_RANDOM_NAME=hybris-libsensorfw-qt5

  cd $MER_ROOT/devel/mer-hybris
  git clone https://github.com/mer-hybris/$PKG.git
  cd $PKG
  mb2 -s rpm/$SPEC.spec -t  $VENDOR-$DEVICE-armv7hl build
  mkdir -p $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG/
  rm -f $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG/*.rpm
  mv RPMS/*.rpm $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG
  createrepo  $ANDROID_ROOT/droid-local-repo/$DEVICE
  sb2 -t  $VENDOR-$DEVICE-armv7hl -R -msdk-install zypper ref

ngfd-plugin-droid-vibrator
~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: console

  MER_SDK $

  PKG=ngfd-plugin-droid-vibrator
  SPEC=$PKG

  cd $MER_ROOT/devel/mer-hybris
  git clone https://github.com/mer-hybris/$PKG.git
  cd $PKG
  mb2 -s rpm/$SPEC.spec -t  $VENDOR-$DEVICE-armv7hl build
  mkdir -p $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG/
  rm -f $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG/*.rpm
  mv RPMS/*.rpm $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG
  createrepo  $ANDROID_ROOT/droid-local-repo/$DEVICE
  sb2 -t  $VENDOR-$DEVICE-armv7hl -R -msdk-install zypper ref


pulseaudio-modules-droid
~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: console

  MER_SDK $

  PKG=pulseaudio-modules-droid
  SPEC=$PKG

  cd $MER_ROOT/devel/mer-hybris
  git clone https://github.com/mer-hybris/$PKG.git
  cd $PKG
  mb2 -s rpm/$SPEC.spec -t  $VENDOR-$DEVICE-armv7hl build
  mkdir -p $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG/
  rm -f $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG/*.rpm
  mv RPMS/*.rpm $ANDROID_ROOT/droid-local-repo/$DEVICE/$PKG
  createrepo  $ANDROID_ROOT/droid-local-repo/$DEVICE
  sb2 -t  $VENDOR-$DEVICE-armv7hl -R -msdk-install zypper ref

