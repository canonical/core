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
	# workaround for http://pad.lv/1605622
	echo "I: listing pwd"
	ls -l
	echo "I: listing binary/"
	ls -l binary
	rm -rf binary/boot/filesystem.dir/meta
	echo "I: listing all non root owned files"
	find binary/boot/filesystem.dir/ \! -user root -print
	echo "I: listing all non root group owned files"
	find binary/boot/filesystem.dir/ \! -group root -print
	cp -a binary/boot/filesystem.dir/* $(DESTDIR)/
	echo "I: checking after copy"
	find $(DESTDIR)/ \! -user root -print
	find $(DESTDIR)/ \! -group root -print
