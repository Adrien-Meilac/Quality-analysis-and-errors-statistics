# -*- coding: utf-8 -*-
# Fichier VarGlobales.py
# Contient les variables importantes du programme pour éviter de les passer en paramètre

import IOfonction as io # Permet d'accéder à la liste des noms des comptables
import Arborescence as arb # Permet de comprendre l'arborescence et de l'adapter aux différentes années


annee = 2015 # Année de l'étude

##Chemins :
N0 = "G:/Cpts_Etat_RAR/" + str(annee)    # Niveau 0 : correspond au chemin qui mène au répertoire qui contient tous les comptables
N1 = arb.liste_sous_chemin(N0)[1]       # Niveau 1 : comptient la liste des comptables
N2 = "Fichiers_ORIGINAUX"               # Niveau 2
N3 = arb.liste_sous_chemin(N0 + "/" + "0000_modele" + "/" + "Fichiers_ORIGINAUX" )[1]  # Niveau 3 : permet d'accéder à l'arborescence de chaque type de document

## Pour chaque catégorie N3:

Ftype = [] # Type à chercher dans le nom des fichiers
Search = [] # Terme sous forme de mots consécutifs (séparés par des espaces) à chercher
ExtAutorise = [] # Extensions autorisés dans chaque répertoire
for i in range(len(N3)):
    if "104" in N3[i]:
        Ftype.append(["R104bis"])
        Search.append([])
        ExtAutorise.append(['ods','pdf'])
    elif "105" in N3[i]:
        Ftype.append(["R105"])
        Search.append(["REFERENCE",":","R105"])
        ExtAutorise.append(['pdf'])
    elif "204" in N3[i]:
        Ftype.append(["R204","2204"])
        Search.append(["REFERENCE",":","R204"])
        ExtAutorise.append(['pdf'])
    elif "420" in N3[i]:
        Ftype.append(["REP420"])
        Search.append(["REP420C"])
        ExtAutorise.append(['pdf'])
    elif "730" in N3[i]:
        Ftype.append(["RAR730"])
        Search.append(["RARB730"])
        ExtAutorise.append(['pdf'])
    elif "173" in N3[i]:
        Ftype.append(['Inventaire_0173'])
        Search.append([])
        ExtAutorise.append(['ods'])
    elif "310" in N3[i]:
        Ftype.append(['REP310_1T', 'REP310_2T', 'REP310_3T', 'REP310_4T'])
        Search.append(["REP310"])
        ExtAutorise.append(["pdf"])
    else:
        Ftype.append([])
        Search.append([])
        ExtAutorise.append([])
             
liste_nom = io.lecture_base('./', 'base') # Liste des numéros des comptables à chercher

Rep = [] # Répertoires (mis dans les paramètres globaux car on les génère dans main.py, mais on a besoin de les utiliser dans RepertoireComptable.py)


#def extraction_N1(N0):
#    '''Création d'une base fictive de nom de comptable'''
#    L = liste_sous_chemin(N0)[1]
#    M = []
#    for k in range(len(L)):
#        if L[k][:4] != '0200':
#            M.append(L[k][:4])
#        else :
#            M.append(L[k][:6])
#    return M