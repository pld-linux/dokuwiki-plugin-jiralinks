%define		subver	2014-11-12
%define		ver		%(echo %{subver} | tr -d -)
%define		plugin		jiralinks
%define		php_min_version 5.2.0
%include	/usr/lib/rpm/macros.php
Summary:	DokuWiki Jira-links Plugin
Name:		dokuwiki-plugin-%{plugin}
Version:	%{ver}
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	https://github.com/meteotest/jiralinks/archive/%{subver}/%{plugin}-%{subver}.tar.gz
# Source0-md5:	301160d33f93ecb55650389c99a68f9f
URL:		https://www.dokuwiki.org/plugin:jiralinks
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	dokuwiki >= 20131208
Requires:	php(core) >= %{php_min_version}
Requires:	php(curl)
Requires:	php(json)
Requires:	php(pcre)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}
%define		find_lang 	%{_usrlibrpm}/dokuwiki-find-lang.sh %{buildroot}

%description
This plugin adds links back and forth between DokuWiki and the
bugtracking software Jira by Atlassian.

%prep
%setup -q -n %{plugin}-%{subver}

%build
version=$(awk '/^date/{print $2}' plugin.info.txt)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}
%{__rm} $RPM_BUILD_ROOT%{plugindir}/{README.md,.gitignore}

%find_lang %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
# force js/css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.md
%dir %{plugindir}
%{plugindir}/*.css
%{plugindir}/*.php
%{plugindir}/*.txt
%{plugindir}/conf
%{plugindir}/images
