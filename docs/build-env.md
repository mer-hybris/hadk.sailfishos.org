# Installing Build Tools for Your Device

It is necessary to emulate your target device architecture and file
system to build hardware adaptation packages in the next section.
Download and install your build tools following instructions below.

::: important
::: title
Important
:::

Minimum version for SFOS target is 4.3.0.15 (same requirement as for the
Platform SDK Chroot earlier)
:::

::: warning
::: title
Warning
:::

To ensure consistency with HADK build scripts, name your tooling
`SailfishOS-4.5.0` (or whichever release you are building for) instead
of suggested `SailfishOS-latest`, and your target as
`$VENDOR-$DEVICE-$PORT_ARCH` (instead of `SailfishOS-latest-aarch64`).
Ignore the i486 target.
:::

For ARM devices, choose `aarch64` build target, unless you are building
for the `armv7hl` Sailfish OS userspace.

<https://docs.sailfishos.org/Tools/Platform_SDK/Target_Installation/>

To verify the correct installation of the build tools, cross-compile a
simple \"Hello, World!\" C application with `mb2 build-shell`:

``` console
PLATFORM_SDK $

cd $HOME
mkdir hadk-test-tmp
cd hadk-test-tmp
cat > main.c << EOF
#include <stdlib.h>
#include <stdio.h>

int main(void) {
  printf("Hello, world!\n");
  return EXIT_SUCCESS;
}
EOF
mb2 -t $VENDOR-$DEVICE-$PORT_ARCH build-init
mb2 -t $VENDOR-$DEVICE-$PORT_ARCH build-shell gcc main.c -o test
```

If the compilation was successful you can test the executable by running
the following command (this will run the executable using `qemu` as
emulation layer, which is part of the `mb2` setup):

``` console
mb2 -t $VENDOR-$DEVICE-$PORT_ARCH build-shell ./test
```

The above command should output \"Hello, world!\" on the console, this
proves that the build tools can compile binaries and execute them for
your architecture.
