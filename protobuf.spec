# Major
%define major		6

# Library names
%define libname		%mklibname %{name} %{major}
%define liblite         %mklibname %{name}-lite %{major}
%define libcompiler     %mklibname protoc %{major}
%define develname       %mklibname %{name} -d
%define staticdevelname %mklibname %{name} -d -s

# don't build python subpackage
%define with_python   %{?_without_python: 0} %{?!_without_python: 1}
# don't build -java subpackages
# -- -- %define with_java     %{?_without_java:   0} %{?!_without_java:   1}
# 15 nov 2009 : java part of the package broken, don't build the subpackages
%define with_java 0

Summary:		Protocol Buffers - Google's data interchange format
Name:			protobuf
Version:		2.3.0
Release:		%mkrel 2
License:		BSD
Group:			Development/Other
Source:			http://protobuf.googlecode.com/files/%{name}-%{version}.tar.bz2
Source1:		ftdetect-proto.vim
URL:			http://code.google.com/p/protobuf/
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:		pkgconfig
BuildRequires:		gtest-devel
%if %{with_python}
BuildRequires:		python-devel
BuildRequires:		python-setuptools
%endif
%if %{with_java}
BuildRequires:		java-devel >= 1.6
BuildRequires:		jpackage-utils
BuildRequires:		maven2
BuildRequires:		maven2-plugin-compiler
BuildRequires:		maven2-plugin-install
BuildRequires:		maven2-plugin-jar
BuildRequires:		maven2-plugin-javadoc
BuildRequires:		maven2-plugin-release
BuildRequires:		maven2-plugin-resources
BuildRequires:		maven2-plugin-surefire
BuildRequires:		maven2-plugin-antrun
%endif

%description
Protocol Buffers are a way of encoding structured data in an efficient
yet extensible format. Google uses Protocol Buffers for almost all of
its internal RPC protocols and file formats.

Protocol buffers are a flexible, efficient, automated mechanism for
serializing structured data - think XML, but smaller, faster, and
simpler. You define how you want your data to be structured once, then
you can use special generated source code to easily write and read
your structured data to and from a variety of data streams and using a
variety of languages. You can even update your data structure without
breaking deployed programs that are compiled against the "old" format.

%package -n		%{libname}
Summary:		Runtime library for %{name}
Group:			System/Libraries

%description -n		%{libname}
Protocol Buffers are a way of encoding structured data in an efficient
yet extensible format. Google uses Protocol Buffers for almost all of
its internal RPC protocols and file formats.

Protocol buffers are a flexible, efficient, automated mechanism for
serializing structured data - think XML, but smaller, faster, and
simpler. You define how you want your data to be structured once, then
you can use special generated source code to easily write and read
your structured data to and from a variety of data streams and using a
variety of languages. You can even update your data structure without
breaking deployed programs that are compiled against the "old" format.

This package contains the shared %{name} library.

%package -n		%{liblite}
Summary:		Protocol Buffers lite version
Group:			Development/Other

%description -n		%{liblite}
This package contains a compiled with "optimize_for = LITE_RUNTIME" 
version of Google's Protocol Buffers library.

The "optimize_for = LITE_RUNTIME" option causes the compiler to 
generate code which only depends libprotobuf-lite, which is much 
smaller than libprotobuf but lacks descriptors, reflection, and some 
other features.

%package		compiler
Summary:		Protocol Buffers compiler
Group:			Development/Other
Suggests:		%{libname}
Suggests:		%{liblite}

%description		compiler
This package contains Protocol Buffers compiler for all programming
languages.

%package -n		%{libcompiler}
Summary:		Protocol Buffers compiler shared library
Group:			System/Libraries

%description -n		%{libcompiler}
This package contains the Protocol Buffers compiler shared library.

%package -n		%{develname}
Summary:		Protocol Buffers C++ headers and libraries
Group:			Development/Other
Requires:		%{libname} = %{version}
Requires:		%{liblite} = %{version}
Requires:		%{name}-compiler
Requires:		pkgconfig
Provides:		%{name}-devel = %{version}-%{release}

%description -n		%{develname}
This package contains Protocol Buffers compiler for all languages and
C++ headers and libraries.

%package -n		%{staticdevelname}
Summary:		Static development files for %{name}
Group:			Development/Other
Requires:		%{libname} = %{version}
Requires:		%{liblite} = %{version}
Provides:		%{name}-static-devel = %{version}-%{release}

%description -n		%{staticdevelname}
This package contains static libraries for Protocol Buffers.

%if %{with_python}
%package -n		python-%{name}
Summary:		Python bindings for Google Protocol Buffers
Group:			Development/Python
Conflicts: %{name}-compiler > %{version}
Conflicts: %{name}-compiler < %{version}

