Addendum: Factory Productisation
================================

This chapter explains the next steps towards the mass-production of a product,
after all HW peripheral functions are in working order.

This includes:

* Package ``system`` partition content as RPM
* Flash Sailfish OS to use the whole ``userdata`` partition as LVM
* Enable Sailfish OS recovery mode
* Enable factory reset support
* Provide flashing tools
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

At first create a tarball of the original ``/system`` contents from the **Android
base** image flashed to your device (we are using Nexus 5 in this guide).

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
 # 1. "simg2img system.img system.raw" (Run inside Platform SDK target)
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

Convert ``userdata`` into the Sailfish OS LVM partition
-------------------------------------------------------

We want to split ``$HOME`` and ``/`` into separate volumes, so we could e.g.
``/``, or encrypt ``$HOME``. For this we'll use the whole ``userdata`` as an LVM
partition, with fixed size ``/`` and let ``$HOME`` take up the rest.

.. _package-img-boot:

Package an LVM-enabled bootloader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In directory ``$ANDROID_ROOT/rpm`` apply the following:

.. code-block:: diff

    diff --git a/droid-hal-$DEVICE.spec b/droid-hal-$DEVICE.spec
    -%define installable_zip 1
    +%define have_custom_img_boot 1
    +%define have_custom_img_recovery 1

And rebuild droid-hal ``rpm/dhd/helpers/build_packages.sh --droid-hal``.

Then create path and file
``$ANDROID_ROOT/hybris/droid-hal-img-boot/rpm/droid-hal-hammerhead-img-boot.spec``
with content:

.. code-block:: spec

 %define device hammerhead

 # Retrieve mkbootimg_cmd contents from
 # $ANDROID_ROOT/device/$VENDOR/$DEVICE/BoardConfig.mk and/or from make output.
 # NOTE: taken from the userdebug build, check after switching to user build!
 # If your Android adaptation produces a separate device tree, it should be
 # packaged within droid-hal-$DEVICE-kernel .rpm as ./boot/dt.img, add this to
 # mkbootimg_cmd: --dt %{devicetree}
 %define mkbootimg_cmd mkbootimg --ramdisk %{initrd} --kernel %{kernel} --base 0x00000000 --pagesize 2048 --ramdisk_offset 0x02900000 --tags_offset 0x02700000 --cmdline "androidboot.hardware=hammerhead user_debug=31 msm_watchdog_v2.enable=1 selinux=0"  --output

 %define root_part_label userdata
 %define factory_part_label system

 %define display_brightness_path /sys/class/leds/lcd-backlight/brightness
 %define display_brightness 16

 %include initrd/droid-hal-device-img-boot.inc

Initiate git repository with our publicly available ``hybris-initrd`` as
submodule; then build dependencies and the new img-boot:

.. code-block:: console

    PLATFORM_SDK $

    cd $ANDROID_ROOT/hybris/droid-hal-img-boot
    git init
    git submodule add https://github.com/mer-hybris/hybris-initrd initrd

    cd $ANDROID_ROOT
    sb2 -t $VENDOR-$DEVICE-$PORT_ARCH -m sdk-install -R zypper in droid-hal-$DEVICE-kernel droid-hal-$DEVICE-kernel-modules
    rpm/dhd/helpers/build_packages.sh --mw=https://github.com/sailfishos/yamui
    rpm/dhd/helpers/build_packages.sh --mw=https://github.com/sailfishos/initrd-helpers
    rpm/dhd/helpers/build_packages.sh --mw=https://github.com/nemomobile/hw-ramdisk
    rpm/dhd/helpers/build_packages.sh --build=hybris/droid-hal-img-boot/

    # Test the success by booting our recovery image (boot image would not boot
    # without LVM yet):
    rpm2cpio droid-local-repo/$DEVICE/droid-hal-img-boot/droid-hal-$DEVICE-img-recovery-*.armv7hl.rpm | cpio -idv
    # Set your device into fastboot mode:
    sudo fastboot boot ./boot/hybris-recovery.img

    # Shortly you should see instructions on device screen on how to telnet in,
    # however avoid testing factory reset, as it is not ready at this stage.


