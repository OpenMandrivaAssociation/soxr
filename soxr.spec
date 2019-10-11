%define major 0
%define libname %mklibname %{name} %{major}
%define liblsr %mklibname %{name}-lsr %{major}
%define devname %mklibname %{name} -d
%define devlsr %mklibname %{name}-lsr -d

%global optflags %{optflags} -O3

Summary:	The SoX Resampler library
Name:		soxr
Version:	0.1.3
Release:	4
License:	LGPLv2+
Group:		Sound
Url:		https://sourceforge.net/p/soxr/wiki/Home/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}-Source.tar.xz
BuildRequires:	cmake
BuildRequires:	pkgconfig(libavutil)
BuildRequires:	pkgconfig(libavcodec)

%description
The SoX Resampler library libsoxr performs one-dimensional sample-rate
conversion -- it may be used, for example, to resample PCM-encoded audio.

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	The SoX Resampler shared library
Group:		System/Libraries

%description -n %{libname}
The SoX Resampler shared library.

It's high quality, one-dimensional sample-rate conversion library.

%files -n %{libname}
%doc LICENCE NEWS README
%{_libdir}/libsoxr.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
This package contains libraries and header files for developing applications
that use %{name}.

It's high quality, one-dimensional sample-rate conversion library.

%files -n %{devname}
%{_includedir}/soxr.h
%{_libdir}/libsoxr.so
%{_libdir}/pkgconfig/soxr.pc

#----------------------------------------------------------------------------

%package -n %{liblsr}
Summary:	The SoX Resampler shared library
Group:		System/Libraries

%description -n %{liblsr}
The SoX Resampler shared library.

It's high quality, one-dimensional sample-rate conversion library
(with libsamplerate-like bindings).

%files -n %{liblsr}
%doc LICENCE NEWS README
%{_libdir}/libsoxr-lsr.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devlsr}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{liblsr} = %{EVRD}

%description -n %{devlsr}
This package contains libraries and header files for developing applications
that use %{name}.

It's high quality, one-dimensional sample-rate conversion library
(with libsamplerate-like bindings).

%files -n %{devlsr}
%{_includedir}/soxr-lsr.h
%{_libdir}/libsoxr-lsr.so
%{_libdir}/pkgconfig/soxr-lsr.pc

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}-Source

%build
%cmake -DCMAKE_BUILD_TYPE='Release' \
    -DLIB_INSTALL_DIR="%{_libdir}" \
    -DBUILD_EXAMPLES='OFF' \
    -DBUILD_SHARED_LIBS='ON' \
    -DWITH_AVFFT='ON' \
    -DWITH_LSR_BINDINGS='ON' \
    -DWITH_OPENMP='ON' \
    -DWITH_PFFFT='ON'

%make_build

%install
%make_install -C build

# Remove docs and use the rpmbuild macro instead
rm -rf %{buildroot}%{_docdir}/*

# fix pc file
sed -i -e "s/-L%{_lib}//g" %{buildroot}%{_libdir}/pkgconfig/*.pc
