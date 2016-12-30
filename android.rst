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

  PLATFORM_SDK $

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

  sudo mkdir -p $ANDROID_ROOT
  sudo chown -R $USER $ANDROID_ROOT
  cd $ANDROID_ROOT
  repo init -u git://github.com/mer-hybris/android.git -b hybris-11.0

Device repos
------------

The local manifest contains device-specific repositories, for Android as well as
for the mer-hybris builds.

If your device has already been ported, its codes properly placed on GitHub,
you should check this repository: https://github.com/local_manifests (choose
the branch of hybris-* that your are porting to), and use $DEVICE.xml file
instead of creating a new one in this chapter.

Create directory at first:

.. code-block:: console

  HABUILD_SDK $

  mkdir $ANDROID_ROOT/.repo/local_manifests

If your are working on a new port, you'll have to create the local
manifest yourself, which contains at least two repos: one for the kernel, another
for the device configuration. Find those CM device wiki, for Nexus 5 it would be
http://wiki.cyanogenmod.org/w/Hammerhead_Info inside the **Source code** table.
Local manifest below will also need pointing to correct branches - identify which
one matches the default manifest branch (``stable/cm-11.0`` in Nexus 5 case).

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

  repo sync --fetch-submodules

The expected disk usage for the source tree after the sync is **13 GB** (as of
2015-09-09, hybris-11.0 branch). Depending on your connection, this might take
some time. In the mean time, make yourself familiar with the rest of this guide.

Configure Mountpoint Information
--------------------------------

Currently in Sailfish OS, ``udev`` starts after ``initrd``, which leaves us not
being able to use generic partition names (independent of partition number).

In ``initrd`` we then have to specify hardcoded ``/dev/mmcblkXpY`` nodes for
``/boot`` and ``/data`` partitions.

After ``initrd``, ``systemd`` needs to mount all other required partitions (such
as ``/system``, ``/firmware``, ``/persist``, ``/config``, ...) for the HAL layer
to work. The required partitions are read from ``*.fstab`` and ``init*.rc``
files, disabled there, and respective ``.mount`` units created -- all done by
``$ANDROID_ROOT/rpm (droid-hal-device)``.

Unfortunately, ``systemd`` cannot recognise named partition paths in ``.mount``
units, because of the same late start of ``udev``, even though one can see
already created nodes under ``/dev/block/platform/SOC/by-name/``.

To work around this, we need to create a map between partition names and numbers
in ``hybris/hybris-boot/fixup-mountpoints`` for each device, for all partitions
-- in this way we are sure to cover them all, because if done manually by
looking through fstab/rc files, some might get unnoticed.

To get that mapping, you should boot to CM and execute via ``adb shell`` this:
``ls -l /dev/block/platform/*/by-name/``

Once you've patched ``fixup-mountpoints``, take care if you ever have to run
``repo sync --fetch-submodules`` again because it will reset your changes,
unless the file ``.repo/local_manifests/$DEVICE.xml`` is pointing
``hybris-boot`` to your fork with the needed fixup-mountpoints changes.

Then when you get to boot to the Sailfish OS UI, please don't forget to upstream
your ``fixup-mountpoints`` patch.

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

  source build/envsetup.sh
  export USE_CCACHE=1

  sudo apt-get install unzip

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

* Examine the output of `make bootimage` for which defconfig is taken when
  you're building kernel, e.g.:
  ``make  -C kernel/lge/hammerhead ... cyanogenmod_hammerhead_defconfig``

* Check CM kernel's commit history of the ``arch/arm/configs`` folder, look for
  defconfig

If you are in a rush, get rid only of ``ERROR`` cases first, but don't forget to
come back to the ``WARNING`` ones too.
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

* If ``repo sync --fetch-submodules`` fails with a message like *fatal: duplicate path
  device/samsung/smdk4412-common in /home/nemo/android/.repo/manifest.xml*,
  remove the local manifest with ``rm .repo/local_manifests/roomservice.xml``
* If you notice ``git clone`` commands starting to write out *"Forbidden ..."* on
  github repos, you might have hit API rate limit. To solve this, put your github
  credentials into ``~/.netrc``. More info can be found following this link:
  `Perm.auth. with Git repositories`_
* *error: Cannot fetch ... (GitError: --force-sync not enabled; cannot overwrite
  a local work tree.*, usually happens if ``repo sync --fetch-submodules`` gets
  interrupted. It is a bug of the repo tool. Ensure all your changes have been
  safely stowed (check with ``repo status``), and then workaround by:

.. code-block:: console

  HABUILD_SDK $

  repo sync --force-sync

  repo sync --fetch-submodules

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

