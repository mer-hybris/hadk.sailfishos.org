# Do not generate empty debuginfo packages
%global debug_package %{nil}

Summary: Sailfish Hardware Adaptation Development Kit
Name: sailfish-hadk-doc
Version: 1.0.0
Release: 1
Source: %{name}-%{version}.tar.gz
BuildArch: noarch
URL: http://sailfishos.org/
License: TBD
Group: Documentation
BuildRequires: python-sphinx

%description
Documentation for building and porting Sailfish OS to new devices.

%prep
%setup -q

%build
# Inject RPM version into the Sphinx configuration file
sed -e "s/^version = '.*'/version = '%{version}'/" \
    -e "s/^release = '.*'/release = '%{version}-%{release}'/" \
    -i.bak conf.py

make html

# Revert RPM version injection after build has been done
mv conf.py.bak conf.py

%install
TARGET=%{buildroot}/%{_datadir}/doc/%{name}
mkdir -p $TARGET
cp -rpv _build/html/* $TARGET/

%files
%defattr(-,root,root,-)
%{_datadir}/doc/%{name}
