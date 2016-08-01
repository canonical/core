DPKG_ARCH := $(shell dpkg --print-architecture)
RELEASE := $(shell lsb_release -c -s)
ENV := PROJECT=ubuntu-core SUBPROJECT=system-image EXTRA_PPAS='snappy-dev/image snappy-dev/edge' IMAGEFORMAT=plain SUITE=$(RELEASE) ARCH=$(DPKG_ARCH) PROPOSED=1

#ifneq ($(shell grep $(RELEASE)-proposed /etc/apt/sources.list),)
#ENV += PROPOSED=1
#endif


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
	# workaround for http://pad.lv/1605622
	rm -rf binary/boot/filesystem.dir/meta
	mv binary/boot/filesystem.dir/* $(DESTDIR)/
