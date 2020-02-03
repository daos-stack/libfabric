NAME    := libfabric
SRC_EXT := gz
SOURCE   = https://github.com/ofiwg/$(NAME)/archive/v$(VERSION).tar.$(SRC_EXT)
PATCHES := v1.8.0...3712eb04919fb9542659da326d295734d974013d.patch \
           3712eb04919fb9542659da326d295734d974013d...86340704a7c73e924d2d6e3112d2350ad0f83d84.patch \
           86340704a7c73e924d2d6e3112d2350ad0f83d84...49ee762bc114a186a1ddfd3cf556b053ae084d0c.patch

OSUSE_HPC_REPO := https://download.opensuse.org/repositories/science:/HPC
LEAP_42_HPC_REPO := $(OSUSE_HPC_REPO)/openSUSE_Leap_42.3/

ifeq ($(DAOS_STACK_LEAP_42_GROUP_REPO),)
LEAP_42_REPOS  := $(LEAP_42_HPC_REPO)
endif
ifeq ($(DAOS_STACK_SLES_12_GROUP_REPO),)
SLES_12_REPOS := $(LEAP_42_HPC_REPO)
endif
ifeq ($(DAOS_STACK_LEAP_15_GROUP_REPO),)
LEAP_15_REPOS := $(OSUSE_HPC_REPO)/openSUSE_Leap_15.1/
endif

include packaging/Makefile_packaging.mk

test:
	$(call install_repos,$(NAME)@$(BRANCH_NAME):$(BUILD_NUMBER))
	yum -y install libfabric
	fi_info -l | grep ^psm2:
	fi_info -l | grep ^verbs:
