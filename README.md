# The core snap

This repository contains the official core snap.

## Reporting issues

Please report all issues on the Launchpad project page
https://bugs.launchpad.net/snapd/+filebug

## Building

To build the core snap locally you need a clean chroot or container with
Ubuntu 16.04. Inside this container or chroot run:

    $ sudo apt install git snapcraft
    $ git clone https://github.com/snapcore/core.git
    $ sudo apt-add-repository ppa:snappy-dev/image
    $ cd core
    $ # now make any modifications of the Makefile you require (see below)
    $ sudo snapcraft # (if you are not root already)

One easy way to customize the content of the built snap is including additional
PPAs with custom packages in the `EXTRA_PPAS` variable inside the Makefile's
`ENV` variable.

Another is to add a script snippet to live-build/hooks (where scripts with the
ending .chroot are executed chrooted inside the resulting rootfs during build, 
the ones with .binary ending are run in the build environment from outside the
resulting rootfs).

Launchpad builds should be done against xenial with the
`~snappy-dev/ubuntu/image` PPA as source archive and `Updates` as the default
pocket.

## Launchpad mirror and automatic builds.

All commits from the master branch of https://github.com/snapcore/core are
automatically mirrored by Launchpad to the https://launchpad.net/core-snap
project.

The master branch is automatically built from the launchpad mirror and
published into the snap store to the edge channel.

You can find build history and other controls here:
https://code.launchpad.net/~snappy-dev/+snap/core/
