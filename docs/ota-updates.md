# OTA (Over-the-Air) Updates

You can setup to upgrade a Sailfish OS device over the air, a.k.a. OTA
update.

## Prepare the infrastructure

-   Ensure your Sailfish OS version is at least 3.2.1 (3.4.0 for
    `aarch64`)
-   Create file `20-mydomain.ini` (rename \"mydomain\" as you see fit)
    under
    `$ANDROID_ROOT/hybris/droid-configs/sparse/usr/share/ssu/repos.d/`
    with the following content:

``` ini
[release]
adaptation=https://mydomain.net/%(release)/%(vendor)-%(adaptation)/%(arch)/
```

-   Substitute `https://mydomain.net/` with your Web server address
    (including subpath if exists)
-   The `%(release)/%(vendor)-%(adaptation)/%(arch)/` format is advised,
    because it\'s the most future-proof. E.g. for the Nexus 5 this
    string would resolve to `4.5.0.19/lge-hammerhead/aarch64/`
-   Commit the above change to droid-configs (including updating the
    submodule, which introduces timestamped versioning, so updates get
    picked up)
-   Make new image and ensure devices are flashed which will be
    receiving future updates
-   Make some changes to your adaptation (e.g. fix some HW issue) and
    rebuild the affected part via `build_packages.sh`, so that version
    numbers increase

## Test for any breakages {#test_repo}

Before deploying any updates to production, they must be tested first.

Prerequisites:

-   Web server (e.g. Apache) running on HOST and accessible within
    network
-   Directory listing doesn\'t need to be enabled
-   Assuming Web server\'s rootdir is `/srv/http`

Perform the following:

``` bash
HOST $

. ~/.hadk.env
rm -rf /srv/http/sailfish-tmp-test-repo
cp -ar $ANDROID_ROOT/droid-local-repo/$DEVICE /srv/http/sailfish-tmp-test-repo
rm -rf /srv/http/sailfish-tmp-test-repo/repo
createrepo_c /srv/http/sailfish-tmp-test-repo
```

SSH into your device and execute (substituting `https://mydomain.net`
with the address to your Web server):

``` bash
DEVICE $

ssu ar sfos-test https://mydomain.net/sailfish-tmp-test-repo
devel-su -p pkcon install zypper
devel-su zypper refresh sfos-test
devel-su zypper dup --from sfos-test
```

Check that all the packages you touched are to be updated or removed as
expected. Afterwards you can press \"Yes\" to execute the update and
check if the device functions as desired, also after reboot.

Once happy, clean up the testing environment:

``` bash
DEVICE $

ssu rr sfos-test


HOST $

rm -rf /srv/http/sailfish-tmp-test-repo
```

## Release into production for all users {#deploy_repo}

Once successfully tested, deploy the stable packages to the release
repo:

``` bash
HOST $

. ~/.hadk.env
rm -rf /srv/http/$RELEASE/$VENDOR-$DEVICE/$PORT_ARCH
mkdir -p /srv/http/$RELEASE/$VENDOR-$DEVICE
cp -ar $ANDROID_ROOT/droid-local-repo/$DEVICE \
       /srv/http/$RELEASE/$VENDOR-$DEVICE/$PORT_ARCH
rm -rf /srv/http/$RELEASE/$VENDOR-$DEVICE/$PORT_ARCH/repo
createrepo_c /srv/http/$RELEASE/$VENDOR-$DEVICE/$PORT_ARCH
```

To receive the update, each device will have to execute
`devel-su -p version --dup`, and reboot when instructed.

## Adding custom RPM packages

You can add any other RPM binary packages to the local build repository
(i.e. packages that were not created by running `build_packages.sh`).
For example:

``` bash
PLATFORM_SDK $

cd $ANDROID_ROOT
# Alternatively you can use `mb2 --output-dir ... build` instead of copying
cp -a path/to/custom-built.rpm droid-local-repo/$DEVICE
```

To make the devices of your users pull this RPM package in, ensure some
other package or pattern requires it, then
`test<test_repo>`{.interpreted-text role="ref"} and
`deploy<deploy_repo>`{.interpreted-text role="ref"} your repo as per
instructions above.

## Updating to the next Sailfish OS release

If another official Sailfish OS update has been released since you last
published your HW adaptation update, perform the following:

Update your SDK target device build environment (see how in the last
paragraph of `enter-sfos-sdk`{.interpreted-text role="ref"}).

Alternatively, you can remove it and create a new one as per
`build-env`{.interpreted-text role="doc"}.

Remove or backup your local build repository:

``` bash
PLATFORM_SDK $

cd $ANDROID_ROOT

PREV_RELEASE=4.4.0.68    # adjust to the previous release version you were on

mv droid-local-repo/$DEVICE droid-local-repo/$DEVICE-$PREV_RELEASE
mkdir droid-local-repo/$DEVICE
```

Then rebuild all packages and a new image by executing
`build_packages.sh`.

Afterwards `test<test_repo>`{.interpreted-text role="ref"} the rebuilt
repo. The actual testing sequence on the device will be different:

``` bash
DEVICE $

ssu ar sfos-test https://mydomain.net/sailfish-tmp-test-repo
ssu dr adaptation0
ssu re 4.5.0.19    # adjust to the actual version
devel-su -p version --dup
ssu rr sfos-test
ssu er adaptation0
```

Then reboot as and test device functionality.

Once satisfactory, `publish<deploy_repo>`{.interpreted-text role="ref"}
your repo for all users.

Finally, to receive the update, each device will have to execute:

``` bash
DEVICE $

ssu re 4.5.0.19    # adjust to the actual version
devel-su -p version --dup
```

NOTE: The %(release) in your self-hosted repo (visible via `ssu lr`)
will get updated automatically after `ssu re`.

After `devel-su -p version --dup` has finished, reboot as instructed.
