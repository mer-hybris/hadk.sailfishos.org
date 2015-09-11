Building the Android HAL
========================

.. _checkout-cm-source:

Checking out CyanogenMod Source
-------------------------------

Our build process is based around the CyanogenMod projects source
tree, but when required we've modified some projects, in order to apply
patches required to make libhybris function correctly, and
to minimise the built-in actions and services in the ``init.*.rc`` files.

Ensure you have setup your name and e-mail address in your Git configuration:

.. code-block:: console

  MER_SDK $

  git config --global user.name "Your Name"
  git config --global user.email "you@example.com"

You also need to install the ``repo`` command from the AOSP source
code repositories, see `Installing repo`_.

.. _Installing repo: http://source.android.com/source/downloading.html#installing-repo

After you've installed the ``repo`` command, a set of commands below download
the required projects for building the modified parts of Android used in
libhybris-based Mer device hardware adaptations.

All available CM versions that you can port on can be seen here:
https://github.com/mer-hybris/android/branches

Choose a CM version which has the best hardware support for your device.

The result of your Sailfish OS port will be an installable ZIP file. Before
deploying it onto your device, you'll have to flash a corresponding version of
CyanogenMod, so Sailfish OS can re-use its Android HAL shared objects.

If your primary ROM is not CyanogenMod, or is of another version, look for
MultiROM support for your device. It supports Sailfish OS starting v28.

.. code-block:: console

  HABUILD_SDK $

  hadk

  sudo mkdir -p $ANDROID_ROOT
  sudo chown -R $USER $ANDROID_ROOT
  cd $ANDROID_ROOT
  #PREREL:
  repo init -u git://github.com/sledges/android.git -b modular-hybris-11.0

Device repos
------------

You will need to provide device-specific repositories, for Android as well as
for the mer-hybris builds. Create directory at first:

.. code-block:: console

  HABUILD_SDK $

  hadk

  mkdir $ANDROID_ROOT/.repo/local_manifests

You'll have to create the local
manifest yourself, which contains at least two repos: one for the kernel, another
for the device configuration. Find those CM device wiki, for Nexus 5 it would be
http://wiki.cyanogenmod.org/w/Hammerhead_Info inside the **Source code** table.
Local manifest below will also need pointing to correct branches - identify which
one matches the default manifest branch.

Add the following content to ``$ANDROID_ROOT/.repo/local_manifests/$DEVICE.xml``:

.. code-block:: console

  <?xml version="1.0" encoding="UTF-8"?>
  <manifest>
    <project path="device/lge/hammerhead"
      name="CyanogenMod/android_device_lge_hammerhead"
      revision="stable/cm-11.0" />
    <project path="kernel/lge/hammerhead"
      name="CyanogenMod/android_kernel_lge_hammerhead"
      revision="stable/cm-11.0" />
  </manifest>

Time to sync the whole source code, this might take a while:

.. code-block:: console

  HABUILD_SDK $

  hadk

  repo sync --fetch-submodules

The expected disk usage for the source tree after the sync is **13 GB** (as of
2015-09-09, hybris-11.0 branch). Depending on your connection, this might take
some time. In the mean time, make yourself familiar with the rest of this guide.

Configure Mountpoint Information
--------------------------------

Until ``systemd`` reached a new enough version, we need to patch
``hybris/hybris-boot/fixup-mountpoints`` for the device. The idea here is to
ensure the udev-less initrd mounts the correct ``/boot`` and ``/data``
partition. If you're lucky the device will simply use ``/dev/block/<somedev>``
and you can use the i9305 approach. If not then look in the recovery ``fstab``
for the right mapping. Please submit patches for the ``fixup-mountpoints`` file!

To double check, you can boot to CM and ``adb shell`` to examine
``/dev/block*`` and ``/dev/mmc*`` (udev-full) contents. Also boot into
ClockworkMod or TWRP recovery, to check those (udev-less) paths there too.

The build log will also have provided feedback like:

.. code-block:: console

  HABUILD_SDK $

  hybris/hybris-boot/Android.mk:48: ********************* /boot should
    live on /dev/block/platform/msm_sdcc.1/by-name/boot
  hybris/hybris-boot/Android.mk:49: ********************* /data should
    live on /dev/block/platform/msm_sdcc.1/by-name/userdata

Note that a subsequent ``repo sync`` will reset this, unless the file
``.repo/local_manifests/hammerhead.xml`` is updated to point to a fork of the
hybris-boot repo.


.. _build-cm-bits:

Building Relevant Bits of CyanogenMod
-------------------------------------

