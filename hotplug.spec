Summary:	Linux Hotplug Scripts
Summary(pl):	Linuksowe skrypty do urz±dzeñ hotplug
Name:		hotplug
Version:	2004_04_01
Release:	7
Group:		Applications/System
License:	GPL
Source0:	ftp://ftp.kernel.org/pub/linux/utils/kernel/hotplug/%{name}-%{version}.tar.bz2
# Source0-md5:	527f0242481024c77255f3c1fa09e6ee
Source1:	%{name}.init
Source2:	%{name}-update-usb.usermap
Source3:	%{name}-update-usb.usermap.8
Source4:	%{name}-digicam
Patch0:		%{name}-PLD.patch
Patch1:		%{name}-ifup.patch
Patch2:		%{name}-devlabel.patch
URL:		http://linux-hotplug.sourceforge.net/
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
# Requires wc
Requires:	textutils
Requires:	awk
Requires:	usbutils
Requires:	sed
Requires:	bash
# it is _not_ noarch as it contains %{_libdir}/hotplug directory
#BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_exec_prefix	/
%define		_libdir		/%{_lib}
%define		_sbindir	/sbin

%description
This package contains the scripts necessary for hotplug Linux support.

%description -l pl
Ten pakiet zawiera skrypty potrzebne do obs³ugi urz±dzeñ hotplug
(pod³±czanych w czasie pracy) pod Linuksem.

%package pci
Summary:	Hotplug pci module
Summary(pl):	Modu³ pci do hotpluga
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description pci
This is mostly to recover lost boot-time PCI hotplug events. Should
handle 2.4.x and 2.6.x PCI (including Cardbus) hotplugging, with a
consistent framework for adding device and driver specific treatments.

%description pci -l pl
Ten modu³ s³u¿y g³ównie do odzyskiwania zdarzeñ hotplug PCI utraconych
w czasie startu systemu. Powinien obs³ugiwaæ pod³±czanie urz±dzeñ PCI
(w³±cznie z Cardbus) dla j±der 2.4.x i 2.6.x ze spójnym szkieletem do
dodawania urz±dzeñ i zachowañ specyficznych dla sterownika.

%package input
Summary:	Hotplug input module
Summary(pl):	Modu³ input do hotpluga
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description input
This loads handlers for those input devices that have drivers compiled
in kernel. Currently stopping is not supported. Should handle 2.6.x
input hotplugging, with a consistent framework for adding device and
driver specific handling.

%description input -l pl
Ten modu³ wczytuje programy obs³uguj±ce te urz±dzenia wej¶ciowe, dla
których sterowniki zosta³y wkompilowane w j±dro. Aktualnie wy³±czanie
nie jest obs³ugiwane. Powinien obs³ugiwaæ pod³±czanie urz±dzeñ
wej¶ciowych dla j±der 2.6.x ze spójnym szkieletem do dodawania
urz±dzeñ i obs³ug± rzeczy specyficznych dla sterownika.

%package digicam
Summary:	Hotplug definitions for USB digital cameras
Summary(pl):	Definicje Hotpluga dla aparatów cyfrowych na USB
Group:		Applications/System
PreReq:		libgphoto2
Requires(post,postun):	fileutils
Requires(post,postun):	grep
Requires:	%{name} = %{version}-%{release}

%description digicam
This creates appropriate definitions to usb.usermap for digital
cameras based on output of libgphoto2.

%description digicam -l pl
Ten modu³ dodaje definicje dla aparatów cyfrowych opieraj±c siê na
danych z libgphoto2.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_sbindir},%{_sysconfdir}/hotplug,/etc/rc.d/init.d,%{_mandir}/man8}

%{__make} install \
	prefix=$RPM_BUILD_ROOT

install %{SOURCE2} $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE3} $RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/hotplug
ln -s %{_sysconfdir}/hotplug.d $RPM_BUILD_ROOT%{_libdir}/%{name}
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/hotplug/usb/digicam

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

%pre digicam
if [ -n "`getgid digicam`" ]; then
        if [ "`getgid digicam`" != "135" ]; then
                echo "Error: group digicam doesn't have gid=135. Correct this before installing hotplug." 1>&2
                exit 1
        fi
else
        /usr/sbin/groupadd -g 135 -r -f digicam
fi

%post digicam
if [ "$1" = "1" ]; then
	usermap="%{_sysconfdir}/hotplug/usb.usermap"
	tmpusermap="${usermap}.tmp"
	umask 022
	if [ -f "$usermap" ]; then
		grep -v "digicam" $usermap > $tmpusermap
		mv -f $tmpusermap $usermap
		/usr/lib/libgphoto2/print-usb-usermap digicam | grep -v '#' >> $usermap
	else
		/usr/lib/libgphoto2/print-usb-usermap digicam | grep -v '#' >> $usermap
	fi
fi

%postun digicam
if [ "$1" = "0" ]; then
	usermap="%{_sysconfdir}/hotplug/usb.usermap"
	tmpusermap="${usermap}.tmp"
	umask 022
	if [ -f "$usermap" ]; then
	        grep -v "digicam" $usermap > $tmpusermap
	        mv -f $tmpusermap $usermap
	fi
fi

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
%dir %{_sysconfdir}/hotplug
%exclude %{_sysconfdir}/hotplug/pci.*
%exclude %{_sysconfdir}/hotplug/input.*
%{_sysconfdir}/hotplug/hotplug.functions
%attr(755,root,root) %{_sysconfdir}/hotplug/*.agent
%attr(755,root,root) %{_sysconfdir}/hotplug/*.rc
%dir %{_sysconfdir}/hotplug/usb
%exclude %{_sysconfdir}/hotplug/usb/digicam
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/hotplug/blacklist
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/hotplug/*map
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

%files digicam
%defattr(644,root,root,755)
%attr(755,root,root) %{_sysconfdir}/hotplug/usb/digicam
