Name:       sdcard-utils
Summary:    SailfishOS scripts to mount/umount external sdcard.
Version:    0.1
Release:    1
Group:      System/Base
License:    MIT
BuildArch:  noarch
URL:        https://github.com/jvihrial/sdcard-utils/
Source0:    %{name}-%{version}.tar.bz2
BuildRequires:   oneshot
Requires(post):  oneshot

%description
%{summary}

%prep
%setup -q -n %{name}-%{version}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sbindir}
cp -r scripts/mount-sd.sh %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_bindir}
cp -r scripts/tracker-sd-indexing.sh %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d
cp -r rules/90-mount-sd.rules %{buildroot}%{_sysconfdir}/udev/rules.d/
mkdir -p %{buildroot}%{_oneshotdir}
cp -r oneshot/add-mmcblk1.sh %{buildroot}%{_oneshotdir}
mkdir -p %{buildroot}/usr/lib/systemd/user/pre-user-session.target.wants
cp -r systemd/* %{buildroot}/usr/lib/systemd/user/
ln -sf ../tracker-sd-indexing.path %{buildroot}/usr/lib/systemd/user/pre-user-session.target.wants/tracker-sd-indexing.path

%post
add-oneshot --now add-mmcblk1.sh

%files
%defattr(-,root,root,-)
%{_sbindir}/mount-sd.sh
%{_bindir}/tracker-sd-indexing.sh
%{_oneshotdir}/add-mmcblk1.sh
%{_sysconfdir}/udev/rules.d/90-mount-sd.rules
%{_libdir}/systemd/user/*

