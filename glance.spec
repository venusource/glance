%global release_name icehouse

Name:             openstack-glance
Version:          2014.1.1
Release:          1%{?dist}
Summary:          OpenStack Image Service

Group:            Applications/System
License:          ASL 2.0
URL:              http://glance.openstack.org
Source0:          glance-%{version}.tar.gz
Source1:          openstack-glance-api.init
Source100:        openstack-glance-api.upstart
Source2:          openstack-glance-registry.init
Source200:        openstack-glance-registry.upstart
Source3:          openstack-glance-scrubber.init
Source300:        openstack-glance-scrubber.upstart
Source4:          openstack-glance.logrotate

Source5:          glance-api-dist.conf
Source6:          glance-registry-dist.conf
Source7:          glance-cache-dist.conf
Source8:          glance-scrubber-dist.conf

#
# patches_base=2014.1.1
#
Patch0001: 0001-Don-t-access-the-net-while-building-docs.patch
Patch0002: 0002-Use-updated-parallel-install-versions-of-epel-packag.patch
Patch0003: 0003-avoid-the-uneeded-dependency-on-Crypto.Random.patch
Patch0004: 0004-Avoid-NULLs-in-crypto-padding.patch
Patch0005: 0005-Remove-runtime-dep-on-python-pbr.patch
Patch0006: 0006-avoid-unsupported-storage-drivers.patch
Patch0007: 0007-notify-calling-process-we-are-ready-to-serve.patch

BuildArch:        noarch
BuildRequires:    python2-devel
BuildRequires:    python-setuptools
BuildRequires:    intltool
# These are required to build due to the requirements check added
BuildRequires:    python-paste-deploy1.5
BuildRequires:    python-routes1.12
BuildRequires:    python-sqlalchemy0.7
BuildRequires:    python-webob1.2
BuildRequires:    python-pbr
BuildRequires:    python-oslo-sphinx

Requires(post):   chkconfig
Requires(preun):  initscripts
Requires(preun):  chkconfig
Requires(pre):    shadow-utils
Requires:         python-glance = %{version}-%{release}
Requires:         python-glanceclient >= 1:0
Requires:         openstack-utils

%description
OpenStack Image Service (code-named Glance) provides discovery, registration,
and delivery services for virtual disk images. The Image Service API server
provides a standard REST interface for querying information about virtual disk
images stored in a variety of back-end stores, including OpenStack Object
Storage. Clients can register new virtual disk images with the Image Service,
query for information on publicly available disk images, and use the Image
Service's client library for streaming virtual disk images.

This package contains the API and registry servers.

%package -n       python-glance
Summary:          Glance Python libraries
Group:            Applications/System

Requires:         MySQL-python
Requires:         pysendfile
Requires:         python-eventlet
Requires:         python-httplib2
Requires:         python-iso8601
Requires:         python-jsonschema
Requires:         python-migrate
Requires:         python-paste-deploy1.5
Requires:         python-routes1.12
Requires:         python-sqlalchemy0.7
Requires:         python-webob1.2
Requires:         python-crypto
Requires:         pyxattr
Requires:         python-swiftclient
Requires:         python-cinderclient
Requires:         python-keystoneclient
Requires:         python-oslo-config >= 1:1.2.0
Requires:         python-oslo-messaging

#test deps: python-mox python-nose python-requests
#test and optional store:
#ceph - glance.store.rdb
#python-boto - glance.store.s3

%description -n   python-glance
OpenStack Image Service (code-named Glance) provides discovery, registration,
and delivery services for virtual disk images.

This package contains the glance Python library.

%package doc
Summary:          Documentation for OpenStack Image Service
Group:            Documentation

Requires:         %{name} = %{version}-%{release}

BuildRequires:    python-sphinx
BuildRequires:    graphviz

# Required to build module documents
BuildRequires:    python-boto
BuildRequires:    python-eventlet

%description      doc
OpenStack Image Service (code-named Glance) provides discovery, registration,
and delivery services for virtual disk images.

This package contains documentation files for glance.

%prep
%setup -q -n glance-%{version}

%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1
%patch0007 -p1


# Remove bundled egg-info
rm -rf glance.egg-info
sed -i '/\/usr\/bin\/env python/d' glance/common/config.py glance/common/crypt.py glance/db/sqlalchemy/migrate_repo/manage.py
# versioninfo is missing in f3 tarball
echo %{version} > glance/versioninfo

sed -i '/setuptools_git/d' setup.py
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py
sed -i s/REDHATGLANCEVERSION/%{version}/ glance/version.py
sed -i s/REDHATGLANCERELEASE/%{release}/ glance/version.py

# make doc build compatible with python-oslo-sphinx RPM
sed -i 's/oslosphinx/oslo.sphinx/' doc/source/conf.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requiers_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

# Programmatically update defaults in example config
api_dist=%{SOURCE5}
registry_dist=%{SOURCE6}
cache_dist=%{SOURCE7}
scrubber_dist=%{SOURCE8}
for svc in api registry cache scrubber; do
  #  First we ensure all values are commented in appropriate format.
  #  Since icehouse, there was an uncommented keystone_authtoken section
  #  at the end of the file which mimics but also conflicted with our
  #  distro editing that had been done for many releases.
  sed -i '/^[^#[]/{s/^/#/; s/ //g}; /^#[^ ]/s/ = /=/' etc/glance-$svc.conf

  #  TODO: Make this more robust
  #  Note it only edits the first occurance, so assumes a section ordering in sample
  #  and also doesn't support multi-valued variables like dhcpbridge_flagfile.
  eval dist_conf=\$${svc}_dist
  while read name eq value; do
    test "$name" && test "$value" || continue
    sed -i "0,/^# *$name=/{s!^# *$name=.*!#$name=$value!}" etc/glance-$svc.conf
  done < $dist_conf
