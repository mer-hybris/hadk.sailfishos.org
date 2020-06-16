Packaging Droid HAL
===================

In this chapter, we will package the build results of :doc:`android`
as RPM packages and create a local RPM repository. From there, the RPM
packages can be added to a local target and used to build libhybris and the
QPA plugin. They can also be used to build the rootfs.

Creating Repositories for a New Device
-------------------------------------

If the folders ``rpm, hybris/droid-configs, hybris-droid-hal-version-$DEVICE``
do not exist yet, create them as follows (example is for Nexus 5, adjust as
appropriate and push to your GitHub home):

.. code-block:: console

 PLATFORM_SDK $

 cd $ANDROID_ROOT
 mkdir rpm
 cd rpm
 git init
 git submodule add https://github.com/mer-hybris/droid-hal-device dhd
 # Rename 'hammerhead' and other values as appropriate
 sed -e "s/@DEVICE@/hammerhead/" \
     -e "s/@VENDOR@/lge/" \
     -e "s/@DEVICE_PRETTY@/Nexus 5/" \
     -e "s/@VENDOR_PRETTY@/LG/" \
     dhd/droid-hal-@DEVICE@.spec.template > droid-hal-hammerhead.spec
 # Please review droid-hal-hammerhead.spec before committing!
 git add .
 git commit -m "[dhd] Initial content"
 # Create this repository under your GitHub home
 git remote add myname https://github.com/myname/droid-hal-hammerhead.git
 git push myname master
 cd -

 mkdir -p hybris/droid-configs
 cd hybris/droid-configs
 git init
 git submodule add https://github.com/mer-hybris/droid-hal-configs \
     droid-configs-device
 mkdir rpm
 sed -e "s/@DEVICE@/hammerhead/" \
     -e "s/@VENDOR@/lge/" \
     -e "s/@DEVICE_PRETTY@/Nexus 5/" \
     -e "s/@VENDOR_PRETTY@/LG/" \
     droid-configs-device/droid-config-@DEVICE@.spec.template > \
     rpm/droid-config-hammerhead.spec
 # Please review rpm/droid-config-hammerhead.spec before committing!
 git add .
 git commit -m "[dcd] Initial content"
 # Create this repository under your GitHub home
 git remote add myname https://github.com/myname/droid-config-hammerhead.git
 git push myname master
 cd -

 rpm/dhd/helpers/add_new_device.sh
 # On Nexus 5 the output of the last command is:
 # Creating the following nodes:
 # sparse/
 # patterns/
 # patterns/jolla-configuration-hammerhead.yaml
 # patterns/jolla-hw-adaptation-hammerhead.yaml
 cd hybris/droid-configs
 COMPOSITOR_CFGS=sparse/var/lib/environment/compositor
 mkdir -p $COMPOSITOR_CFGS
 cat <<EOF >$COMPOSITOR_CFGS/droid-hal-device.conf
 # Config for $VENDOR/$DEVICE
 EGL_PLATFORM=hwcomposer
 QT_QPA_PLATFORM=hwcomposer
 # Determine which node is your touchscreen by checking /dev/input/event*. WRITE ALL IN ONE LINE(:
 LIPSTICK_OPTIONS=-plugin evdevtouch:/dev/input/event0 -plugin evdevkeyboard:keymap=/usr/share/qt5/keymaps/droid.qmap
 EOF
 git add .
 git commit -m "[dcd] Patterns and compositor config"
 git push myname master
 cd -

 mkdir -p hybris/droid-hal-version-hammerhead
 cd hybris/droid-hal-version-hammerhead
 git init
 git submodule add https://github.com/mer-hybris/droid-hal-version
 mkdir rpm
 sed -e "s/@DEVICE@/hammerhead/" \
     -e "s/@VENDOR@/lge/" \
     -e "s/@DEVICE_PRETTY@/Nexus 5/" \
     -e "s/@VENDOR_PRETTY@/LG/" \
     droid-hal-version/droid-hal-version-@DEVICE@.spec.template > \
     rpm/droid-hal-version-hammerhead.spec
 # Please review rpm/droid-hal-version-hammerhead.spec before committing!
 git add .
 git commit -m "[dvd] Initial content"
 # Create this repository under your GitHub home
 git remote add myname \
     https://github.com/myname/droid-hal-version-hammerhead.git
 git push myname master

Now to complete you local manifest, this is how it would be done for Nexus 5.
Do it for your device by renaming accordingly:

.. code-block:: console

  # add the next 3 entries into .repo/local_manifests/hammerhead.xml

  <project path="rpm/"
           name="myname/droid-hal-hammerhead" revision="master" />
  <project path="hybris/droid-configs"
           name="myname/droid-config-hammerhead" revision="master" />
  <project path="hybris/droid-hal-version-hammerhead"
           name="myname/droid-hal-version-hammerhead" revision="master" />

Once all these 3 repositories get upstreamed under https://github.com/mer-hybris
create PR into an appropriate branch of the file
``.repo/local_manifests/hammerhead.xml`` to the
 https://github.com/mer-hybris/local_manifests repository.


Packaging ``droid-hal-device``
------------------------------

The ``$ANDROID_ROOT/rpm/`` dir contains the needed ``.spec`` file to make a set
of RPM packages that form the core Droid hardware adaptation part of the
hardware adaptation. It also builds a development package (ends with -devel)
that contains libraries and headers, which are used when building middleware
components later on.

.. _build-rpms:

Building the droid-hal-device packages
``````````````````````````````````````

The next step has to be carried out in the Platform SDK chroot:

.. code-block:: console

    PLATFORM_SDK $

    cd $ANDROID_ROOT

    rpm/dhd/helpers/build_packages.sh --droid-hal
    rpm/dhd/helpers/build_packages.sh --configs
    rpm/dhd/helpers/build_packages.sh --mw
    rpm/dhd/helpers/build_packages.sh --gg
    rpm/dhd/helpers/build_packages.sh --version

This will compile all the needed packages, patterns, middleware and put them
under local repository. If anything gets modified, just re-run the appropriate part.

Troubleshoot errors from build_packages.sh
``````````````````````````````````````````

* **Installed (but unpackaged) file(s) found**: Add those files to straggler section
  in your rpm/droid-hal-$DEVICE.spec before the ``%include ...`` line, for example:
.. code-block:: console

 %define straggler_files \
 /init.mmi.boot.sh\
 /init.mmi.touch.sh\
 /init.qcom.ssr.sh\
 /selinux_version\
 /service_contexts\
 %{nil}

* Then add ``- droid-hal-hammerhead-detritus`` to ``droid-configs/patterns/
  jolla-hw-adaptation-hammerhead.yaml`` (substitute as appropriate for your
  device)

* Lastly, re-run ``build_packages.sh --droid-hal``

