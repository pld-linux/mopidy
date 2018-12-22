%define		module		mopidy
%define		egg_name	Mopidy
Summary:	Music server with MPD and Spotify support
Name:		mopidy
Version:	2.2.1
Release:	1
License:	Apache v2.0
Group:		Development/Libraries
Source0:	https://github.com/mopidy/mopidy/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	bf4afeadcc4b909e7ef9426a208036a3
Source1:	%{name}.conf
Source2:	%{name}.service
URL:		https://www.mopidy.com/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	gstreamer-audiosink-alsa
Requires:	gstreamer-mad
Requires:	gstreamer-pulseaudio
Requires:	python-backports-ssl_match_hostname
Requires:	python-certifi
Requires:	python-dbus
Requires:	python-gstreamer
Requires:	python-pygobject
Provides:	group(mopidy)
Provides:	user(mopidy)
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mopidy is a Python application that runs in a terminal or in the
background on Linux computers or Macs that have network connectivity
and audio output. Out of the box, Mopidy is an MPD and HTTP server.
Additional frontends for controlling Mopidy can be installed from
extensions.

%prep
%setup -q

%build
%py_build

%install
rm -rf $RPM_BUILD_ROOT
%py_install
%py_postclean

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{systemdunitdir}} \
	$RPM_BUILD_ROOT%{_localstatedir}/cache/%{name} \
	$RPM_BUILD_ROOT%{_localstatedir}/log/%{name} \
	$RPM_BUILD_ROOT%{_sharedstatedir}/%{name}/{local,media,playlists}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 332 %{name}
%useradd -u 332 -d /var/lib/%{name} -g %{name} -c "System user to run mopidy service" %{name}

%postun
if [ "$1" = "0" ]; then
	%userremove %{name}
	%groupremove %{name}
fi

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.conf
%{systemdunitdir}/%{name}.service
%attr(755,root,root) %{_bindir}/mopidy
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info

%attr(770,root,%{name}) %dir %{_localstatedir}/cache/%{name}
%attr(770,root,%{name}) %dir %{_localstatedir}/log/%{name}
%attr(770,root,%{name}) %dir %{_sharedstatedir}/%{name}
%attr(770,root,%{name}) %dir %{_sharedstatedir}/%{name}/local
%attr(770,root,%{name}) %dir %{_sharedstatedir}/%{name}/media
%attr(770,root,%{name}) %dir %{_sharedstatedir}/%{name}/playlists
