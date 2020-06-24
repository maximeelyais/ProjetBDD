#!/usr/bin/python3
# encoding=utf8

import requests,csv
import pymysql as mariadb
from getpass import getpass

#TODO: install mysql & requests modules
#if there's an encoding problem: export PYTHONIOENCODING=utf-8

"""
README:

Ce script permet de se connecter à une base de données à distance en utilisant un nom d'utlisateur et un mot de passe. 
Une fois connecté, il télécharge un fichier CSV contenant les données à insérer dans la base. 
Il parcours ensuite chaque ligne du csv et traite les colonnes afin d'insérer les bonnes valeurs.

Concernat les erreurs liées à l'OS, j'en ai relevé 2:
		- Erreur d'encodage des caractères accentués: Car l'encodage par défaut est 'ASCII'. Pour résoudre ce problème, il suffit d'ajouter cette variable à l'environnemnt PYTHONIOENCODING=utf-8.
													 * Pour Linux: export PYTHONIOENCODING=utf-8
													 * Pour Windows Ouvrir la liste des variables d'environnements depuis les paramètres Windows et ajouter PYTHONIOENCODING=utf-8

		- Erreur du module mysql: Il existe plusieurs module sql pour python. Dans ce script, c'est pymysql qui est utilisé. Il faut donc l'installer avant d'exécuter le script: pip3 install pymysql

Détails de l'enviroinnement sur lequel le script a été testé:

		- OS: Linux Debian 4.9
		- Version Python: 3
		- 

Modules requis:
		- csv
		- requests
		- pymysql

"""

#-----------------------Other functions--------------------------------------
def mailParser(email):
	if "mailto:" in email:
		return email.split(':')[1]
	else: return email


def selectFromDB(connexion,req,att=''):
	curs=connexion.cursor()
	curs.execute(req,att)
	res= curs.fetchall()
	curs.close()
	if len(res)==0:
		return None
	else: return res

def getConnexionInfo():
	user=input("Utilisateur de la base: ")
	password=getpass('Mot de passe: ')
	return (user,password)
#-----------------------Download the CSV file from data gouv-----------------
def getCSV():
	csv_url="https://www.data.gouv.fr/fr/datasets/r/81ce135e-4460-4363-923a-8e861644ed16"
	req=requests.get(csv_url)
	with open('/tmp/hotels.csv','wb') as f:
		f.write(req.content)

#---------------Connexion To MariaDB server------------------------------
def Connection():
	user,password=getConnexionInfo()
	return mariadb.connect(use_unicode=True, charset="utf8", user=user, password=password, database='hotels',host='20.188.32.133')

#----------------------------Table HOTEL----------------------------------------------------------------------------
def remplissageHotel(connexion,nom,photo,siret,ape,fixe,mobile,fax,mail,site,description,gratuite_groupes,ouverture,langue,num_chaine,num_classe,num_loca,id_equipement,id_confort,id_service):
	hotel_req="INSERT INTO HOTEL (NOM,PHOTO_HOTEL,SIRET,APE,TEL_FIXE,TEL_MOBILE,FAX,EMAIL,SITEWEB,DESCRIPTION,GRATUITE_GROUPES,OUVERTURE,LANGUE,NUM_CHAINE,NUM_CLASSE,NUM_LOCA,ID_EQUIPEMENT,ID_CONFORT,ID_SERVICE) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	curs=connexion.cursor()
	val=(nom,photo,siret,ape,fixe,mobile,fax,mail,site,description,gratuite_groupes,ouverture,langue,num_chaine,num_classe,num_loca,id_equipement,id_confort,id_service)
	curs.execute(hotel_req,val)
	curs.execute("SET @id_hotel=LAST_INSERT_ID()")
	connexion.commit()
	curs.execute("SELECT LAST_INSERT_ID()")
	id_hotel=curs.fetchone()[0]
	curs.close()
	return id_hotel

def isHotelinDB(connexion,nom,latitude,longitude):
	req="SELECT NUMHOTEL FROM HOTEL NATURAL JOIN LOCALISATION WHERE NOM=%s AND LATITUDE='{0}' AND LONGITUDE='{1}'".format(latitude,longitude)
	res=selectFromDB(connexion,req,nom)
	return not(res==None)

#---------------------------- Table CHAINE------------------------------------------------------------------------
def isChaineinDB(connexion,chaine):
	req="SELECT NOM_CHAINE FROM CHAINE WHERE NOM_CHAINE=%s"
	res=selectFromDB(connexion,req,chaine)
	return not(res==None) #return true si l'enregidtrement existe

def remplissageChaine(connexion,chaine):
	req="INSERT INTO CHAINE (NOM_CHAINE) VALUES (%s)"
	curs=connexion.cursor()
	curs.execute(req,chaine)
	connexion.commit()
	curs.close()

def remplissageChaineVide(connexion):
	req="INSERT INTO CHAINE (NUM_CHAINE,NOM_CHAINE) VALUES (1,'')"
	curs=connexion.cursor()
	curs.execute(req)
	connexion.commit()
	curs.close()	

#-------------------------------Table CLASSES----------------------------------------------------------
def isClasseinDB(connexion,classe):
	req="SELECT NBREETOILES FROM CLASSES WHERE NBREETOILES=%s"
	res=selectFromDB(connexion,req,classesParser(classe))
	return not(res==None) #return true si l'enregidtrement existe

def remplissageClasse(connexion,classe):
	req="INSERT INTO CLASSES (NBREETOILES) VALUES (%s)"
	curs=connexion.cursor()
	curs.execute(req,classesParser(classe))
	connexion.commit()
	curs.close()

def remplissageClasseVide(connexion):
	req="INSERT INTO CLASSES (NUM_CLASSE,NBREETOILES) VALUES (1,'Sans étoiles')"
	curs=connexion.cursor()
	curs.execute(req)
	connexion.commit()
	curs.close()

def classesParser(string):
	res = [int(i) for i in string.split() if i.isdigit()]
	if len(res) != 0:
		if res[0]==1:return ('{0} étoile'.format(str(res[0])))
		else: return ('{0} étoiles'.format(str(res[0])))
	else : return "Sans étoiles"

#------------------------------Table EQUIPEMENTS--------------------------------------------------------------------
def isEquipementinDB(connexion,equipement):
	req="SELECT DESCRIPTION FROM EQUIPEMENTS WHERE DESCRIPTION=%s"
	res=selectFromDB(connexion,req,equipement)
	return not(res==None) #return true si l'enregidtrement existe

def remplissageEquipements(connexion,equipement):
	req="INSERT INTO EQUIPEMENTS (DESCRIPTION) VALUES (%s)"
	curs=connexion.cursor()
	curs.execute(req,equipement)
	connexion.commit()
	curs.close()

def remplissageEquipementsVide(connexion):
	req="INSERT INTO EQUIPEMENTS (ID_EQUIPEMENT,DESCRIPTION) VALUES (1,'')"
	curs=connexion.cursor()
	curs.execute(req)
	connexion.commit()
	curs.close()

#---------------------------------Table CONFORT ------------------------------------------------------------------------
def isConfortinDB(connexion,confort):
	req="SELECT DESCRIPTION FROM CONFORT WHERE DESCRIPTION=%s"
	res=selectFromDB(connexion,req,confort)
	return not(res==None) #return true si l'enregidtrement existe

def remplissageConfort(connexion,confort):
	req="INSERT INTO CONFORT (DESCRIPTION) VALUES (%s)"
	curs=connexion.cursor()
	curs.execute(req,confort)
	connexion.commit()
	curs.close()

def remplissageConfortVide(connexion):
	req="INSERT INTO CONFORT (ID_CONFORT,DESCRIPTION) VALUES (1,'')"
	curs=connexion.cursor()
	curs.execute(req)
	connexion.commit()
	curs.close()

#-------------------------------Table SERVICES--------------------------------------------------------------------------
def isServiceinDB(connexion,service):
	req="SELECT DESCRIPTION FROM SERVICES WHERE DESCRIPTION=%s"
	res=selectFromDB(connexion,req,service)
	return not(res==None) #return true si l'enregidtrement existe

def remplissageService(connexion,service):
	req="INSERT INTO SERVICES (DESCRIPTION) VALUES (%s)"
	curs=connexion.cursor()
	curs.execute(req,service)
	connexion.commit()
	curs.close()

def remplissageServiceVide(connexion):
	req="INSERT INTO SERVICES (ID_SERVICE,DESCRIPTION) VALUES (1,'')"
	curs=connexion.cursor()
	curs.execute(req)
	connexion.commit()
	curs.close()
#------------------------------Table LOCALISATION ----------------------------------------------------------------------
def remplissageLocalisation(connexion,adresse,code_postale,ville,latitude,longitude):
	req="INSERT INTO LOCALISATION (ADRESSE,CODE_POSTAL,VILLE,LATITUDE,LONGITUDE) VALUES (%s,%s,%s,%s,%s)"
	curs=connexion.cursor()
	val=(adresse,code_postale,ville,latitude,longitude)
	curs.execute(req,val)
	connexion.commit()
	curs.close()

#------------------------------Table Oneshot ------------------------------------------------------------
#pk oneshot: pask les valeurs des colonnes c les colonnes du csv donc constant donc execution une seule fois

#REGLEMENTS
def remplissageReglements(connexion):
	reglements_tab=["tarif_mini_chambre_double_hors_petit_dej","tarif_maxi_chambre_double_hors_petit_dej","tarif_mini_chambre_familiale","tarif_maxi_chambre_familiale","tarif_mini_suite","tarif_maxi_suite","tarif_mini_petit_dej","tarif_maxi_petit_dej","tarif_mini_demi_pension","tarif_maxi_demi_pension","tarif_mini_VRP_diner_petit_dej","tarif_maxi_VRP_diner_petit_dej","tarif_mini_groupe_chambre_double_petit_dej","tarif_maxi_groupe_chambre_double_petit_dej","tarif_mini_groupe_demi_pension","tarif_maxi_groupe_demi_pension"]
	curs=connexion.cursor()
	req_regl="INSERT INTO REGLEMENTS (DESCRIPTION) VALUES (%s)"
	#req_propose=""
	for regl in reglements_tab:
		curs.execute(req_regl,regl)
	connexion.commit()
	curs.close()

def getIdReglement(connexion,reglement):
	req="SELECT IDREGLEMENT FROM REGLEMENTS WHERE DESCRIPTION=%s"
	return selectFromDB(connexion,req,reglement)[0]

def getReglementCount(connexion):
	req="SELECT COUNT(*) FROM REGLEMENTS"
	curs=connexion.cursor()
	curs.execute(req)
	count=curs.fetchone()[0]
	curs.close()
	return (count)

#ORGANISATION
def remplissageOrganisation(connexion):
	organisations_tab=["nb_chambre_pref","nb_chambre_dispo_location","nb_chambre","nb_chambre_familiales","nb_suites","nb_chambre_pers_mobilite_reduite","nb_salle_reunion"]
	curs=connexion.cursor()
	req_desc="INSERT INTO ORGANISATION (DESCRIPTION) VALUES (%s)"
	#req_propose=""
	for desc in organisations_tab:
		curs.execute(req_desc,desc)
	connexion.commit()
	curs.close()	

def getIdOrganisation(connexion,description):
	req="SELECT NUM_ORGA FROM ORGANISATION WHERE DESCRIPTION=%s"
	return selectFromDB(connexion,req,description)[0]


def getOrganisationCount(connexion):
	req="SELECT COUNT(*) FROM ORGANISATION"
	curs=connexion.cursor()
	curs.execute(req)
	count=curs.fetchone()[0]
	curs.close()
	return (count)

#LESPLUS
def remplissageLesPlus(connexion):
	Lesplus_tab=["animaux_acceptes","resa_derniere_minute","parking_autocars","groupes_acceptes","commissionnement_agence_voyages"]
	curs=connexion.cursor()
	req_desc="INSERT INTO LESPLUS (DESCRIPTION) VALUES (%s)"
	#req_propose=""
	for desc in Lesplus_tab:
		curs.execute(req_desc,desc)
	connexion.commit()
	curs.close()	