In the Android build tree, run the following in a ``bash`` shell (if you
are using e.g. ``zsh``, you need to run these commands in a ``bash`` shell,
as the Android build scripts are assuming you are running ``bash``).

You'll probably need to iterate this a few times to spot missing repositories,
tools, configuration files and others:

.. code-block:: console

  HABUILD_SDK $

  hadk

  source build/envsetup.sh
  export USE_CCACHE=1

  breakfast $DEVICE

  make -j4 hybris-hal

The relevant output bits will be in ``out/target/product/$DEVICE/``, in
particular:

* ``hybris-boot.img``: Kernel and initrd
* ``hybris-recovery.img``: Recovery boot image
* ``system/`` and ``root/``: HAL system libraries and binaries

The expected disk usage ny the source and binaries after ``make hybris-hal``
is **19 GB** (as of 2015-09-09, hybris-11.0 branch).

.. _kernel-config:

Kernel config
`````````````

Once the kernel has built you can check the kernel config. You can use the Mer
kernel config checker:

.. code-block:: console

  HABUILD_SDK $

  cd $ANDROID_ROOT

  hybris/mer-kernel-check/mer_verify_kernel_config \
      ./out/target/product/$DEVICE/obj/KERNEL_OBJ/.config

Apply listed modifications to the defconfig file that CM is using. Which one?
It's different for every device, most likely first:

* Check the value of ``TARGET_KERNEL_CONFIG`` under
  $ANDROID_ROOT/device/$VENDOR/\*/BoardConfig\*.mk

* Double-check which defconfig is taken when you're building kernel, e.g.:
  make  -C kernel/lge/hammerhead ... cyanogenmod_hammerhead_defconfig

* Check CM kernel's commit history of the ``arch/arm/configs`` folder, look for
  defconfig

First get rid of ``ERROR`` flags, then take care of ``WARNING`` ones if you're
extra picky and/or your kernel still compiles fine.
After you'll have applied the needed changes, re-run ``make hybris-boot`` and
re-verify. Lather, rinse, repeat :) Run also ``make hybris-recovery`` in the end
when no more errors.

Contribute your mods back
'''''''''''''''''''''''''

Fork the kernel repo to your GitHub home (indicated by ``myname`` in this doc).

For Nexus 5 with CM 11.0 as base, the next action would be (rename where
appropriate to match your device/branch):

.. code-block:: console

  HABUILD_SDK $

  cd kernel/lge/hammerhead
  git checkout -b hybris-11.0

  DEFCONFIG=arch/arm/configs/cyanogenmod_hammerhead_defconfig

  git add $DEFCONFIG

  git commit -m "Mer-friendly defconfig"
  git remote add myname https://github.com/myname/android_kernel_lge_hammerhead
  git push myname hybris-11.0

Create PR to the forked kernel repo under github/mer-hybris. Ask a mer-hybris
admin to create one, if it isn't there.

Adjust your ``.repo/local_manifests/$DEVICE.xml`` by replacing the line

.. code-block:: console

  <project path="kernel/lge/hammerhead"
    name="CyanogenMod/android_kernel_lge_hammerhead"
    revision="stable/cm-11.0-XNG3C" />

with

.. code-block:: console

  <project path="kernel/lge/hammerhead"
    name="myname/android_kernel_lge_hammerhead"
    revision="hybris-11.0" />

.. _common-pitfalls:

Common Pitfalls
---------------

* If ``repo sync`` fails with a message like *fatal: duplicate path
  device/samsung/smdk4412-common in /home/nemo/android/.repo/manifest.xml*,
  remove the local manifest with ``rm .repo/local_manifests/roomservice.xml``
* If you notice ``git clone`` commands starting to write out *"Forbidden ..."* on
  github repos, you might have hit API rate limit. To solve this, put your github
  credentials into ``~/.netrc``. More info can be found following this link:
  `Perm.auth. with Git repositories`_
* In some cases (with parallel builds), the build can fail, in this case, use
  ``make -j1 hybris-hal`` to retry with a non-parallel build and see the error
  message without output from parallel jobs. The build usually ends with
  the following output:

.. _Perm.auth. with Git repositories: https://confluence.atlassian.com/display/STASH/Permanently+authenticating+with+Git+repositories#PermanentlyauthenticatingwithGitrepositories-Usingthe.netrcfile

.. code-block:: console

  HABUILD_SDK $

  ...
  Install: .../out/target/product/$DEVICE/hybris-recovery.img
  ...
  Install: .../out/target/product/$DEVICE/hybris-boot.img

