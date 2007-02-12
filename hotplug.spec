# TODO
# - define _libdir as /lib for all arch?
Summary:	Linux Hotplug Scripts
Summary(pl.UTF-8):   Linuksowe skrypty do urządzeń hotplug
Name:		hotplug
Version:	2004_09_23
Release:	8
License:	GPL
Group:		Applications/System
Source0:	ftp://ftp.kernel.org/pub/linux/utils/kernel/hotplug/%{name}-%{version}.tar.bz2
# Source0-md5:	58e6995f9df71ce59b0ec2787019e5fe
Source1:	%{name}.init
Source2:	%{name}-update-usb.usermap
Source3:	%{name}-update-usb.usermap.8
Source4:	%{name}-digicam
Patch0:		%{name}-PLD.patch
Patch1:		%{name}-ifup.patch
Patch2:		%{name}-devlabel.patch
Patch3:		%{name}-sh_shift9.patch
URL:		http://linux-hotplug.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	/sbin/chkconfig
Requires:	awk
Requires:	bash
Requires:	rc-scripts
Requires:	sed
# Requires wc
Requires:	textutils
Requires:	usbutils
# it is _not_ noarch as it contains %{_libdir}/hotplug directory
#BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_exec_prefix	/
%define		_libdir			/%{_lib}
%define		_sbindir		/sbin
%define		_gphoto_lib		/usr/%{_lib}/libgphoto2

%description
This package contains the scripts necessary for hotplug Linux support.

%description -l pl.UTF-8
Ten pakiet zawiera skrypty potrzebne do obsługi urządzeń hotplug
(podłączanych w czasie pracy) pod Linuksem.

%package pci
Summary:	Hotplug pci module
Summary(pl.UTF-8):   Moduł pci do hotpluga
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description pci
This is mostly to recover lost boot-time PCI hotplug events. Should
handle 2.4.x and 2.6.x PCI (including Cardbus) hotplugging, with a
consistent framework for adding device and driver specific treatments.

%description pci -l pl.UTF-8
Ten moduł służy głównie do odzyskiwania zdarzeń hotplug PCI utraconych
w czasie startu systemu. Powinien obsługiwać podłączanie urządzeń PCI
(włącznie z Cardbus) dla jąder 2.4.x i 2.6.x ze spójnym szkieletem do
dodawania urządzeń i zachowań specyficznych dla sterownika.

%package input
Summary:	Hotplug input module
Summary(pl.UTF-8):   Moduł input do hotpluga
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description input
This loads handlers for those input devices that have drivers compiled
in kernel. Currently stopping is not supported. Should handle 2.6.x
input hotplugging, with a consistent framework for adding device and
driver specific handling.

%description input -l pl.UTF-8
Ten moduł wczytuje programy obsługujące te urządzenia wejściowe, dla
których sterowniki zostały wkompilowane w jądro. Aktualnie wyłączanie
nie jest obsługiwane. Powinien obsługiwać podłączanie urządzeń
wejściowych dla jąder 2.6.x ze spójnym szkieletem do dodawania
urządzeń i obsługą rzeczy specyficznych dla sterownika.

%package isapnp
Summary:	Hotplug isapnp module
Summary(pl.UTF-8):   Moduł isapnp do hotpluga
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description isapnp
This module supports PnP ISA cards. Stopping is not supported.

%description isapnp -l pl.UTF-8
Ten moduł obsługuje karty PnP ISA. Wyłączanie urządzeń nie jest
obsługiwane.

%package digicam
Summary:	Hotplug definitions for USB digital cameras
Summary(pl.UTF-8):   Definicje Hotpluga dla aparatów cyfrowych na USB
Group:		Applications/System
Requires(post):	grep
Requires(post,postun):	fileutils
Requires(post,postun):	sed >= 4.0
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires:	%{name} = %{version}-%{release}
Requires:	libgphoto2
Requires:	util-linux
Provides:	group(digicam)
Obsoletes:	udev-digicam

%description digicam
This creates appropriate definitions to usb.usermap for digital
cameras based on output of libgphoto2.

%description digicam -l pl.UTF-8
Ten moduł dodaje definicje dla aparatów cyfrowych opierając się na
danych z libgphoto2.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_sbindir},%{_sysconfdir}/hotplug,/etc/rc.d/init.d,%{_mandir}/man8}

%{__make} install \
	prefix=$RPM_BUILD_ROOT

install etc/hotplug/{dasd.permissions,pnp.distmap,tape.permissions} $RPM_BUILD_ROOT%{_sysconfdir}/hotplug/

install %{SOURCE2} $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE3} $RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/hotplug
ln -s %{_sysconfdir}/hotplug.d $RPM_BUILD_ROOT%{_libdir}/%{name}
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/hotplug/usb/digicam

%clean
rm -rf $RPM_BUILD_ROOT

# NOTE: don't restart hotplug on upgrade (not needed and does evil things
# like reconfiguring hotplug-driven devices, disabling network connections
# etc.)

%post
/sbin/chkconfig --add hotplug

%preun
if [ "$1" = "0" ] ; then
	%service hotplug stop
	/sbin/chkconfig --del hotplug
fi

%pre digicam
%groupadd -P %{name}-digicam -g 135 digicam

%post digicam
if [ "$1" = "1" ]; then
	usermap="%{_sysconfdir}/hotplug/usb.usermap"
	if [ -f "$usermap" ]; then
		%{__sed} -i -e '/digicam/d' $usermap
		%{_gphoto_lib}/print-usb-usermap digicam | grep -v '#' >> "$usermap"
	else
		umask 022
		%{_gphoto_lib}/print-usb-usermap digicam | grep -v '#' > "$usermap"
	fi
fi

%postun digicam
if [ "$1" = "0" ]; then
	usermap="%{_sysconfdir}/hotplug/usb.usermap"
	if [ -f "$usermap" ]; then
		%{__sed} -i -e '/digicam/d' "$usermap"
	fi
	%groupremove digicam
fi

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
%dir %{_sysconfdir}/hotplug
%exclude %{_sysconfdir}/hotplug/pci.*
%exclude %{_sysconfdir}/hotplug/input.*
%exclude %{_sysconfdir}/hotplug/pnp.*
%{_sysconfdir}/hotplug/hotplug.functions
%attr(755,root,root) %{_sysconfdir}/hotplug/*.agent
%attr(755,root,root) %{_sysconfdir}/hotplug/*.rc
%dir %{_sysconfdir}/hotplug/usb
%exclude %{_sysconfdir}/hotplug/usb/digicam
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/hotplug/blacklist
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/hotplug/*map
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/hotplug/*.permissions
%dir %{_sysconfdir}/hotplug.d
%dir %{_sysconfdir}/hotplug.d/default
%attr(755,root,root) %{_sysconfdir}/hotplug.d/default/*.hotplug
%{_libdir}/hotplug
%{_mandir}/man8/*.8*
%dir /var/run/usb
%dir /var/log/hotplug

%files pci
%defattr(644,root,root,755)
%dir %{_sysconfdir}/hotplug/pci
%attr(755,root,root) %{_sysconfdir}/hotplug/pci.*

%files input
%defattr(644,root,root,755)
%attr(755,root,root) %{_sysconfdir}/hotplug/input.*

%files isapnp
%defattr(644,root,root,755)
%{_sysconfdir}/hotplug/pnp.*
%attr(755,root,root) %{_sysconfdir}/hotplug/pnp.rc

%files digicam
%defattr(644,root,root,755)
%attr(755,root,root) %{_sysconfdir}/hotplug/usb/digicam
