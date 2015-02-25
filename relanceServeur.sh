#!/bin/bash
while [ 1 = 1 ]; do
	# chemin du serveur
	process="/usr/bin/monserveur"
	# recherche parmis les processus en cours le process en excluant la chaine "grep"
	ps ax | grep $process | grep -v grep
	# si il y a un résultat
	if [ $? -eq 0 ]; then
		echo "le script est actuellement en train de tourner"
	else 
		/etc/init.d/monserveur stop
		/etc/init.d/monserveur start
	fi
	sleep 5
done
