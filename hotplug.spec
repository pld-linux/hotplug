Summary:	Linux Hotplug Scripts
Summary(pl):	Linuksowe skrypty do urz±dzeñ hotplug
Name:		hotplug
Version:	2002_08_26
Release:	1
Group:		Applications/System
License:	GPL
Source0:	http://unc.dl.sourceforge.net/sourceforge/linux-hotplug/%{name}-%{version}.tar.gz
# Source0-md5:	eb3e3aacfe072e7bd31a4e01fd8af2e0
Source1:	%{name}.init
Patch0:		%{name}-PLD.patch
URL:		http://linux-hotplug.sourceforge.net/
BuildArch:	noarch
# Requires wc
Requires:	textutils
Requires:	awk
Requires:	usbutils
Requires:	sed
Requires:	bash
Prereq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_exec_prefix	/

%description
This package contains the scripts necessary for hotplug Linux support.

%description -l pl
Ten pakiet zawiera skrypty potrzebne do obs³ugi urz±dzeñ hotplug
(pod³±czanych w czasie pracy) pod Linuksem.

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/hotplug,/etc/rc.d/init.d,%{_mandir}/man8}

install -m 755 sbin/* $RPM_BUILD_ROOT%{_sbindir}

cp -a -r etc/hotplug/* $RPM_BUILD_ROOT%{_sysconfdir}/hotplug/

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/hotplug
install *.8  $RPM_BUILD_ROOT%{_mandir}/man8

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
%attr(755,root,root) /etc/rc.d/init.d/*
%attr(755,root,root) %{_sysconfdir}/hotplug/*.agent
%attr(755,root,root) %{_sysconfdir}/hotplug/*.rc
%dir %{_sysconfdir}/hotplug/usb
%dir %{_sysconfdir}/hotplug/pci
%{_sysconfdir}/hotplug/hotplug.functions
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/hotplug/blacklist
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/hotplug/*map
%{_mandir}/man8/*.8*