def getIdLesPlus(connexion,description):
	req="SELECT ID_PLUS FROM LESPLUS WHERE DESCRIPTION=%s"
	return selectFromDB(connexion,req,description)[0]


def getLesPlusCount(connexion):
	req="SELECT COUNT(*) FROM LESPLUS"
	curs=connexion.cursor()
	curs.execute(req)
	count=curs.fetchone()[0]
	curs.close()
	return (count)

#-------------------------------------Table LABEL-----------------------------------------
def remplissageLabel(connexion,label):
	req="INSERT INTO LABEL (DESCRIPTION) VALUES (%s)"
	curs=connexion.cursor()
	curs.execute(req,label)
	connexion.commit()
	curs.close()

def getIdLabel(connexion,label):
	req="SELECT IDLABEL FROM LABEL WHERE DESCRIPTION=%s"
	return selectFromDB(connexion,req,label)[0]

def isLabelinDB(connexion,label):
	req="SELECT IDLABEL FROM LABEL WHERE DESCRIPTION=%s"
	res=selectFromDB(connexion,req,label)
	return not(res==None) #return true si l'enregidtrement existe

def remplissageLabelVide(connexion):
	req="INSERT INTO LABEL (IDLABEL,DESCRIPTION) VALUES (1,'')"
	curs=connexion.cursor()
	curs.execute(req)
	connexion.commit()
	curs.close()

#------------------------------------Table ACTIVITE--------------------------------------
def remplissageActivite(connexion,activite,description):
	req="INSERT INTO ACTIVITE (ACTIVITES,DESCRIPTION_ANIMATIONS) VALUES (%s,%s)"
	curs=connexion.cursor()
	curs.execute(req,(activite,description))
	connexion.commit()
	curs.close()

def getIdActivite(connexion,activite):
	req="SELECT ID_ACTIVITE FROM ACTIVITE WHERE ACTIVITES=%s"
	return selectFromDB(connexion,req,activite)[0]

def isActiviteinDB(connexion,activite):
	req="SELECT ID_ACTIVITE FROM ACTIVITE WHERE ACTIVITES=%s"
	res=selectFromDB(connexion,req,activite)
	return not(res==None) #return true si l'enregidtrement existe

def remplissageActiviteVide(connexion):
	req="INSERT INTO ACTIVITE (ID_ACTIVITE,ACTIVITES,DESCRIPTION_ANIMATIONS) VALUES (1,'','')"
	curs=connexion.cursor()
	curs.execute(req)
	connexion.commit()
	curs.close()
#------------------------------------Table CATEGORIE--------------------------------------
def remplissageCategorie(connexion,description):
	req="INSERT INTO CATEGORIE (DESCRIPTION) VALUES (%s)"
	curs=connexion.cursor()
	curs.execute(req,description)
	connexion.commit()
	curs.close()

def getIdCategorie(connexion,description):
	req="SELECT CODECATEGORIE FROM CATEGORIE WHERE DESCRIPTION=%s"
	return selectFromDB(connexion,req,description)[0]

def isCategorieinDB(connexion,description):
	req="SELECT CODECATEGORIE FROM CATEGORIE WHERE DESCRIPTION=%s"
	res=selectFromDB(connexion,req,description)
	return not(res==None) #return true si l'enregidtrement existe


#---------------------------------Table APPARTIENT ----------------------------------------
def remplissageAppartient(connexion,id_hotel,categorie):
	id_categorie=getIdCategorie(connexion,categorie)
	req="INSERT INTO APPARTIENT (CODECATEGORIE,NUMHOTEL) VALUES (%s,%s)"
	curs=connexion.cursor()
	val=(id_categorie,id_hotel)
	curs.execute(req,val)
	connexion.commit()
	curs.close()

#---------------------------------Table POSSEDE--------------------------------------------
def remplissagePossede(connexion,id_hotel,label):
	id_label=getIdLabel(connexion,label)
	req="INSERT INTO POSSEDE (IDLABEL,NUMHOTEL) VALUES (%s,%s)"
	curs=connexion.cursor()
	val=(id_label,id_hotel)
	curs.execute(req,val)
	connexion.commit()
	curs.close()

