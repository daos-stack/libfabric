# SPDX-License-Identifier: BSD-2-Clause-Patent
# Copyright (C) 2019-2024 Intel Corporation

NAME    := libfabric
SRC_EXT := bz2

OSUSE_HPC_REPO := https://download.opensuse.org/repositories/science:/HPC

ifeq ($(DAOS_STACK_LEAP_15_GROUP_REPO),)
LEAP_15_REPOS := $(OSUSE_HPC_REPO)/openSUSE_Leap_15.1/
endif

include packaging/Makefile_packaging.mk

test:
	$(call install_repos,$(NAME)@$(BRANCH_NAME):$(BUILD_NUMBER))
	yum -y install libfabric
	fi_info -l | grep ^verbs:
