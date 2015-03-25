#!/usr/bin/python
# -*- coding: latin-1 -*-
__author__ = 'cedric'
import urllib2, jsonpickle, copy, urllib
from datetime import datetime
from  time import mktime

class Importation:
    def __init__(self, adresseServeur):
        self.adresseServeur=adresseServeur
        self.data=[]

    def lancerImport(self):
        if "user.id" in self.data[0]:
            self.importUsers(self.data)
        elif "promotion.id" in self.data[0]:
            print("import promotion")
        elif "scheduling.date" in self.data[0]:
            self.importSchedulings(self.data)
        else:
            print("import room")

    def isPresent(self,tab,name):
        for liste in tab:
            if liste["name"] == name:
                return True
        return False

    def importSchedulings(self, liste):
        tabRooms=[]
        tabRoomsExistantes=[]
        for scheduling in liste:
            if not self.isPresent(tabRooms, scheduling["scheduling.room_id"]) and not self.isPresent(tabRoomsExistantes,scheduling["scheduling.room_id"]):
                url=self.adresseServeur+"rooms/?"+ urllib.urlencode({"name" : scheduling["scheduling.room_id"]})
                try:
                    room=urllib2.urlopen(url)
                    tabRoomsExistantes.append({"name" : scheduling["scheduling.room_id"], "add" : False})
                except urllib2.HTTPError as e:
                    if e.getcode() == 404:
                        tabRooms.append({"name" : scheduling["scheduling.room_id"]})
                    pass
        print(tabRooms)
        self.ajouterRooms(tabRooms)

        schedulings=[]
        rooms={}
        users={}
        for planning in liste:
            # planning={}
            scheduling={}
            planning["scheduling.date"]=str(planning["scheduling.date"]).split('. ')[1]
            # print planning["scheduling.date"]
            heures=str(planning["scheduling.heure"]).split(" / ")
            # print heures

            from_dateStart=planning["scheduling.date"]+ " " + heures[0]
            scheduling["date_start"] = str(mktime(datetime.strptime(from_dateStart,"%d/%m/%y %H:%M").timetuple()))
            from_dateEnd=planning["scheduling.date"] + " " + heures[1]
            scheduling["date_end"]= str(mktime(datetime.strptime(from_dateEnd,"%d/%m/%y %H:%M").timetuple()))

            if not planning["scheduling.room_id"] in rooms:
                rooms[planning["scheduling.room_id"]]=self.obtenirIdRoom(planning["scheduling.room_id"])
            scheduling["room_id"]=str(rooms[planning["scheduling.room_id"]])

            if not planning["scheduling.user_id"] in users:
                users[planning["scheduling.user_id"]]=self.obtenirIdUser(planning["scheduling.user_id"])
            scheduling["user_id"]=users[planning["scheduling.user_id"]]

            scheduling["promotion_id"]=planning["scheduling.promotion_id"]

            if planning.has_key("scheduling.course"):
                scheduling["course"] = planning["scheduling.course"]

            schedulings.append(scheduling)

        print(schedulings)
        self.ajouterSchedulings(schedulings)
        return

    def importUsers(self, liste):
        tabPromo=[]
        for utilisateur in liste:
            url=self.adresseServeur + "promotions/" + utilisateur["user.promotion_id"]
            req = urllib2.Request(url)
            try:
                promo=urllib2.urlopen(req)
                # print(promo.read())
            except urllib2.HTTPError as e:
                if e.getcode() == 404:
                    name=str(utilisateur["promotion.name"]).split(" ")
                    # print(name)
                    tabPromo.append({"id" : utilisateur["user.promotion_id"], "name" : name[0] + name[1]})
                    # print(tabPromo)
                pass
        self.ajouterPromotions(tabPromo)

        users=[]
        for utilisateur in liste:
            # utilisateur={}
            user={}
            # print(utilisateur)
            utilisateur["user.fullname"] = utilisateur["user.firstname"] + " " + utilisateur["user.name"]
            utilisateur["user.role"]="stagiaire"
            del utilisateur["user.name"]
            del utilisateur["user.firstname"]
            # print(utilisateur)
            for clef,valeur in utilisateur.items():
                key=str(clef).split('.')
                if key[0] == "user":
                    user[key[1]]=valeur
            # print user
            users.append(user)
        self.ajouterUsers(users)
        return

    def obtenirIdUser(self, nomUser):
        url=self.adresseServeur +"users/?"
        data=urllib.urlencode({"fullname":nomUser})
        try:
            resp=urllib2.urlopen(url+data)
            return jsonpickle.decode(resp.read())[0]["id"]
        except urllib2.HTTPError as e:
            if e.getcode() == 404:
                return ""
            pass

    def obtenirIdRoom(self, nomRoom):
        url=self.adresseServeur+"rooms/?"
        data=urllib.urlencode({"name":nomRoom})
        resp=urllib2.urlopen(url + data)
        return jsonpickle.decode(resp.read())[0]["id"]

    def ajouterTableauDonnees(self,tableau,url):
        req=urllib2.Request(url,tableau,{"content-type":"application/json"})
        resp=urllib2.urlopen(req)
        print(resp.read())

    def ajouterUsers(self,users):
        self.ajouterTableauDonnees(jsonpickle.encode(users),self.adresseServeur+"users/")

    def ajouterPromotions(self, promos):
        self.ajouterTableauDonnees(jsonpickle.encode(promos),self.adresseServeur+"promotions/")

    def ajouterRooms(self, rooms):
        self.ajouterTableauDonnees(jsonpickle.encode(rooms),self.adresseServeur+"rooms/")

    def ajouterSchedulings(self, schedulings):
        self.ajouterTableauDonnees(jsonpickle.encode(schedulings), self.adresseServeur+"schedulings/")

    def ajouterDonnees(self,ligne):
        self.data.append(copy.copy(ligne))