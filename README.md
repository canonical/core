# The core snap

This repository contains the official core snap.

## Reporting issues

Please report all issues on the Launchpad project page
https://bugs.launchpad.net/snapd/+filebug

## Building

To build the core snap locally please use `sudo snapcraft`.

An easy way to customize the content of the built snap is including additional
PPAs with custom packages in the `EXTRA_PPAS` variable inside the Makefile's
`ENV` variable.

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
