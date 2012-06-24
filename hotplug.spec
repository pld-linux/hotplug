Summary:	Linux Hotplug Scripts
Name:		hotplug
Version:	2001_04_24
Release:	2
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
License:	GPL
Url:		http://linux-hotplug.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/linux-hotplug/%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Prereq:		/sbin/chkconfig

%define		_exec_prefix	/

%description
This package contains the scripts necessary for hotplug Linux support.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/hotplug,/etc/rc.d/init.d,%{_mandir}/man8}
	
install -m 755 sbin/* $RPM_BUILD_ROOT/%{_sbindir}

cp -a -r etc/hotplug/* $RPM_BUILD_ROOT%{_sysconfdir}/hotplug/

install etc/rc.d/init.d/* $RPM_BUILD_ROOT/etc/rc.d/init.d/
install *.8  $RPM_BUILD_ROOT%{_mandir}/man8

%{__gzip} README ChangeLog

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
if [ "$1" = 0 ] ; then
	/etc/rc.d/init.d/hotplug stop >&2
	/sbin/chkconfig --del hotplug
fi

%files
%defattr(644,root,root,755)
%doc {README,ChangeLog}.gz
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) /etc/rc.d/init.d/*
%{_sysconfdir}/hotplug/*
%{_mandir}/man8/*.8*
