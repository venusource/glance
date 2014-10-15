%define name glance
%define version 2014.1.dev3481.g3a3b3af
%define unmangled_version 2014.1.dev3481.g3a3b3af
%define unmangled_version 2014.1.dev3481.g3a3b3af
%define release vs1

Summary: OpenStack Image Service
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: ASL 2.0
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: OpenStack <openstack-dev@lists.openstack.org>


Requires:  MySQL-python 
Requires:  pysendfile 
Requires:  python(abi) = 2.6 
Requires:  python-cinderclient 
Requires:  python-crypto >= 2.6
Requires:  python-eventlet
Requires:  python-httplib2 
Requires:  python-iso8601 
Requires:  python-jsonschema 
Requires:  python-keystoneclient >= 1:0.7.0
Requires:  python-migrate 
Requires:  python-oslo-config >= 1:1.2.0 
Requires:  python-suds 
Requires:  python-oslo-messaging 
Requires:  python-paste-deploy >= 1.3.0 
Requires:  python-routes >= 1.10 
Requires:  python-swiftclient 
Requires:  python-webob >= 1.2 
Requires:  pyxattr 
Requires:  rpmlib(CompressedFileNames) <= 3.0.4-1 
Requires:  rpmlib(FileDigests) <= 4.6.0-1 
Requires:  rpmlib(PartialHardlinkSets) <= 4.0.4-1 
Requires:  rpmlib(PayloadFilesHavePrefix) <= 4.0-1 
Requires:  rpmlib(PayloadIsXz) <= 5.2-1 
Requires:  initscripts 
Requires:  openstack-utils 
Requires:  shadow-utils 
Requires:  chkconfig 
Requires:  python-glanceclient >= 1:0 
Requires:  python-pbr 
Requires:  gmp 
Requires:  git
Requires:  python-oslo-vmware
Requires:  python-sqlalchemy >= 0.8.0
Url: http://www.openstack.org/

%description
======
Glance
======

Glance is a project that defines services for discovering, registering,
retrieving and storing virtual machine images. Use the following resources
to learn more:

* `Official Glance documentation <http://docs.openstack.org/developer/glance/>`_
* `Official Client documentation <http://docs.openstack.org/developer/python-glanceclient/>`_



%prep
%setup -n %{name}-%{unmangled_version}

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT


%{__python} setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{python_sitelib}/glance
install -d -m 755 $RPM_BUILD_ROOT%{python_sitelib}/glance-2014.1.2.dev3481.g3a3b3af-py2.6.egg-info

install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/glance
install -d -m 755 $RPM_BUILD_ROOT%{_sharedstatedir}/glance/images

install -p -D -m 640 etc/glance-api.conf $RPM_BUILD_ROOT%{_sysconfdir}/glance/glance-api.conf
install -p -D -m 644 etc/glance-api-paste.ini $RPM_BUILD_ROOT%{_sysconfdir}/glance/glance-api-paste.ini
install -p -D -m 640 etc/glance-registry.conf $RPM_BUILD_ROOT%{_sysconfdir}/glance/glance-registry.conf
install -p -D -m 644 etc/glance-registry-paste.ini $RPM_BUILD_ROOT%{_sysconfdir}/glance/glance-registry-paste.ini
install -p -D -m 640 etc/glance-cache.conf $RPM_BUILD_ROOT%{_sysconfdir}/glance/glance-cache.conf
install -p -D -m 640 etc/glance-scrubber.conf $RPM_BUILD_ROOT%{_sysconfdir}/glance/glance-scrubber.conf

install -p -D -m 640 etc/policy.json $RPM_BUILD_ROOT%{_sysconfdir}/glance/policy.json
install -p -D -m 640 etc/schema-image.json $RPM_BUILD_ROOT%{_sysconfdir}/glance/schema-image.json

install -p -D -m 755 etc/setup-scripts/openstack-glance-api $RPM_BUILD_ROOT%{_initrddir}/openstack-glance-api
install -p -D -m 755 etc/setup-scripts/openstack-glance-registry $RPM_BUILD_ROOT%{_initrddir}/openstack-glance-registry
install -p -D -m 755 etc/setup-scripts/openstack-glance-scrubber $RPM_BUILD_ROOT%{_initrddir}/openstack-glance-scrubber

