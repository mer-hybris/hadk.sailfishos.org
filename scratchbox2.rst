Setting up Scratchbox2 Target
-----------------------------

It is necessary to setup a Scratchbox2 target to use for packaging your
hardware adaptation packages in the next section. Download and create your
Scratchbox2 target following this wiki:

.. important::
    Minimum version for SFOS target is 4.3.0.15 (same requirement as for the
    Platform SDK Chroot earlier)

.. warning::
    To ensure consistency with HADK build scripts, name your tooling
    ``SailfishOS-4.3.0`` (or whichever release you are building for) instead of
    wiki's suggested ``SailfishOS-latest``, and your target as
    ``$VENDOR-$DEVICE-$PORT_ARCH`` (instead of ``SailfishOS-latest-aarch64``).
    Ignore the i486 target.

Choose ``aarch64`` target, unless you are building for the ``armv7hl``
Sailfish OS userspace.

https://docs.sailfishos.org/Tools/Platform_SDK/Target_Installation/

To verify the correct installation of the Scratchbox2 target, cross-compile
a simple "Hello, World!" C application with ``sb2``:

.. code-block:: console

    PLATFORM_SDK $

    cd $HOME
    cat > main.c << EOF
    #include <stdlib.h>
    #include <stdio.h>

    int main(void) {
      printf("Hello, world!\n");
      return EXIT_SUCCESS;
    }
    EOF

    sb2 -t $VENDOR-$DEVICE-$PORT_ARCH gcc main.c -o test

If the compilation was successful you can test the executable by running the
following command (this will run the executable using ``qemu`` as emulation
layer, which is part of the ``sb2`` setup):

.. code-block:: console

    sb2 -t $VENDOR-$DEVICE-$PORT_ARCH ./test

The above command should output "Hello, world!" on the console, this proves
that the target can compile binaries and execute them for your architecture.