%description -n		python-%{name}
This package contains Python bindings for Google Protocol Buffers.
%endif

%package		vim
Summary:		Vim syntax highlighting for Google Protocol Buffers
Group:			Development/Other
Requires:		vim-enhanced

%description		vim
This package contains syntax highlighting for Google Protocol Buffers
descriptions in Vim editor.

%if %{with_java}
%package		java
Summary:		Java Protocol Buffers runtime library
Group:			Development/Java
Requires:		java
Requires:		jpackage-utils
Requires(post):		jpackage-utils
Requires(postun):	jpackage-utils
Conflicts:		%{name}-compiler > %{version}
Conflicts:		%{name}-compiler < %{version}

%description		java
This package contains Java Protocol Buffers runtime library.

%package		javadoc
Summary:		Javadocs for %{name}-java
Group:			Development/Java
Requires:		jpackage-utils
Requires:		%{name}-java

%description		javadoc
This package contains the API documentation for %{name}-java.

%endif

%prep
%setup -q
chmod 644 examples/*

%build
export PTHREAD_LIBS="-lpthread"
./autogen.sh
%configure
%make

%if %{with_python}
pushd python
%__python ./setup.py build
sed -i -e 1d build/lib/google/protobuf/descriptor_pb2.py
popd
%endif

%if %{with_java}
pushd java
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL
mvn-jpp -Dmaven.repo.local=$MAVEN_REPO_LOCAL install javadoc:javadoc
popd
%endif

%check
%make check

%install
rm -rf %{buildroot}
%makeinstall
find %{buildroot} -type f -name "*.la" -exec rm -f {} \;
%if %{with_python}
pushd python
%__python ./setup.py install --root=%{buildroot} --single-version-externally-managed --record=INSTALLED_FILES --optimize=1
popd
%endif
install -p -m 644 -D %{SOURCE1} %{buildroot}%{_datadir}/vim/vimfiles/ftdetect/proto.vim
install -p -m 644 -D editors/proto.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/proto.vim

%if %{with_java}
pushd java
install -d -m 755 %{buildroot}%{_javadir}
install -pm 644 target/%{name}-java-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar

install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -rp target/site/apidocs %{buildroot}%{_javadocdir}/%{name}

install -d -m 755 %{buildroot}%{_datadir}/maven2/poms
install -pm 644 pom.xml %{buildroot}%{_datadir}/maven2/poms/JPP-%{name}.pom
%add_to_maven_depmap org.apache.maven %{name} %{version} JPP %{name}

%endif

%if %{with_java}
%post java
%update_maven_depmap

%postun java
%update_maven_depmap
%endif

%clean
rm -rf %{buildroot}

%files -n		%{libname}
%defattr(-, root, root, -)
%doc CHANGES.txt CONTRIBUTORS.txt COPYING.txt README.txt
%{_libdir}/lib%{name}.so.*

%files -n		%{liblite}
%defattr(-, root, root, -)
%doc COPYING.txt README.txt
%{_libdir}/lib%{name}-lite.so.*

%files			compiler
%defattr(-, root, root, -)
%doc COPYING.txt README.txt
%{_bindir}/protoc

%files -n		%{libcompiler}
%defattr(-,root,root,-)
%{_libdir}/libprotoc.so.*

%files -n		%{develname}
%defattr(-, root, root, -)
%doc examples/add_person.cc examples/addressbook.proto
%doc  examples/list_people.cc examples/Makefile examples/README.txt
%dir %{_includedir}/google
%{_includedir}/google/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}-lite.so
%{_libdir}/libprotoc.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-lite.pc

%files -n		%{staticdevelname}
%defattr(-, root, root, -)
%{_libdir}/lib%{name}.a
%{_libdir}/lib%{name}-lite.a
%{_libdir}/libprotoc.a

%if %{with_python}
%files -n		python-%{name}
%doc python/README.txt
%doc examples/add_person.py examples/list_people.py examples/addressbook.proto
%defattr(-, root, root, -)
%dir %{py_puresitedir}/google
%{py_puresitedir}/google/%{name}/
%{py_puresitedir}/%{name}-%{version}-py%{python_version}.egg-info/
%{py_puresitedir}/%{name}-%{version}-py%{python_version}-nspkg.pth
%endif

%files			vim
%defattr(-, root, root, -)
%{_datadir}/vim/vimfiles/ftdetect/proto.vim
%{_datadir}/vim/vimfiles/syntax/proto.vim

%if %{with_java}
%files			java
%defattr(-, root, root, -)
%doc examples/AddPerson.java examples/ListPeople.java
%{_datadir}/maven2/poms/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%{_javadir}/*

%files			javadoc
%defattr(-, root, root,-)
%{_javadocdir}/%{name}
%endif

