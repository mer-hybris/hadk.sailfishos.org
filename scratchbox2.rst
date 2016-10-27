Setting up Scratchbox2 Target
-----------------------------

It is necessary to setup a Scratchbox2 target to use for packaging your
hardware adaptation packages in the next section. Download and create your
Scratchbox2 target following this wiki:

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

