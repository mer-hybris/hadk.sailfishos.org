Setting up the SDKs
===================

Setting up required environment variables
-----------------------------------------

Throughout this guide we will be referencing the installed location of
your SDK, targets and src; your device vendor and device codename,
both in scripts and configuration files.

(Refer to :doc:`devices` for information on obtaining the $DEVICE and
$VENDOR values.)

Now run the following commands on your host operating system substituting
the obtained information where indicated.

.. _CyanogenMod Devices: http://wiki.cyanogenmod.org/w/Devices

.. code-block:: console

  HOST $

  cat <<EOF > $HOME/.hadk.env
  export MER_ROOT="$HOME/mer"
  export ANDROID_ROOT="\$MER_ROOT/android/droid"
  export VENDOR="[MANUFACTURER]"
  export DEVICE="[CODENAME]"
  EOF

  cat <<EOF >> $HOME/.mersdkubu.profile
  alias hadk='source $HOME/.hadk.env'
  hadk
  EOF

  cat <<EOF >> $HOME/.mersdk.profile
  alias hadk='source $HOME/.hadk.env'
  hadk
  EOF

This ensures that the environment is setup correctly when you use the
`ubu-chroot` command to enter the android sdk.

You can also now simply type **hadk** when you work on a different DEVICE/VENDOR.

FIXME: This depends on lbt's updates to android-tools. Verify this
works by entering...

Setup the Mer SDK
-----------------

The Mer SDK setup is described on `the Mer wiki`_.

Ensure you are able to enter the Mer SDK before moving on.

.. _the Mer wiki: http://wiki.merproject.org/wiki/Platform_SDK

Preparing the Mer SDK
---------------------

You'll need some tools which are not installed into the Mer SDK by default:


.. code-block:: console

  MER_SDK $

  sudo zypper in createrepo zip

createrepo is needed to build repos if you want/need to update local targets

zip is needed to create the final installer

Setting up an Android Build Environment
---------------------------------------

Downloading and Unpacking Ubuntu Chroot
```````````````````````````````````````

In order to maintain build stability, we use an *Ubuntu GNU/Linux*
chroot environment from within the *Mer SDK* to build our Android
source tree. The following commands download and unpack the rootfs to
the appropriate location.

.. code-block:: console

  MER_SDK $

  hadk

  cd $HOME; curl -O http://img.merproject.org/images/mer-hybris/ubu/ubuntu-lucid-android-rootfs.tar.bz2
  sudo mkdir -p /parentroot/$MER_ROOT/sdks/ubuntu
  sudo tar --numeric-owner -xvjf $HOME/ubuntu-lucid-android-rootfs.tar.bz2 -C /parentroot/$MER_ROOT/sdks/ubuntu

**WARNING:** ^^ tarball extracts to /parentroot/$HOME/mer/sdks/ubuntu/ubuntu/*


You can now enter the ubuntu chroot like this:

.. code-block:: console

  MER_SDK $

  hadk

  ubu-chroot -r /$MER_ROOT/sdks/ubuntu


