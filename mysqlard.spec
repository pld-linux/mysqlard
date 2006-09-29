# TODO:
# - prepare separate user to run the daemon
# - deamon should be in separate package
# - webapps framework
Summary:	MySQL performance logging daemon
Name:		mysqlard
Version:	1.0.0
Release:	0.1
License:	GPL v2
Group:		Applications/Databases
Source0:	http://gert.sos.be/downloads/mysqlar/%{name}-%{version}.tar.gz
# Source0-md5:	693ef6f36ca232131b22db7063cae940
URL:		http://www.sos.be/
Requires:	rrdtool
BuildRequires:	autoconf
BuildRequires:	automake
Buildrequires:	mysql-devel
Buildrequires:	rrdtool-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		_appdir		%{_datadir}/%{name}

%description
mysqlard daemon collects MySQL(TM) performance data in a Round Robin
Database. The package also contains example graphing and php scripts.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,cron.{daily,weekly,monthly}},%{_sysconfdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_appdir}/*.cnf $RPM_BUILD_ROOT%{_sysconfdir}
mv $RPM_BUILD_ROOT%{_appdir}/*.server $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
ln -s %{_sysconfdir}/init.d/mysqlard $RPM_BUILD_ROOT%{_sbindir}/rcmysqlard

mv $RPM_BUILD_ROOT%{_appdir}/mysqlar.daily $RPM_BUILD_ROOT/etc/cron.daily/%{name}
mv $RPM_BUILD_ROOT%{_appdir}/mysqlar.weekly $RPM_BUILD_ROOT/etc/cron.weekly/%{name}
mv $RPM_BUILD_ROOT%{_appdir}/mysqlar.monthly $RPM_BUILD_ROOT/etc/cron.monthly/%{name}
#install -d $RPM_BUILD_ROOT%{_appdir}/archive

# cleanup trash:
rm -f $RPM_BUILD_ROOT%{_appdir}/*.spec

%post
elif test -x /sbin/chkconfig
then
  /sbin/chkconfig --add mysqlard
fi

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
%dir %{_appdir}
%{_appdir}/*.gif
%{_appdir}/*.php
%{_appdir}/*.css
%{_mandir}/man1/*.1*
%{_mandir}/man8/*.8*
