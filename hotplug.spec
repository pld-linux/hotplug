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
%chkconfig_add

%preun
%chkconfig_del

%files
%defattr(644,root,root,755)
%doc {README,ChangeLog}.gz
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) /etc/rc.d/init.d/*
%{_sysconfdir}/hotplug/*
%{_mandir}/man8/*.8*
