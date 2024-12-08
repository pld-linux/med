Summary:	Library to exchange meshed data
Name:		med
Version:	5.0.0
Release:	1
License:	LGPL 3.0 / GPL v3
Source0:	https://files.salome-platform.org/Salome/medfile/%{name}-%{version}.tar.bz2
# Source0-md5:	3c5ae8a37d7971658870b77caad1d73b
URL:		https://www.salome-platform.org/
Patch0:		%{name}_cmake.patch
Patch1:		%{name}-py3.13.patch
Patch2:		hdf5-1.14.patch
Patch3:		%{name}-swig-4.3.0.patch
BuildRequires:	cmake
BuildRequires:	gcc-fortran
BuildRequires:	hdf5-devel >= 1.12.1
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	python3-devel
BuildRequires:	swig
BuildRequires:	zlib-devel

%description
MED-fichier (Modélisation et Echanges de Données, in English
Modelisation and Data Exchange) is a library to store and exchange
meshed data or computation results. It uses the HDF5 file format to
store the data.

%package -n python3-%{name}
Summary:	Python3 bindings for %{name}
Requires:	%{name} = %{version}-%{release}

%description -n python3-%{name}
The python3-%{name} package contains python3 bindings for %{name}.

%package tools
Summary:	Runtime tools for %{name}
Requires:	%{name} = %{version}-%{release}
Requires:	tk

%description tools
This package contains runtime tools for %{name}:
- mdump: a tool to dump MED files
- xmdump: graphical version of mdump.
- medconforme: a tool to validate a MED file
- medimport: a tool to convert a MED v2.1 or v2.2 file into a MED v2.3
  file

%package devel
Summary:	Development files for %{name}
Requires:	%{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package doc
Summary:	Documentation for %{name}
BuildArch:	noarch

%description doc
Documentation for %{name}.

%prep
%setup -q
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1
%patch -P 3 -p1

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+wish(\s|$),#!/usr/bin/wish\1,' \
	tools/mdump/xmdump*.in

%build
mkdir -p build
cd build
%cmake ../ \
	-DMEDFILE_BUILD_PYTHON=1 \
	-DPYTHON_EXECUTABLE=%{__python3} \
	-DPYTHON_INCLUDE_DIR=%{py3_incdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# Remove test-suite files
%{__rm} -r $RPM_BUILD_ROOT%{_bindir}/{testc,testf,testpy}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README COPYING.LESSER
%{_libdir}/libmed.so.1*
%{_libdir}/libmedC.so.1*
%{_libdir}/libmedimport.so.0*
%{_libdir}/libmedfwrap.so.11*

%files -n python3-%{name}
%defattr(644,root,root,755)
%{py3_sitedir}/%{name}/

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*mdump*
%attr(755,root,root) %{_bindir}/medconforme
%attr(755,root,root) %{_bindir}/medimport

%files devel
%defattr(644,root,root,755)
%{_libdir}/*.so
%{_libdir}/cmake/MEDFile/
%{_includedir}/%{name}/

%files doc
%defattr(644,root,root,755)
%doc %{_docdir}
