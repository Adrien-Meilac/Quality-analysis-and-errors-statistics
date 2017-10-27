# -*- coding: utf-8 -*-
# Fichier InfoFichier.py
# Calcule différentes informations sur le fichier 

import os # Pour tester l'existence de fichiers et pour séparer le nom du fichier de son extension (compliqué à faire manuellement)
import IOfonction as io # Pour accéder aux options de lecture de pdf
import VarGlobales as vg # Accès aux chemins de l'arborescence et aux nomx de comptables pour vérifier les codics et faire des exceptions en fonction du type de répertoire
from copy import copy # Pour copier les objets par valeur et non par référence

def info_fichier(adresse, f, i, codic):
    ''' Renvoit les informations sur un fichier
        *args = adresse : lien vers le répertoire contenant le fichier
                f : nom du fichier avec extension
        *out = liste sous la forme
                [adresse, f, ext, Bextcorrecte, dual, Bnommage, Bcodic, Btype, Bannee, Trim, Bouverture, Btexte, Bref]
                adresse : l'adresse du repertoire contenant le fichier
                f : nom du fichier avec extension (car il peut y avoir des espaces invisibles à la fin du nom sans extension)
                ext : extension
                Bext : L'extension du fichier est elle la bonne par rapport à une liste donnée par répertoire dans ExtAutorise (variable globale)
                dual : Pour les fichiers de type R104bis, existe-t-il un fichier de même nom en format ods et pdf ?
        
                Bnommage : le nommage du fichier est il correct ? 
                Btype : Le type du fichier est-il correct ?
                Bcodic : Le codic du fichier est-il correct ? 
                Bannee : l'annee du fichier est-elle bonne ?
                Trim : si le repertoire est du genre REP310, le fichier existe-t-il en un exemplaire pour chaque trimestre ?
                
                Bouverture : Le fichier peut-il être ouvert ?
                Btexte : Le fichier contient-il du texte ? 
                Bref : La référence définie dans Search (variable globale), spécifique au répertoire, apparait-elle dans le fichier ?
    '''
    (fname, ext) = os.path.splitext(f) # sépare le titre de l'extention
    Bouverture = 'True' # Par défaut, on peut l'ouvrir
    dual = ''           # Par défaut, la question ne se pose pas
    Btexte = Bref = ''  # Par défaut, les questions ne se posent pas
    ext = ext[1:].lower() # on met l'extension en minuscule et on retire le point devant (correction du cas des formats .PDF rencontrés)
    if (len(vg.ExtAutorise[i]) > 0 and ext in vg.ExtAutorise[i]) or len(vg.ExtAutorise[i]) == 0: # Si l'extension est dans la liste des extensions autorisées, on valide
        Bextcorrecte = 'True'
    else:
        Bextcorrecte = 'False'
    Titre = info_titre(adresse, fname, i, codic) # On demande des informations spécifiques au nom du fichier
    if ("Autre" in vg.N3[i]): # Si le fichier est "Autre" on effectue aucun test pour ne pas obtenir d'erreur
        return [adresse, f, ext, Bextcorrecte, dual] + Titre + [Bouverture, Btexte, Bref] 
    try : # Sinon, on essaye d'ouvrir le fichier
        flux = open(adresse + "/" + f, "rb")
        flux.close()
        if ext == 'pdf': # Si c'est un pdf alors :
            if ("104" in vg.N3[i]): # S'il est du genre R104, on vérifie qu'il y a bien un ods correspondant, mais on se fiche de ce qu'il contient
                dual = str(os.path.isfile(adresse + "/" + fname + '.' + 'ods'))
            else: # Sinon, on va voir si on peut voir du texte dans le pdf, Bouverture ici provient du fait que le lecteur peut ne pas arriver à lire le fichier s'il est corrompu
                (Bouverture, Btexte) = io.pdf_non_vide(adresse + "/" + fname + '.' + 'pdf')
                (Bouverture, Btexte) = (str(Bouverture), str(Btexte)) # Les informations sont stockées comme des chaines de caractères pour ne pas avoir des formats différents pour chaque valeur/colonne 
                if len(vg.Search[i]) == 0 or Btexte != 'True': # Si on n'a pas de mot à chercher ou que c'est une image, on ne recherche rien dans le pdf
                    Bref = ''
                else: #Sinon, on effectue une recherche de mots
                    if ("204" in vg.N3[i]) and "R204" in fname: #dans le cas des "R204", il faut regarder à la fin du fichier (le premier test en soi est inutile sauf pour vérifier que le fichier est bien dans le bon répertoire) 
                        Bref = str(io.recherche_mot(adresse + "/" + fname + '.' + 'pdf', vg.Search[i], rev = True))
    
                    else:  # Dans les autres documents il faut regarder au début
                        Bref = str(io.recherche_mot(adresse + "/" + fname + '.' + 'pdf', vg.Search[i]))
        elif ext == 'ods' and ("104" in vg.N3[i]): # Dans le cas des ods, on cherche aussi le dual
            dual = str(os.path.isfile(adresse + "/" + fname + '.' + 'pdf'))
    except IOError: # Si on a pas réussi à ouvrir le fichier, on le met dans Bouverture et on ne fait rien à l'interieur du fichier
        Bouverture = 'False'
    return [adresse, f, ext, Bextcorrecte, dual] + Titre + [Bouverture, Btexte, Bref] 
    

def info_titre(adresse, fname, i, codic):
    '''Renvoit les informations relatives au nom du fichier spécifiquement
        *args = adresse : lien vers le répertoire contenant le fichier
                fname : nom du fichier sans extension
        *out = liste sous la forme
                [Bnommage, Bcodic, Btype, Bannee, Trim]
                Bnommage : le nommage du fichier est il correct ? 
                Btype : Le type du fichier est-il correct ?
                Bcodic : Le codic du fichier est-il correct ? 
                Bannee : l'annee du fichier est-elle bonne ?
                Trim : si le repertoire est du genre REP310, le fichier existe-t-il en un exemplaire pour chaque trimestre ?
    '''
    L = fname.split("_") # découpage du nom par rapport aux underscores
    Bcodic = False  
    Btype = False 
    Bannee = False 
    Trim = ''
    if "Autre" in vg.N3[i]: # Dans la catégorie autre, tout est bien, on ne cherche aucune erreur
        return ["True"] * 4 + [""]
    if len(L) not in [3,4]: # Si la liste ne se découpe pas comme il faut : on cherche le codic sur les premiers caractères quand même :
        # On spécifie pour les 310 le trimestre d'où les tests suivant
        if len(fname) >= 4 and fname[:4] == codic and ("310" in vg.N3[i]):
            return ["True"]  + ["False"] * 4
        elif len(fname) >= 4 and fname[:4] == codic and not("310" in vg.N3[i]):
            return ["True"]  + ["False"] * 3 + ['']
        elif not(len(fname) >= 4 and fname[:4] == codic) and ("310" in vg.N3[i]):
            return ["False"] * 5
        else:
           return ["False"] * 4 + [''] 
    elif len(L) == 4: # Cas du rep 310 ou le nom se retrouve découpé en 2 entre REP310 et 1T par exemple, on rassemble ces deux parties
        L = [L[0], L[1] + "_" + L[2], L[3]]
     
    # Le cas est normal : le nom doit être en trois parties (codic, type, annee)
    if L[0][:4] == codic: # Vérification du codic au début du nom
        Bcodic = True
    
    for j in range(len(vg.Ftype[i])): # Vérification du type par rapport à une liste préféfinie dans Ftype 
        if L[1] == vg.Ftype[i][j]:
            Btype = True
    if Btype and ("310" in vg.N3[i]): # Cas particulier des fichiers de type REP310, on s'interresse au trimestre
        Trim = True
        for p in range(1,5): # On regarde s'il existe bien un fichier par trimestre de nom similaire
            M = copy(L)
            M[1] = "REP310_{}T".format(p)
            fnamebis = '_'.join(M) + ".pdf"
            if not(os.path.isfile(adresse + "/" + fnamebis)):
                Trim = False
        
    if L[2] == str(vg.annee): # Vérification de l'année à la fin du mot
        Bannee = True
        
    Bnommage = Bcodic and Btype and Bannee # Avoir un bon nomage c'est vérifier les 3 conditions précédentes
    
    return [str(Bnommage), str(Bcodic), str(Btype), str(Bannee), str(Trim)]
