# -*- coding: utf-8 -*-

import numpy as np

import urllib

####################
#Constantes#
####################

class simulation:

    G = 6.67408*10**-11
    MT = 5.9772*10**24
    mu = G*MT
    RT = 6371.*10**3
    affichage_label = False;
    
    def __init__(self):    
        pass
    
    
    def metres(self, m):
        return m/self.RT
        
    R = metres(RT + 20000*10**3)


####################
#Obtention des données gps#
####################
def TLE_parser():
    satellites = list()
    
    f = urllib.urlopen("https://www.celestrak.com/NORAD/elements/supplemental/gps.txt")
    fp = f.read().splitlines()
    for i in range(0,len(fp),3):
        satellites.append([])
        '''0'''; satellites[i//3].append(fp[i][:-2]) #NOM !!!
        
        #LIGNE 1
        '''1''';satellites[i//3].append(fp[i+1][2:7])#NUMERO DE SATELLITE
        '''2''';satellites[i//3].append(fp[i+1][7])#CLASSIFICATION
        '''3''';satellites[i//3].append(fp[i+1][9:12])#ANNEE DE LANCEMENT
        '''4''';satellites[i//3].append(fp[i+1][11:14])#NUMERO DE LANCEMENT DANS L'ANNEE
        '''5''';satellites[i//3].append(fp[i+1][14:17])#IDENTIFIANT D'OBJET DU LANCEMENT
        '''6''';satellites[i//3].append(fp[i+1][18:20])#EPOQUE(ANNEE)
        '''7''';satellites[i//3].append(fp[i+1][20:32])#EPOQUE(JOUR DE L'ANNEE ET PORTION FRACTIONELLE DU JOUR)
        '''8''';satellites[i//3].append(fp[i+1][33:43])
        '''9''';satellites[i//3].append(fp[i+1][44:52])
        '''10''';satellites[i//3].append(fp[i+1][53:61])
        '''11''';satellites[i//3].append(fp[i+1][63])
        '''12''';satellites[i//3].append(fp[i+1][64:68])
        
        #LIGNE 2
        '''13''';satellites[i//3].append(fp[i+2][2:7])#NUMERO DE SATELLITE
        '''14''';satellites[i//3].append(float(fp[i+2][8:16]))#INCLINAISON
        '''15''';satellites[i//3].append(float(fp[i+2][17:25]))#LONGITUDE DU NOEUD DESCENDANT
        '''16''';satellites[i//3].append(str(fp[i+2][26:33]))#EXCENTRICITE
        '''17''';satellites[i//3].append(float(fp[i+2][34:42]))#ARGUMENT DU PERIASTRE
        '''18''';satellites[i//3].append(float(fp[i+2][43:51]))#ANOMALIE MOYENNE
        '''19''';satellites[i//3].append(float(fp[i+2][52:63]))#MOYEN MOUVEMENT
        '''20''';satellites[i//3].append(float(fp[i+2][64:68]))#NOMBRE DE REVOLUTIONS A L'EPOQUE DONNEE
    return satellites,fp
    
    