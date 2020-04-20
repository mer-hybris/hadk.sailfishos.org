OTA (Over-the-Air) Updates
==========================

You can setup to upgrade a Sailfish OS device over the air, a.k.a. OTA update.

Prepare the infrastructure
--------------------------

* Ensure your Sailfish OS version is at least 3.2.1
* Create file ``20-mydomain.ini`` (rename "mydomain" as you see fit) under
  ``$ANDROID_ROOT/hybris/droid-configs/sparse/usr/share/ssu/repos.d/`` with the
  following content:

.. code-block:: ini

  [release]
  adaptation=https://mydomain.net/%(release)/%(vendor)-%(adaptation)/%(arch)/

* Substitute ``https://mydomain.net/`` with your Web server address (including
  subpath if exists)
* The ``%(release)/%(vendor)-%(adaptation)/%(arch)/`` format is advised, because
  it's the most future-proof. E.g. for the Nexus 5 this string would resolve to
  ``3.2.1.20/lge-hammerhead/armv7hl/``
* Commit the above change to droid-configs (including updating the submodule,
  which introduces timestamped versioning, so updates get picked up)
* Make new image and ensure devices are flashed which will be receiving future
  updates
* Make some changes to your adaptation (e.g. fix some HW issue) and rebuild the
  affected part via ``build_packages.sh``, so that version numbers increase

.. _test_repo:

Test for any breakages
----------------------

Before deploying any updates to production, they must be tested first.

Prerequisites:

* Web server (e.g. Apache) running on HOST and accessible within network
* Directory listing doesn't need to be enabled
* Assuming Web server's rootdir is ``/srv/http``

Perform the following:

.. code-block:: bash

  HOST $

  . ~/.hadk.env
  rm -rf /srv/http/sailfish-tmp-test-repo
  cp -ar $ANDROID_ROOT/droid-local-repo/$DEVICE /srv/http/sailfish-tmp-test-repo

SSH into your device and execute (substituting ``https://mydomain.net`` with
the address to your Web server):

.. code-block:: bash

  DEVICE $

  ssu ar sfos-test https://mydomain.net/sailfish-tmp-test-repo
  devel-su -p pkcon install zypper
  devel-su zypper refresh sfos-test
  devel-su zypper dup --from sfos-test

Check that all the packages you touched are to be updated or removed as
expected. Afterwards you can press "Yes" to execute the update and check if
the device functions as desired, also after reboot.

Once happy, clean up the testing environment:

.. code-block:: bash

  DEVICE $

  ssu rr sfos-test


  HOST $

  rm -rf /srv/http/sailfish-tmp-test-repo

.. _deploy_repo:

Release into production for all users
-------------------------------------

Once successfully tested, deploy the stable packages to the release repo:

.. code-block:: bash

  HOST $

  . ~/.hadk.env
  rm -rf /srv/http/$RELEASE/$VENDOR-$DEVICE/$PORT_ARCH
  mkdir -p /srv/http/$RELEASE/$VENDOR-$DEVICE
  cp -ar $ANDROID_ROOT/droid-local-repo/$DEVICE \
         /srv/http/$RELEASE/$VENDOR-$DEVICE/$PORT_ARCH

To receive the update, each device will have to execute ``devel-su -p
version --dup``, and reboot when instructed.

Updating to the next Sailfish OS release
----------------------------------------

If another official Sailfish OS update has been released since you last
published your HW adaptation update, perform the following:

Update your SDK Target (see how in the last paragraph of :ref:`enter-sfos-sdk`).

Alternatively, you can remove it and create a new one as per :doc:`scratchbox2`.

Remove or backup your local build repository:

.. code-block:: bash

  PLATFORM_SDK $

  cd $ANDROID_ROOT

  PREV_RELEASE=3.2.1.16    # adjust to what previous release version you were on

  mv droid-local-repo/$DEVICE droid-local-repo/$DEVICE-$PREV_RELEASE
  mkdir droid-local-repo/$DEVICE

Then rebuild all packages and a new image by executing ``build_packages.sh``.

Afterwards :ref:`test<test_repo>` the rebuilt repo. The actual testing sequence
on the device will be different:

.. code-block:: bash

  DEVICE $

  ssu ar sfos-test https://mydomain.net/sailfish-tmp-test-repo
  ssu dr adaptation0
  ssu re 3.3.0.16    # adjust to the actual version
  devel-su -p version --dup
  ssu rr sfos-test
  ssu er adaptation0

Then reboot as and test device functionality.

Once satisfactory, :ref:`publish<deploy_repo>` your repo for all users.

Finally, to receive the update, each device will have to execute:

.. code-block:: bash

  DEVICE $

  ssu re 3.3.0.16    # adjust to the actual version
  devel-su -p version --dup

NOTE: The %(release) in your self-hosted repo (visible via ``ssu lr``) will get
updated automatically after ``ssu re``.

After ``devel-su -p version --dup`` has finished, reboot as instructed.
