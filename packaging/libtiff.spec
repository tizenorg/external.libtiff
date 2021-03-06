Name:           libtiff
License:        PERMISSIVE-OSI-COMPLIANT ; MIT License (or similar)
Group:          Productivity/Graphics/Convertors
AutoReqProv:    on
Url:            http://www.remotesensing.org/libtiff/
Version:        3.9.4
Release:	5
Summary:        Tools for Converting from and to the Tiff  Format
Source:        %{name}-%{version}.tar.gz

%description
This package contains the library and support programs for the TIFF
image format.

%package devel
License:        PERMISSIVE-OSI-COMPLIANT
Summary:        Development Tools for Programs which will use the libtiff Library
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains the header files and static libraries for
developing programs which will manipulate TIFF format image files using
the libtiff library.


%prep
%setup -q

%build
rm m4/ltversion.m4 m4/ltsugar.m4 m4/ltoptions.m4 m4/libtool.m4
autoreconf --force --install -v
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -fstack-protector" \
  ./configure --prefix=/usr/ --mandir=%{_mandir} --libdir=%{_libdir} --disable-static
make %{?_smp_mflags}

%install
mkdir -p $RPM_BUILD_ROOT/{%{_mandir}/{man1,man3},usr/{bin,lib,include}}
make install DESTDIR=$RPM_BUILD_ROOT
for f in `find $RPM_BUILD_ROOT/%{_mandir} -type f -print ` ; do
  if [ `wc -l <$f` -eq 1 ] && grep -q "^\.so " $f ; then
    linkto=`sed -e "s|^\.so ||" $f`
    [ -f "`dirname $f`/$linkto" ] && ln -sf "$linkto" $f
  fi
done
rm -rf $RPM_BUILD_ROOT/usr/share/doc/tiff*
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
find html -name "Makefile*" | xargs rm


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
#%{_bindir}/* for progs
%{_libdir}/libtiff.so.*
%{_libdir}/libtiffxx.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/tiffconf.h
%{_includedir}/tiffio.hxx
%{_includedir}/tiffvers.h
%{_includedir}/tiffio.h
%{_includedir}/tiff.h
%{_libdir}/libtiff.so
%{_libdir}/libtiffxx.so
%{_mandir}/man3/*