done

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/glance/tests

# Drop old glance CLI it has been deprecated
# and replaced glanceclient
rm -f %{buildroot}%{_bindir}/glance

export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html source build/html
sphinx-build -b man source build/man

mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 build/man/*.1 %{buildroot}%{_mandir}/man1/
popd

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
rm -f %{buildroot}%{_sysconfdir}/glance*.conf
rm -f %{buildroot}%{_sysconfdir}/glance*.ini
rm -f %{buildroot}%{_sysconfdir}/logging.cnf.sample
rm -f %{buildroot}%{_sysconfdir}/policy.json
rm -f %{buildroot}%{_sysconfdir}/schema-image.json
rm -f %{buildroot}/usr/share/doc/glance/README.rst

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/glance
install -d -m 755 %{buildroot}%{_sharedstatedir}/glance/images

# Config file
install -p -D -m 640 etc/glance-api.conf %{buildroot}%{_sysconfdir}/glance/glance-api.conf
install -p -D -m 644 %{SOURCE5} %{buildroot}%{_datadir}/glance/glance-api-dist.conf
install -p -D -m 644 etc/glance-api-paste.ini %{buildroot}%{_datadir}/glance/glance-api-dist-paste.ini
install -p -D -m 640 etc/glance-registry.conf %{buildroot}%{_sysconfdir}/glance/glance-registry.conf
install -p -D -m 644 %{SOURCE6} %{buildroot}%{_datadir}/glance/glance-registry-dist.conf
install -p -D -m 644 etc/glance-registry-paste.ini %{buildroot}%{_datadir}/glance/glance-registry-dist-paste.ini
install -p -D -m 640 etc/glance-cache.conf %{buildroot}%{_sysconfdir}/glance/glance-cache.conf
install -p -D -m 644 %{SOURCE7} %{buildroot}%{_datadir}/glance/glance-cache-dist.conf
install -p -D -m 640 etc/glance-scrubber.conf %{buildroot}%{_sysconfdir}/glance/glance-scrubber.conf
install -p -D -m 644 %{SOURCE8} %{buildroot}%{_datadir}/glance/glance-scrubber-dist.conf

install -p -D -m 640 etc/policy.json %{buildroot}%{_sysconfdir}/glance/policy.json
install -p -D -m 640 etc/schema-image.json %{buildroot}%{_sysconfdir}/glance/schema-image.json

# Initscripts
install -p -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/openstack-glance-api
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/openstack-glance-registry
install -p -D -m 755 %{SOURCE3} %{buildroot}%{_initrddir}/openstack-glance-scrubber

# Install upstart jobs examples
install -p -m 644 %{SOURCE100} %{buildroot}%{_datadir}/glance/
install -p -m 644 %{SOURCE200} %{buildroot}%{_datadir}/glance/
install -p -m 644 %{SOURCE300} %{buildroot}%{_datadir}/glance/

# Logrotate config
install -p -D -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-glance

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/glance

# Install log directory
install -d -m 755 %{buildroot}%{_localstatedir}/log/glance

# Programmatically update defaults in sample config
# which is installed at /etc/$project/$program.conf
# TODO: Make this more robust
# Note it only edits the first occurance, so assumes a section ordering in sample
# and also doesn't support multi-valued variables.
for svc in api registry cache scrubber; do
  cfg=%{buildroot}%{_sysconfdir}/glance/glance-$svc.conf
  test -e $cfg || continue
  while read name eq value; do
    test "$name" && test "$value" || continue
    # Note some values in upstream glance config may not be commented
    # and if not, they might not match the default value in code.
    # So we comment out both froms to have dist config take precedence.
    sed -i "0,/^#* *$name *=/{s!^#* *$name *=.*!#$name=$value!}" $cfg
  done < %{buildroot}%{_datadir}/glance/glance-$svc-dist.conf
done

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

%preun
if [ $1 = 0 ] ; then
    /sbin/service openstack-glance-api stop >/dev/null 2>&1
    /sbin/chkconfig --del openstack-glance-api
    /sbin/service openstack-glance-registry stop >/dev/null 2>&1
    /sbin/chkconfig --del openstack-glance-registry
    /sbin/service openstack-glance-scrubber stop >/dev/null 2>&1
    /sbin/chkconfig --del openstack-glance-scrubber
fi

%postun
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in api registry scrubber; do
        /sbin/service openstack-glance-${svc} condrestart > /dev/null 2>&1 || :
    done
fi

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

%{_mandir}/man1/glance*.1.gz
%dir %{_sysconfdir}/glance
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-api.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-registry.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-cache.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-scrubber.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/policy.json
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/schema-image.json
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/logrotate.d/openstack-glance
%dir %attr(0755, glance, nobody) %{_sharedstatedir}/glance
%dir %attr(0755, glance, nobody) %{_localstatedir}/log/glance
%dir %attr(0755, glance, nobody) %{_localstatedir}/run/glance

%files -n python-glance
%doc README.rst
%{python_sitelib}/glance
%{python_sitelib}/glance-%{version}*.egg-info


%files doc
%doc doc/build/html