Configuring the LVM packaging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Within ``$ANDROID_ROOT/hybris/droid-configs`` create the following paths and
files:

``kickstart/pack/$DEVICE/hybris``

.. code-block:: bash

 pushd $IMG_OUT_DIR

 MD5SUMFILE=md5.lst

 DEVICE_VERSION_FILE=./hw-release

 EXTRA_NAME=""

 if [ -n "@EXTRA_NAME@" ] && [ "@EXTRA_NAME@" != @"EXTRA_NAME"@ ]; then
   EXTRA_NAME="@EXTRA_NAME@-"
 fi

 DEVICE=""
 DEVICE_VERSION=""

 if [[ -a $DEVICE_VERSION_FILE ]]; then
   source $DEVICE_VERSION_FILE
   DEVICE=$MER_HA_DEVICE
   DEVICE_VERSION=-$VERSION_ID
 fi

 source ./sailfish-release
 if [ "$SSU_RELEASE_TYPE" = "rnd" ]; then
   RELEASENAME=$NAME-${EXTRA_NAME// /_}$SAILFISH_FLAVOUR-$VERSION_ID-$DEVICE$DEVICE_VERSION
 else
   RELEASENAME=$NAME-${EXTRA_NAME// /_}$VERSION_ID-$DEVICE$DEVICE_VERSION
 fi

 # Setup LVM image
 dd if=/dev/zero bs=1 count=0 of=temp.img seek=3000M
 LVM_LOOP=$(/sbin/losetup -f)
 /sbin/losetup $LVM_LOOP temp.img
 /usr/sbin/pvcreate $LVM_LOOP
 /usr/sbin/vgcreate sailfish $LVM_LOOP

 # Resize root and home to minimum
 ROOT_LOOP=$(/sbin/losetup -f)
 /sbin/losetup $ROOT_LOOP root.img
 /sbin/e2fsck -f -y $ROOT_LOOP
 BLOCKS=$(/sbin/resize2fs -M $ROOT_LOOP | /bin/grep "The filesystem on" | /bin/cut -d ' ' -f 7)
 echo We got ourselves root blocks _ $BLOCKS _
 SIZE=$(/usr/bin/expr $BLOCKS \* 4096)
 echo after maths size _ $SIZE _
 /usr/sbin/lvcreate -L ${SIZE}B --name root sailfish
 /bin/sync
 /sbin/losetup -d $ROOT_LOOP
 /usr/sbin/vgchange -a y
 dd if=root.img bs=4096 count=$BLOCKS of=/dev/sailfish/root


 HOME_LOOP=$(/sbin/losetup -f)
 /sbin/losetup $HOME_LOOP home.img
 /sbin/e2fsck -f -y $HOME_LOOP
 BLOCKS=$(/sbin/resize2fs -M $HOME_LOOP | /bin/grep "The filesystem on" | /bin/cut -d ' ' -f 7)
 echo We got ourselves home size _ $BLOCKS _
 SIZE=$(/usr/bin/expr $BLOCKS \* 4096)

 /usr/sbin/lvcreate -L ${SIZE}B --name home sailfish
 /bin/sync
 /sbin/losetup -d $HOME_LOOP
 /usr/sbin/vgchange -a y
 dd if=home.img bs=4096 count=$BLOCKS of=/dev/sailfish/home

 /usr/sbin/vgchange -a n sailfish

 rm home.img root.img

 /sbin/losetup -d $LVM_LOOP

 mv temp.img sailfish.img

 /usr/bin/atruncate sailfish.img

 chmod 755 flash.*

 FILES="flash* *.img* *-release"
 FILES_TO_COPY="*.urls"

 mkdir -p ${RELEASENAME}
 cp ${FILES_TO_COPY} ${RELEASENAME}/
 mv ${FILES} ${RELEASENAME}/

 # Calculate md5sums of files included to the tarball
 cd ${RELEASENAME}
 md5sum * > $MD5SUMFILE
 cd ..

 # Package stuff back to tarball
 tar -cjf ${RELEASENAME}.tar.bz2 $RELEASENAME

 # Remove the files from the output directory
 rm -r ${RELEASENAME}

 popd


``kickstart/part/$DEVICE``

.. code-block:: bash

 part / --fstype="ext4" --size=1800 --label=root
 part /home --fstype="ext4" --size=800 --label=home


``kickstart/attachment/$DEVICE``

.. code-block:: bash

 /boot/hybris-boot.img
 /boot/hybris-recovery.img
 droid-config-hammerhead-out-of-image-files
 /etc/hw-release


``out-of-image-files.files``

.. code-block:: bash

 /boot/flash.sh
 /boot/extracting-README.txt
 /boot/flashing-README.txt


``sparse/boot/flash.sh``

.. code-block:: bash

 #!/bin/bash

 # Contact: Marko Saukko <marko.saukko@jollamobile.com>
 #
 # Copyright (c) 2016, Jolla Ltd.
 # All rights reserved.
 #
 # Redistribution and use in source and binary forms, with or without
 # modification, are permitted provided that the following conditions are met:
 # * Redistributions of source code must retain the above copyright
 # notice, this list of conditions and the following disclaimer.
 # * Redistributions in binary form must reproduce the above copyright
 # notice, this list of conditions and the following disclaimer in the
 # documentation and/or other materials provided with the distribution.
 # * Neither the name of the <organization> nor the
 # names of its contributors may be used to endorse or promote products
 # derived from this software without specific prior written permission.
 #
 # THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 # ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 # WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 # DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
 # DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 # (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 # LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 # ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 # (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 # SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

 set -e

 function check_fastboot {
   FASTBOOT_BIN_NAME=$1
   if [ -f "$FASTBOOT_BIN_NAME" ]; then
     chmod 755 $FASTBOOT_BIN_NAME
     # Ensure that the binary that is found can be executed fine
     if ./$FASTBOOT_BIN_NAME help &>/dev/null; then
       FASTBOOT_BIN_PATH="./"
       return 0
     fi
   fi
   return 1
 }


 # Do not need root for fastboot on Mac OS X
 if [ "$(uname)" != "Darwin" -a $(id -u) -ne 0 ]; then
   exec sudo -E bash $0
 fi

 UNAME=$(uname)
 OS_VERSION=

 case $UNAME in
   Linux)
     echo "Detected Linux"
     ;;
   Darwin)
     IFS='.' read -r major minor patch <<< $(sw_vers -productVersion)
     OS_VERSION=$major-$minor
     echo "Detected Mac OS X - Version: $OS_VERSION"
     ;;
   *)
     echo "Failed to detect operating system!"
     exit 1
     ;;
 esac

 VENDORIDLIST=(
 "18d1"
 )

 echo "Searching device to flash.."
 IFS=$'\n'
 if [ "$UNAME" = "Darwin" ]; then
   # Mac OS X: Use System Profiler, get only the Vendor IDs and
   # append a colon at the end to make the lsusb-specific grep
   # from below work the same way as on Linux.
   LSUSB=( $(system_profiler SPUSBDataType | \
       grep -o 'Vendor ID: [x0-9a-f]*' | \
       sed -e 's/$/:/') )
 else
   # Linux
   LSUSB=( $(lsusb) )
 fi
 unset IFS

 VENDORIDFOUND=

 for USB in "${LSUSB[@]}"; do
   for VENDORID in ${VENDORIDLIST[@]}; do
     # : after vendor id is to make sure we don't select based on product id.
     if [[ "$USB" =~ $VENDORID: ]]; then
       echo "Found device with vendor id '$VENDORID': $USB"
       VENDORIDFOUND=$VENDORID
     fi
   done
 done

 if [ -z $VENDORIDFOUND ]; then
   echo "No device that can be flashed found. Please connect device to fastboot mode before running this script."
   exit 1
 fi

 FASTBOOT_BIN_PATH=
 FASTBOOT_BIN_NAME=

 if ! check_fastboot "fastboot-$UNAME-$OS_VERSION" ; then
   if ! check_fastboot "fastboot-$UNAME"; then
     # In case we didn't provide functional fastboot binary to the system
     # lets check that one is found from the system.
     if ! which fastboot &>/dev/null; then
       echo "No 'fastboot' found in \$PATH. To install, use:"
       echo ""
       echo "    Debian/Ubuntu/.deb distros:  apt-get install android-tools-fastboot"
       echo "    Fedora:  yum install android-tools"
       echo "    OS X:    brew install android-sdk"
       echo ""
       exit 1
     else
       FASTBOOT_BIN_NAME=fastboot
     fi
   fi
 fi

 # TODO: There are cases where the fastboot provided by the system is too old and doesn support
 # for example the erase command below.

 FASTBOOTCMD="${FASTBOOT_BIN_PATH}${FASTBOOT_BIN_NAME} -i 0x$VENDORIDFOUND $FASTBOOTEXTRAOPTS"

 echo "Fastboot command: $FASTBOOTCMD"

 FLASHCMD="$FASTBOOTCMD flash"
 ERASECMD="$FASTBOOTCMD erase"
 ABOOTREBOOTCMD="$FASTBOOTCMD reboot-bootloader"

 if [ -z ${BINARY_PATH} ]; then
   BINARY_PATH=./
 fi

 if [ -z ${SAILFISH_IMAGE_PATH} ]; then
   SAILFISH_IMAGE_PATH=./
 fi

 IMAGES=(
 "boot ${SAILFISH_IMAGE_PATH}hybris-boot.img"
 "recovery ${SAILFISH_IMAGE_PATH}hybris-recovery.img"
 )

 for IMAGE in "${IMAGES[@]}"; do
   read partition ifile <<< $IMAGE
   if [ ! -e ${ifile} ]; then
     echo "Image binary missing: ${ifile}."
     exit 1
   fi
 done

 for IMAGE in "${IMAGES[@]}"; do
   read partition ifile <<< $IMAGE
   echo "Flashing $partition partition.."
   $FLASHCMD $partition $ifile
 done

 # Flashing to userdata..
 for x in sailfish.img*; do
   $FLASHCMD userdata $x
 done

 echo "Flashing completed. Choose "Start" with Volume buttons then press Power."


