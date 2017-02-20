Name:		rapidpatch
Version:	0.1
Release:	4%{?dist}
Summary:	 Tools to make creating patch faster 

Group:		Development/Tools
License:	MIT
URL:		https://github.com/hhorak/rapidpatch
Source0:	rapidpatch
Source1:	README.md
Source2:	LICENSE
Source3:	rpmdev-spec-sections
Source4:	template-rapidpatch-x86_64.cfg

BuildArch:	noarch

Requires:	mock
Requires:	rpmdevtools

%description
Helper tool for creating patch for a package and check whether it compiles,
that all with strong focus on effectivity. The tool generates a mock config,
prepares directory for dependencies available only locally, allows to create
patch from unpacked source easily. The tool also allows to run only specific
section (or part of it) of the RPM Spec file, which makes the whole testing
faster, especially in case of large projects, that compile long time.
The tool also supports test-driven development, so ideally packager writes
a simple test before writing the patch.

%prep
%setup -cT
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} .

%build

%install
mkdir -p %{buildroot}%{_bindir}
cp rapidpatch %{buildroot}%{_bindir}/${name}
cp rpmdev-spec-sections %{buildroot}%{_bindir}/rpmdev-spec-sections

mkdir -p %{buildroot}%{_datadir}/%{name}
cp template-rapidpatch-x86_64.cfg %{buildroot}%{_datadir}/%{name}

%files
%doc README.md LICENSE
%{_bindir}/%{name}
%{_bindir}/rpmdev-spec-sections
%{_datadir}/%{name}

%changelog
* Mon Feb 20 2017 Honza Horak <hhorak@redhat.com> - 0.1-4
- Crash sanely in case not run in dist-git directory

* Mon Feb 20 2017 Honza Horak <hhorak@redhat.com> - 0.1-3
- Fix few packaging issues

* Sun Feb 19 2017 Honza Horak <hhorak@redhat.com> - 0.1-2
- Initial packaging