#--------------------------- Table PROPOSE --------------------------------------------
def remplissagePropose(connexion,tarif,id_hotel,desc_regl):

	id_reglement=getIdReglement(connexion,desc_regl)
	req="INSERT INTO PROPOSE (IDREGLEMENT,NUMHOTEL,tarif) VALUES (%s,%s,%s)"
	curs=connexion.cursor()
	val=(id_reglement,id_hotel,tarif)
	curs.execute(req,val)
	connexion.commit()
	curs.close()

#-------------------------Table DISPOSE----------------------------------------------------
def remplissageDispose(connexion,nombre,id_hotel,desc_orga):
	id_organisation=getIdOrganisation(connexion,desc_orga)
	req="INSERT INTO DISPOSE (NUM_ORGA,NUMHOTEL,NOMBRE) VALUES (%s,%s,%s)"
	curs=connexion.cursor()
	val=(id_organisation,id_hotel,nombre)
	curs.execute(req,val)
	connexion.commit()
	curs.close()

#--------------------------------Table CONTIENT--------------------------------------------------
def remplissageContient(connexion,contrainte,id_hotel,desc_lesplus):
	id_plus=getIdLesPlus(connexion,desc_lesplus)
	req="INSERT INTO CONTIENT (ID_PLUS,NUMHOTEL,CONTRAINTE) VALUES (%s,%s,%s)"
	curs=connexion.cursor()
	val=(id_plus,id_hotel,contrainte)
	curs.execute(req,val)
	connexion.commit()
	curs.close()

#-------------------------------Table REALISE-----------------------------------------------------------
def remplissageRealise(connexion,id_hotel,activite):
	id_activite=getIdActivite(connexion,activite)
	req="INSERT INTO REALISE (ID_ACTIVITE,NUMHOTEL) VALUES (%s,%s)"
	curs=connexion.cursor()
	val=(id_activite,id_hotel)
	curs.execute(req,val)
	connexion.commit()
	curs.close()

#-----------------------------------------------------------------------------------------------------------------

