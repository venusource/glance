INSTALL_ENV=`python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`
[ -d ${INSTALL_ENV}/glance ] || mkdir -p ${INSTALL_ENV}/glance
cp -rf /usr/share/glance* ${INSTALL_ENV}/
cp -rf /usr/local/etc/setup-scripts/openstack-glance* /etc/init.d
cp  /usr/local/etc/setup-scripts/openstack-glance* /etc/rc.d/init.d/

[ -d /etc/glance ] || mkdir /etc/glance
cp /usr/local/etc/* /etc/glance
 
if [ -f /etc/glance/glance.conf.sample ];then
mv -f /etc/glance/glance.conf.sample /etc/glance/glance.conf
fi

groupadd -g 161 glance 2>/dev/null
useradd -u 161 -g glance -c "OpenStack Glance Daemons" -d /var/lib/glance -s /sbin/nologin glance 2>/dev/null

[ -d /var/lib/glance ] || mkdir /var/lib/glance
[ -d /var/log/glance ] || mkdir /var/log/glance
[ -d /var/run/glance ] || mkdir /var/run/glance

chown -R glance:glance /var/lib/glance
chown -R glance:glance /var/log/glance
chown -R glance:glance /var/run/glance
