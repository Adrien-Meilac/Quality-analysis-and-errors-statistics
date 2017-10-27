# -*- coding: utf-8 -*-
# Fichier Arborescence.py
# Offre des fonctions qui facilitent l'utilisation des arborescences de fichiers et de répertoires

import os


def liste_sous_chemin(chemin_parent):
    '''Renvoit l'arborescence (au premier niveau uniquement)
        *args = chemin_parent : chemin dont on veut écrire l'aborescence
        *out = (fichier, repertoire) avec des liens sous forme de noms (chemin relatifs et non absolus)
    '''
    L = os.listdir(chemin_parent)
    F = [] # Stocke les liens des fichiers
    R = [] # Stocke les liens des repertoires
    for lien in L:
        if os.path.isfile(chemin_parent + "/" + lien): #teste si le lien est un fichier ou un répertoire
            F.append(lien)
        else :
            R.append(lien)
    return (F, R)    
    

def nb_fichier_arborescence(chemin):
    '''Fonction récursive qui renvoit le nombre de fichier dans l'arborescence
        *args = chemin : chemin vers le répertoire dont on veut compter le nombre de sous fichier
        *out = nombre de fichiers dans un répertoire
    '''
    (F, R) = liste_sous_chemin(chemin) #On regarde tous les sous liens de niveau 1 
    s = 0
    for f in F: # On compte les fichiers
        (_, ext) = os.path.splitext(f)
        if not(ext == '.db' or ('#' == ext[-1])): # Attention, dans le compte on n'inclue pas les fichiers systèmes générés par python et les fichiers en cours d'utilisation ods# et pdf#  
            s += 1
    if len(R) == 0: #Si on a que des fichiers alors on a tout compté
        return s
    return s + sum([nb_fichier_arborescence(chemin + '/' + r) for r in R]) # Sinon, on doit compter aussi les fichiers des sous-répertoires
 
    
def all_file_path(chemin):
    '''Fonction récursive qui renvoit les liens vers tout les fichiers contenus dans l'arborescence d'un répertoire
        *args = chemin : chemin vers le répertoire dont on veut définir les sous liens vers chaque fichier
        *out = liste des liens relatifs vers les fichiers de l'arborescence
    '''
    (F, R) = liste_sous_chemin(chemin) # On regarde les sous liens de niveau 1
    T = [ [chemin, f] for f in F ]    # On ajoute les liens relatifs pour les fichiers
    if len(R) == 0: # S'il n'y a pas de sous répertoire on a tous les liens relatifs pour les fichiers
        return T 
    for r in R: #Sinon, on va chercher dans les sous liens de répertoire les liens vers les fichiers récursivement
        T.extend(all_file_path(chemin + '/' + r))
    return T