#!/bin/bash
if [ "$(whoami)" != "root" ]; then
	echo "Ce script doit être lancé avec les droits administrateur."
	exit 1
else
	echo "You're a super admin motherfucker !"
	apt-get install mysql-client-5.5 > ./result.txt
	apt-get install python-pip >> ./result.txt
	apt-get install python-mysqldb >> ./result.txt
	pip install jsonpickle >> ./result.txt
	pip install flask >> ./result.txt
	pip install passlib >> ./result.txt
	cp ./APIPresenceManagement /etc/init.d/
	ln -s `pwd`/server.py /usr/bin/APIPresenceManagement
	ln -s `pwd`/relanceService.sh /usr/bin/relanceService
	echo "*/3 7-19 * * * root      cd / && /usr/bin/relanceService /usr/bin/APIPresenceManagement >> /var/log/relanceService" >> /etc/crontab
	chmod 755 /etc/init.d/APIPresenceManagement
	update-rc.d APIPresenceManagement defaults
fi
