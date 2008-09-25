%define name protobuf
%define version 2.0.1
%define release %mkrel 1

# Majors
%define major 0

# Library names
%define libname %mklibname %{name} %{major}
%define libname_devel %mklibname -d %{name}

Summary: Protocol Buffers - Google's data interchange format
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2


License: ASL 2.0
Group: Development/Other
Url: http://code.google.com/apis/protocolbuffers/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Protocol buffers are Google's language-neutral, platform-neutral, extensible
mechanism for serializing structured data – think XML, but smaller, faster,
and simpler. You define how you want your data to be structured once, then you
can use special generated source code to easily write and read your structured
data to and from a variety of data streams and using a variety of languages
 – Java, C++, or Python. 

%package -n %{libname}
Summary: Libraries for Google's Protocol Buffers
Group: System/Libraries

%description -n %{libname}
This package contains the runtime libraries for any application that use
Google's Protocol Buffers.


%package -n %{libname_devel}
Summary: Headers and libraries for Google's Protocol Buffers development
Group: Development/Other
Requires: %{name} = %{version}-%{release}
Requires: %{libname} = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}

%description -n %{libname_devel}
Headers and libraries for developing applications that use
Google's Protocol Buffers.



%prep
%setup -q

%build
%configure2_5x --disable-static
%make

%install
rm -rf %{buildroot}
%makeinstall_std
# Remove static libraries (configure switch is not enough)
find %{buildroot} \( -name "*.a" -o -name "*.la" \) -exec rm {} \;

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/protoc


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libprotobuf.so.%{major}*
%{_libdir}/libprotoc.so.%{major}*

%files -n %{libname_devel}
%defattr(-,root,root)
%doc editors examples java python
%dir %{_includedir}/google/protobuf
%{_includedir}/google/protobuf/*
%{_libdir}/libprotobuf.so
%{_libdir}/libprotoc.so
