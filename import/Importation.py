#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'cedric'
import urllib2, jsonpickle, copy

class Importation:
    def __init__(self, adresseServeur):
        self.adresseServeur=adresseServeur
        self.data=[]

    def lancerImport(self):
        if "user.id" in self.data[0]:
            self.importUsers(self.data)
        elif "promotion.id" in self.data[0]:
            print "import promotion"
        elif "scheduling.*" in self.data[0]:
            print "import scheduling"
        else:
            print "import room"

    def importUsers(self, liste):
        tabPromo=[]
        for utilisateur in liste:
            url=self.adresseServeur + "promotions/" + utilisateur["user.promotion_id"]
            req = urllib2.Request(url)
            try:
                promo=urllib2.urlopen(req)
                print promo.read()
            except urllib2.HTTPError as e:
                if e.getcode() == 404:
                    name=str(utilisateur["promotion.name"]).split(" ")
                    print name
                    tabPromo.append({"id" : utilisateur["user.promotion_id"], "name" : name[0] + name[1]})
                    print tabPromo
                pass
        self.ajouterPromotions(tabPromo)

        users=[]
        for utilisateur in liste:
            user={}
            print utilisateur
            for clef,valeur in utilisateur.items():
                key=str(clef).split('.')
                if key[0] == "user":
                    user[key[1]]=valeur
            users.append(user)
        self.ajouterUsers(users)
        return

    def ajouterTableauDonnees(self,tableau,url):
        req=urllib2.Request(url,tableau,{"content-type":"application/json"})
        resp=urllib2.urlopen(req)
        print resp.read()

    def ajouterUsers(self,users):
        self.ajouterTableauDonnees(jsonpickle.encode(users),self.adresseServeur+"users/")

    def ajouterPromotions(self, promos):
        self.ajouterTableauDonnees(jsonpickle.encode(promos),self.adresseServeur+"promotions/")

    def ajouterDonnees(self,ligne):
        self.data.append(copy.copy(ligne))