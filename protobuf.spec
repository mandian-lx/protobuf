%define old_libname %mklibname %{name} 8
%define old_liblite %mklibname %{name}-lite 8
%define old_libprotoc %mklibname protoc 8
%define old_devname %mklibname %{name} -d
%define old_statname %mklibname %{name} -d -s

# Build -python subpackages
%bcond_without python
%bcond_without python2
# Build -java subpackage
%bcond_without java
# Don't require gtest
%bcond_with gtest

%global emacs_lispdir %{_datadir}/emacs/site-lisp
%global emacs_startdir %{_datadir}/emacs/site-lisp/site-start.d

Summary:	Protocol Buffers - Google's data interchange format
Name:		protobuf
Version:	3.3.2
Release:	1
Group:		Development/Other
License:	BSD
URL:		https://github.com/google/protobuf
Source0:	https://github.com/google/protobuf/archive/v%{version}.tar.gz
Source1:	ftdetect-proto.vim
Source2:	protobuf-init.el
Source3:	%{name}.rpmlintrc
Patch0:		protobuf-3.2.0-emacs-24.4.patch
Patch1:		protobuf-3.2.0-gtest.patch

BuildRequires:	automake autoconf libtool pkgconfig zlib-devel
BuildRequires:	emacs
BuildRequires:	emacs-el >= 24.1
%if %{with gtest}
BuildRequires:	gtest-devel
%endif
%rename %{old_libname}
%rename %{old_liblite}
%rename %{old_libprotoc}

%description
Protocol Buffers are a way of encoding structured data in an efficient
yet extensible format. Google uses Protocol Buffers for almost all of
its internal RPC protocols and file formats.

Protocol buffers are a flexible, efficient, automated mechanism for
serializing structured data – think XML, but smaller, faster, and
simpler. You define how you want your data to be structured once, then
you can use special generated source code to easily write and read
your structured data to and from a variety of data streams and using a
variety of languages. You can even update your data structure without
breaking deployed programs that are compiled against the "old" format.

%package compiler
Summary:	Protocol Buffers compiler
Requires:	%{name} = %{EVRD}
Group:		Development/Other

%description compiler
This package contains Protocol Buffers compiler for all programming
languages.

%package devel
Summary:	Protocol Buffers C++ headers and libraries
Group:		Development/Other
Requires:	%{name} = %{EVRD}
Requires:	%{name}-compiler = %{EVRD}
Requires:	pkgconfig
%rename %{old_devname}

%description devel
This package contains Protocol Buffers compiler for all languages and
C++ headers and libraries

%package lite
Summary:	Protocol Buffers LITE_RUNTIME libraries
Group:		Development/Other

%description lite
Protocol Buffers built with optimize_for = LITE_RUNTIME.

The "optimize_for = LITE_RUNTIME" option causes the compiler to generate code
which only depends libprotobuf-lite, which is much smaller than libprotobuf but
lacks descriptors, reflection, and some other features.

%package lite-devel
Summary:	Protocol Buffers LITE_RUNTIME development libraries
Requires:	%{name}-devel = %{EVRD}
Requires:	%{name}-lite = %{EVRD}
Group:		Development/Other

%description lite-devel
This package contains development libraries built with
optimize_for = LITE_RUNTIME.

The "optimize_for = LITE_RUNTIME" option causes the compiler to generate code
which only depends libprotobuf-lite, which is much smaller than libprotobuf but
lacks descriptors, reflection, and some other features.

%if %{with python}
%package python
Summary:	Python bindings for Google Protocol Buffers
Group:		Development/Python
BuildRequires:	python-devel
BuildRequires:	python-setuptools

%description python
This package contains Python libraries for Google Protocol Buffers
%endif

%if %{with python2}
%package python2
Summary:	Python2 bindings for Google Protocol Buffers
Group:		Development/Python
BuildRequires:	python2-devel
BuildRequires:	python2-setuptools

