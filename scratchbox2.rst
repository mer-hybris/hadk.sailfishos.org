Setting up Scratchbox2 Target
-----------------------------

It is necessary to setup a Scratchbox2 target to use for packaging your
hardware adaptation packages in the next section. Download and create your
Scratchbox2 target with the following commands:

.. code-block:: console

  MERSDK $

  hadk

  cd $HOME

  SFE_SB2_TARGET=$MER_ROOT/targets/$VENDOR-$DEVICE-$ARCH
  TARBALL_URL=http://releases.sailfishos.org/sdk/latest/targets/targets.json
  TARBALL=$(curl $TARBALL_URL | grep "$ARCH.tar.bz2" | cut -d\" -f4)
  curl -O $TARBALL

  sudo mkdir -p $SFE_SB2_TARGET
  sudo tar --numeric-owner -pxjf $(basename $TARBALL) -C $SFE_SB2_TARGET

  sudo chown -R $USER $SFE_SB2_TARGET

  cd $SFE_SB2_TARGET
  grep :$(id -u): /etc/passwd >> etc/passwd
  grep :$(id -g): /etc/group >> etc/group

  # don't worry about this message: collect2: cannot find 'ld'
  # FIXME: qemu-arm won't work for Intel Architecture builds
  sb2-init -d -L "--sysroot=/" -C "--sysroot=/" \
           -c /usr/bin/qemu-arm-dynamic -m sdk-build \
           -n -N -t / $VENDOR-$DEVICE-$ARCH \
           /opt/cross/bin/$ARCH-meego-linux-gnueabi-gcc

  sb2 -t $VENDOR-$DEVICE-$ARCH -m sdk-install -R rpm --rebuilddb

  sb2 -t $VENDOR-$DEVICE-$ARCH -m sdk-install -R zypper ar \
    -G http://repo.merproject.org/releases/mer-tools/rolling/builds/$ARCH/packages/ \
    mer-tools-rolling

  sb2 -t $VENDOR-$DEVICE-$ARCH -m sdk-install -R zypper ref --force

To verify the correct installation of the Scratchbox2 target, cross-compile
a simple "Hello, World!" C application with ``sb2``:

.. code-block:: console

    MERSDK $

    cd $HOME
    cat > main.c << EOF
    #include <stdlib.h>
    #include <stdio.h>

    int main(void) {
      printf("Hello, world!\n");
      return EXIT_SUCCESS;
    }
    EOF

    sb2 -t $VENDOR-$DEVICE-$ARCH gcc main.c -o test

If the compilation was successful you can test the executable by running the
following command (this will run the executable using ``qemu`` as emulation
layer, which is part of the ``sb2`` setup):

.. code-block:: console

    sb2 -t $VENDOR-$DEVICE-$ARCH ./test

The above command should output "Hello, world!" on the console, this proves
that the target can compile binaries and execute them for your architecture.

