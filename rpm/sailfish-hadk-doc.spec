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
make html

%install
TARGET=%{buildroot}/%{_datadir}/%{name}
mkdir -p $TARGET
cp -rpv _build/html/* $TARGET/

%files
%defattr(-,root,root,-)
%{_datadir}/%{name}
