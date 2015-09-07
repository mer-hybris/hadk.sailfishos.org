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

After you've installed the ``repo`` command, the following set of
commands download the required projects for building the modified parts
of Android used in libhybris-based Mer device hardware adaptations.

.. code-block:: console

  HABUILD_SDK $

  hadk

  sudo mkdir -p $ANDROID_ROOT
  sudo chown -R $USER $ANDROID_ROOT
  cd $ANDROID_ROOT
  repo init -u git://github.com/mer-hybris/android.git -b hybris-10.1
  repo sync

The expected disk usage for the source tree after ``repo sync``
is **9.4 GB** (as of 2014-02-18). Depending on your connection, this
might take some time. In the mean time, make yourself familiar with the
rest of this guide.

.. _build-cm-bits:

Building Relevant Bits of CyanogenMod
-------------------------------------

In the Android build tree, run the following in a ``bash`` shell (if you
are using e.g. ``zsh``, you need to run these commands in a ``bash`` shell,
as the Android build scripts are assuming you are running ``bash``):

.. code-block:: console

  HABUILD_SDK $

  hadk

  source build/envsetup.sh
  export USE_CCACHE=1

  breakfast $DEVICE

  rm .repo/local_manifests/roomservice.xml

The last command removes the CyanogenMod "roomservice" repository list,
which contains any additional device-specific repositories you need. In our
case, the ``hybris-10.1`` manifest file already contains device-specific
repositories, and the repositories added by roomservice would conflict with
those.

.. code-block:: console

  HABUILD_SDK $

  make -j4 hybris-hal

The relevant output bits will be in ``out/target/product/$DEVICE/``, in
particular:

* ``hybris-boot.img``: Kernel and initrd
* ``hybris-recovery.img``: Recovery boot image
* ``system/`` and ``root/``: HAL system libraries and binaries

The expected disk usage for the source and binaries after ``make hybris-hal``
is **16 GB** (as of 2014-02-18).

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
  ...
  Made boot image: .../out/target/product/$DEVICE/boot.img

