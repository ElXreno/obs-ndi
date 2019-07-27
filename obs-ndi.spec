Name:           obs-ndi
Version:        4.6.0
Release:        1%{?dist}
Summary:        Network A/V in OBS Studio with NewTek's NDI technology

License:        GPLv2
URL:            https://github.com/Palakis/obs-ndi
Source0:        https://github.com/Palakis/obs-ndi/archive/%{version}.tar.gz

ExclusiveArch:  i686 x86_64

BuildRequires:  gcc-c++
BuildRequires:  cmake3
BuildRequires:  cmake(Qt5Core)
BuildRequires:  pkgconfig(libobs)

Requires:       obs-studio
Requires:       libndi


%description
This plugin adds simple audio/video input and output over IP using
NewTek's NDI technology.

Three integrations are currently available:
- NDI Source: add NDI Sources into OBS like any traditional source
- NDI Output: transmit the main program view over NDI
- NDI Filter: a special OBS filter that outputs its parent OBS 
source to NDI (audio works only with video capture sources, media 
sources and VLC sources)


%prep
%autosetup -n %{name}-%{version}

# Correct cmake path
sed -i 's|/../cmake/external||' external/FindLibObs.cmake

# Correct libndi path for x86_64
%ifarch x86_64
    sed -i 's|/usr/lib|/usr/lib64|' src/obs-ndi.cpp
    sed -i 's|/usr/local/lib|/usr/local/lib64|' src/obs-ndi.cpp
%endif

%build
mkdir build
pushd build
    %cmake3 \
        -DLIBOBS_INCLUDE_DIR="%{_libdir}/cmake/LibObs" \
        -DLIBOBS_LIB="%{_libdir}/libobs.so.0" \
        ..
    %make_build
popd


%install
pushd build
    %make_install
popd

%ifarch x86_64
mkdir -p %{buildroot}%{_libdir}
mv -f %{buildroot}%{_prefix}/lib/obs-plugins %{buildroot}%{_libdir}/obs-plugins
%endif


%files
%license LICENSE
%doc README.md
%{_libdir}/obs-plugins/%{name}.so
%{_datadir}/obs/obs-plugins/obs-ndi


%changelog
* Tue Jul  9 2019 ElXreno <elxreno@gmail.com>
- Init
