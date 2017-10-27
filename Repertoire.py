# -*- coding: utf-8 -*-

import os # Utilisé pour confirmer l'existence d'un fichier
import VarGlobales as vg # Contient des paramètres globaux utiles pour la recherche
import Arborescence as arb # Contient les fonctions qui permettent d'accéder plus simplement aux fichier
import InfoFichier as inf  # Contient les méthodes d'études pour chaque fichier

def Repertoire_N3(i, noprint = False): 
    '''Renvoit un tableau d'étude détaillée des fichiers contenu dans un type de répertoire défini par la variable N3 (variable globale)
        *args = i : on génère la table définie par N3[i]
                noprint : affiche le lien du fichier qui vient d'être parcouru (utile car le programme met 1h)
                          par défaut l'affichage est mis, préciser noprint = True pour le supprimer lors de l'exécution
        *out = tableau sous forme de liste de liste. Chaque ligne est définie par :
               [Comptable, adresse, f, ext, Bextcorrecte, dual, Bnomage,Bcodic, Btype, Bannee, Trim, Bouverture, Btexte, Bref] 
               adresse = lien vers le répertoire qui contient le fichier
               f = nom du fichier
               ext = extension du fichier
               Bextcorrecte = l'extension du fichier est elle celle attendue (par rapport à Ext autorisé défini en variable globale)
               dual = Le fichier ODS et PDF du même nom existe t'il ? (uniquement pour les R104bis)
               Bnomage = Le fichier a-t-il le bon nommage ? (Les 4 conditions suivantes doivent être respectées)
               Bcodic = Le fichiers a-t-il le bon codic ? (4 premiers chiffres du nom)
               Btype = le type du fichier (au milieu du nom) correspond-t-il au type attendu (défini dans Ftype en variable globale)
               Bannee = l'année écrite dans le nom du fichier est-elle la bonne ?
               Trim = Trimestre trouvé et bien mis dans le nom (pour les fichier REP310 uniquement)
               Bouverture = Le fichier peut-il être ouvert ? 
               Btexte = Le fichier contient-il du texte ? 
               Bref = Le fichier contient-il la bonne référence ? (la référence est définie dans Search, paramètre global)
    '''     
    legende = ['comptable','adresse', 'fname', 'ext', 'Bextcorrecte', 'dual','Bnomage', 'Bcodic', 'Btype', 'Bannee', 'Trim','Bouverture', 'Btexte','Bref']
    T = [legende]  # On écrit la légende dans le tableau
    for niv1 in vg.N1:
        adresse = vg.N0 +"/" + niv1 + "/" + vg.N2 + "/" + vg.N3[i] # On parcours tous les comptables et on cherche le répertoire N3[i]
        if os.path.exists(adresse): #S'il existe, alors :
            Lien = arb.all_file_path(adresse) #On regarde tous les fichiers qu'il y a dedans
            for [chemin, f] in Lien:
                if niv1[:4] != '0200': 
                    ligne = inf.info_fichier(chemin, f, i, niv1[:4]) # On demande des infos sur chaque fichier (fonction de InfoFochier.py)
                else:
                    if 'CORSE_SUD' in niv1: # Attention, pour la corse, le codic est particulier !!
                        ligne = inf.info_fichier(chemin, f, i, '02A0')
                    else:
                        ligne = inf.info_fichier(chemin, f, i, '02B0')
                if not(ligne[2] == 'db' or '#' == ligne[2][-1]): # On s'assure qu'il ne s'agit pas d'un fichier système d'extension .db ou d'un fichier en cours de lecture ods# ou pdf#
                    if not(noprint):
                        print(chemin + '/' + f) # On affiche le chemin du fichier qu'on vient de regarder
                    T.append([niv1] + ligne) # On ajoute la ligne au tableau qu'on crée                      
    return T #On renvoit le tableau
