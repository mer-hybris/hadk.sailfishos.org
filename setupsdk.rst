Setting up the SDKs
===================

Setting up required environment variables
-----------------------------------------

Throughout this guide we will be referencing the location of your SDK,
targets and source code. As is customary with Android hardware adaptations,
the device vendor (``$VENDOR``) and device codename (``$DEVICE``) are also
used, both in scripts and configuration files. For a list of vendor and
device names, refer to :doc:`devices`.

Now run the following commands on your host operating system substituting
the obtained information where indicated with ``[]`` (MER_ROOT value from
:ref:`mer-root`):

.. _CyanogenMod Devices: http://wiki.cyanogenmod.org/w/Devices

.. code-block:: console

  HOST $

  cat <<'EOF' > $HOME/.hadk.env
  export MER_ROOT="[insert value of your choosing]"
  export ANDROID_ROOT="$MER_ROOT/android/droid"
  export VENDOR="[insert vendor name here]"
  export DEVICE="[insert device codename here]"
  EOF

  cat <<'EOF' >> $HOME/.mersdkubu.profile
  function hadk() { source $HOME/.hadk.env${1:+.$1}; echo "Env setup for $DEVICE"; }
  export PS1="HABUILD_SDK [\${DEVICE}] $PS1"
  hadk
  EOF

  cat <<'EOF' >> $HOME/.mersdk.profile
  function hadk() { source $HOME/.hadk.env${1:+.$1}; echo "Env setup for $DEVICE"; }
  hadk
  EOF

This ensures that the environment is setup correctly when you use the
``ubu-chroot`` command to enter the Android SDK.

It also creates a function ``hadk`` that you can use to set or reset the environment
variables. As you can see it also supports ~/.hadk.env.<name> to allow you to work on
multiple devices in different sessions.

.. _enter-mer-sdk:

Setup the Mer SDK
-----------------

Mer Platform SDK should be installed under your $HOME, to avoid possible
mount/options issues. Setup is described on `the Mer wiki`_.

Ensure you are able to open a shell in the Mer SDK before moving on.

.. _the Mer wiki: https://wiki.merproject.org/wiki/Platform_SDK#tl.3Bdr

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

In order to maintain build stability, we use an *Ubuntu GNU/Linux*
``chroot`` environment from within the Mer SDK to build our Android
source tree. The following commands download and unpack the rootfs to
the appropriate location:

.. code-block:: console

  MER_SDK $

  hadk

  TARBALL=ubuntu-trusty-android-rootfs.tar.bz2
  curl -O http://img.merproject.org/images/mer-hybris/ubu/$TARBALL
  UBUNTU_CHROOT=/parentroot/$MER_ROOT/sdks/ubuntu
  sudo mkdir -p $UBUNTU_CHROOT
  sudo tar --numeric-owner -xvjf $TARBALL -C $UBUNTU_CHROOT

.. _enter-ubu-chroot:

Entering Ubuntu Chroot
``````````````````````

.. code-block:: console

  MER_SDK $

  hadk

  ubu-chroot -r /parentroot/$MER_ROOT/sdks/ubuntu

  #FIXME: Hostname resolution might fail. This error can be ignored.
  Can be fixed manually by adding the hostname to /etc/hosts

