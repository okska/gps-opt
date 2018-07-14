# -*- coding: utf-8 -*-

import numpy as np

import urllib

class simulation:

    G = 6.67408*10**-11
    MT = 5.9772*10**24
    mu = G*MT
    RT = 6371.*10**3
    affichage_label = False;
    satellites = list()
    
    def __init__(self):    
        pass
    
    
    def metres(self, m):
        return m/self.RT
        
    R = metres(RT + 20000*10**3)
    
    ####################
    #Obtention des données gps#
    ####################
    def TLE_parser(self):
    
        f = urllib.urlopen("https://www.celestrak.com/NORAD/elements/supplemental/gps.txt")
        fp = f.read().splitlines()
        s = self.satellites
        for i in range(0,len(fp),3):
            s.append([])
            '''0'''; s[i//3].append(fp[i][:-2]) #NOM !!!
            
            #LIGNE 1
            '''1''';s[i//3].append(fp[i+1][2:7])#NUMERO DE SATELLITE
            '''2''';s[i//3].append(fp[i+1][7])#CLASSIFICATION
            '''3''';s[i//3].append(fp[i+1][9:12])#ANNEE DE LANCEMENT
            '''4''';s[i//3].append(fp[i+1][11:14])#NUMERO DE LANCEMENT DANS L'ANNEE
            '''5''';s[i//3].append(fp[i+1][14:17])#IDENTIFIANT D'OBJET DU LANCEMENT
            '''6''';s[i//3].append(fp[i+1][18:20])#EPOQUE(ANNEE)
            '''7''';s[i//3].append(fp[i+1][20:32])#EPOQUE(JOUR DE L'ANNEE ET PORTION FRACTIONELLE DU JOUR)
            '''8''';s[i//3].append(fp[i+1][33:43])
            '''9''';s[i//3].append(fp[i+1][44:52])
            '''10''';s[i//3].append(fp[i+1][53:61])
            '''11''';s[i//3].append(fp[i+1][63])
            '''12''';s[i//3].append(fp[i+1][64:68])
            
            #LIGNE 2
            '''13''';s[i//3].append(fp[i+2][2:7])#NUMERO DE SATELLITE
            '''14''';s[i//3].append(float(fp[i+2][8:16]))#INCLINAISON
            '''15''';s[i//3].append(float(fp[i+2][17:25]))#LONGITUDE DU NOEUD DESCENDANT
            '''16''';s[i//3].append(str(fp[i+2][26:33]))#EXCENTRICITE
            '''17''';s[i//3].append(float(fp[i+2][34:42]))#ARGUMENT DU PERIASTRE
            '''18''';s[i//3].append(float(fp[i+2][43:51]))#ANOMALIE MOYENNE
            '''19''';s[i//3].append(float(fp[i+2][52:63]))#MOYEN MOUVEMENT
            '''20''';s[i//3].append(float(fp[i+2][64:68]))#NOMBRE DE REVOLUTIONS A L'EPOQUE DONNEE
        return s,fp
    
    


    