# -*- coding: utf-8 -*-
# Fichier AnaGlobale.py
# Réalise l'analyse globale des répertoire en indiquant le nombre de fichiers dans chacun

import IOfonction as io # La fonction est_dedans qui apparie chaque nom de liste_nom (paramètre global) à des liens réels
import VarGlobales as vg # Accès aux chemins de l'arborescence et aux nomx de comptables
import Arborescence as arb # Parcours de l'arborescence


def Analyse_globale():
    '''Genere la table Analyse_globale
        *args = None
        *out = Un tableau (liste de listes) avec pour chaque ligne la forme:
            ['comptable','exist_comptable','Boriginaux', nombre de fichier dans le répertoire N3[i] de chaque comptable]
            comptable = numéro issu de la liste des comptables
            exist_comptable = Le comptable existe-t-il dans les chemins ?
            Boriginaux = Le nom "Fichier_Originaux" existe t-il dans le répertoire d'un comptable donné ?
    '''
    legende = ['comptable','exist_comptable','Boriginaux'] + vg.N3
    T = [legende]
    L1 = arb.liste_sous_chemin(vg.N0)[1]        
    B = io.est_dans(vg.liste_nom, L1)# On associe chaque nom de liste_nom à un nom de chemin réel si c'est possible
    for [i,j] in B: # On accède au niveau 1
        indic_comptable = i        # Indice du comptable dans le fichier texte
        exist_comptable = (j >= 0) # Existence du comptable avec l'indice i, -1 = indice si aucun lien réel correspond au comptable de la liste liste_nom
        Boriginaux = False
        Brep = [-1] * len(vg.N3)
        if exist_comptable:
            lien = vg.N0 + "/" + L1[j]
            L2 = arb.liste_sous_chemin(lien)
            if vg.N2 in L2[1]: # On accède au niveau 2 "Fichier_Originaux" s'il existe
                Boriginaux = True
                lien += "/" + vg.N2
                L3 = arb.liste_sous_chemin(lien)
                for k in range(len(vg.N3)): 
                    if vg.N3[k] in L3[1]: # On accède à chaque répertoire de niveau 3 s'il existe 
                        Brep[k] = arb.nb_fichier_arborescence(lien + "/" + vg.N3[k]) # et on compte le nombre de fichier dedans
        ligne = ["\'"+ vg.liste_nom[indic_comptable] + "\'", exist_comptable, Boriginaux] + Brep
        T.append(ligne)
    return T