# TODO:
# - preun
# - webapps framework: lighttpd
Summary:	MySQL performance logging daemon
Summary(pl.UTF-8):   Demon logujący wydajność MySQL-a
Name:		mysqlard
Version:	1.0.0
Release:	1.6
License:	GPL v2
Group:		Applications/Databases
Source0:	http://gert.sos.be/downloads/mysqlar/%{name}-%{version}.tar.gz
# Source0-md5:	693ef6f36ca232131b22db7063cae940
Source1:	%{name}.conf
Source2:	%{name}.init
Source3:	%{name}.crontab
Source4:	%{name}.hourly
Patch0:		%{name}-use_mysqlar_user.patch
URL:		http://gert.sos.be/
BuildRequires:	autoconf
BuildRequires:	automake
Buildrequires:	mysql-devel
Buildrequires:	rrdtool-devel
Requires(post):	/sbin/chkconfig
Requires:	rc-scripts
Requires:	rrdtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		_appdir		%{_datadir}/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_webappconfdir	%{_webapps}/%{_webapp}
%define		_pkglibdir	/var/lib/%{name}

%description
mysqlard daemon collects MySQL(TM) performance data in a Round Robin
Database. The package also contains example graphing and PHP scripts.

%description -l pl.UTF-8
Demon mysqlard zbiera dane o wydajności MySQL-a w bazie danych RRD.
Pakiet zawiera także proste skrypty do wykresów i PHP.

%package php
Summary:	PHP interface for %{name}
Summary(pl.UTF-8):   Interfejs PHP dla mysqlarda
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	php(mysql)
Requires:	webapps

%description php
PHP interface for %{name}.

%description php -l pl.UTF-8
Interfejs PHP dla mysqlarda.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--localstatedir=%{_pkglibdir} \
	--datadir=/var/lib
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,cron.d},%{_sysconfdir}} \
	$RPM_BUILD_ROOT{%{_webappconfdir},%{_pkglibdir}/archive,%{_appdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_pkglibdir}/*.cnf $RPM_BUILD_ROOT%{_sysconfdir}
ln -s /etc/rc.d/init.d/mysqlard $RPM_BUILD_ROOT%{_sbindir}/rcmysqlard

mv $RPM_BUILD_ROOT%{_pkglibdir}/mysqlar.daily $RPM_BUILD_ROOT%{_sbindir}
mv $RPM_BUILD_ROOT%{_pkglibdir}/mysqlar.weekly $RPM_BUILD_ROOT%{_sbindir}
mv $RPM_BUILD_ROOT%{_pkglibdir}/mysqlar.monthly $RPM_BUILD_ROOT%{_sbindir}

# Move php-related things to %{_appdir}
mv $RPM_BUILD_ROOT%{_pkglibdir}/*.css $RPM_BUILD_ROOT%{_appdir}
mv $RPM_BUILD_ROOT%{_pkglibdir}/*.gif $RPM_BUILD_ROOT%{_appdir}
mv $RPM_BUILD_ROOT%{_pkglibdir}/*.php $RPM_BUILD_ROOT%{_appdir}

# make links for php-frontend:
for part in queries con tab tmptab key keybuf join range read slow slave slavec; do
	for time in hour day week month year; do
		ln -sf %{_pkglibdir}/$part-$time.png $RPM_BUILD_ROOT%{_appdir}
	done
done

install %{SOURCE1} $RPM_BUILD_ROOT%{_webappconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_webappconfdir}/httpd.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/cron.d/%{name}
install %{SOURCE4} $RPM_BUILD_ROOT%{_sbindir}/mysqlar.hourly

# cleanup trash:
rm -f $RPM_BUILD_ROOT%{_appdir}/*.spec
rm -f $RPM_BUILD_ROOT%{_pkglibdir}/*.server

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%triggerin php -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun php -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin php -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun php -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%dir %{_sysconfdir}
%attr(640,root,stats) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_bindir}/mysqlar_graph
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man1/*.1*
%{_mandir}/man8/*.8*
%attr(750,stats,http) %dir %{_pkglibdir}
%attr(750,stats,http) %dir %{_pkglibdir}/archive

%files php
%defattr(644,root,root,755)
%dir %attr(750,root,http) %{_webapps}/%{_webapp}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/httpd.conf
%dir %{_appdir}
%{_appdir}/*.gif
%{_appdir}/*.png
%{_appdir}/*.php
%{_appdir}/*.css
