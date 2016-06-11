%define api %(echo %{version} |cut -d. -f1)
%define major %api
%define beta %nil

%define qtbluetooth %mklibname qt%{api}bluetooth %{major}
%define qtbluetoothd %mklibname qt%{api}bluetooth -d
%define qtbluetooth_p_d %mklibname qt%{api}bluetooth-private -d

%define qtnfc %mklibname qt%{api}nfc %{major}
%define qtnfcd %mklibname qt%{api}nfc -d
%define qtnfc_p_d %mklibname qt%{api}nfc-private -d

%define _qt5_prefix %{_libdir}/qt%{api}

Name:		qt5-qtconnectivity
Version:	5.6.1
%if "%{beta}" != ""
Release:	1.%{beta}.1
%define qttarballdir qtconnectivity-opensource-src-%{version}-%{beta}
Source0:	http://download.qt.io/development_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/%{qttarballdir}.tar.xz
%else
Release:	1
%define qttarballdir qtconnectivity-opensource-src-%{version}
Source0:	http://download.qt.io/official_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}/submodules/%{qttarballdir}.tar.xz
%endif
Summary:	Qt Connectivity
Group:		Development/KDE and Qt
License:	LGPLv2 with exceptions or GPLv3 with exceptions and GFDL
URL:		http://www.qt.io
BuildRequires:	qmake5
BuildRequires:	pkgconfig(Qt5Quick) >= %{version}
BuildRequires:	pkgconfig(Qt5Qml) >= %{version}
BuildRequires:	pkgconfig(Qt5DBus) >= %{version}
BuildRequires:	pkgconfig(Qt5Concurrent) >= %{version}
BuildRequires:	pkgconfig(bluez)

%description
Qt is a GUI software toolkit which simplifies the task of writing and
maintaining GUI (Graphical User Interface) applications for the X
Window System. Qt is written in C++ and is fully object-oriented.

#------------------------------------------------------------------------------

%package -n	qtbluetooth5
Summary:	Qt%{api} Bluetooth Component Library
Group:		System/Libraries
Requires:	%{qtbluetooth} = %{version}

%description -n qtbluetooth5
Qt%{api} Component Library.

The Qt Bluetooth enables connectivity between Bluetooth enabled devices.

%files -n qtbluetooth5
%{_qt5_bindir}/sdpscanner
%{_qt5_prefix}/qml/QtBluetooth

#------------------------------------------------------------------------------

%package -n	%{qtbluetooth}
Summary:	Qt%{api} Component Library
Group:		System/Libraries
Requires:	bluez

%description -n %{qtbluetooth}
Qt%{api} Component Library.

The Qt Bluetooth enables connectivity between Bluetooth enabled devices.

%files -n %{qtbluetooth}
%{_qt5_libdir}/libQt5Bluetooth.so.%{api}*

#------------------------------------------------------------------------------

%package -n %{qtbluetoothd}
Summary: Devel files needed to build apps based on QtBluetooth
Group: Development/KDE and Qt
Requires: %{qtbluetooth} = %version

%description -n %{qtbluetoothd}
Devel files needed to build apps based on Qt Bluetooth.

%files -n %{qtbluetoothd}
%{_qt5_libdir}/libQt5Bluetooth.prl
%{_qt5_libdir}/libQt5Bluetooth.so
%{_qt5_libdir}/pkgconfig/Qt5Bluetooth.pc
%{_qt5_libdir}/cmake/Qt5Bluetooth
%{_qt5_exampledir}/bluetooth
%{_qt5_prefix}/mkspecs/modules/qt_lib_bluetooth.pri
%{_qt5_includedir}/QtBluetooth
%exclude %{_qt5_includedir}/QtBluetooth/%version

#------------------------------------------------------------------------------

%package -n %{qtbluetooth_p_d}
Summary: Devel files needed to build apps based on QtBluetooth
Group:    Development/KDE and Qt
Requires: %{qtbluetoothd} = %version
Provides: qt5-qtbluetooth-private-devel = %version

%description -n %{qtbluetooth_p_d}
Devel files needed to build apps based on QtBluetooth.

%files -n %{qtbluetooth_p_d}
%{_qt5_includedir}/QtBluetooth/%version
%{_qt5_prefix}/mkspecs/modules/qt_lib_bluetooth_private.pri

#------------------------------------------------------------------------------

%package -n qt5-nfc
Summary: Qt%{api} Nfc Component Library
Group: System/Libraries
Requires: %{qtnfc} = %{version}
Provides: qt5nfc = %{version}

%description -n qt5-nfc
Qt%{api} Component Library.

The Qt Nfc Enables connectivity between NFC enabled devices.

%files -n qt5-nfc
%{_qt5_prefix}/qml/QtNfc

#------------------------------------------------------------------------------

%package -n %{qtnfc}
Summary: Qt%{api} Component Library
Group: System/Libraries

%description -n %{qtnfc}
Qt%{api} Component Library.

The Qt Nfc Enables connectivity between NFC enabled devices.

%files -n %{qtnfc}
%{_qt5_libdir}/libQt5Nfc.so.%{api}*

#------------------------------------------------------------------------------

%package -n %{qtnfcd}
Summary: Devel files needed to build apps based on QtNfc
Group: Development/KDE and Qt
Requires: %{qtnfc} = %version
Provides: qt5-nfc-devel = %version

%description -n %{qtnfcd}
Devel files needed to build apps based on Qt Nfc.

%files -n %{qtnfcd}
%{_qt5_libdir}/libQt5Nfc.prl
%{_qt5_libdir}/libQt5Nfc.so
%{_qt5_libdir}/pkgconfig/Qt5Nfc.pc
%{_qt5_libdir}/cmake/Qt5Nfc
%{_qt5_exampledir}/nfc
%{_qt5_prefix}/mkspecs/modules/qt_lib_nfc.pri
%{_qt5_includedir}/QtNfc
%exclude %{_qt5_includedir}/QtNfc/%version

#------------------------------------------------------------------------------

%package -n %{qtnfc_p_d}
Summary: Devel files needed to build apps based on QtNfc
Group:    Development/KDE and Qt
Requires: %{qtnfcd} = %version
Provides: qt5-nfc-private-devel = %version

%description -n %{qtnfc_p_d}
Devel files needed to build apps based on QtNfc.

%files -n %{qtnfc_p_d}
%{_qt5_includedir}/QtNfc/%version
%{_qt5_prefix}/mkspecs/modules/qt_lib_nfc_private.pri

#------------------------------------------------------------------------------

%prep
%setup -q -n %qttarballdir

%build
%qmake_qt5
%make

#------------------------------------------------------------------------------
%install
%makeinstall_std INSTALL_ROOT=%{buildroot}

# .la and .a files, die, die, die.
rm -f %{buildroot}%{_qt5_libdir}/lib*.la

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd
