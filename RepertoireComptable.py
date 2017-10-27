# -*- coding: utf-8 -*-
# Fichier RepertoireComptable.py
# Contient des fonction permettant de créer des données exploitables pour l'étude des différents comptables 

import VarGlobales as vg # Pour accéder à l'arborescence et à la liste des noms des comptables
from copy import deepcopy # Pour les copies par valeurs et non par références

   
def info_comptable(nomComptable):
    '''Crée un tableau spécifique au comptable à partir des répertoires créés
        *args: nomComtable sous une forme simifaire à celle sotckée dans base.txt
        *out : C est un tableau avec des lignes sous forme :
         ["Répertoire",'adresse', 'fname', 'ext', 'Bextcorrecte', 'dual','Bnomage', 'Bcodic', 'Btype', 'Bannee', 'Trim','Bouverture', 'Btexte','Bref']
         Les colonnes sont décrites dans le fichier Repertoire.py
    '''
    niv1 = ''
    for n1 in vg.N1:
        if nomComptable == n1[:len(nomComptable)]:
           niv1 = n1 
    if len(niv1) == 0:
        print("Le comptable " + nomComptable + " n'existe pas")
        return 
    C = [["Répertoire",'adresse', 'fname', 'ext', 'Bextcorrecte', 'dual','Bnomage', 'Bcodic', 'Btype', 'Bannee', 'Trim','Bouverture', 'Btexte','Bref']]  
    for i in range(len(vg.N3)):
        for ligne in vg.Rep[i][1:]: # On enlève la légende contenue dans le csv, ça suppose que tous les répertoires sont non vides
            if ligne[0] == niv1 :
                lign_copy = deepcopy(ligne) # Attention, on fait une copie par valeur sinon la liste d'origine sera modifiée
                lign_copy[0] = vg.N3[i]
                C.append(lign_copy)
    return C
    
def traitement_comptable(nomComptable):
    '''
        Calcule des statistiques globales et les comptables à relancer pour une année
            *args : nomComptable = nom sous le format d'entrée base.txt
            *out : EC : Tableau de comptage du nombres de fichiers dans différentes catégories sous le format:
                        [Nfichier, NFichierFortementIncorrect, NFichierIncorrect, NExtIncorrecte, NDualInexistant, NNomage, NCorrompu, NImage, NReference]
                        Nfichier = Liste du nombre de fichiers produit par les comptables de la liste pour une année en fonction du type de répertoire
                        NFichierFortementIncorrect =  Liste du nombre de fichiers ayant une erreur d'importance égale à 2 
                            produit par les comptables de la liste pour une année en fonction du type de répertoire
                        NFichierIncorrect = Liste du nombre de fichiers ayant une erreur (peu importe sa gravité) produit par les comptables de la liste pour une année en fonction du type de répertoire
                        NExtIncorrecte = Liste du nombre de fichiers ayant une extension incorrecte produit par les comptables de la liste pour une année en fonction du type de répertoire
                        NDualInexistant = Liste du nombre de fichiers ayant été produit uniquement en PDS ou en ODS produit par les comptables de la liste pour une année 
                            en fonction du type de répertoire mais comptabilisés uniquement dans le cas des R104
                        NNomage = Liste du nombre de fichiers ayant un nomage incorrect produit par les comptables de la liste pour une année en fonction du type de répertoire
                        NCorrompu = Liste du nombre de fichiers corrompus ou illisibles produit par les comptables de la liste pour une année en fonction du type de répertoire
                        NImage = Liste du nombre de fichiers étant des pdfs avec des images scannés au début produit par les comptables de la liste pour une année en fonction du type de répertoire, non comptabilisé dans le cas du R104
                        NReference = Liste du nombre de fichiers ayant une mauvaise référence à l'interieur produit par les comptables de la liste pour une année en fonction du type de répertoire, non comptabilisé pour la catégorie autre
    
                 EM : Tableau général de la liste des comptables ayant au moins une erreur grave et qu'il faut relancer :
                      [nom du comptable, nombre d'erreur graves]'''
    C = info_comptable(nomComptable)
    if C == None:
        return
    EM = [] # Message d'erreur
    Nfichier = [0] * len(vg.N3)
    NFichierFortementIncorrect = [0] * len(vg.N3)
    NFichierIncorrect = [0] * len(vg.N3)
    NExtIncorrecte = [0] * len(vg.N3)
    NDualInexistant = [0] * len(vg.N3)
    NNomage = [0] * len(vg.N3)
    NCorrompu = [0] * len(vg.N3)
    NImage = [0] * len(vg.N3)
    NReference = [0] * len(vg.N3)
    for i in range(len(vg.N3)):
        T = []
        for ligne in C[1:]:
            if ligne[0] == vg.N3[i]:
                Nfichier[i] +=1
                importance = 0 # 0 = fichier correct, 1 = incorrect mais legerement, 2 = incorrect et vraiment problématique
                msgErreur = []
                if ligne[4] == "False": # Mauvaise extension
                    NExtIncorrecte[i] += 1
                    importance = 2
                    msgErreur.append('Extension incorrecte')
                if ligne[5] == "False": # Le fichier dual existe t il ?
                    NDualInexistant[i] += 1
                    importance = 2
                    if ligne[3] == "pdf":
                        msgErreur.append("Le fichier ods de même nom n'existe pas")
                    elif ligne[3] == "ods":
                        msgErreur.append("Le fichier pdf de même nom n'existe pas")
                if ligne[6] == "False":
                    NNomage[i] += 1
                    importance = 1
                    msgErreur.append("Le nom est incorrect (causes probables : ")
                    c = True
                    if str(ligne[7]) == 'False':
                        msgErreur[-1] += 'codic incorrect'
                        c = False
                    if str(ligne[8]) == 'False':
                        if c == False:
                            msgErreur[-1] += ', '
                        msgErreur[-1] += 'type dans le nom incorrect'
                    if str(ligne[9]) == 'False':
                        if c == False:
                            msgErreur[-1] += ', '
                        msgErreur[-1] += 'année incorrecte'     
                    if str(ligne[10]) == '-1':    
                        if c == False:
                            msgErreur[-1] += ', '
                        msgErreur[-1] += 'trimestre incorrect ou illisible'
                    msgErreur[-1] += ')'
                if ligne[11] == "False":
                    NCorrompu[i] += 1
                    importance = 2
                    msgErreur.append("Le fichier est illisible")
                if ligne[12] == "False":
                    NImage[i] += 1
                    importance = 2
                    msgErreur.append("Le fichier est une image")
                if ligne[13] == "False":
                    NReference[i] += 1
                    importance = 2
                    msgErreur.append("Le fichier ne contient pas la bonne référence")
                if importance > 0: # Sil'erreur est importante, on note le fichier dans EM
                    NFichierIncorrect[i] += 1
                    if importance == 2:
                        NFichierFortementIncorrect[i] += 1
                    T.append([ligne[1], ligne[2], ", ".join(msgErreur), importance])
        EM.append(T)
    EC = [Nfichier, NFichierFortementIncorrect, NFichierIncorrect, NExtIncorrecte, NDualInexistant, NNomage, NCorrompu, NImage, NReference]
    return (EC, EM)
    
    
def ecrire_all_comptable(liste_comptable):    
    '''
        Calcule des statistiques globales et les comptables à relancer pour une année
            *args : liste_comptable = liste des comptables à prendre en considération
            *out : ECG : Tableau de comptage général du nombres de fichiers dans différentes catégories sous le format:
                        [Nfichier, NFichierFortementIncorrect, NFichierIncorrect, NExtIncorrecte, NDualInexistant, NNomage, NCorrompu, NImage, NReference]
                        Nfichier = Liste du nombre de fichiers produit par les comptables de la liste pour une année en fonction du type de répertoire
                        NFichierFortementIncorrect =  Liste du nombre de fichiers ayant une erreur d'importance égale à 2 
                            produit par les comptables de la liste pour une année en fonction du type de répertoire
                        NFichierIncorrect = Liste du nombre de fichiers ayant une erreur (peu importe sa gravité) produit par les comptables de la liste pour une année en fonction du type de répertoire
                        NExtIncorrecte = Liste du nombre de fichiers ayant une extension incorrecte produit par les comptables de la liste pour une année en fonction du type de répertoire
                        NDualInexistant = Liste du nombre de fichiers ayant été produit uniquement en PDS ou en ODS produit par les comptables de la liste pour une année 
                            en fonction du type de répertoire mais comptabilisés uniquement dans le cas des R104
                        NNomage = Liste du nombre de fichiers ayant un nomage incorrect produit par les comptables de la liste pour une année en fonction du type de répertoire
                        NCorrompu = Liste du nombre de fichiers corrompus ou illisibles produit par les comptables de la liste pour une année en fonction du type de répertoire
                        NImage = Liste du nombre de fichiers étant des pdfs avec des images scannés au début produit par les comptables de la liste pour une année en fonction du type de répertoire, non comptabilisé dans le cas du R104
                        NReference = Liste du nombre de fichiers ayant une mauvaise référence à l'interieur produit par les comptables de la liste pour une année en fonction du type de répertoire, non comptabilisé pour la catégorie autre
    
                 EMG : Tableau général de la liste des comptables ayant au moins une erreur grave et qu'il faut relancer :
                      [nom du comptable, nombre d'erreur graves]
    '''
    ECG = [[0 for i in range(len(vg.N3))] for i in range(9)]
    EMG = []
    for nomComptable in liste_comptable:
        a = traitement_comptable(nomComptable)
        if a != None: # Si le comptable existe...
            (EC, EM) = a
            for i in range(len(EC)): # On ajoute ses stats au stat globales
                for j in range(len(EC[0])):
                    ECG[i][j] += EC[i][j]
            nb_erreur_importante = 0    
            for p in range(len(vg.N3)): # On compte le nombre d'erreur que le comptable à fait qui sont graves
                for i in range(len(EM[p])):
                    if EM[p][i][3] == 2:
                        nb_erreur_importante += 1  
            if nb_erreur_importante > 0: # S'il a fait au moins une erreur grave, on le note dans EMG
                EMG.append([nomComptable, nb_erreur_importante])
    return (ECG, EMG)
    
