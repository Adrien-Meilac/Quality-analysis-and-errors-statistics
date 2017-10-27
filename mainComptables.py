# -*- coding: utf-8 -*-
# Fichier main.py
# Permet l'execution du code

import os
import IOfonction as io
import VarGlobales as vg
import AnaGlobale as ag
import Repertoire as rep
import RepertoireComptable as rc
import SauvegardeRepertoireComptable as sauvrc

 # L'année se définit dans les paramètres globaux

adresseStockageRep = "./Analyse_par_repertoire_" + str(vg.annee)
adresseStockageCom = "./Analyse_par_comptable_" + str(vg.annee)

# Création du répertoire contenant les infos par répertoire
if not os.path.exists(adresseStockageRep):
    os.mkdir(adresseStockageRep)

T = ag.Analyse_globale()
io.ecrire_csv(adresseStockageRep, "Analyse_globale_repertoire_annee_" + str(vg.annee), T)
    
for i in range(len(vg.N3)):
    T = rep.Repertoire_N3(i) # Calcul des infos pour un répertoire
    io.ecrire_csv(adresseStockageRep, "Rep_"+ vg.N3[i], T) #Sauvegarde des infos

for i in range(len(vg.N3)): # Récupération des infos générés dans les fichiers csv pour chaque répertoire
    vg.Rep.append(io.lire_csv(adresseStockageRep, "Rep_"+ vg.N3[i]))

#Création du répertoire contenant les infos par comptables
if not os.path.exists(adresseStockageCom):
    os.mkdir(adresseStockageCom)
    

for nomComptable in vg.liste_nom:  # Création d'un fichier par comptable
    a = rc.traitement_comptable(nomComptable)
    if a != None:
        (EC, EM) = a
        sauvrc.sauvegarder_comptable(adresseStockageCom, nomComptable, EC, EM)
        
(ECG, EMG) = rc.ecrire_all_comptable(vg.liste_nom) # Création de l'étude globale sur tout les comptables
sauvrc.sauvegarder_analyse_globale_comptables(adresseStockageCom, ECG, EMG)