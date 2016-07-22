DPKG_ARCH := $(shell dpkg --print-architecture)
RELEASE := $(shell lsb_release -c -s)
ENV := PROJECT=ubuntu-core SUBPROJECT=system-image EXTRA_PPAS='snappy-dev/image snappy-dev/edge' IMAGEFORMAT=plain SUITE=$(RELEASE) ARCH=$(DPKG_ARCH)


all:
	mkdir -p auto
	for f in config build clean; \
	    do ln -s /usr/share/livecd-rootfs/live-build/auto/$$f auto/; \
	done
	$(ENV) lb clean
	$(ENV) lb config
	$(ENV) lb build

install:
	echo "I: in install target"
	mv binary/boot/filesystem.dir $(DESTDIR)
