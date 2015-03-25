#!/usr/bin/python
# -*- coding: utf-8 -*-
import __future__
__author__ = 'cedric'
import configparser
import csv
import unicodedata
from Importation import Importation
from sys import argv

def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

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

#print open("lectureExport.cfg","r")
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
        "de la date l'entrée du planning : " : 'scheduling.date',
        "de l'heure de l'entrée du planning : " : 'scheduling.heure',
        "de la salle de l'entrée du planning : " : 'scheduling.room_id',
        "de la promo pour l'entrée du planning : " : 'scheduling.promotion_id',
        "de l'identifiant de l'intervenant de l'entrée du planning : " : 'scheduling.user_id',
        "de la matière de l'entrée du planning : " : 'scheduling.course',
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
if len(argv) == 1:
    nomFichier="seancesDebut.csv"
else:
    nomFichier=argv[1]

cr = csv.reader(open(nomFichier,"rb"))
map={}
pos={}
champsImportes={}
promo=0
importation = Importation(configuration.get("autres","adresseserveur"))
for row in cr:
    if pos == {}:
        if len(row) > 1:
            index=0
            for nomChamps in row:
                nomChamps = remove_accents(nomChamps.decode("utf-8"))
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
            pos["scheduling.date"] =mappageConfig("scheduling.date",map)
            pos["scheduling.heure"]=mappageConfig("scheduling.heure",map)
            pos["scheduling.room_id"]=mappageConfig("scheduling.room_id",map)
            pos["scheduling.promotion_id"]=mappageConfig("scheduling.promotion_id",map)
            pos["scheduling.user_id"]=mappageConfig("scheduling.user_id",map)
            pos["scheduling.course"]=mappageConfig("scheduling.course", map)
        else:
            promo=row[0]
    else:
        for clef,valeur in pos.items():
            if valeur <> -1:
                champsImportes[clef]="%s"%(remove_accents(row[valeur].decode("utf-8")))
        if promo <> 0:
            champsImportes["scheduling.promotion_id"]=promo
        # print champsImportes
        importation.ajouterDonnees(champsImportes)
        champsImportes.clear()

importation.lancerImport()