install -p -D -m 644 etc/glance-api-paste.ini $RPM_BUILD_ROOT%{_datadir}/glance/glance-api-dist-paste.ini
install -p -D -m 644 etc/glance-registry-paste.ini $RPM_BUILD_ROOT%{_datadir}/glance/glance-registry-dist-paste.ini
install -p -D -m 644 etc/glance-api-dist.conf $RPM_BUILD_ROOT%{_datadir}/glance/glance-api-dist.conf
install -p -D -m 644 etc/glance-registry-dist.conf $RPM_BUILD_ROOT%{_datadir}/glance/glance-registry-dist.conf
install -p -D -m 644 etc/glance-scrubber-dist.conf $RPM_BUILD_ROOT%{_datadir}/glance/glance-scrubber-dist.conf
install -p -D -m 644 etc/glance-cache-dist.conf $RPM_BUILD_ROOT%{_datadir}/glance/glance-cache-dist.conf
install -p -D -m 644 etc/openstack-glance-api.upstart $RPM_BUILD_ROOT%{_datadir}/glance/openstack-glance-api.upstart
install -p -D -m 644 etc/openstack-glance-registry.upstart $RPM_BUILD_ROOT%{_datadir}/glance/openstack-glance-registry.upstart
install -p -D -m 644 etc/openstack-glance-scrubber.upstart $RPM_BUILD_ROOT%{_datadir}/glance/openstack-glance-scrubber.upstart

install -d -m 755 $RPM_BUILD_ROOT%{_localstatedir}/run/glance
install -d -m 755 $RPM_BUILD_ROOT%{_localstatedir}/log/glance

%clean
rm -rf $RPM_BUILD_ROOT



%pre
getent group glance >/dev/null || groupadd -r glance -g 161
getent passwd glance >/dev/null || \
useradd -u 161 -r -g glance -d %{_sharedstatedir}/glance -s /sbin/nologin \
-c "OpenStack Glance Daemons" glance
exit 0

%post


/sbin/chkconfig --add openstack-glance-api
/sbin/chkconfig --add openstack-glance-registry
/sbin/chkconfig --add openstack-glance-scrubber

%files
%doc README.rst
%{_bindir}/glance-api
%{_bindir}/glance-control
%{_bindir}/glance-manage
%{_bindir}/glance-registry
%{_bindir}/glance-cache-cleaner
%{_bindir}/glance-cache-manage
%{_bindir}/glance-cache-prefetcher
%{_bindir}/glance-cache-pruner
%{_bindir}/glance-scrubber
%{_bindir}/glance-replicator
%{_initrddir}/openstack-glance-api
%{_initrddir}/openstack-glance-registry
%{_initrddir}/openstack-glance-scrubber
%dir %{_datadir}/glance
%{_datadir}/glance/openstack-glance-api.upstart
%{_datadir}/glance/openstack-glance-registry.upstart
%{_datadir}/glance/openstack-glance-scrubber.upstart

%{_datadir}/glance/glance-api-dist.conf
%{_datadir}/glance/glance-registry-dist.conf
%{_datadir}/glance/glance-cache-dist.conf
%{_datadir}/glance/glance-scrubber-dist.conf
%{_datadir}/glance/glance-api-dist-paste.ini
%{_datadir}/glance/glance-registry-dist-paste.ini

%dir %{_sysconfdir}/glance
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-api.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-registry.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-cache.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-scrubber.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/policy.json
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/schema-image.json
%dir %attr(0755, glance, nobody) %{_sharedstatedir}/glance
%dir %attr(0755, glance, nobody) %{_localstatedir}/log/glance
%dir %attr(0755, glance, nobody) %{_localstatedir}/run/glance
%{python_sitelib}/glance
%{python_sitelib}/glance-%{version}*.egg-info
   /etc/glance/glance-api-paste.ini
   /etc/glance/glance-registry-paste.ini
   /usr/local/etc/glance-api-dist.conf
   /usr/local/etc/glance-api-paste.ini
   /usr/local/etc/glance-api.conf
   /usr/local/etc/glance-cache-dist.conf
   /usr/local/etc/glance-cache.conf
   /usr/local/etc/glance-registry-dist.conf
   /usr/local/etc/glance-registry-paste.ini
   /usr/local/etc/glance-registry.conf
   /usr/local/etc/glance-scrubber-dist.conf
   /usr/local/etc/glance-scrubber.conf
   /usr/local/etc/logging.cnf.sample
   /usr/local/etc/openstack-glance-api.upstart
   /usr/local/etc/openstack-glance-registry.upstart
   /usr/local/etc/openstack-glance-scrubber.upstart
   /usr/local/etc/policy.json
   /usr/local/etc/property-protections-policies.conf.sample
   /usr/local/etc/property-protections-roles.conf.sample
   /usr/local/etc/schema-image.json
   /usr/local/etc/setup-scripts/openstack-glance-api
   /usr/local/etc/setup-scripts/openstack-glance-registry
   /usr/local/etc/setup-scripts/openstack-glance-scrubber
%defattr(-,root,root,-)
