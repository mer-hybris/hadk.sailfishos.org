Setting up Scratchbox2 Target
-----------------------------

It is necessary to setup a scratchbox2 target to use for packaging your
hardware adaptation packages in the next section. Download and create your
scratchbox2 target from *within the Mer SDK* with the following commands.

.. code-block:: console

  MERSDK $

  . $HOME/.mersdkubu.profile
  cd $HOME

  export SFFE_SB2_TARGET=/parentroot/$MER_ROOT/targets/$VENDOR-$DEVICE-armv7hl

  curl -O http://releases.sailfishos.org/sdk/latest/targets/Jolla-latest-Sailfish_SDK_Target-armv7hl.tar.bz2
    
  sudo mkdir -p $SFFE_SB2_TARGET
  sudo tar --numeric-owner -pxjf Jolla-latest-Sailfish_SDK_Target-armv7hl.tar.bz2 -C $SFFE_SB2_TARGET
    
  sudo chown -R $USER $SFFE_SB2_TARGET
    
  cd $SFFE_SB2_TARGET
  grep :$(id -u): /etc/passwd >> etc/passwd
  grep :$(id -g): /etc/group >> etc/group
    
  sb2-init -d -L "--sysroot=/" -C "--sysroot=/" -c /usr/bin/qemu-arm-dynamic -m sdk-build -n -N -t / $VENDOR-$DEVICE-armv7hl /opt/cross/bin/armv7hl-meego-linux-gnueabi-gcc
  
  sb2 -t $VENDOR-$DEVICE-armv7hl -m sdk-install -R rpm --rebuilddb
  sb2 -t $VENDOR-$DEVICE-armv7hl -m sdk-install -R zypper ref --force

We also need to add a tools repo to the target::

.. code-block:: console

  MER_SDK $

  sb2 -t $VENDOR-$DEVICE-armv7hl -m sdk-install -R zypper ar -G http://repo.merproject.org/obs/mer-tools:/testing/latest_i486/ mer-tools-testing
  # FIXME: This should be mer-tools and use rolling repo
  sb2 -t $VENDOR-$DEVICE-armv7hl -m sdk-install -R zypper ref


Do a sanity check on scratchbox2 target:

.. code-block:: console

    cd $HOME
    cat > main.c << EOF
    #include <stdlib.h>
    #include <stdio.h>
    
    int main(void) {
      printf("Hello, world!\n");
      return EXIT_SUCCESS;
    }
    EOF

    sb2 -t $VENDOR-$DEVICE-armv7hl gcc main.c -o test

If the compilation was successful you can test the executable by running the
following command.

.. code-block:: console

    sb2 -t $VENDOR-$DEVICE-armv7hl ./test

The above command should output "Hello, world" on the console, this proves
that the target can compile binaries and execute them for your architecture.

