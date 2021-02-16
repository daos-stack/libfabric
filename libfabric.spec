%define suse_libname libfabric1
#global dl_version 1.11.1rc1

%{?dl_version:%global autosetup_args --p1 -n libfabric-%{dl_version}}

Name: libfabric
Version: 1.12.0~rc1
Release: 1%{?dist}
Summary: User-space RDMA Fabric Interfaces
%if 0%{?suse_version} >= 1315
License: GPL-2.0-only OR BSD-2-Clause
Group: Development/Libraries/C and C++
%else
Group: System Environment/Libraries
License: GPLv2 or BSD
%endif
Url: https://www.github.com/ofiwg/libfabric
Source: https://github.com/ofiwg/%{name}/archive/v%{?dl_version}%{!?dl_version:%version}.tar.gz

%if 0%{?rhel} >= 7
BuildRequires: librdmacm-devel >= 1.0.16
%else
%if 0%{?suse_version} >= 1315
BuildRequires: rdma-core-devel >= 1.0.16
%endif
%endif
BuildRequires: libibverbs-devel >= 1.2.0
BuildRequires: libnl3-devel
BuildRequires: fdupes

# infinipath-psm-devel only available for x86_64
%ifarch x86_64
# BuildRequires: infinipath-psm-devel
%if 0%{?suse_version} >= 1315 || 0%{?rhel} >= 7
BuildRequires: libpsm2-devel >= 11.2.78
%endif
%endif
# valgrind is unavailable for s390
%ifnarch s390
BuildRequires: valgrind-devel
%endif

# to be able to generate configure if not present
BuildRequires: autoconf, automake, libtool

%ifarch x86_64
%if 0%{?suse_version} >= 01315 || 0%{?rhel} >= 7
%global configopts --enable-sockets --enable-verbs --enable-usnic --disable-static --enable-psm2 --disable-efa
%else
%global configopts --enable-sockets --enable-verbs --enable-usnic --disable-static --disable-efa
%endif
%else
%global configopts --enable-sockets --enable-verbs --enable-usnic --disable-static
%endif

%description
libfabric provides a user-space API to access high-performance fabric
services, such as RDMA.

%if 0%{?suse_version} >= 01315
%package -n %{suse_libname}
Summary: Shared library for libfabric
Group:  System/Libraries

%description -n %{suse_libname}
libfabric provides a user-space API to access high-performance fabric
services, such as RDMA. This package contains the runtime library.
%endif

%package devel
Summary: Development files for the libfabric library
%if 0%{?suse_version} >= 01315
Group: Development/Libraries/C and C++
Requires: %{suse_libname}%{?_isa} = %{version}-%{release}
%else
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
%endif
Requires: libpsm2-devel >= 11.2.78

%description devel
Development files for the libfabric library.

%prep
%autosetup %autosetup_args

%build
if [ ! -f configure ]; then
    ./autogen.sh
fi
# defaults: with-dlopen can be over-rode:
%configure %{?_without_dlopen} %{configopts} \
%ifnarch s390
        --with-valgrind
%endif
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags} V=1

%install
%make_install
# remove unpackaged files from the buildroot
rm -f %{buildroot}%{_libdir}/*.la
%fdupes %{buildroot}/%{_prefix}

%if 0%{?suse_version} >= 01315
%post -n %{suse_libname} -p /sbin/ldconfig
%postun -n %{suse_libname} -p /sbin/ldconfig
%else
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root,-)
%if 0%{?rhel} >= 7
%{_libdir}/libfabric.so.*
%endif
%{_bindir}/fi_info
%{_bindir}/fi_pingpong
%{_bindir}/fi_strerror
%if 0%{?rhel} >= 7
%{_libdir}/pkgconfig/%{name}.pc
%endif
%{_mandir}/man1/*
%doc NEWS.md
%license COPYING

%if 0%{?suse_version} >= 01315
%files -n %{suse_libname}
%defattr(-,root,root)
%{_libdir}/libfabric.so.*
%license COPYING
%doc AUTHORS README
%endif

%files devel
%defattr(-,root,root)
%{_libdir}/libfabric.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/*
%{_mandir}/man3/*
%{_mandir}/man7/*

%changelog
* Tue Feb 16 2021 Alexander Oganezov <alexander.a.oganezov@intel.com> - 1.12.0~rc1-1
- Update to v1.12.0rc1

* Tue Nov 24 2020 Brian J. Murrell <brian.murrell@intel.com> - 1.11.1-1
- Update to 1.11.1 GA
- Make the use of %%{dl_verison} more automatic

* Thu Oct 15 2020 Alexander Oganezov <alexander.a.oganezov@intel.com> - 1.11.1~rc1-2
- Fix to include DL_VERSION in Makefile

* Fri Oct 9 2020 Alexander Oganezov <alexander.a.oganezov@intel.com> - 1.11.1~rc1-1
- Update to libfabric v1.11.1rc1

* Thu Oct 1 2020 Alexander Oganezov <alexander.a.oganezov@intel.com> - 1.11.0-2
- Disable EFA provider

* Mon Sep 14 2020 Alexander Oganezov <alexander.a.oganezov@intel.com> - 1.11.0-1
- Update to libfabric v1.11.0

* Thu Aug 20 2020 Li Wei <wei.g.li@intel.com> - 1.9.0-8
- Update sockets_provider.patch to report the original connect errors

* Wed Jul 1 2020 Alexander Oganezov <alexander.a.oganezov@intel.com> - 1.9.0-7
- Commented out infinipath from BuildRequires
- Removed --enable-psm from configuration flags

* Mon May 18 2020 Alexander Oganezov <alexander.a.oganezov@intel.com> - 1.9.0-6
- update to 8fa7c5bbbfee7df5194b65d9294929a893eb4093
- apply custom patch for sockets provider

* Wed Mar 25 2020 Alexander Oganezov <alexander.a.oganezov@intel.com> - 1.9.0-5
- update to 62f6c937601776dac8a1f97c8bb1b1a6acfbc3c0

* Tue Mar 17 2020 Alexander Oganezov <alexander.a.oganezov@intel.com> - 1.9.0-4
- update to 15ce5c62e2f87715b32bc546d33bb132b97aea4c

* Fri Mar 6 2020 Alexander Oganezov <alexander.a.oganezov@intel.com> - 1.9.0-3
- update to 8af3c112bfce155eb04218bef656f58f3609ce19

* Thu Feb 6 2020 Alexander Oganezov <alexander.a.oganezov@intel.com> - 1.9.0-2
- update to 955f3a07dd011fb1dbfa6b6c772ada03d5af320e to pick configure.ac fix

* Wed Feb 5 2020 Brian J. Murrell <brian.murrell@intel.com> - 1.9.0-1
- Update to 1b8ed7876204692fd95b07df8cba21683707e5dc

* Sat Nov 9 2019 Alexander Oganezov <alexander.a.oganezov@intel.com> - 1.8.0-6
- Update to 863407

* Wed Sep 25 2019 Brian J. Murrell <brian.murrell@intel.com> - 1.8.0-5
- Update BR: for psm2 to 11.2.78
- Accordingly, devel subpackage should Requires: psm2-devel

* Mon Sep 23 2019 Brian J. Murrell <brian.murrell@intel.com> - 1.8.0-4
- %setup -> %autosetup
- Add patch to bring up to 3712eb0
- Set _default_patch_fuzz 1 due to GitHub's dirty compare/ patches
- Once again create the libfabric1 subpackage for SLES

* Thu Aug 22 2019 Brian J. Murrell <brian.murrell@intel.com> - 1.8.0-3
- Revert previous change as it was causing (on SLES 12.3):
/usr/lib64/libfabric.so.1: undefined reference to `psm2_epaddr_to_epid@PSM2_1.0'
/usr/lib64/libfabric.so.1: undefined reference to `psm2_ep_disconnect2@PSM2_1.0'
/usr/lib64/libfabric.so.1: undefined reference to `psm2_am_register_handlers_2@PSM2_1.0'
/usr/lib64/libfabric.so.1: undefined reference to `psm2_info_query@PSM2_1.0'
/usr/lib64/libfabric.so.1: undefined reference to `psm2_get_capability_mask@PSM2_1.0'
/usr/lib64/libfabric.so.1: undefined reference to `psm2_ep_epid_lookup2@PSM2_1.0'

* Tue Aug 20 2019 Brian J. Murrell <brian.murrell@intel.com> - 1.8.0-2
- Install libnl3-devel on all platforms
- Create a libfabric1 subpackage with the shared library
- Clean up much of SUSE's post build linting errors/warnings

* Thu Jul 25 2019 Alexander A. Oganezov <alexnader.a.oganezov@intel.com> - 1.8.0-1
- Update to 1.8.0

* Wed Jun 26 2019 Brian J. Murrell <brian.murrell@intel.com> - 1.7.1rc1-4
- Add BuildRequires: libpsm2-devel >= 10.3.58
  - needed for psm2_am_register_handlers_2@PSM2_1.0

* Tue May 14 2019 Brian J. Murrell <brian.murrell@intel.com> - 1.7.1rc1-3
- Fix SLES 12.3 OS conditionals >= 1315

* Wed May 01 2019 Brian J. Murrell <brian.murrell@intel.com> - 1.7.1rc1-2
- Disable psm2 on SLES 12.3 as the psm2 library there is too old

* Tue Mar 19 2019 Brian J. Murrell <brian.murrell@intel.com> - 1.7.1rc1-1
- Update to 1.7.1 RC1

* Mon Mar 11 2019 Brian J. Murrell <brian.murrell@intel.com> - 1.7.0rc3-1
- Rebase to latest release 1.7.0rc3

* Wed Aug 15 2018 Brian J. Murrell <brian.murrell@intel.com> - 1.6.0-1
- Rebase to latest release 1.6.0
- Remove obsolete patch
- Strip out local libtool Rpathing per
  https://fedoraproject.org/wiki/RPath_Packaging_Draft#Removing_Rpath

* Wed Jan 10 2018 Honggang Li <honli@redhat.com> - 1.5.3-1
- Rebase to latest release 1.5.3
- Resolves: bz1533293

* Thu Jan  4 2018 Honggang Li <honli@redhat.com> - 1.5.1-3
- Add support of different CQ formats for the verbs/RDM
- Resolves: bz1530715

* Fri Oct 20 2017 Honggang Li <honli@redhat.com> - 1.5.1-2
- Fix PPC32 compiling issue
- Resolves: bz1504395

* Tue Oct 17 2017 Honggang Li <honli@redhat.com> - 1.5.1-1
- Rebase to v1.5.1
- Resolves: bz1452791

* Tue May 16 2017 Honggang Li <honli@redhat.com> - 1.4.2-1
- Update to upstream v1.4.2 release
- Related: bz1451100

* Wed Mar 01 2017 Jarod Wilson <jarod@redhat.com> - 1.4.1-1
- Update to upstream v1.4.1 release
- Related: bz1382827

* Mon May 30 2016 Honggang Li <honli@redhat.com> - 1.3.0-3
- Rebuild against latest infinipath-psm.
- Related: bz1280143

* Mon May 30 2016 Honggang Li <honli@redhat.com> - 1.3.0-2
- Rebuild libfabric to support Intel OPA PSM2.
- Related: bz1280143

* Wed May  4 2016 Honggang Li <honli@redhat.com> - 1.3.0-1
- Update to latest upstream release
- Related: bz1280143

* Wed Sep 30 2015 Doug Ledford <dledford@redhat.com> - 1.1.0-2
- Rebuild against libnl3 now that the UD RoCE bug is fixed
- Related: bz1261028

* Fri Aug 14 2015 Honggang Li <honli@redhat.com> - 1.1.0-1
- Rebase to upstream 1.1.0
- Resolves: bz1253381

* Fri Aug 07 2015 Michal Schmidt <mschmidt@redhat.com> - 1.1.0-0.2.rc4
- Packaging Guidelines conformance fixes and spec file cleanups
- Related: bz1235266

* Thu Aug  6 2015 Honggang Li <honli@redhat.com> - 1.1.0-0.1.rc4
- fix N-V-R issue and disable static library
- Related: bz1235266

* Tue Aug  4 2015 Honggang Li <honli@redhat.com> - 1.1.0rc4
- Initial build for RHEL-7.2
- Related: bz1235266

* Fri Jun 26 2015 Open Fabrics Interfaces Working Group <ofiwg@lists.openfabrics.org> 1.1.0rc1
- Release 1.1.0rc1

* Sun May 3 2015 Open Fabrics Interfaces Working Group <ofiwg@lists.openfabrics.org> 1.0.0
- Release 1.0.0
