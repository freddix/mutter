Summary:	Window manager
Name:		mutter
Version:	3.14.0
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/mutter/3.14/%{name}-%{version}.tar.xz
# Source0-md5:	f980505e4198399aa2224343dd0a9f3e
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	clutter-devel
BuildRequires:	gettext-devel
BuildRequires:	gobject-introspection-devel >= 1.42.0
BuildRequires:	gsettings-desktop-schemas-devel >= 3.14.0
BuildRequires:	gtk+3-devel >= 3.14.0
BuildRequires:	libcanberra-gtk3-devel
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRequires:	startup-notification-devel
Requires(post,postun):	glib-gio-gsettings
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gsettings-desktop-schemas >= 3.14.0
Provides:	window-manager
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/mutter

%description
Window manager.

%package libs
Summary:	Mutter library
Group:		Libraries

%description libs
Mutter library.

%package devel
Summary:	Header files for Mutter library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This is the package containing the header files for Mutter library.

%package apidocs
Summary:	Meta API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
Meta API documentation.

%prep
%setup -q

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	ZENITY=%{_bindir}/zenity	\
	--disable-schemas-compile	\
	--disable-silent-rules		\
	--disable-static		\
	--enable-compile-warnings=minimum   \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/GConf
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{la,ca@valencia}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_gsettings_cache

%postun
%update_gsettings_cache

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS
%dir %{_libdir}/mutter/plugins
%attr(755,root,root) %{_bindir}/mutter
%attr(755,root,root) %{_libdir}/mutter/plugins/default.so
%attr(755,root,root) %{_libexecdir}/mutter-restart-helper
%{_datadir}/glib-2.0/schemas/org.gnome.mutter.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.mutter.wayland.gschema.xml
%{_datadir}/gnome-control-center/keybindings/50-mutter-navigation.xml
%{_datadir}/gnome-control-center/keybindings/50-mutter-system.xml
%{_datadir}/gnome-control-center/keybindings/50-mutter-windows.xml
%{_desktopdir}/mutter.desktop
%{_desktopdir}/mutter-wayland.desktop
%{_mandir}/man1/*.1*

%files libs
%defattr(644,root,root,755)
%dir %{_libdir}/mutter
%attr(755,root,root) %ghost %{_libdir}/libmutter.so.?
%attr(755,root,root) %{_libdir}/libmutter.so.*.*.*
%{_libdir}/mutter/Meta-*.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmutter.so
%{_includedir}/mutter
%{_pkgconfigdir}/*.pc
%{_libdir}/mutter/Meta-*.gir

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/meta

