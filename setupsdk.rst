Setting up the SDKs
===================

Setting up required environment variables
-----------------------------------------

Throughout this guide we will be referencing the location of your SDK,
targets and source code. As is customary with Android hardware adaptations,
the device vendor (``$VENDOR``) and device codename (``$DEVICE``) are also
used, both in scripts and configuration files. **Throughout this guide as example,
we'll use Nexus 5 (lge/hammerhead for its vendor/device pair), and port it
basing on CyanogenMod 11.0 version.** Thus ensure you read snippets carefully
and rename where appropriate for your ported device/vendor/base.

Now run the following commands on your host operating system fitting for your
device and setup (MER_ROOT value from :ref:`mer-root`):

.. _CyanogenMod Devices: http://wiki.cyanogenmod.org/w/Devices

.. code-block:: console

  HOST $

  cat <<'EOF' > $HOME/.hadk.env
  export MER_ROOT="/path/to/mer"
  export ANDROID_ROOT="$MER_ROOT/android/droid"
  export VENDOR="lge"
  export DEVICE="hammerhead"
  EOF

  cat <<'EOF' >> $HOME/.mersdkubu.profile
  function hadk() { source $HOME/.hadk.env; echo "Env setup for $DEVICE"; }
  export PS1="HABUILD_SDK [\${DEVICE}] $PS1"
  hadk
  EOF

  cat <<'EOF' >> $HOME/.mersdk.profile
  function hadk() { source $HOME/.hadk.env; echo "Env setup for $DEVICE"; }
  hadk
  EOF

This ensures that the environment is setup correctly when you use the
``ubu-chroot`` command to enter the Android SDK.

It also creates a function ``hadk`` that you can use to set or reset the environment
variables.

.. _enter-mer-sdk:

Setup the Mer SDK
-----------------

Mer Platform SDK should be installed under your $HOME, big enough and without
mount --binds, to avoid possible mount/options issues. Setup MerSDK as follows::

 HOST $

 export MER_ROOT=$HOME/mer
 cd $HOME
 TARBALL=mer-i486-latest-sdk-rolling-chroot-armv7hl-sb2.tar.bz2
 curl -k -O https://img.merproject.org/images/mer-sdk/$TARBALL
 sudo mkdir -p $MER_ROOT/sdks/sdk
 cd $MER_ROOT/sdks/sdk
 sudo tar --numeric-owner -p -xjf $HOME/$TARBALL
 echo "export MER_ROOT=$MER_ROOT" >> ~/.bashrc
 echo 'alias sdk=$MER_ROOT/sdks/sdk/mer-sdk-chroot' >> ~/.bashrc
 exec bash
 echo 'PS1="MerSDK $PS1"' >> ~/.mersdk.profile
 cd $HOME
 sdk
 # These commands are a tmp workaround of glitch when working with target:
 zypper ar http://repo.merproject.org/obs/home:/sledge:/mer/latest_i486/ \
  curlfix
 zypper ref curlfix
 zypper dup --from curlfix

Ensure you are able to open a shell in the Mer SDK before moving on.

Preparing the Mer SDK
---------------------

You'll need some tools which are not installed into the Mer SDK by default:

* **android-tools** contains tools and utilities needed for working with
  the Android SDK
* **createrepo** is needed to build repositories locally if you want to
  create or update local RPM repositories
* **zip** is needed to pack the final updater package into an .zip file

The latest SDK tarballs should include these but if not you can
install those tools with the following command:

.. code-block:: console

  MER_SDK $

  sudo zypper in android-tools createrepo zip

Setting up an Android Build Environment
---------------------------------------

Downloading and Unpacking Ubuntu Chroot
```````````````````````````````````````

In order to maintain build stability, we use a *Ubuntu GNU/Linux*
``chroot`` environment from within the Mer SDK to build our Android
source tree. The following commands download and unpack the rootfs to
the appropriate location:

.. code-block:: console

  MER_SDK $

  hadk

  TARBALL=ubuntu-trusty-android-rootfs.tar.bz2
  curl -O http://img.merproject.org/images/mer-hybris/ubu/$TARBALL
  UBUNTU_CHROOT=$MER_ROOT/sdks/ubuntu
  sudo mkdir -p $UBUNTU_CHROOT
  sudo tar --numeric-owner -xvjf $TARBALL -C $UBUNTU_CHROOT

.. _enter-ubu-chroot:

Entering Ubuntu Chroot
``````````````````````

.. code-block:: console

  MER_SDK $

  hadk

  ubu-chroot -r $MER_ROOT/sdks/ubuntu

  #FIXME: Hostname resolution might fail. This error can be ignored.
  Can be fixed manually by adding the hostname to /etc/hosts

