Summary:		Linux Hotplug Scripts
Name:			hotplug
Version:		2001_04_24
Release:		1_7.x
Group:			Applications/System
License:		GPL
Url:			http://linux-hotplug.sourceforge.net/
BuildArchitectures:	noarch
Source0:		%{name}-%{version}.tar.gz
BuildRoot:		%{_tmppath}/%{name}-root
Prereq:			/sbin/chkconfig

%description
This package contains the scripts necessary for hotplug Linux support.


%prep
%setup -q


%install
# build directories
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/sbin
mkdir -p ${RPM_BUILD_ROOT}/etc/hotplug
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/init.d
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8
	
# install the main hotplug script
install -m 755 sbin/* ${RPM_BUILD_ROOT}/sbin/

# install the helper hotplug scripts
cp -a -r etc/hotplug/* ${RPM_BUILD_ROOT}/etc/hotplug/

# install the usb startup script
cp -a etc/rc.d/init.d/* ${RPM_BUILD_ROOT}/etc/rc.d/init.d/

# install the hotplug man page
cp -a *.8  ${RPM_BUILD_ROOT}%{_mandir}/man8

%files
%defattr(-,root,root)
/sbin/*
/etc/rc.d/init.d/*
/etc/hotplug/*
%{_mandir}/*
%doc README ChangeLog


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


%changelog
* Tue Apr 24 2001 Greg Kroah-Hartman <greg@kroah.com>
- added the hotplug.8 manpage written by Fumitoshi UKAI <ukai@debian.or.jp>

* Fri Mar 2 2001 Greg Kroah-Hartman <greg@kroah.com>
- tweaked the post and preun sections to fix problem of hotplug
  not starting automatically when the package is upgraded.

* Wed Feb 28 2001 Greg Kroah-Hartman <greg@kroah.com>
- 2001_02_28 release

* Wed Feb 14 2001 Greg Kroah-Hartman <greg@kroah.com>
- 2001_02_14 release

* Wed Jan 17 2001 Greg Kroah-Hartman <greg@kroah.com>
- changed specfile based on Chmouel Boudjnah's <chmouel@mandrakesoft.com> comments.

* Tue Jan 16 2001 Greg Kroah-Hartman <greg@kroah.com>
- tweaked the file locations due to the change in the tarball structure.
- 2001_01_16 release

* Mon Jan 15 2001 Greg Kroah-Hartman <greg@kroah.com>
- First cut at a spec file for the hotplug scripts.
- added patch to usb.rc to allow chkconfig to install and remove it.
