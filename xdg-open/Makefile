
CC = gcc
INSTALL = install

CFLAGS = -O2 -g -Wall $(shell pkg-config --cflags gio-unix-2.0)
LDFLAGS = -O2 -g
LIBS = $(shell pkg-config --libs gio-2.0)

DESTDIR ?=

all: xdg-open

xdg-open: xdg-open.o
	$(CC) $(LDFLAGS) -o $@ $^ $(LIBS)

install: all
	$(INSTALL) -m 755 -d $(DESTDIR)/usr/bin $(DESTDIR)/usr/share/applications
	$(INSTALL) -m 755 -s xdg-open $(DESTDIR)/usr/bin
	$(INSTALL) -m 644 xdg-open.desktop $(DESTDIR)/usr/share/applications
	$(INSTALL) -m 644 mimeapps.list $(DESTDIR)/usr/share/applications

.PHONY: all install