``sparse/boot/flashing-README.txt``

.. code-block:: text

 = FLASHING =

 Before starting flashing on any host turn off the device. After this follow the
 instructions given for your host PC operating system.

 By this point of time you should already have the .tar.bz2 file that contains
 the image as this flashing instructions file that you are reading at the moment
 is inside that .tar.bz2 file. As a general note the flashing can take a long
 time (>10 minutes) and it flashes image with similar name multiple times in the
 end which is expected behaviour.


 == LINUX ==

 Open terminal application and go to the folder where the image is extracted.

 Next:
 * Connect device to computer with USB-cable while holding volume down button
 * When you feel vibra from device you can release the volume down button
 * Next start flashing script by entering following command:

   bash ./flash.sh

 * Enter your password if requested to gain root access for flashing the device
 * Once flashing is completed you will see text:

   "Flashing completed. Detact usb cable, press and hold the powerkey to reboot."

 * After following the guidance from script device should boot up to new Sailfish OS

 NOTE: If flashing does not succeed, you might have missing fastboot binary or
 it is too old. Many distros include andoid-tools package, but that might not
 be new enough to support tk7001 flashing.

 Installation commands for some linux distributions:
 * Ubuntu: sudo apt-get install android-tools-fastboot

 If you want to compile fastboot binary for your distro you can compile version
 5.0.0 release 7 or newer from:
 https://github.com/mer-qa/qa-droid-tools


