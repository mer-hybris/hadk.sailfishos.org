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
the obtained information where indicated with ``<>`` (MER_ROOT value from
:ref:`mer-root`):

.. _CyanogenMod Devices: http://wiki.cyanogenmod.org/w/Devices

.. code-block:: console

  HOST $

  cat <<EOF > $HOME/.hadk.env
  export MER_ROOT="<insert value of your choosing>"
  export ANDROID_ROOT="$MER_ROOT/android/droid"
  export VENDOR="<insert vendor name here>"
  export DEVICE="<insert device codename here>"
  EOF

  cat <<EOF >> $HOME/.mersdkubu.profile
  alias hadk='source $HOME/.hadk.env'
  export PS1="Android SDK $PS1"
  hadk
  EOF

  cat <<EOF >> $HOME/.mersdk.profile
  alias hadk='source $HOME/.hadk.env'
  hadk
  EOF

This ensures that the environment is setup correctly when you use the
``ubu-chroot`` command to enter the Android SDK.

It also creates an alias ``hadk`` that you can use to reset the environment
variables in case you temporarily set it to some other values.

Setup the Mer SDK
-----------------

The Mer SDK setup is described on `the Mer wiki`_.

Ensure you are able to open a shell in the Mer SDK before moving on.

.. _the Mer wiki: http://wiki.merproject.org/wiki/Platform_SDK

Preparing the Mer SDK
---------------------

You'll need some tools which are not installed into the Mer SDK by default:

* **android-tools** contains tools and utilities needed for working with
  the Android SDK
* **createrepo** is needed to build repositories locally if you want to
  create or update local RPM repositories
* **zip** is needed to pack the final updater package into an .zip file

You can install those tools with the following command:

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

  TARBALL=ubuntu-quantal-android-rootfs.tar.bz2
  curl -O http://img.merproject.org/images/mer-hybris/ubu/$TARBALL
  UBUNTU_CHROOT=/parentroot/$MER_ROOT/sdks/ubuntu
  sudo mkdir -p $UBUNTU_CHROOT
  sudo tar --numeric-owner -xvjf $TARBALL -C $UBUNTU_CHROOT

You can now enter the ubuntu chroot like this:

.. code-block:: console

  MER_SDK $

  hadk

  ubu-chroot -r /$MER_ROOT/sdks/ubuntu


