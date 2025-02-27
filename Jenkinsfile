#!/usr/bin/groovy
// SPDX-License-Identifier: BSD-2-Clause-Patent
// Copyright 2019-2024 Intel Corporation
// Copyright 2025 Hewlett Packard Enterprise Development LP

// To use a test branch (i.e. PR) until it lands to master
// I.e. for testing library changes
//@Library(value="pipeline-lib@your_branch") _

/* groovylint-disable-next-line CompileStatic */
packageBuildingPipelineDAOSTest(['distros': ['el8', 'el9', 'leap15', 'ubuntu20.04'],
                                 'make args': 'DISTRO_VERSION_EL8=8.5',
                                 'test-tag': 'DmgNetworkScanTest daosio'])
