DPKG_ARCH := $(shell dpkg --print-architecture)
RELEASE := $(shell lsb_release -c -s)
SUDO := sudo
EXTRA_PPAS := snappy-dev/image
ENV := $(SUDO) PROJECT=ubuntu-core SUBPROJECT=system-image IMAGEFORMAT=plain SUITE=$(RELEASE) ARCH=$(DPKG_ARCH)

ifneq ($(shell apt-cache policy snapd|grep -E 'ppa\.launchpad(content)?\.net/snappy-dev/edge'),)
EXTRA_PPAS += snappy-dev/edge
endif

all: check
	mkdir -p auto
	for f in config build clean; \
	    do ln -s /usr/share/livecd-rootfs/live-build/auto/$$f auto/; \
	done
	$(ENV) EXTRA_PPAS='$(EXTRA_PPAS)' lb clean
	$(ENV) EXTRA_PPAS='$(EXTRA_PPAS)' lb config
	# lb config copies the live-build/ubuntu-core/hooks/ from the
	# livecd-rootfs package to config/hooks/, we want to maintain these
	# hooks in the github tree instead, so remove the ones from the
	# package and put ours in place instead.
	$(SUDO) rm -f config/hooks/*
	$(SUDO) cp -a live-build/hooks/* config/hooks/
	$(ENV) EXTRA_PPAS='$(EXTRA_PPAS)' lb build

install:
	echo "I: in install target"
	# workaround for http://pad.lv/1605622
	$(SUDO) rm -rf binary/boot/filesystem.dir/meta
	# make sure /tmp in the snap is mode 1777
	$(SUDO) chmod 1777 binary/boot/filesystem.dir/tmp
	$(SUDO) mv binary/boot/filesystem.dir/* $(DESTDIR)/
	# only copy the manifest file if we are in a launchpad buildd
	set -e ; if [ -e /build/core ]; then \
	  TARGET_BASENAME=/build/core/core_16-$$(grep ^VERSION= $(DESTDIR)/usr/lib/snapd/info|cut -f2 -d=|cut -f1 -d~|cut -b1-29)_$(DPKG_ARCH); \
	  $(SUDO) mv livecd.ubuntu-core.manifest "$${TARGET_BASENAME}".manifest;  \
	  $(SUDO) cp /build/core/parts/livebuild/install/usr/share/snappy/dpkg.yaml "$${TARGET_BASENAME}".dpkg.yaml; \
	  ls -lah /build/core; \
	fi

check:
	# exclude "useless cat" from checks, while useless also makes
	# some things more readable
	shellcheck -e SC2002 hooks/* live-build/hooks/*
	python3 -m unittest