%description python2
This package contains Python2 libraries for Google Protocol Buffers
%endif

%package vim
Summary:	Vim syntax highlighting for Google Protocol Buffers descriptions
Requires:	vim-enhanced
Group:		Development/Other

%description vim
This package contains syntax highlighting for Google Protocol Buffers
descriptions in Vim editor

%package emacs
Summary:	Emacs mode for Google Protocol Buffers descriptions
Group:		Development/Other

%description emacs
This package contains syntax highlighting for Google Protocol Buffers
descriptions in the Emacs editor.

%package emacs-el
Summary:	Elisp source files for Google protobuf Emacs mode
Group:		Development/Other
Requires:	protobuf-emacs = %{version}

%description emacs-el
This package contains the elisp source files for %{name}-emacs
under GNU Emacs. You do not need to install this package to use
%{name}-emacs.


%if %{with java}
%package java
Summary:	Java Protocol Buffers runtime library
Group:		Development/Java
BuildRequires:	java-devel >= 1.6
BuildRequires:	jpackage-utils
BuildRequires:  maven-local
BuildRequires:  mvn(com.google.code.gson:gson)
BuildRequires:  mvn(com.google.truth:truth)
BuildRequires:  mvn(com.google.guava:guava)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.easymock:easymock)
Requires:	java
Requires:	jpackage-utils
Provides:	mvn(com.google.protobuf:protobuf-java) = %{version}
Provides:	osgi(com.google.protobuf.java) = %{version}

%description java
This package contains Java Protocol Buffers runtime library.

%package java-util
Summary:        Utilities for Protocol Buffers
BuildArch:      noarch

%description java-util
Utilities to work with protos. It contains JSON support
as well as utilities to work with proto3 well-known types.

%package javadoc
Summary:	Javadocs for %{name}-java
Group:		Development/Java
Requires:	jpackage-utils
Requires:	%{name}-java = %{EVRD}

%description javadoc
This package contains the API documentation for %{name}-java.

%package javanano
Summary:        Protocol Buffer JavaNano API
BuildArch:      noarch

%description javanano
JavaNano is a special code generator and runtime
library designed specially for resource-restricted
systems, like Android.

%package parent
Summary:        Protocol Buffer Parent POM
BuildArch:      noarch

%description parent
Protocol Buffer Parent POM.

%endif