getCSV()
def main():
	conObj=Connection()
	organisations_tab=["nb_chambre_pref","nb_chambre_dispo_location","nb_chambre","nb_chambre_familiales","nb_suites","nb_chambre_pers_mobilite_reduite","nb_salle_reunion"]
	reglements_tab=["tarif_mini_chambre_double_hors_petit_dej","tarif_maxi_chambre_double_hors_petit_dej","tarif_mini_chambre_familiale","tarif_maxi_chambre_familiale","tarif_mini_suite","tarif_maxi_suite","tarif_mini_petit_dej","tarif_maxi_petit_dej","tarif_mini_demi_pension","tarif_maxi_demi_pension","tarif_mini_VRP_diner_petit_dej","tarif_maxi_VRP_diner_petit_dej","tarif_mini_groupe_chambre_double_petit_dej","tarif_maxi_groupe_chambre_double_petit_dej","tarif_mini_groupe_demi_pension","tarif_maxi_groupe_demi_pension"]
	Lesplus_tab=["animaux_acceptes","resa_derniere_minute","parking_autocars","groupes_acceptes","commissionnement_agence_voyages"]
	try:
		remplissageChaineVide(conObj)
		remplissageClasseVide(conObj)
		remplissageLabelVide(conObj)
		remplissageActiviteVide(conObj)
		remplissageEquipementsVide(conObj)
		remplissageConfortVide(conObj)
		remplissageServiceVide(conObj)
	except mariadb.err.IntegrityError:
		pass
	with open('/tmp/hotels.csv','r',encoding='latin-1',errors='replace',newline='') as f:
		reader=csv.DictReader(f,delimiter=';')
		if getReglementCount(conObj) ==0:
			remplissageReglements(conObj)
		if getOrganisationCount(conObj)==0:
			remplissageOrganisation(conObj)
		if getLesPlusCount(conObj)==0:
			remplissageLesPlus(conObj)
		for hotel in reader: #tester si l hotel est deja dans la base
			if not isHotelinDB(conObj,hotel['nom'],hotel['latitude'].replace(',','.'),hotel['longitude'].replace(',','.')):
				if len(hotel['chaine'])!=0:
					if not isChaineinDB(conObj,hotel['chaine']):
						remplissageChaine(conObj,hotel['chaine'])
				if hotel['categorie'] !="":
					if not isClasseinDB(conObj,hotel['categorie']):
						remplissageClasse(conObj,hotel['categorie'])
				if hotel['equipement'] !="":
					if not isEquipementinDB(conObj,hotel['equipement']):
						remplissageEquipements(conObj,hotel['equipement'])
				if hotel['confort'] !="":
					if not isConfortinDB(conObj,hotel['confort']):
						remplissageConfort(conObj,hotel['confort'])
				if hotel['service'] != "":
					if not isServiceinDB(conObj,hotel['service']):
						remplissageService(conObj,hotel['service'])
				remplissageLocalisation(conObj,hotel['adresse1']+" "+hotel['adresse2'],hotel['code_postal'],hotel['ville'],hotel['latitude'].replace(',','.'),hotel['longitude'].replace(',','.'))
				id_service=selectFromDB(conObj,"SELECT ID_SERVICE FROM SERVICES WHERE DESCRIPTION=%s",(hotel['service']))[0][0]
				id_chaine=selectFromDB(conObj,"SELECT NUM_CHAINE FROM CHAINE WHERE NOM_CHAINE=%s",hotel['chaine'])[0][0]
				id_classe=selectFromDB(conObj,"SELECT NUM_CLASSE FROM CLASSES WHERE NBREETOILES=%s",classesParser(hotel['categorie']))[0][0]
				id_loca=selectFromDB(conObj,"SELECT NUM_LOCA FROM LOCALISATION WHERE LATITUDE='{0}' AND LONGITUDE=%s".format(hotel['latitude'].replace(',','.')),hotel['longitude'].replace(',','.'))[0][0]
				id_equipement=selectFromDB(conObj,"SELECT ID_EQUIPEMENT FROM EQUIPEMENTS WHERE DESCRIPTION=%s",hotel['equipement'])[0][0]
				id_confort=selectFromDB(conObj,"SELECT ID_CONFORT FROM CONFORT WHERE DESCRIPTION=%s",hotel['confort'])[0][0]
				id_hotel=remplissageHotel(conObj,hotel['nom'],photo=hotel['visuel'],siret=hotel['SIRET'],ape=hotel['APE'],fixe=hotel['tel_fixe'].split(",")[0],mobile=hotel['tel_mobile'].split(",")[0],fax=hotel['fax'].split(",")[0],mail=mailParser(hotel['email']),site=hotel['site_web'],description=hotel['description'],gratuite_groupes=hotel['gratuite_groupes'],ouverture=hotel['ouverture'],langue=hotel['langue'],num_chaine=id_chaine,num_classe=id_classe,num_loca=id_loca,id_equipement=id_equipement,id_confort=id_confort,id_service=id_service)
				print(hotel['nom'])
				if not isCategorieinDB(conObj,hotel['type_hotel']):
					remplissageCategorie(conObj,hotel['type_hotel'])
				remplissageAppartient(conObj,id_hotel,hotel['type_hotel'])
				if hotel['label'] !="":
					if not isLabelinDB(conObj,hotel['label']):
						remplissageLabel(conObj,hotel['label'])
				remplissagePossede(conObj,id_hotel,hotel['label'])
				if hotel['activites'] !='':
					if not isActiviteinDB(conObj,hotel['activites']):
						remplissageActivite(conObj,hotel['activites'],hotel['description_animations'])
				remplissageRealise(conObj,id_hotel,hotel['activites'])
				for reglem in reglements_tab:
					remplissagePropose(conObj,hotel[reglem],id_hotel,reglem)
				for orga in organisations_tab:
					remplissageDispose(conObj,hotel[orga],id_hotel,orga)
				for plus in Lesplus_tab:
					remplissageContient(conObj,hotel[plus],id_hotel,plus)
		conObj.close()
main()