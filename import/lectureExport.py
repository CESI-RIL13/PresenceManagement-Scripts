#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'cedric'
import configparser
import csv
from Importation import Importation
from sys import argv

def creerConfig(configuration, prompt, champs, section="nomChamps"):
    configuration.set(section, champs, raw_input(prompt))

def getNomConfig(config, value, section = "nomChamps"):
    # config=configparser.RawConfigParser()
    for item in config.items(section):
        if item[1] == value:
            return item[0]
    return None

def mappageConfig(nomConfig, map):
    return map[nomConfig] if nomConfig in map else -1

configuration=configparser.RawConfigParser()
configuration.read("lectureExport.cfg")
complete= configuration.has_section("nomChamps") and configuration.has_section("autres")

if not complete:
    beginPrompt="Entrer le nom du champs "
    configuration.add_section("nomChamps")
    configuration.add_section("autres")
    clefsConfiguration={
        "de l'identifiant de l'utilisateur : " : 'user.id',
        "du nom de l'utilisateur : " : 'user.name',
        "du prénom de l'utilisateur : " : 'user.firstname',
        "de l'adresse mail de l'utilisateur : " : 'user.mail',
        "de l'identifiant de la promotion de l'utilisateur : " : 'user.promotion_id',
        "de l'identifiant d'une promotion : " : 'promotion.id',
        "du nom de la promotion : " : 'promotion.name',
        "du nom de la salle : " : 'room.name',
        "de la date de début de l'entrée du planning : " : 'scheduling.date_start',
        "de la date de fin de l'entrée du planning : " : 'scheduling.date_end',
        "de la salle de l'entrée du planning : " : 'scheduling.room_id',
        "de la promo pour l'entrée du planning : " : 'scheduling.promotion_id',
        "de l'identifiant de l'intervenant de l'entrée du planning : " : 'scheduling.user_id',
        "Entrer l'adresse du serveur : " : "adresseserveur"
    }

    for prompt,champs in clefsConfiguration.items():
        if "." in champs:
            creerConfig(configuration, beginPrompt + prompt, champs)
        else:
            creerConfig(configuration, prompt,champs,"autres")

    # Writing our configuration file to 'lectureExport.cfg'
    with open('lectureExport.cfg', 'wb') as configfile:
        configuration.write(configfile)

URLSERVEUR=configuration.get("autres","adresseserveur")

nomFichier=""
if __debug__:
    nomFichier="structure export AD.csv"
else:
    nomFichier=argv[1]

cr = csv.reader(open(nomFichier,"rb"))
map={}
pos={}
champsImportes={}
importation = Importation(configuration.get("autres","adresseserveur"))
for row in cr:
    if pos == {}:
        index=0
        for nomChamps in row:
            if getNomConfig(configuration,nomChamps) <> None:
                map[getNomConfig(configuration,nomChamps)]=index
            index+=1
        pos["user.id"]=mappageConfig("user.id",map)
        pos["user.name"]=mappageConfig("user.name",map)
        pos["user.firstname"]= mappageConfig("user.firstname",map)
        pos["user.mail"]= mappageConfig("user.mail",map)
        pos["user.promotion_id"]=mappageConfig("user.promotion_id",map)
        pos["promotion.id"]=mappageConfig("promotion.id",map)
        pos["promotion.name"]= mappageConfig("promotion.name",map)
        pos["room.name"]=mappageConfig("room.name",map)
        pos["scheduling.date_start"] =mappageConfig("scheduling.date_start",map)
        pos["scheduling.date_end"]=mappageConfig("scheduling.date_end",map)
        pos["scheduling.room_id"]=mappageConfig("scheduling.room_id",map)
        pos["scheduling.promotion_id"]=mappageConfig("scheduling.promotion_id",map)
        pos["scheduling.user_id"]=mappageConfig("scheduling.user_id",map)
    else:
        for clef,valeur in pos.items():
            if valeur <> -1:
                champsImportes[clef]="%s"%(row[valeur])
        importation.ajouterDonnees(champsImportes)
        champsImportes.clear()

importation.lancerImport()