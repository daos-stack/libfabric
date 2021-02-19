NAME    := libfabric
SRC_EXT := gz
SOURCE   = https://github.com/ofiwg/$(NAME)/archive/v$(VERSION).tar.$(SRC_EXT)

OSUSE_HPC_REPO := https://download.opensuse.org/repositories/science:/HPC

ifeq ($(DAOS_STACK_LEAP_15_GROUP_REPO),)
LEAP_15_REPOS := $(OSUSE_HPC_REPO)/openSUSE_Leap_$(lsb_release -s -r)/
endif

include Makefile_packaging.mk
