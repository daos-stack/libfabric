NAME    := libfabric
VERSION := 1.6.0
RELEASE := 1
DIST    := $(shell rpm --eval %{dist})
SRPM    := _topdir/SRPMS/$(NAME)-$(VERSION)-$(RELEASE)$(DIST).src.rpm
RPMS    := _topdir/RPMS/x86_64/$(NAME)-$(VERSION)-$(RELEASE)$(DIST).x86_64.rpm           \
	   _topdir/RPMS/x86_64/$(NAME)-devel-$(VERSION)-$(RELEASE)$(DIST).x86_64.rpm     \
	   _topdir/RPMS/x86_64/$(NAME)-debuginfo-$(VERSION)-$(RELEASE)$(DIST).x86_64.rpm
SPEC    := $(NAME).spec
SRC_EXT := bz2
SOURCE  := https://github.com/ofiwg/libfabric/releases/download/v$(VERSION)/libfabric-$(VERSION).tar.$(SRC_EXT)
TARGETS := $(RPMS) $(SRPM)

all: $(TARGETS)

%/:
	mkdir -p $@

_topdir/SOURCES/%: % | _topdir/SOURCES/
	ln $< $@

$(NAME)-$(VERSION).tar.$(SRC_EXT):
	curl -L -O '$(SOURCE)'

# see https://stackoverflow.com/questions/2973445/ for why we subst
# the "rpm" for "%" to effectively turn this into a multiple matching
# target pattern rule
$(subst rpm,%,$(RPMS)): $(SPEC) _topdir/SOURCES/$(NAME)-$(VERSION).tar.$(SRC_EXT)
	rpmbuild -bb --define "%_topdir $$PWD/_topdir" $(SPEC)

$(SRPM): $(SPEC) _topdir/SOURCES/$(NAME)-$(VERSION).tar.$(SRC_EXT)
	rpmbuild -bs --define "%_topdir $$PWD/_topdir" $(SPEC)

srpm: $(SRPM)

rpms: $(RPMS)

ls: $(TARGETS)
	ls -ld $^

mockbuild: $(SRPM)
	mock $<

rpmlint: $(SPEC)
	rpmlint $<
