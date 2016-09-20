%define		module		mopidy
%define		egg_name	Mopidy
Summary:	Music server with MPD and Spotify support
Name:		mopidy
Version:	2.0.0
Release:	0.1
License:	Apache v2.0
Group:		Development/Libraries
Source0:	https://github.com/mopidy/mopidy/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ada9471fe369a7c70c2d4cb3f0e10abc
Source1:	%{name}.conf
Source2:	%{name}.service
URL:		http://www.mopidy.com/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	gstreamer-python
Requires:	pykka
Requires:	python-backports-ssl_match_hostname
Requires:	python-dbus
Requires:	python-pygobject
Requires:	python-pygobject
Requires:	python-requests
Requires:	python-tornado
Requires:	python2-certifi
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

# install mopidy config file
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
cp %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.conf

# install mopidy service file
install -d $RPM_BUILD_ROOT%{systemdunitdir}
cp %{SOURCE2} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{systemdunitdir}/%{name}.service
%attr(755,root,root) %{_bindir}/mopidy
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
