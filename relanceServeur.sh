#!/bin/bash
# chemin du serveur
process=$1
if [ -e $process ]; then
	while [ 1 = 1 ]; do
		# recherche parmis les processus en cours le process en excluant la chaine "grep"
		ps ax | grep $process | grep -v grep | grep -v $0
		# si il y a un résultat
		if [ $? -eq 0 ]; then
			echo "le script est actuellement en train de tourner"
		else 
			/etc/init.d/monserveur restart
		fi
		sleep 5
	done
else
	echo $1 + "n'existe pas"
fi
