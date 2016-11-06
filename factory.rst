Addendum: Factory Productisation
================================

This chapter explains the next steps towards the mass-production of a product,
after all HW peripheral functions are in working order.

This includes:

* Package ``system`` partition content as RPM
* Flash Sailfish OS to use the whole ``userdata`` partition as LVM
* Enable Sailfish OS recovery mode
* Provide flashing tools
* Enable factory reset support
* Modify bootloader, splash screen, and other partitions
* Optimising size and layout of partitions
* Provide a raw image for factory testing and flashing

Package ``system`` partition
----------------------------

Sailfish OS needs a mounted ``system`` partition under ``/system`` to use
the underlying Android parts.

However to provide BSP updates that an ODM may give, its content needs to be
packaged as RPM and deployed in ``userdata`` together with the rest of our
rootfs.

In this way we get to win free space by removing unused files, and use
``system`` partition for e.g. flashing the factory reset image.

At first create a tarball of the original ``/system`` contents from Android
or CyanogenMod flashed to your device (we are using Nexus 5 in this guide).

Transfer the tarball to your host and extract it.

Alternatively you may have a ready-built ``system.img`` from the original
Android build, the file snippet below explains how to extract it.

Create directory ``$ANDROID_ROOT/hybris/droid-system/`` and create file
``copy_system.sh`` with the following content:

