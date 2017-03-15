DPKG_ARCH := $(shell dpkg --print-architecture)
RELEASE := $(shell lsb_release -c -s)
ENV := PROJECT=ubuntu-core SUBPROJECT=system-image EXTRA_PPAS='snappy-dev/image snappy-dev/edge' IMAGEFORMAT=plain SUITE=$(RELEASE) ARCH=$(DPKG_ARCH)

# workaround for LP: #1588336, needs to be bumped along
# with the snapcraft.yaml version for now
VERSION := 16-2

#ifneq ($(shell grep $(RELEASE)-proposed /etc/apt/sources.list),)
#ENV += PROPOSED=1
#endif

all: check
	mkdir -p auto
	for f in config build clean; \
	    do ln -s /usr/share/livecd-rootfs/live-build/auto/$$f auto/; \
	done
	$(ENV) lb clean
	$(ENV) lb config
	# lb config copies the live-build/ubuntu-core/hooks/ from the
	# livecd-rootfs package to config/hooks/, we want to maintain these
	# hooks in the github tree instead, so remove the ones from the
	# package and put ours in place instead.
	rm -f config/hooks/*
	cp -a live-build/hooks/* config/hooks/
	$(ENV) lb build

install:
	echo "I: in install target"
	# workaround for http://pad.lv/1605622
	rm -rf binary/boot/filesystem.dir/meta
	# make sure /tmp in the snap is mode 1777
	chmod 1777 binary/boot/filesystem.dir/tmp
	mv binary/boot/filesystem.dir/* $(DESTDIR)/
	# only copy the manifest file if we are in a launchpad buildd
	if [ -e /build/core ]; then \
	  mv livecd.ubuntu-core.manifest /build/core/core_$(VERSION)_$(DPKG_ARCH).manifest; \
	  ls -l /build/core; \
	fi

check:
	# exlucde "useless cat" from checks, while useless also makes
	# some things more readable
	shellcheck -e SC2002 hooks/* live-build/hooks/*
	python3 -m unittest
