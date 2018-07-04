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
device and setup:

.. _CyanogenMod Devices: http://wiki.cyanogenmod.org/w/Devices

.. code-block:: console

  HOST $

  cat <<'EOF' > $HOME/.hadk.env
  export PLATFORM_SDK_ROOT="/srv/mer"
  export ANDROID_ROOT="$HOME/hadk"
  export VENDOR="lge"
  export DEVICE="hammerhead"
  # ARCH conflicts with kernel build
  export PORT_ARCH="armv7hl"
  EOF

  cat <<'EOF' >> $HOME/.mersdkubu.profile
  function hadk() { source $HOME/.hadk.env; echo "Env setup for $DEVICE"; }
  export PS1="HABUILD_SDK [\${DEVICE}] $PS1"
  hadk
  EOF

This ensures that the environment is setup correctly when you use the
``ubu-chroot`` command to enter the Android SDK.

It also creates a function ``hadk`` that you can use to set or reset the environment
variables.

.. _enter-mer-sdk:

Setup the Platform SDK
----------------------

Instructions are found on Sailfish OS wiki: https://sailfishos.org/wiki/Platform_SDK_Installation

Afterwards, topup the newly created ``~/.mersdk.profile`` with necessary commands:

.. code-block:: console

  HOST $

  cat <<'EOF' >> $HOME/.mersdk.profile
  function hadk() { source $HOME/.hadk.env; echo "Env setup for $DEVICE"; }
  hadk
  EOF

We strongly encourage all porters to use at least 2.2.0.29 Platform SDK. Use
``sdk-manage`` command to upgrade your toolings and targets, or create from new.
To check what release you are on:

.. code-block:: console

  PLATFORM_SDK $

  cat /etc/system-release

Setting up an Android Build Environment
---------------------------------------

Downloading and Unpacking Ubuntu Chroot
```````````````````````````````````````

In order to maintain build stability, we use a *Ubuntu GNU/Linux*
``chroot`` environment from within the Platform SDK to build our Android
source tree. The following commands download and unpack the rootfs to
the appropriate location:

.. code-block:: console

  PLATFORM_SDK $

  TARBALL=ubuntu-trusty-20180613-android-rootfs.tar.bz2
  curl -O https://releases.sailfishos.org/ubu/$TARBALL
  UBUNTU_CHROOT=$PLATFORM_SDK_ROOT/sdks/ubuntu
  sudo mkdir -p $UBUNTU_CHROOT
  sudo tar --numeric-owner -xjf $TARBALL -C $UBUNTU_CHROOT

.. _enter-ubu-chroot:

Entering Ubuntu Chroot
``````````````````````

.. code-block:: console

  PLATFORM_SDK $

  ubu-chroot -r $PLATFORM_SDK_ROOT/sdks/ubuntu

  # FIXME: Hostname resolution might fail. This error can be ignored.
  # Can be fixed manually by adding the hostname to /etc/hosts

