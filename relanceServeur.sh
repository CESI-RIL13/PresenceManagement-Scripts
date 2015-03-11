#!/bin/bash
# chemin du serveur
process=$1
if [ -e $process ]; then	
	# recherche parmis les processus en cours le process en excluant la chaine "grep"
	ps ax | grep $process | grep -v grep | grep -v $0
	# si il y a un résultat
	if [ $? -eq 0 ]; then
		nbLigne= ps ax | grep $process | grep -v grep | grep -v $0 | wc -l
		if [ $nbLigne -le 1 ]; then
			/etc/init.d/monserveur start
		else
			echo "le script est actuellement en train de tourner"
		fi
	else 
		/etc/init.d/monserveur start
	fi
else
	echo $1 + "n'existe pas"
fi
