NAME    := libfabric
SOURCE  := https://github.com/ofiwg/$(NAME)/archive/v$(VERSION).tar.$(SRC_EXT)

DIST    := $(shell rpm --eval %{?dist})
ifeq ($(DIST),)
SED_EXPR := 1p
else
SED_EXPR := 1s/$(DIST)//p
endif
VERSION := $(shell rpm --specfile --qf '%{version}\n' $(NAME).spec | sed -n '1p')
RELEASE := $(shell rpm --specfile --qf '%{release}\n' $(NAME).spec | sed -n '$(SED_EXPR)')
SRPM    := _topdir/SRPMS/$(NAME)-$(VERSION)-$(RELEASE)$(DIST).src.rpm
RPMS    := $(addsuffix .rpm,$(addprefix _topdir/RPMS/x86_64/,$(shell rpm --specfile $(NAME).spec)))
SPEC    := $(NAME).spec
SRC_EXT := gz
SOURCES := _topdir/SOURCES/v$(VERSION).tar.$(SRC_EXT)
TARGETS := $(RPMS) $(SRPM)

# need to use -k because the certificate store is not properly
# configured on SLES 12.3 containers
ifeq ($(shell lsb_release -sir),SUSE 12.3)
  CURL_INSECURE := -k
endif

all: $(TARGETS)

%/:
	mkdir -p $@

_topdir/SOURCES/%: % | _topdir/SOURCES/
	rm -f $@
	ln $< $@

v$(VERSION).tar.$(SRC_EXT):
	curl $(CURL_INSECURE) -f -L -O '$(SOURCE)'

# see https://stackoverflow.com/questions/2973445/ for why we subst
# the "rpm" for "%" to effectively turn this into a multiple matching
# target pattern rule
$(subst rpm,%,$(RPMS)): $(SPEC) $(SOURCES)
	rpmbuild -bb --define "%_topdir $$PWD/_topdir" $(SPEC)

$(SRPM): $(SPEC) $(SOURCES)
	rpmbuild -bs --define "%_topdir $$PWD/_topdir" $(SPEC)

srpm: $(SRPM)

$(RPMS): Makefile

rpms: $(RPMS)

ls: $(TARGETS)
	ls -ld $^

mockbuild: $(SRPM) Makefile
	mock $<

rpmlint: $(SPEC)
	rpmlint $<

show_version:
	@echo $(VERSION)

show_release:
	@echo $(RELEASE)

show_rpms:
	@echo $(RPMS)

.PHONY: srpm rpms ls mockbuild rpmlint FORCE show_version show_release show_rpms
