%global debug_package %{nil}
# soxr is used by pulseaudio, pulseaudio is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define major 0
%define libname %mklibname %{name} %{major}
%define liblsr %mklibname %{name}-lsr %{major}
%define devname %mklibname %{name} -d
%define devlsr %mklibname %{name}-lsr -d
%define lib32name %mklib32name %{name} %{major}
%define lib32lsr %mklib32name %{name}-lsr %{major}
%define dev32name %mklib32name %{name} -d
%define dev32lsr %mklib32name %{name}-lsr -d

%global optflags %{optflags} -O3

Summary:	The SoX Resampler library
Name:		soxr
Version:	0.1.3
Release:	11
License:	LGPLv2+
Group:		Sound
Url:		https://sourceforge.net/p/soxr/wiki/Home/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}-Source.tar.xz
Patch0:		0001-always-generate-.pc.patch
Patch1:		0003-add-aarch64-support.patch
Patch2:		0004-arm-fix-SIGILL-when-doing-divisions-on-some-old-arch.patch
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	pkgconfig(libavutil)
BuildRequires:	pkgconfig(libavcodec)
%if %{with compat32}
BuildRequires:	libc6
%endif

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
%if %{with compat32}
%package -n %{lib32name}
Summary:	The SoX Resampler shared library (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
The SoX Resampler shared library.

It's high quality, one-dimensional sample-rate conversion library.

%files -n %{lib32name}
%{_prefix}/lib/libsoxr.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{dev32name}
Summary:	Development files for %{name} (32-bit)
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Requires:	%{lib32name} = %{EVRD}

%description -n %{dev32name}
This package contains libraries and header files for developing applications
that use %{name}.

It's high quality, one-dimensional sample-rate conversion library.

%files -n %{dev32name}
%{_prefix}/lib/libsoxr.so
%{_prefix}/lib/pkgconfig/soxr.pc

#----------------------------------------------------------------------------

%package -n %{lib32lsr}
Summary:	The SoX Resampler shared library (32-bit)
Group:		System/Libraries

%description -n %{lib32lsr}
The SoX Resampler shared library.

It's high quality, one-dimensional sample-rate conversion library
(with libsamplerate-like bindings).

%files -n %{lib32lsr}
%{_prefix}/lib/libsoxr-lsr.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{dev32lsr}
Summary:	Development files for %{name} (32-bit)
Group:		Development/C
Requires:	%{lib32lsr} = %{EVRD}
Requires:	%{devlsr} = %{EVRD}

%description -n %{dev32lsr}
This package contains libraries and header files for developing applications
that use %{name}.

It's high quality, one-dimensional sample-rate conversion library
(with libsamplerate-like bindings).

%files -n %{dev32lsr}
%{_prefix}/lib/libsoxr-lsr.so
%{_prefix}/lib/pkgconfig/soxr-lsr.pc
%endif

%prep
%autosetup -p1 -n %{name}-%{version}-Source
%if %{with compat32}
%cmake32 -DCMAKE_BUILD_TYPE='Release' \
	-DCMAKE_VERBOSE_BUILD:BOOL=ON \
	-DLIB_INSTALL_DIR="%{_prefix}/lib" \
	-DBUILD_EXAMPLES='OFF' \
	-DBUILD_SHARED_LIBS='ON' \
	-DWITH_AVFFT='OFF' \
	-DWITH_LSR_BINDINGS='ON' \
	-DWITH_OPENMP='ON' \
	-DWITH_PFFFT='ON' \
	-G Ninja
cd ..
%endif
%cmake -DCMAKE_BUILD_TYPE='Release' \
	-DLIB_INSTALL_DIR="%{_libdir}" \
	-DBUILD_EXAMPLES='OFF' \
	-DBUILD_SHARED_LIBS='ON' \
	-DWITH_AVFFT='ON' \
	-DWITH_LSR_BINDINGS='ON' \
	-DWITH_OPENMP='ON' \
	-DWITH_PFFFT='ON' \
	-G Ninja

%build
%if %{with compat32}
export LD_LIBRARY_PATH="$(pwd)/build32/src"
%ninja_build -C build32
%endif
export LD_LIBRARY_PATH="$(pwd)/build/src"
%ninja_build -C build

%install
%if %{with compat32}
%ninja_install -C build32
%endif
%ninja_install -C build

# Remove docs and use the rpmbuild macro instead
rm -rf %{buildroot}%{_docdir}/*

# fix pc file
sed -i -e "s/-L%{_lib}//g" %{buildroot}%{_libdir}/pkgconfig/*.pc