%prep
%setup -q
%patch0 -p1 -b .emacs
%if %{without gtest}
rm -rf gtest
%patch1 -p1 -b .gtest
%endif
chmod 644 examples/*
%if %{with java}
%pom_remove_parent java/pom.xml
%pom_remove_dep -r org.easymock:easymockclassextension java/
# Remove class using easymockclassextension
rm -f java/core/src/test/java/com/google/protobuf/ServiceTest.java

# used by https://github.com/googlei18n/libphonenumber
%pom_xpath_inject "pom:project/pom:modules" "<module>../javanano</module>" java/pom.xml
%pom_remove_parent javanano/pom.xml
%pom_remove_dep org.easymock:easymockclassextension javanano/pom.xml

%endif

%if %{with python2}
cp -ra python python2
%endif

%build
iconv -f iso8859-1 -t utf-8 CONTRIBUTORS.txt > CONTRIBUTORS.txt.utf8
mv CONTRIBUTORS.txt.utf8 CONTRIBUTORS.txt
export PTHREAD_LIBS="-lpthread"
./autogen.sh
%configure --disable-static

%make

%if %{with python}
pushd python
%{__python} ./setup.py build
sed -i -e 1d build/lib/google/protobuf/descriptor_pb2.py
popd
%endif

%if %{with python2}
pushd python2
%{__python2} ./setup.py build
sed -i -e 1d build/lib/google/protobuf/descriptor_pb2.py
popd
%endif

%if %{with java}
# Tests currently disabled because of mvn(com.google.truth:truth) dep -- needs to be packaged/updated first
%mvn_build -f -s -- -f java/pom.xml
%endif

emacs -batch -f batch-byte-compile editors/protobuf-mode.el

%check
#make %{?_smp_mflags} check

%install
rm -rf %{buildroot}
%makeinstall_std DESTDIR=%{buildroot} STRIPBINARIES=no INSTALL="%{__install} -p" CPPROG="cp -p"
find %{buildroot} -type f -name "*.la" -exec rm -f {} \;

%if %{with python}
pushd python
%{__python} ./setup.py install --skip-build --root=%{buildroot} --single-version-externally-managed --record=INSTALLED_FILES --optimize=1
popd
%endif
%if %{with python2}
pushd python2
%{__python2} ./setup.py install --skip-build --root=%{buildroot} --single-version-externally-managed --record=INSTALLED_FILES --optimize=1
popd
%endif
install -p -m 644 -D %{SOURCE1} %{buildroot}%{_datadir}/vim/vimfiles/ftdetect/proto.vim
install -p -m 644 -D editors/proto.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/proto.vim

%if %{with java}
%mvn_install
%endif

mkdir -p %{buildroot}%{emacs_lispdir}
mkdir -p %{buildroot}%{emacs_startdir}
install -p -m 0644 editors/protobuf-mode.el %{buildroot}%{emacs_lispdir}
install -p -m 0644 editors/protobuf-mode.elc %{buildroot}%{emacs_lispdir}
install -p -m 0644 %{SOURCE2} %{buildroot}%{emacs_startdir}

%files
%{_libdir}/libprotobuf.so.*
%doc CHANGES.txt CONTRIBUTORS.txt

%files compiler
%{_bindir}/protoc
%{_libdir}/libprotoc.so.*

%files devel
%dir %{_includedir}/google
%{_includedir}/google/protobuf/
%{_libdir}/libprotobuf.so
%{_libdir}/libprotoc.so
%{_libdir}/pkgconfig/protobuf.pc
%doc examples/add_person.cc examples/addressbook.proto examples/list_people.cc examples/Makefile examples/README.txt

%files lite
%{_libdir}/libprotobuf-lite.so.*

%files lite-devel
%{_libdir}/libprotobuf-lite.so
%{_libdir}/pkgconfig/protobuf-lite.pc


%if %{with python}
%files python
%dir %{py3_puresitedir}/google
%{py3_puresitedir}/google/protobuf/
%{py3_puresitedir}/protobuf-%{version}-py3.?.egg-info/
%{py3_puresitedir}/protobuf-%{version}-py3.?-nspkg.pth
%doc python/README.md
%doc examples/add_person.py examples/list_people.py examples/addressbook.proto
%endif

%if %{with python2}
%files python2
%dir %{py2_puresitedir}/google
%{py2_puresitedir}/google/protobuf/
%{py2_puresitedir}/protobuf-%{version}-py2.?.egg-info/
%{py2_puresitedir}/protobuf-%{version}-py2.?-nspkg.pth
%doc python2/README.md
%doc examples/add_person.py examples/list_people.py examples/addressbook.proto
%endif

%files vim
%{_datadir}/vim/vimfiles/ftdetect/proto.vim
%{_datadir}/vim/vimfiles/syntax/proto.vim

%files emacs
%{emacs_startdir}/protobuf-init.el
%{emacs_lispdir}/protobuf-mode.elc

%files emacs-el
%{emacs_lispdir}/protobuf-mode.el

%if %{with java}
%files java -f .mfiles-protobuf-java
%doc examples/AddPerson.java examples/ListPeople.java
%doc java/README.md
%doc LICENSE

%files java-util -f .mfiles-protobuf-java-util
%doc LICENSE

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%files javanano -f .mfiles-protobuf-javanano
%doc javanano/README.md
%doc LICENSE

%files parent -f .mfiles-protobuf-parent
%doc LICENSE
%endif
