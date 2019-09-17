NAME    := libfabric
SRC_EXT := gz
SOURCE   = https://github.com/ofiwg/$(NAME)/archive/v$(VERSION).tar.$(SRC_EXT)
PATCHES := v1.8.0...3712eb04919fb9542659da326d295734d974013d.patch

sl42_REPOS    := --repo https://download.opensuse.org/repositories/science:/HPC/openSUSE_Leap_42.3/
sle12_REPOS   := $(sl42_REPOS)
sl15_REPOS    := --repo https://download.opensuse.org/repositories/science:/HPC/openSUSE_Leap_15.1/

include packaging/Makefile_packaging.mk

test:
	$(call install_repos,$(NAME)@$(BRANCH_NAME):$(BUILD_NUMBER))
	yum -y install libfabric
	fi_info -l | grep ^psm2:
	fi_info -l | grep ^verbs:
