Name: libfabric
Version: 1.7.1rc1
Release: 1%{?dist}
Summary: User-space RDMA Fabric Interfaces
Group: System Environment/Libraries
License: GPLv2 or BSD
Url: https://www.github.com/ofiwg/libfabric
Source: https://github.com/ofiwg/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: librdmacm-devel
BuildRequires: libibverbs-devel >= 1.2.0
BuildRequires: libnl3-devel

# infinipath-psm-devel only available for x86_64
%ifarch x86_64
BuildRequires: infinipath-psm-devel
BuildRequires: libpsm2-devel
%endif
# valgrind is unavailable for s390
%ifnarch s390
BuildRequires: valgrind-devel
%endif

# to be able to generate configure if not present
BuildRequires: autoconf, automake, libtool

%ifarch x86_64
%global configopts --enable-sockets --enable-verbs --enable-usnic --disable-static --enable-psm --enable-psm2
%else
%global configopts --enable-sockets --enable-verbs --enable-usnic --disable-static
%endif

%description
libfabric provides a user-space API to access high-performance fabric
services, such as RDMA.

%package devel
Summary: Development files for the libfabric library
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for the libfabric library.

%prep
%setup -q

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

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/libfabric.so.*
%{_bindir}/fi_info
%{_bindir}/fi_pingpong
%{_bindir}/fi_strerror
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man1/*
%license COPYING
%doc AUTHORS README

%files devel
%{_libdir}/libfabric.so
%{_includedir}/*
%{_mandir}/man3/*
%{_mandir}/man7/*

%changelog
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