``sparse/boot/extracting-README.txt``

.. code-block:: text

 Step1: Download the image

 The image name is usually in following format SailfishOS-FLAVOUR-VERSION-DEVICE.tar.bz2
 which you need to download.

 Step2: Extract the image

 = Linux =

 Following command line extracts the image to the current working directory (pwd):

 $ tar -xvf SailfishOS-FLAVOUR-VERSION-DEVICE.tar.bz2

 Step3: Read the flashing-README.txt from the extracted directory for further instructions


Add recovery to patterns and provide flashing script and instructions out of
the image:

.. code-block:: diff

    diff --git a/patterns/jolla-hw-adaptation-$DEVICE.yaml b/patterns/jolla-hw-adaptation-$DEVICE.yaml
     - droid-hal-tk7001-img-boot
    +- droid-hal-tk7001-img-recovery
     - droid-hal-tk7001-kernel-modules

    diff --git a/rpm/droid-config-$DEVICE.spec v/rpm/droid-config-$DEVICE.spec
    +%define out_of_image_files 1
     %include droid-configs-device/droid-configs.inc

.. _flashing-lvm:

Flashing LVM-enabled image
~~~~~~~~~~~~~~~~~~~~~~~~~~

Rebuild configs via ``rpm/dhd/helpers/build_packages.sh --droid-configs``, add
LVM tools to PLATFORM_SDK ``sudo zypper in lvm2 atruncate``, and lastly rebuild
the whole image (refer to :doc:`mic`), but use ``loop`` instead of ``fs`` within
``mic create`` as well as drop the ``--pack-to`` parameter.

