%global xfceversion 4.14
Name:           libxfce4ui
Version:        4.14.1
Release:        1%{?dist}
Summary:        Commonly used Xfce widgets
License:        LGPLv2+
#Group:          Development/Libraries
URL:            http://xfce.org/
Source0:        http://archive.xfce.org/src/xfce/%{name}/%{xfceversion}/%{name}-%{version}.tar.bz2
# add more keyboard shortcuts to make multimedia keyboards work out of the box
# Terminal changed to xfce4-terminal in the patch
Patch10:        libxfce4ui-%{xfceversion}-keyboard-shortcuts.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#BuildArch:      noarch

BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(gobject-2.0) >= 2.24.0
BuildRequires:  pkgconfig(gtk+-2.0) >= 2.20.0
BuildRequires:  pkgconfig(libxfce4util-1.0) >= %{xfceversion}
BuildRequires:  pkgconfig(libxfconf-0) >= %{xfceversion}
BuildRequires:  pkgconfig(libstartup-notification-1.0) >= 0.4
BuildRequires:  gtk-doc
BuildRequires:  desktop-file-utils
BuildRequires:  gtk3-devel
BuildRequires:  glade-devel
BuildRequires:  gettext
BuildRequires:  gobject-introspection-devel
BuildRequires:  intltool
BuildRequires:  libSM-devel
BuildRequires:  vala

%description
Libxfce4ui is used to share commonly used Xfce widgets among the Xfce applications.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       gtk2-devel
Requires:       libxfce4util-devel
Requires:       glade-devel
Requires:       pkgconfig

%description    devel
This package contains libraries and header files for developing applications that use %{name}.

%prep
%setup -q
%patch10

%build
%configure --disable-static

# Remove rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
export LD_LIBRARY_PATH="`pwd`/libxfce4ui/.libs"

%make_build

%install
%make_install

# fix permissions for installed libraries
chmod 755 $RPM_BUILD_ROOT/%{_libdir}/*.so

find %{buildroot} -name '*.la' -exec rm -f {} ';'
%find_lang %{name}

%ldconfig_scriptlets

%files -f %{name}.lang
%license COPYING
%doc AUTHORS NEWS README THANKS
%config(noreplace) %{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/%{name}-2.0.typelib
%{_bindir}/xfce4-about
%{_datadir}/gir-1.0/%{name}-2.0.gir
%{_datadir}/vala/vapi/%{name}-2.deps
%{_datadir}/vala/vapi/%{name}-2.vapi
%{_datadir}/applications/xfce4-about.desktop
%{_datadir}/icons/hicolor/48x48/apps/xfce4-logo.png

%files devel
%doc TODO
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%doc %{_datadir}/gtk-doc/
%{_libdir}/glade/modules/lib*.so
%{_datadir}/glade/catalogs/%{name}*.xml*
%{_datadir}/glade/pixmaps/hicolor/*/actions/*

%changelog
* Wed Jul 8 2020 Dillon Chen <dillon.chen@turbolinux.com.cn> - 4.14.1-1
- Init package
