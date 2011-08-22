# --with-tcl enables sqlite-tcl subpackage, and also makes %%check possible.
%define tcl 0%{?_with_tcl:1}
# --with static enables static library in -devel subpackage
%define static 0%{?_with_static:1}

Summary: Library that implements an embeddable SQL database engine
Name: sqlite
Version: 3.7.3
Release: 0
License: Public Domain
Group:  Applications/Databases
URL: http://www.sqlite.org/
Source: http://www.sqlite.org/sqlite-amalgamation-%{version}.tar.gz
Obsoletes: sqlite3 sqlite3-devel
BuildRequires: ncurses-devel readline-devel
BuildRequires: /usr/bin/tclsh
%if %{tcl}
BuildRequires: tcl-devel
%endif
BuildRoot: %{_tmppath}/%{name}-root

%description
SQLite is a C library that implements an SQL database engine. A large
subset of SQL92 is supported. A complete database is stored in a
single disk file. The API is designed for convenience and ease of use.
Applications that link against SQLite can enjoy the power and
flexibility of an SQL database without the administrative hassles of
supporting a separate database server.  Version 2 and version 3 binaries
are named to permit each to be installed on a single host

%package devel
Summary: Development tools for the sqlite3 embeddable SQL database engine.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%if %{tcl}
%package tcl
Summary: Tcl module for the sqlite3 embeddable SQL database engine.
Group: Development/Languages
Requires: %{name} = %{version}-%{release}

%description tcl
This package contains the tcl modules for %{name}.
%endif

%prep
%setup -q
#%patch0 -p1 -b .opcode

%build
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%configure --enable-threadsafe
make %{?_smp_mflags}
#make doc

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=${RPM_BUILD_ROOT} install

%{__install} -D -m0644 sqlite3.1 %{buildroot}%{_mandir}/man1/sqlite3.1

%if ! %{static}
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.{la,a}
%endif

%if %{tcl}
%check
make test
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc README
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man?/*

%files devel
%defattr(-, root, root)
#%doc doc/
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%if %{static}
%{_libdir}/*.a
%exclude %{_libdir}/*.la
%endif
%if %{tcl}
%files tcl
%defattr(-, root, root)
%{_datadir}/tcl*/sqlite3
%endif
