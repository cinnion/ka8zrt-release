Name:           ka8zrt-release
Version:        0.5.1
Release:        1%{?dist}
Summary:        KA8ZRT local repository repo file and fixes for local mirroring.
BuildArch:      noarch

Group:          KA8ZRT/Base
License:        GPL
URL:            http://www.ka8zrt.com
Source0:        http://www.ka8zrt.com/ka8zrt-release-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(post): policycoreutils
Requires(post): sed

%description
This is a rpm for installing the local repos for KA8ZRT, and making
modifications to other repo files for repositories which are mirrored locally.

%prep
%autosetup -v

%install
pwd
ls -laR
rm -rf ${RPM_BUILD_ROOT}
install -D src/ka8zrt.repo ${RPM_BUILD_ROOT}/etc/yum.repos.d/ka8zrt.repo
%if 0%{?centos}
%define _distro "centos"
%else
%if 0%{?fedora}
%define _distro "fedora"
%endif
%endif
mkdir -p ${RPM_BUILD_ROOT}/etc/yum/vars
echo %{_distro} > ${RPM_BUILD_ROOT}/etc/yum/vars/os

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -e /etc/yum.repos.d/CentOS-Base.repo.orig ]
then
    logger --stderr --tag ka8zrt-release --priority info Fixing repo files for things mirrored locally.
    (cd /etc/yum.repos.d ; sed -e's|^mirrorlist|#mirrorlist|' -e's|^#baseurl|baseurl|' -e's|mirror.centos.org|mirror.ka8zrt.com|' --in-place=.orig CentOS-Base.repo )
fi

restorecon -R /etc/yum || :
restorecon -R /etc/yum.repos.d || :

%files
%defattr(644,root,root)
%config /etc/yum.repos.d/ka8zrt.repo
%config /etc/yum/vars/os

%doc

%changelog
* Sat Dec 01 2018 Douglas Needham <cinnion@gmail.com> 0.5.1-1
- new package built with tito
* Wed Nov 28 2018 Jenkins KA8ZRT <jenkins@ka8zrt.com> 0.5-1
- new package built with tito, pre-jenkins
* Sun Nov 11 2018 Douglas Needham <cinnion@gmail.com>
- ka8zrt-release 0.4.0 release