.. code-block:: bash

 #
 # Use this script everytime you receive an updated /system from your ODM.
 #
 # Before running this script please extract raw system image
 # and mount loop image to some mount point. Give that mount point
 # parameter for this script.
 #
 # 1. "simg2img system.img system.raw" (Run inside Mer SDK target)
 # 2. "mkdir ~/system"
 # 3. "sudo mount -t ext4 -o loop system.raw ~/system"
 # 4. "./copy_system.sh ~/system"

 if [ -z "$1" ]; then
   echo "No argument supplied, try $0 ~/path/to/system"
   exit
 fi

 SYSTEM_SPARSE="sparse/system"
 SYSTEM_MOUNT=$1

 # Add read permission for some binaries under system mount
 sudo chmod a+r $SYSTEM_MOUNT/bin/netcfg
 sudo chmod a+r $SYSTEM_MOUNT/bin/run-as
 sudo chmod a+r $SYSTEM_MOUNT/bin/uncrypt
 sudo chmod a+r $SYSTEM_MOUNT/bin/install-recovery.sh
 sudo chmod a+r $SYSTEM_MOUNT/etc/dhcpcd/dhcpcd-run-hooks

 # Remove current sparse and create it again
 rm -rf $SYSTEM_SPARSE
 mkdir -p $SYSTEM_SPARSE

 # Copy content
 echo "Copy $SYSTEM_MOUNT/* to $SYSTEM_SPARSE"
 cp -r $SYSTEM_MOUNT/* $SYSTEM_SPARSE

 # Remove unused directories and files
 rm -rf $SYSTEM_SPARSE/app/
 rm -rf $SYSTEM_SPARSE/priv-app/
 rm -rf $SYSTEM_SPARSE/media/
 rm -rf $SYSTEM_SPARSE/lib/modules/
 rm -rf $SYSTEM_SPARSE/framework/
 rm -rf $SYSTEM_SPARSE/fonts/
 rm -rf $SYSTEM_SPARSE/usr/keylayout/
 rm -rf $SYSTEM_SPARSE/vendor/app
 rm -rf $SYSTEM_SPARSE/vendor/speccfg
 rm -rf $SYSTEM_SPARSE/vendor/Default/system/media
 rm -rf $SYSTEM_SPARSE/bin/install-recovery.sh
 rm -rf $SYSTEM_SPARSE/recovery-from-boot.p
 rm -rf $SYSTEM_SPARSE/etc/install_apk.sh
 rm -rf $SYSTEM_SPARSE/etc/cdrom_install.iso
 rm -rf $SYSTEM_SPARSE/etc/mmi/fonts.ttf
 rm -rf $SYSTEM_SPARSE/build.prop.bakforspec
 rm -rf $SYSTEM_SPARSE/lib/libchromium_client.so
 rm -rf $SYSTEM_SPARSE/lib/libswenetxt_plugin.so
 rm -rf $SYSTEM_SPARSE/lib/libswewebviewchromium.so
 rm -rf $SYSTEM_SPARSE/lib/libwebviewchromium.so
 rm -rf $SYSTEM_SPARSE/lib/libwebviewchromium_loader.so
 rm -rf $SYSTEM_SPARSE/lib/libwebviewchromium_plat_support.so
 rm -rf $SYSTEM_SPARSE/lib/libWnnJpnDic.so
 rm -rf $SYSTEM_SPARSE/lib/libWnnEngDic.so
 rm -rf $SYSTEM_SPARSE/lib/libpac.so
 rm -rf $SYSTEM_SPARSE/lib/libjni_pacprocessor.so
 rm -rf $SYSTEM_SPARSE/lib/libswev8.so
 rm -rf $SYSTEM_SPARSE/lib/libsweskia.so
 rm -rf $SYSTEM_SPARSE/usr/qfipsverify/bootimg.hmac
 rm -rf $SYSTEM_SPARSE/etc/recovery-resource.dat
 rm -rf $SYSTEM_SPARSE/etc/security/otacerts.zip
 rm -rf $SYSTEM_SPARSE/vendor/bin/slim_ap_daemon

 # If you want to make customisations to your /system, create ./patches
 # directory and apply them below, e.g.:
 #echo "Patch Jolla changes on top of ODM's delivery:"
 #patch -p1 < patches/0001-bug-Don-t-use-GPS-Sensor-Assisted-Positioning.patch

Afterwards execute ``copy_system.sh ~/path/to/system`` ensuring you point to
files within directory as opposed to a path that contains ``system/`` directory
itself.

Now you have a reduced yet functional (tested on Nexus 5, Jolla C/Aqua Fish, and
Turing Phone) ``system`` under ``./sparse/system`` that will be packaged as
follows:

Create path and file
``$ANDROID_ROOT/hybris/droid-system/rpm/droid-system-hammerhead.spec`` with
content:

.. code-block:: spec

 %define device hammerhead

 %define dsd_path ./

 %include droid-system-device/droid-system.inc


And ``$ANDROID_ROOT/hybris/droid-system/droid-system-device/droid-system.inc``
with:

.. important:: We shall provide access to Git repo containing this file in due
 time, then you'll be able to use it as submodule for maximum code re-use,
 minimising fragmentation.

.. code-block:: spec

 %define __find_provides %{nil}
 %define __find_requires %{nil}
 %define __strip /bin/true
 %define __provides_exclude_from ^/system/.*$
 %define __requires_exclude ^.*$
 %global debug_package %{nil}

 %if 0%{!?rpm_device:1}
 %define rpm_device %{device}
 %endif

 Name:       droid-system-%{rpm_device}
 Provides:   droid-system
 Summary:    System package for Droid HAL adaptations
 Version:    1
 Release:    1
 Group:      Development/Tools
 License:    Proprietary
 Source0:    %{name}-%{version}.tar.bz2
 %description
 %{summary}.

 %prep
 %if 0%{?_obs_build_project:1}
 # For OBS builds we need to have tarball extracted after tar_git packaging it
 %setup -q -n %{name}-%{version}
 %endif

 %install
 rm -rf %{buildroot}
 mkdir -p %{buildroot}

 # Retain permissions:
 rm -rf tmp/
 mkdir -p tmp/
 echo "%defattr(-,root,root,-)" > tmp/droid-system.files

 # Prefer files from sparse/ in the HA specific
 # area over sparse/ in the dsd area
 copy_files_from() {
   source_dir=$1
   if [ -d $source_dir ]; then
     (cd $source_dir; find . \( -type f -or -type l \) -print ) | sed 's/^.//' >> tmp/droid-system.files
     cp -R $source_dir/* $RPM_BUILD_ROOT/
   fi
 }

 delete_files() {
   files=$1
   deletelist=$2
   dorm=$3
   if [ -e $deletelist ]; then
     egrep -v '^#' $deletelist | (
       while read file; do
         [ "x$dorm" == "x1" ] && rm $RPM_BUILD_ROOT/$file
         grep -vE "$file" $files > tmp/$$.files
         mv tmp/$$.files $files
       done)
   fi
 }

 # Copy from sparse; erase any we don't want
 copy_files_from %{dsd_path}/sparse
 delete_files tmp/droid-system.files delete_file.list 1

 %files -f tmp/droid-system.files
 %defattr(-,root,root,-)

Thereafter, build the package:

    PLATFORM_SDK $

    cd $ANDROID_ROOT

    rpm/dhd/helpers/build_packages.sh --build=hybris/droid-system

And effectively enable our home-grown /system in ``$ANDROID_ROOT/rpm``:

.. code-block:: diff

    diff --git a/droid-hal-$DEVICE.spec b/droid-hal-$DEVICE.spec
    +%define makefstab_skip_entries /system
    +Requires: droid-system
    +
     %include rpm/dhd/droid-hal-device.inc

Rebuild dhd via ``rpm/dhd/helpers/build_packages.sh --droid-hal`` and then the
whole image (refer to :doc:`mic`).

