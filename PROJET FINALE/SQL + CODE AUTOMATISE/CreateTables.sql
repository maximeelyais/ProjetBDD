
#------------------------------------------------------------
#        Script MySQL.
#------------------------------------------------------------


#------------------------------------------------------------
# Table: CATEGORIE
#------------------------------------------------------------


CREATE TABLE CATEGORIE(
        CODECATEGORIE Int  Auto_increment  NOT NULL ,
        DESCRIPTION   Varchar (200)
        ,CONSTRAINT CATEGORIE_PK PRIMARY KEY (CODECATEGORIE)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: CLASSES
#------------------------------------------------------------

CREATE TABLE CLASSES(
        NUM_CLASSE  Int  Auto_increment  NOT NULL ,
        NBREETOILES Varchar (200)
        ,CONSTRAINT CLASSES_PK PRIMARY KEY (NUM_CLASSE)
)ENGINE=InnoDB;



#------------------------------------------------------------
# Table: ORGANISATION
#------------------------------------------------------------

CREATE TABLE ORGANISATION(
        NUM_ORGA    Int  Auto_increment  NOT NULL ,
        DESCRIPTION Varchar (200)
        ,CONSTRAINT ORGANISATION_PK PRIMARY KEY (NUM_ORGA)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: CHAINE
#------------------------------------------------------------

CREATE TABLE CHAINE(
        NUM_CHAINE Int  Auto_increment  NOT NULL ,
        NOM_CHAINE Varchar (200)
        ,CONSTRAINT CHAINE_PK PRIMARY KEY (NUM_CHAINE)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: LESPLUS
#------------------------------------------------------------

CREATE TABLE LESPLUS(
        ID_PLUS     Int  Auto_increment  NOT NULL ,
        DESCRIPTION Varchar (200)
        ,CONSTRAINT LESPLUS_PK PRIMARY KEY (ID_PLUS)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: EQUIPEMENTS
#------------------------------------------------------------

CREATE TABLE EQUIPEMENTS(
        ID_EQUIPEMENT Int  Auto_increment  NOT NULL ,
        DESCRIPTION   Varchar (200)
        ,CONSTRAINT EQUIPEMENTS_PK PRIMARY KEY (ID_EQUIPEMENT)
)ENGINE=InnoDB;



#------------------------------------------------------------
# Table: SERVICES
#------------------------------------------------------------

CREATE TABLE SERVICES(
        ID_SERVICE  Int  Auto_increment  NOT NULL ,
        DESCRIPTION Varchar (200)
        ,CONSTRAINT SERVICES_PK PRIMARY KEY (ID_SERVICE)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: CONFORT
#------------------------------------------------------------

CREATE TABLE CONFORT(
        ID_CONFORT  Int  Auto_increment  NOT NULL ,
        DESCRIPTION Varchar (200)
        ,CONSTRAINT CONFORT_PK PRIMARY KEY (ID_CONFORT)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: ACTIVITE
#------------------------------------------------------------


CREATE TABLE ACTIVITE(
        ID_ACTIVITE            Int  Auto_increment  NOT NULL ,
        ACTIVITES              Varchar (200) ,
        DESCRIPTION_ANIMATIONS Varchar (500)
        ,CONSTRAINT ACTIVITE_PK PRIMARY KEY (ID_ACTIVITE)
)ENGINE=InnoDB;



#------------------------------------------------------------
# Table: REGLEMENTS
#------------------------------------------------------------

CREATE TABLE REGLEMENTS(
        IDREGLEMENT Int  Auto_increment  NOT NULL ,
        DESCRIPTION Varchar (200)
        ,CONSTRAINT REGLEMENTS_PK PRIMARY KEY (IDREGLEMENT)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: LOCALISATION
#------------------------------------------------------------
CREATE TABLE LOCALISATION(
        NUM_LOCA    Int  Auto_increment  NOT NULL ,
        ADRESSE     Varchar (200) ,
        CODE_POSTAL Int NOT NULL ,
        VILLE       Varchar (200) ,
        LATITUDE    Varchar (200) ,
        LONGITUDE   Varchar (200)
        ,CONSTRAINT LOCALISATION_PK PRIMARY KEY (NUM_LOCA)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: HOTEL
#------------------------------------------------------------

CREATE TABLE HOTEL(
        NUMHOTEL      Int  Auto_increment  NOT NULL ,
        NOM           Varchar (200) NOT NULL ,
        PHOTO_HOTEL   Varchar (200) ,
        SIRET         Varchar (200) ,
        APE           Varchar (50) ,
        TEL_FIXE      Varchar (14) ,
        TEL_MOBILE    Varchar (14) ,
        FAX           Varchar (14) ,
        EMAIL         Varchar (200) ,
        SITEWEB       Varchar (200) ,
        DESCRIPTION   Varchar (3000) ,
        GRATUITE_GROUPES Varchar (200) ,
        OUVERTURE     Varchar (300) ,
        LANGUE        Varchar (200) ,
        NUM_CLASSE    Int ,
        NUM_CHAINE  Int ,
        NUM_LOCA    Int NOT NULL,
        ID_EQUIPEMENT Int,
        ID_CONFORT Int,
        ID_SERVICE Int


        ,CONSTRAINT HOTEL_PK PRIMARY KEY (NUMHOTEL)

        ,CONSTRAINT HOTEL_CLASSES_FK FOREIGN KEY (NUM_CLASSE) REFERENCES CLASSES(NUM_CLASSE)
        ,CONSTRAINT HOTEL_CHAINE0_FK FOREIGN KEY (NUM_CHAINE) REFERENCES CHAINE(NUM_CHAINE)
        ,CONSTRAINT HOTEL_LOCALISATION1_FK FOREIGN KEY (NUM_LOCA) REFERENCES LOCALISATION(NUM_LOCA)
        ,CONSTRAINT HOTEL_EQUIPEMENT FOREIGN KEY (ID_EQUIPEMENT) REFERENCES EQUIPEMENTS(ID_EQUIPEMENT)
        ,CONSTRAINT HOTEL_CONFORT FOREIGN KEY (ID_CONFORT) REFERENCES CONFORT(ID_CONFORT)
        ,CONSTRAINT HOTEL_SERVICES FOREIGN KEY (ID_SERVICE) REFERENCES SERVICES(ID_SERVICE)

)ENGINE=InnoDB;




#------------------------------------------------------------
# Table: DISPOSE
#------------------------------------------------------------


CREATE TABLE DISPOSE(
        NUM_ORGA Int NOT NULL ,
        NUMHOTEL Int NOT NULL ,
        NOMBRE   Int
        ,CONSTRAINT DISPOSE_PK PRIMARY KEY (NUM_ORGA,NUMHOTEL)
        ,CONSTRAINT DISPOSE_ORGANISATION_FK FOREIGN KEY (NUM_ORGA) REFERENCES ORGANISATION(NUM_ORGA)
        ,CONSTRAINT DISPOSE_HOTEL0_FK FOREIGN KEY (NUMHOTEL) REFERENCES HOTEL(NUMHOTEL)
)ENGINE=InnoDB;

#------------------------------------------------------------
# Table: CONTIENT
#------------------------------------------------------------

CREATE TABLE CONTIENT(
        ID_PLUS Int NOT NULL ,
        NUMHOTEL      Int NOT NULL ,
        CONTRAINTE    VARCHAR (100)
        ,CONSTRAINT CONTIENT_PK PRIMARY KEY (ID_PLUS,NUMHOTEL)
        ,CONSTRAINT contient_LESPLUS_FK FOREIGN KEY (ID_PLUS) REFERENCES LESPLUS(ID_PLUS)
        ,CONSTRAINT contient_hotel_FK FOREIGN KEY (NUMHOTEL) REFERENCES HOTEL(NUMHOTEL)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: PROPOSE
#------------------------------------------------------------

CREATE TABLE PROPOSE(
        IDREGLEMENT Int NOT NULL ,
        NUMHOTEL    Int NOT NULL ,
        tarif       Float
        ,CONSTRAINT PROPOSE_PK PRIMARY KEY (IDREGLEMENT,NUMHOTEL)
        ,CONSTRAINT propose_reglements_FK FOREIGN KEY (IDREGLEMENT) REFERENCES REGLEMENTS(IDREGLEMENT)
        ,CONSTRAINT propose_hotel_FK FOREIGN KEY (NUMHOTEL) REFERENCES HOTEL(NUMHOTEL)
)ENGINE=InnoDB;


#------------------------------------------------------------

#------------------------------------------------------------
# Table: Appartient
#------------------------------------------------------------

CREATE TABLE APPARTIENT(
        CODECATEGORIE Int(11) NOT NULL ,
        NUMHOTEL      Int(11) NOT NULL ,
         CONSTRAINT appartient_PK PRIMARY KEY (CODECATEGORIE,NUMHOTEL)
        ,CONSTRAINT appartient_categorie_FK FOREIGN KEY (CODECATEGORIE) REFERENCES CATEGORIE(CODECATEGORIE)
        ,CONSTRAINT appartient_hotel_FK FOREIGN KEY (NUMHOTEL) REFERENCES HOTEL(NUMHOTEL)

)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Realise
#------------------------------------------------------------


CREATE TABLE REALISE(
        ID_ACTIVITE   Int(11) NOT NULL ,
        NUMHOTEL      Int(11) NOT NULL ,
        CONSTRAINT realise_PK PRIMARY KEY (ID_ACTIVITE,NUMHOTEL)
        ,CONSTRAINT realise_activite_FK FOREIGN KEY (ID_ACTIVITE) REFERENCES ACTIVITE(ID_ACTIVITE)
        ,CONSTRAINT realise_hotel_FK FOREIGN KEY (NUMHOTEL) REFERENCES HOTEL(NUMHOTEL)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: LABEL
#------------------------------------------------------------



CREATE TABLE LABEL(
        IDLABEL     Int  Auto_increment  NOT NULL ,
        DESCRIPTION Varchar (200)
        ,CONSTRAINT LABEL_PK PRIMARY KEY (IDLABEL)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: POSSEDE
#------------------------------------------------------------
CREATE TABLE POSSEDE(
        IDLABEL   Int(11) NOT NULL ,
        NUMHOTEL      Int(11) NOT NULL ,
        CONSTRAINT possede_PK PRIMARY KEY (IDLABEL,NUMHOTEL)
        ,CONSTRAINT possede_activite_FK FOREIGN KEY (IDLABEL) REFERENCES LABEL(IDLABEL)
        ,CONSTRAINT possede_hotel_FK FOREIGN KEY (NUMHOTEL) REFERENCES HOTEL(NUMHOTEL)
)ENGINE=InnoDB;


grant all privileges on *.* to 'root'@'20.188.32.133' identified by 'CaptainPrice';
flush privileges;
DELIMITER |
DROP FUNCTION IF EXISTS get_distance_metres|
CREATE FUNCTION get_distance_metres (lat1 DOUBLE, lng1 DOUBLE, lat2 DOUBLE, lng2 DOUBLE) RETURNS DOUBLE
BEGIN
    DECLARE rlo1 DOUBLE;
    DECLARE rla1 DOUBLE;
    DECLARE rlo2 DOUBLE;
    DECLARE rla2 DOUBLE;
    DECLARE dlo DOUBLE;
    DECLARE dla DOUBLE;
    DECLARE a DOUBLE;
   
    SET rlo1 = RADIANS(lng1);
    SET rla1 = RADIANS(lat1);
    SET rlo2 = RADIANS(lng2);
    SET rla2 = RADIANS(lat2);
    SET dlo = (rlo2 - rlo1) / 2;
    SET dla = (rla2 - rla1) / 2;
    SET a = SIN(dla) * SIN(dla) + COS(rla1) * COS(rla2) * SIN(dlo) * SIN(dlo);
    RETURN (6378137 * 2 * ATAN2(SQRT(a), SQRT(1 - a)));
END|
DELIMITER ;

DELIMITER $$

CREATE FUNCTION `ExtractNumber`(in_string VARCHAR(50)) 
RETURNS INT
NO SQL
BEGIN
    DECLARE ctrNumber VARCHAR(50);
    DECLARE finNumber VARCHAR(50) DEFAULT '';
    DECLARE sChar VARCHAR(1);
    DECLARE inti INTEGER DEFAULT 1;

    IF LENGTH(in_string) > 0 THEN
        WHILE(inti <= LENGTH(in_string)) DO
            SET sChar = SUBSTRING(in_string, inti, 1);
            SET ctrNumber = FIND_IN_SET(sChar, '0,1,2,3,4,5,6,7,8,9'); 
            IF ctrNumber > 0 THEN
                SET finNumber = CONCAT(finNumber, sChar);
            END IF;
            SET inti = inti + 1;
        END WHILE;
        RETURN CAST(finNumber AS UNSIGNED);
    ELSE
        RETURN 0;
    END IF;    
END$$
DELIMITER ;