You may also want to change ``EXTRA_NAME`` to preserve the non-LVM version, yet
to ever go back to that you'd need to format userdata partition as ``ext3`` or
``ext4``.

``mic`` will produce a tarball and place extracting-README.txt next to it,
simply follow instructions how to flash to your device.

Enable Sailfish OS recovery mode
--------------------------------

Our recovery mode is already provided by the ``droid-hal-$DEVICE-img-boot`` (see
section :ref:`package-img-boot`), and flashed to device together with the LVM
image.

To enter recovery on Nexus 5, press Volume Down and Power buttons
simultaneously, this enter fastboot mode (bootloader). Using Volume Up/Down
buttons select ``Recovery mode`` and press Power key to enter it.

Follow instructions on screen to ``telnet`` and perform desired actions.


Enable factory reset support
----------------------------

Whilst packaging up LVM images, we'll also place ``root.img`` and ``home.img``
to ``system`` partition, since we are packaging ``/system`` ourselves.

Within ``$ANDROID_ROOT/hybris/droid-configs`` patch the following files:

.. code-block:: diff

 diff --git a/kickstart/part/$DEVICE b/kickstart/part/$DEVICE
  part / --fstype="ext4" --size=1800 --label=root
  part /home --fstype="ext4" --size=800 --label=home
 +part /fimage --fstype="ext4" --size=10 --label=fimage

 diff --git a/kickstart/pack/$DEVICE/hybris b/kickstart/pack/$DEVICE/hybris
  /usr/sbin/vgchange -a n sailfish
 -rm home.img root.img
 +# Temporary dir for making factory image backups.
 +FIMAGE_TEMP=$(mktemp -d -p $(pwd))
 +
 +# For some reason loop files created by imager don't shrink properly when
 +# running resize2fs -M on them. Hence manually growing the loop file here
 +# to make the shrinking work once we have the image populated.
 +dd if=/dev/zero bs=1 seek=1400000000 count=1 of=fimage.img
 +/sbin/e2fsck -f -y fimage.img
 +/sbin/resize2fs -f fimage.img
 +
 +pigz -7 root.img
 +md5sum -b root.img.gz > root.img.gz.md5
 +
 +pigz -7 home.img
 +md5sum -b home.img.gz > home.img.gz.md5
 +
 +mount -o loop fimage.img $FIMAGE_TEMP
 +mkdir -p $FIMAGE_TEMP/${RELEASENAME}
 +mv root.img.gz* $FIMAGE_TEMP/${RELEASENAME}
 +mv home.img.gz* $FIMAGE_TEMP/${RELEASENAME}
 +umount $FIMAGE_TEMP
 +rmdir $FIMAGE_TEMP
 +
 +/sbin/e2fsck -f -y fimage.img
 +/sbin/resize2fs -f -M fimage.img
 +
  /sbin/losetup -d $LVM_LOOP

 diff --git a/sparse/boot/flash.sh b/sparse/boot/flash.sh
    $FLASHCMD userdata $x
  done

 +# Flashing fimage to system partition
 +for x in fimage.img*; do
 +  $FLASHCMD system $x
 +done
 +

Repeat the flashing process as outlined in :ref:`flashing-lvm`, boot the device,
go to ``Settings | Reset device``, and perform reset.

Device will reboot into recovery and you will see the spinner image with status.

Afterwards device will power off (unless you ticked ``Reboot after reset``
earlier), power it back on and it will boot as new.

