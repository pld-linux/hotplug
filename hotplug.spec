Summary:	Linux Hotplug Scripts
Summary(pl):	Linuksowe skrypty do urz±dzeñ hotplug
Name:		hotplug
Version:	2004_04_01
Release:	1
Group:		Applications/System
License:	GPL
Source0:	ftp://ftp.kernel.org/pub/linux/utils/kernel/hotplug/%{name}-%{version}.tar.bz2
# Source0-md5:	527f0242481024c77255f3c1fa09e6ee
Source1:	%{name}.init
Source2:	%{name}-update-usb.usermap
Source3:	%{name}-update-usb.usermap.8
Patch0:		%{name}-PLD.patch
Patch1:		%{name}-ifup.patch
URL:		http://linux-hotplug.sourceforge.net/
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
# Requires wc
Requires:	textutils
Requires:	awk
Requires:	usbutils
Requires:	sed
Requires:	bash
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_exec_prefix	/

%description
This package contains the scripts necessary for hotplug Linux support.

%description -l pl
Ten pakiet zawiera skrypty potrzebne do obs³ugi urz±dzeñ hotplug
(pod³±czanych w czasie pracy) pod Linuksem.

%package pci
Summary:	Hotplug pci module
Summary(pl):	Modu³ pci do hotpluga
Group:		Applications/System
Requires:	%{name} = %{version}

%description pci
This is mostly to recover lost boot-time pci hotplug events. Should handle
2.4.* and 2.6.* PCI (including Cardbus) hotplugging, with a consistent
framework for adding device and driver specific treatments.

%package input
Summary:	Hotplug input module
Summary(pl):	Modu³ input do hotpluga
Group:		Applications/System
Requires:	%{name} = %{version}

%description input
This loads handlers for those input devices that have drivers compiled in
kernel. Currently stopping is not supported. Should handle 2.6.* input
hotplugging, with a consistent framework for adding device and driver
specific handling.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_sbindir},%{_sysconfdir}/hotplug,/etc/rc.d/init.d,%{_mandir}/man8}

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	etcdir=$RPM_BUILD_ROOT%{_sysconfdir} \
	sbindir=$RPM_BUILD_ROOT%{_sbindir} \
	mandir=$RPM_BUILD_ROOT%{_mandir}

install sbin/* %{SOURCE2} $RPM_BUILD_ROOT%{_sbindir}
install *.8 %{SOURCE3}  $RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/hotplug
ln -s %{_sysconfdir}/hotplug.d $RPM_BUILD_ROOT%{_libdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add hotplug
# Uncomment this out if we find that we need to restart the system when
# we have loaded a new copy of the package.
#if test -r /var/lock/subsys/hotplug ; then
#	/etc/rc.d/init.d/hotplug restart >&2
#fi

%preun
if [ "$1" = "0" ] ; then
	if [ -f /var/lock/subsys/hotplug ]; then
		/etc/rc.d/init.d/hotplug stop >&2
	fi
	/sbin/chkconfig --del hotplug
fi

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
%dir %{_sysconfdir}/hotplug
%exclude %{_sysconfdir}/hotplug/pci.*
%exclude %{_sysconfdir}/hotplug/input.*
%attr(755,root,root) %{_sysconfdir}/hotplug/*.agent
%attr(755,root,root) %{_sysconfdir}/hotplug/*.rc
%dir %{_sysconfdir}/hotplug/usb
%{_sysconfdir}/hotplug/hotplug.functions
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/hotplug/blacklist
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/hotplug/*map
%dir %{_sysconfdir}/hotplug.d
%dir %{_sysconfdir}/hotplug.d/default
%attr(755,root,root) %{_sysconfdir}/hotplug.d/default/*.hotplug
%{_libdir}/hotplug
%{_mandir}/man8/*.8*

%files pci
%dir %{_sysconfdir}/hotplug/pci
%attr(755,root,root) %{_sysconfdir}/hotplug/pci.*

%files input
%attr(755,root,root) %{_sysconfdir}/hotplug/input.*
