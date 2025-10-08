# OTA (Over-the-Air) Updates

You can setup to upgrade a Sailfish OS device over the air, a.k.a. OTA
update.

## Prepare the infrastructure

- Ensure your Sailfish OS version is at least 3.2.1 (3.4.0 for `aarch64`)
- Create file `20-mydomain.ini` (rename "mydomain" as you see fit)
  under `$ANDROID_ROOT/hybris/droid-configs/sparse/usr/share/ssu/repos.d/`
  with the following content:

```ini
[release]
adaptation=https://mydomain.net/%(release)/%(vendor)-%(adaptation)/%(arch)/
```

- Substitute `https://mydomain.net/` with your Web server address
  (including subpath if exists)
- The `%(release)/%(vendor)-%(adaptation)/%(arch)/` format is advised,
  because it's the most future-proof. E.g. for the Nexus 5 this
  string would resolve to `4.5.0.19/lge-hammerhead/aarch64/`
- Commit the above change to droid-configs (including updating the
  submodule, which introduces timestamped versioning, so updates get
  picked up)
- Make new image and ensure devices are flashed which will be
  receiving future updates
- Make some changes to your adaptation (e.g. fix some HW issue) and
  rebuild the affected part via `build_packages.sh`, so that version
  numbers increase

## Test for any breakages

Before deploying any updates to production, they must be tested first.

Prerequisites:

- Web server (e.g. Apache) running on HOST and accessible within network
- Directory listing doesn't need to be enabled
- Assuming Web server's rootdir is `/srv/http`

Perform the following:

```sh title="HOST"

. ~/.hadk.env
rm -rf /srv/http/sailfish-tmp-test-repo
cp -ar $ANDROID_ROOT/droid-local-repo/$DEVICE /srv/http/sailfish-tmp-test-repo
rm -rf /srv/http/sailfish-tmp-test-repo/repo
createrepo_c /srv/http/sailfish-tmp-test-repo
```

SSH into your device and execute (substituting `https://mydomain.net`
with the address to your Web server):

```sh title="DEVICE"

ssu ar sfos-test https://mydomain.net/sailfish-tmp-test-repo
devel-su -p pkcon install zypper
devel-su zypper refresh sfos-test
devel-su zypper dup --from sfos-test
```

Check that all the packages you touched are to be updated or removed as
expected. Afterwards you can press "Yes" to execute the update and
check if the device functions as desired, also after reboot.

Once happy, clean up the testing environment:

```sh title="DEVICE"

ssu rr sfos-test
```

```sh title="HOST"

rm -rf /srv/http/sailfish-tmp-test-repo
```

## Release into production for all users

Once successfully tested, deploy the stable packages to the release
repo:

```sh title="HOST"

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

```sh title="PLATFORM SDK"

cd $ANDROID_ROOT
# Alternatively you can use `mb2 --output-dir ... build` instead of copying
cp -a path/to/custom-built.rpm droid-local-repo/$DEVICE
```

To make the devices of your users pull this RPM package in, ensure some
other package or pattern requires it, then [test](#test-for-any-breakages)
and [deploy](#release-into-production-for-all-users) your repo as per
instructions above.

## Updating to the next Sailfish OS release

If another official Sailfish OS update has been released since you last
published your HW adaptation update, perform the following:

Update your SDK target device build environment (see how in the last
paragraph of [Setup the Platform SDK](setupsdk.md#setup-the-platform-sdk)).

Alternatively, you can remove it and create a new one as per
[Installing Build Tools for Your Device](build-env.md).

Remove or backup your local build repository:

```sh title="PLATFORM SDK"

cd $ANDROID_ROOT

PREV_RELEASE=4.4.0.68    # adjust to the previous release version you were on

mv droid-local-repo/$DEVICE droid-local-repo/$DEVICE-$PREV_RELEASE
mkdir droid-local-repo/$DEVICE
```

Then rebuild all packages and a new image by executing `build_packages.sh`.

Afterwards [test](#test-for-any-breakages) the rebuilt repo. The actual testing
sequence on the device will be different:

```sh title="DEVICE"

ssu ar sfos-test https://mydomain.net/sailfish-tmp-test-repo
ssu dr adaptation0
ssu re 4.5.0.19    # adjust to the actual version
devel-su -p version --dup
ssu rr sfos-test
ssu er adaptation0
```

Then reboot as and test device functionality.

Once satisfactory, [publish](#release-into-production-for-all-users)
your repo for all users.

Finally, to receive the update, each device will have to execute:

```sh title="DEVICE"

ssu re 4.5.0.19    # adjust to the actual version
devel-su -p version --dup
```

!!!note
    The `%(release)` in your self-hosted repo (visible via `ssu lr`)
    will get updated automatically after `ssu re`.

After `devel-su -p version --dup` has finished, reboot as instructed.
