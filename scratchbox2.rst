Setting up Scratchbox2 Target
-----------------------------

It is necessary to setup a Scratchbox2 target to use for packaging your
hardware adaptation packages in the next section. Download and create your
Scratchbox2 target following this wiki:

.. important::
    Please use the 2.1.1.24 target
    (http://releases.sailfishos.org/sdk/latest/targets-1707/Jolla-2.1.1.24-Sailfish_SDK_Target-armv7hl.tar.bz2)
    and build Sailfish OS (in chapter 8) for 2.1.1.26, even if it has been
    discontinued at the time of writing (2017-09-23). All community ports
    building tools have been setup around 2.1.1, as well as Sailfish X is meant
    to be run on 2.1.1. This banner will be removed when 2.1.2 is released.

.. warning::
    To ensure consistency with HADK build scripts, name your target as
    ``$VENDOR-$DEVICE-$PORT_ARCH`` instead of the wiki's suggested
    ``SailfishOS-armv7hl``.

https://sailfishos.org/wiki/Platform_SDK_Target_Installation

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

