Building the Android HAL
========================

Setting up required environment variables
-----------------------------------------

Throughout this guide we will be referencing the installed location of
your SDK, targets and src; your device vendor and device codename,
both in scripts and configuration files.

To get this information if you're not sure, find your device here:
`CyanogenMod Devices`_, note down the "*Manufacturer*" and
"*Codename*" values, which are displayed in the side bar on the right.

Now run the following commands substituting the obtained information
where indicated.

.. _CyanogenMod Devices: http://wiki.cyanogenmod.org/w/Devices

.. code-block:: console

  ANDROID_SDK $

  cat <<EOF > $HOME/.mersdkubu.profile
  export MER_ROOT="$HOME/mer"
  export ANDROID_ROOT="$MER_ROOT/android/droid"
  export VENDOR="[MANUFACTURER]"
  export DEVICE="[CODENAME]"
  EOF

This ensures that the environment is setup correctly when you use the
`ubu-chroot` command to enter the android sdk.

FIXME: This depends on lbt's updates to android-tools. Verify this
works by entering...

Setting up an Android Build Environment
---------------------------------------

Downloading and Unpacking Ubuntu Chroot
```````````````````````````````````````

In order to maintain build stability, we use an *Ubuntu GNU/Linux*
chroot environment from within the *Mer SDK* to build our Android
source tree. The following commands download and unpack the rootfs to
the appropriate location.

.. code-block:: console

  ANDROID_SDK $
  
  cd $HOME; curl -O http://img.merproject.org/images/mer-hybris/ubu/ubuntu-lucid-android-rootfs.tar.bz2
  sudo mkdir -p /parentroot/$MER_ROOT/targets/ubuntu
  sudo tar --numeric-owner -xvjf $HOME/ubuntu-lucid-android-rootfs.tar.bz2 -C /parentroot/$MER_ROOT/targets/ubuntu

WARNING: ^^ tarball extracts to /parentroot/$MER_ROOT/targets/ubuntu/unbuntu/*


Checking out CyanogenMod Source
-------------------------------

Our build process is based around the *CyanogenMod* projects source
tree, but when required we've forked some projects, in order to apply
patches required to make *libhybris* function correctly, to build
hybris based hardware adaptations and to minimise the actions and
services in the .rc files.

Firstly you need to install the *repo* command from the AOSP source
code repositories, the instructions can be found from the below link:

* `Installing repo`_

.. _Installing repo: http://source.android.com/source/downloading.html#installing-repo

After you've installed the *repo* command, the following set of
commands, download the required projects and also our officially
supported device profiles, for building libhybris based *Mer* device
hardware adaptations.

Ensure you have done `git config --global user.email
"you@example.com"` and `git config --global user.name "Your Name"`.

.. code-block:: console

    ANDROID_SDK $

    . $HOME/.mersdkubu.profile
    sudo mkdir -p $ANDROID_ROOT
    sudo chown -R $USER $ANDROID_ROOT
    cd $ANDROID_ROOT
    repo init -u git://github.com/mer-hybris/android.git -b hybris-10.1
    repo sync

The expected disk usage for the source tree after ``repo sync``
is **9.4 GB** (as of 2014-02-18).

This may take some time(!)

Building Relevant Bits of CyanogenMod
-------------------------------------

In the Android build tree, run the following in a ``bash`` shell (if you
are using e.g. ``zsh``, you need to run these commands in a ``bash`` shell):

.. code-block:: console

  ANDROID_SDK $

  source build/envsetup.sh
  export USE_CCACHE=1

.. code-block:: console

  ANDROID_SDK $

  breakfast $DEVICE

  # [lbt] This works for me
  rm .repo/local_manifests/roomservice.xml

*XXX: [thp]: For i9305 the ``breakfast`` results in duplicate repos for me? Had to
use "lunch cm_$DEVICE-eng" instead (because we have modified repos for that device
in our default.xml) [sl]: There is no cm_mako among options, and I just ignored
the duplicate error - all went ahead fine. Play with roomservice is welcomed though,
thanks*

.. code-block:: console

  ANDROID_SDK $

  mka hybris-hal

The relevant output bits will be in ``out/target/product/$DEVICE/``, in
particular:

* ``hybris-boot.img``: Kernel and initrd
* ``hybris-recovery.img``: Recovery boot image
* ``system/`` and ``root/``: HAL system libraries and binaries

The expected disk usage for the source and binaries after ``mka hybris-hal``
is **16 GB** (as of 2014-02-18).

For Supported Devices
`````````````````````

See :doc:`devices` for a list of devices supported by HADK. Supported
devices are automatically downloaded as part of the HADK android build
environment.

Common Pitfalls
---------------

* If ``repo sync`` fails with a message like *fatal: duplicate path
  device/samsung/smdk4412-common in /home/nemo/android/.repo/manifest.xml*,
  remove the local manifest with ``rm .repo/local_manifests/roomservice.xml``
* In some cases (with parallel builds), the build can fail, in this case, use
  ``mka hybris-hal -j1`` to retry with a non-parallel build and see the error
  message without output from parallel jobs. The build usually ends with:

.. code-block:: console

  ANDROID_SDK $

  ...
  Install: .../out/target/product/$DEVICE/hybris-recovery.img
  ...
  Install: .../out/target/product/$DEVICE/hybris-boot.img
  ...
  Made boot image: .../out/target/product/$DEVICE/boot.img

