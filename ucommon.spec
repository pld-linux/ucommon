#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_with	gnutls		# use GnuTLS instead of OpenSSL

Summary:	GNU uCommon C++ - very light-weight C++ framework
Summary(pl.UTF-8):	GNU uCommon C++ - bardzo lekki szkielet C++
Name:		ucommon
Version:	6.3.0
Release:	1
License:	LGPL v3+ (libucommon and secure component), GPL v3+ with runtime exception (commoncpp2)
Group:		Libraries
Source0:	http://ftp.gnu.org/gnu/commoncpp/%{name}-%{version}.tar.gz
# Source0-md5:	86523e6a016919dee64b346631be3da0
URL:		http://www.gnu.org/software/commoncpp/
%{?with_apidocs:BuildRequires:	doxygen}
%{?with_gnutls:BuildRequires:	gnutls-devel >= 3.0.0}
BuildRequires:	libstdc++-devel >= 5:3.0
%{!?with_gnutls:BuildRequires:	openssl-devel >= 0.9.7}
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNU uCommon C++ is meant as a very light-weight C++ library to
facilitate using C++ design patterns even for very deeply embedded
applications, such as for systems using uClibc along with POSIX
threading support. For this reason, uCommon disables language features
that consume memory or introduce runtime overhead, such as rtti and
exception handling, and assumes one will mostly be linking
applications with other pure C based libraries rather than using the
overhead of the standard C++ library and other class frameworks.

%description -l pl.UTF-8
GNU uCommon C++ ma być bardzo lekką biblioteką C++ ułatwiającą
wykorzystywanie wzorców projektowych C++, nawet w bardzo wbudowanych
zastosowaniach, takich jak systemy wykorzystujące uClibc, wraz z
obsługą wątków POSIX. Z tego powodu uCommon wyłącza elementy języka
pochłaniające pamięć lub wprowadzające narzut w czasie działania,
takie jak rtti czy obsługa wyjątków i zakłada, że aplikacje będą
linkowane z innymi bibliotekami opartymi na czystym C zamiast narzutu
pełnej biblioteki standardowej C++ czy innych szkieletów klas.

%package devel
Summary:	Header files for uCommon C++ library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki uCommon C++
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%{?with_gnutls:Requires:	gnutls-devel >= 3.0.0}
Requires:	libstdc++-devel >= 5:3.0
%{!?with_gnutls:Requires:	openssl-devel >= 0.9.7}

%description devel
Header files for uCommon C++ library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki uCommon C++.

%package static
Summary:	Static uCommon C++ library
Summary(pl.UTF-8):	Statyczna biblioteka uCommon C++
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static uCommon C++ library.

%description static -l pl.UTF-8
Statyczna biblioteka uCommon C++.

%package apidocs
Summary:	uCommon C++ API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki uCommon C++
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API and internal documentation for uCommon C++ library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki uCommon C++.

%package tools
Summary:	uCommon system and support applications
Summary(pl.UTF-8):	uCommon - aplikacje systemowe i pomocnicze
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description tools
uCommon system and support applications.

%description tools -l pl.UTF-8
uCommon - aplikacje systemowe i pomocnicze.

%prep
%setup -q

%build
%configure \
	--with-sslstack=%{?with_gnutls:gnutls}%{!?with_gnutls:openssl}
%{__make}

%if %{with apidocs}
%{__make} doxy
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYRIGHT ChangeLog NEWS README README.secure SUPPORT TODO
%attr(755,root,root) %{_libdir}/libcommoncpp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcommoncpp.so.7
%attr(755,root,root) %{_libdir}/libucommon.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libucommon.so.7
%attr(755,root,root) %{_libdir}/libusecure.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libusecure.so.7

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/commoncpp-config
%attr(755,root,root) %{_bindir}/ucommon-config
%attr(755,root,root) %{_libdir}/libcommoncpp.so
%attr(755,root,root) %{_libdir}/libucommon.so
%attr(755,root,root) %{_libdir}/libusecure.so
%{_libdir}/libcommoncpp.la
%{_libdir}/libucommon.la
%{_libdir}/libusecure.la
%{_includedir}/commoncpp
%{_includedir}/ucommon
%{_pkgconfigdir}/commoncpp.pc
%{_pkgconfigdir}/ucommon.pc
%{_mandir}/man1/commoncpp-config.1*
%{_mandir}/man1/ucommon-config.1*

%files static
%defattr(644,root,root,755)
%{_libdir}/libcommoncpp.a
%{_libdir}/libucommon.a
%{_libdir}/libusecure.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*
%endif

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/args
%attr(755,root,root) %{_bindir}/car
%attr(755,root,root) %{_bindir}/keywait
%attr(755,root,root) %{_bindir}/mdsum
%attr(755,root,root) %{_bindir}/pdetach
%attr(755,root,root) %{_bindir}/scrub-files
%attr(755,root,root) %{_bindir}/sockaddr
%attr(755,root,root) %{_bindir}/zerofill
%{_mandir}/man1/args.1*
%{_mandir}/man1/car.1*
%{_mandir}/man1/keywait.1*
%{_mandir}/man1/mdsum.1*
%{_mandir}/man1/pdetach.1*
%{_mandir}/man1/scrub-files.1*
%{_mandir}/man1/sockaddr.1*
%{_mandir}/man1/zerofill.1*
