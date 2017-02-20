# Core Snap

This repository contains the official Core snap. The core snap plays

## Reporting Issues

Please report all issues on the Launchpad project page
https://bugs.launchpad.net/snapd/+filebug

## Building

To build the gadget snap locally please use `snapcraft`.

This snapcraft yaml allows you to create an Ubuntu Core os snap package
To build your own against i.e. an additional PPA that provides changed
packages you want to test, please edit the `EXTRA_PPAS` variable inside
the `ENV` variable in the Makefile.

If you do builds of this snap on launchpad, please make sure to build
against xenial, with the `~snappy-dev/ubuntu/image` PPA as source archive
and the `Updates` pocket as default pocket.
