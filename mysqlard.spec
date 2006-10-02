# TODO:
# - prepare separate user to run the daemon (mysqlar)
# - webapps framework: lighttpd
# - switch init-script to be PLD-like
# - patch default config to put rrd's and images to /var, not %{_appdir}
Summary:	MySQL performance logging daemon
Name:		mysqlard
Version:	1.0.0
Release:	0.4
License:	GPL v2
Group:		Applications/Databases
Source0:	http://gert.sos.be/downloads/mysqlar/%{name}-%{version}.tar.gz
# Source0-md5:	693ef6f36ca232131b22db7063cae940
Source1:	%{name}.conf
Patch0:		%{name}-use_mysqlar_user.patch
URL:		http://gert.sos.be/
Requires:	rrdtool
BuildRequires:	autoconf
BuildRequires:	automake
Buildrequires:	mysql-devel
Buildrequires:	rrdtool-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		_appdir		%{_datadir}/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_webappconfdir	%{_webapps}/%{_webapp}
%define		_pkglibdir	/var/lib/%{name}


%description
mysqlard daemon collects MySQL(TM) performance data in a Round Robin
Database. The package also contains example graphing and php scripts.

%package php
Summary:	PHP interface for %{name}
Summary(pl):	Interfejs PHP dla %{name}
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:       php-mysql
Requires:       webapps

%description php
PHP interface for %{name}.

%description php -l pl
Interfejs PHP dla %{name}.

%prep
%setup -q
%patch0 -p1

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,cron.{daily,weekly,monthly}},%{_sysconfdir}} \
	$RPM_BUILD_ROOT%{_webappconfdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_appdir}/*.cnf $RPM_BUILD_ROOT%{_sysconfdir}
mv $RPM_BUILD_ROOT%{_appdir}/*.server $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
ln -s %{_sysconfdir}/init.d/mysqlard $RPM_BUILD_ROOT%{_sbindir}/rcmysqlard

mv $RPM_BUILD_ROOT%{_appdir}/mysqlar.daily $RPM_BUILD_ROOT/etc/cron.daily/%{name}
mv $RPM_BUILD_ROOT%{_appdir}/mysqlar.weekly $RPM_BUILD_ROOT/etc/cron.weekly/%{name}
mv $RPM_BUILD_ROOT%{_appdir}/mysqlar.monthly $RPM_BUILD_ROOT/etc/cron.monthly/%{name}
#install -d $RPM_BUILD_ROOT%{_appdir}/archive

install %{SOURCE1} $RPM_BUILD_ROOT%{_webappconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_webappconfdir}/httpd.conf

# cleanup trash:
rm -f $RPM_BUILD_ROOT%{_appdir}/*.spec

%triggerin php -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun php -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin php -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun php -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.*/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{_bindir}/mysqlar_graph
%{_sbindir}/%{name}
%{_mandir}/man1/*.1*
%{_mandir}/man8/*.8*

%files php
%defattr(644,root,root,755)
%dir %attr(750,root,http) %{_webapps}/%{_webapp}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/httpd.conf
%dir %{_appdir}
%{_appdir}/*.gif
%{_appdir}/*.php
%{_appdir}/*.css
