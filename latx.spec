%global debug_package %{nil}

Name: latx
Summary: LoongArch Architecture Translator for x86
Version: 1.6.6
Release: 1%{?dist}
License: GPL2
URL: https://github.com/lat-opensource/lat
Source0: https://github.com/lat-opensource/lat/archive/refs/tags/%{version}.tar.gz

BuildRequires: gcc g++ make git ninja-build meson
BuildRequires: openssl-devel
BuildRequires: glib2-devel

Obsoletes: qemu-user-static-x86 < 0

# box64 only supports loongarch architectures
ExclusiveArch:  loongarch64

%description
LoongArch Architecture Translator for x86.


%prep
%autosetup -n lat-%{version} -S git_am

%build
mkdir -p build-x86_64
pushd build-x86_64
../configure \
	--prefix="%{_prefix}" \
	--libdir="%{_libdir}" \
	--datadir="%{_datadir}" \
	--sysconfdir="%{_sysconfdir}" \
	--localstatedir="%{_localstatedir}" \
	--docdir="%{_docdir}" \
	--libexecdir="%{_libexecdir}" \
	--target-list=x86_64-linux-user \
	--enable-latx \
	--optimize-O1 \
	--enable-kzt \
	--disable-docs \
	--disable-werror

%ninja_build
popd

mkdir -p build-i386
pushd build-i386
                
../configure \
	--prefix="%{_prefix}" \
	--libdir="%{_libdir}" \
	--datadir="%{_datadir}" \
	--sysconfdir="%{_sysconfdir}" \
	--localstatedir="%{_localstatedir}" \
	--docdir="%{_docdir}" \
	--libexecdir="%{_libexecdir}" \
	--target-list=i386-linux-user \
	--enable-latx \
	--optimize-O1 \
	--enable-guest-base-zero \
	--disable-docs \
	--disable-werror \
	--disable-pie

%ninja_build
popd
%install

mkdir -p %{buildroot}/etc/binfmt.d/
pushd build-x86_64
%ninja_install
echo ":latx-x86_64:M::\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x3e\x00:\xff\xff\xff\xff\xff\xfe\xfe\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff:/usr/bin/latx-x86_64:" > %{buildroot}/etc/binfmt.d/latx-x86_64.conf
popd

pushd build-i386
%ninja_install
echo ":latx-i386:M::\x7fELF\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x03\x00:\xff\xff\xff\xff\xff\xfe\xfe\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff:/usr/bin/latx-i386:" > %{buildroot}/etc/binfmt.d/latx-i386.conf
popd

%post
/bin/systemctl --system restart systemd-binfmt.service &>/dev/null || :
%postun
/bin/systemctl --system restart systemd-binfmt.service &>/dev/null || :

%files
%{_bindir}/latx-x86_64
%{_bindir}/latx-i386
%{_sysconfdir}/binfmt.d/latx-x86_64.conf
%{_sysconfdir}/binfmt.d/latx-i386.conf

%changelog
* Wed Jun  3 2026 Sun Haiyong <sunhaiyong@zdbr.net> - 1.6.6-1
- Initial latx spec.
