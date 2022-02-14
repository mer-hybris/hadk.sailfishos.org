Setting up the SDKs
===================

Setting up required environment variables
-----------------------------------------

Throughout this guide we will be referencing the location of your SDK,
targets and source code. As is customary with Android hardware adaptations,
the device vendor (``$VENDOR``) and device codename (``$DEVICE``) are also
used, both in scripts and configuration files. **Throughout this guide as example,
we'll use Nexus 5 (lge/hammerhead for its vendor/device pair), and port it
using CyanogenMod 11.0 version as the "Android base".** Thus ensure you read
the code snippets carefully and rename where appropriate for your ported
device/vendor/base.

Now run the following commands on your host operating system fitting for your
device and setup:

.. code-block:: console

  HOST $

  cat <<'EOF' > $HOME/.hadk.env
  export ANDROID_ROOT="$HOME/hadk"
  export VENDOR="lge"
  export DEVICE="hammerhead"
  # "armv7hl" is still supported, but we encourage to have full 64bit ports
  export PORT_ARCH="aarch64"
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

.. _enter-sfos-sdk:

Setup the Platform SDK
----------------------

Instructions are found on Sailfish OS wiki ("Quick start" section is enough,
do not install SDK Targets yet): https://docs.sailfishos.org/Tools/Platform_SDK/Installation/

Afterwards, temporarily leave the PLATFORM_SDK to topup the newly created ``~/.mersdk.profile`` with necessary commands:

.. code-block:: console

  PLATFORM_SDK $

  exit

  HOST $

  cat <<'EOF' >> $HOME/.mersdk.profile
  function hadk() { source $HOME/.hadk.env; echo "Env setup for $DEVICE"; }
  hadk
  EOF

  sfossdk

You'll need some tools which are not installed into the Platform SDK by default:

* **android-tools-hadk** contains tools and utilities needed for working with
  the Android SDK
* **kmod** is needed by mic's qemu to build the image

.. code-block:: console

  PLATFORM_SDK $

  sudo zypper ref
  sudo zypper in android-tools-hadk kmod

The minimum Platform SDK SFOS version is 4.3.0.15. Use
``sdk-assistant`` command to upgrade your toolings and targets, or create from new
(especially when updating from 2.x to 3.x). To check what release you are on:

.. code-block:: console

  PLATFORM_SDK $

  # if no such file, you're on an old SDK version
  cat /etc/os-release

More information about keeping your SDK up-to-date:
https://github.com/sailfishos/sdk-setup/blob/master/sdk-setup/README.tips.wiki#SDK_Maintenance

Setting up an Android Build Environment
---------------------------------------

Downloading and Unpacking Ubuntu Chroot
```````````````````````````````````````

In order to maintain build stability, we use a *Ubuntu GNU/Linux*
``chroot`` environment from within the Platform SDK to build our Android
source tree. For Android device ports that require OpenJDK 1.8 or newer,
the following commands download and unpack the rootfs to
the appropriate location:

.. code-block:: console

  PLATFORM_SDK $

  TARBALL=ubuntu-focal-20210531-android-rootfs.tar.bz2
  curl -O https://releases.sailfishos.org/ubu/$TARBALL
  UBUNTU_CHROOT=$PLATFORM_SDK_ROOT/sdks/ubuntu
  sudo mkdir -p $UBUNTU_CHROOT
  sudo tar --numeric-owner -xjf $TARBALL -C $UBUNTU_CHROOT

In case you find you're not able to gain ``sudo`` privileges inside the Ubuntu
Chroot, execute the following inside the Platform SDK:

.. code-block:: console

  PLATFORM_SDK $

  sudo chroot $UBUNTU_CHROOT /bin/bash -c "chage -M 999999 $(id -nu 1000)"

.. _enter-ubu-chroot:

Entering Ubuntu Chroot
``````````````````````

.. code-block:: console

  PLATFORM_SDK $

  ubu-chroot -r $PLATFORM_SDK_ROOT/sdks/ubuntu

  # FIXME: Hostname resolution might fail. This error can be ignored.
  # Can be fixed manually by adding the hostname to /etc/hosts

  HABUILD_SDK $

  # Now you are in the HABUILD_SDK environment
  # To leave, just type `exit` or Ctrl+D, and you'll be back to the PLATFORM_SDK

.. _older-ubu-chroot:

If your port requires OpenJDK 1.7 or older
``````````````````````````````````````````

Our ubu-chroot environment is based on 20.04 LTS which provides OpenJDK 1.8 or
newer.

If your Android base build requires an older Java Development Kit, please
install the legacy ubu-chroot instead:

.. code-block:: console

  PLATFORM_SDK $

  TARBALL=ubuntu-trusty-20180613-android-rootfs.tar.bz2
  curl -O https://releases.sailfishos.org/ubu/$TARBALL
  UBUNTU_CHROOT=$PLATFORM_SDK_ROOT/sdks/ubuntu
  sudo mkdir -p $UBUNTU_CHROOT
  sudo tar --numeric-owner -xjf $TARBALL -C $UBUNTU_CHROOT

