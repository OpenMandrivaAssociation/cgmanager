%define major 0
%define libname %mklibname cgmanager %{major}
%define develname %mklibname cgmanager -d

Name:		cgmanager
Version:	0.41
Release:	2
Summary:	CGroup manager for LXC containers
URL:		http://linuxcontainers.org/cgmanager/
Source0:	http://linuxcontainers.org/downloads/cgmanager/%{name}-%{version}.tar.gz
Patch0:		cgmanager-0.41-fix-systemd-services.patch
Group:		System/Kernel and hardware
License:	LGPLv2.1+, parts GPLv2
BuildRequires:	docbook-utils
BuildRequires:  kernel-headers
BuildRequires:	cap-devel
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(libnih)
BuildRequires:	pkgconfig(libnih-dbus)
Buildrequires:	docbook-dtd30-sgml
Buildrequires:	docbook2x
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pam-devel

%description
CGManager is a central privileged daemon that manages all your cgroups for you
through a simple D-Bus API. It's designed to work with nested LXC containers
as well as accepting unprivileged requests including resolving user namespaces
UIDs/GIDs.

%package -n	%{libname}
Summary:	Library for LXC
Group:		System/Libraries

%description -n %{libname}
Library for the Linux Kernel Containers.

%package -n	%{develname}
Summary:	Development files for LXC
Group:		Development/C
Requires:	%{libname} = %{EVRD}

%description -n %{develname}
Developement files for the Linux Kernel Containers.

%prep
%setup -q
%apply_patches

# Clang spews a few more warnings than gcc...
sed -i -e 's,-Werror,,g' configure*

autoreconf -fi

%build
%configure \
		--with-init-script=systemd

# remove rpath ( rpmlint error )
# sed -i '/AM_LDFLAGS = -Wl,-E -Wl,-rpath -Wl,$(libdir)/d' src/lxc/Makefile.in
%make

%install
%makeinstall_std

%files
/%{_lib}/security/pam_cgm.so
%{_libexecdir}/cgmanager
%{_prefix}/lib/systemd/system/*.service
%{_datadir}/cgmanager
%{_mandir}/man*/*
%{_bindir}/cgm
%{_sbindir}/cgmanager
%{_sbindir}/cgproxy

%files -n %{libname}
%{_libdir}/libcgmanager.so.%{major}*

%files -n %{develname}
%{_libdir}/libcgmanager.so
%{_includedir}/cgmanager
%{_libdir}/pkgconfig/*.pc
