# -*- coding: utf-8 -*-
# Fichier SauvegardeRepertoireComptable.py
# Contient des fonctions qui permettent d'écrire des fichiers excels à partir des données générées par RepertoireComptable.py

import VarGlobales as vg
import xlsxwriter

def sauvegarder_comptable(adresseStockage, nomComptable, EC, EM):
    '''Permet de sauvegarder un fichier excel pour un comptable donné
        *args = adresseStockage : endroit ou stocker le fichier (le répertoire doit déjà exister)
                nomComptable : nom du comptable stocké dans la variable globale liste_nom
                EC : Tableau des erreurs de comptage sous le format :
                    [Nfichier, NFichierFortementIncorrect, NFichierIncorrect, NExtIncorrecte, NDualInexistant, NNomage, NCorrompu, NImage, NReference]
                    chaque element est une liste de même longueur que la liste N3 globale
                EM : Tableau des messages d'erreurs pour chaque fichier sous le format :
                    [dossier, nom du fichier, message d'erreur, importance]
                    avec importance = 1 si 'erreur est peu importante et 2 si l'erreur est très importante
        *out = Ne renvoit rien
    '''
    workbook = xlsxwriter.Workbook(adresseStockage + "/" +"Comptable_" +str(nomComptable) + "_annee_" + str(vg.annee) +".xlsx") #Création d'un fichier excel
    worksheet = workbook.add_worksheet("Statistiques") # Création de la feuille de statistique
    bold_percent = workbook.add_format({'num_format': '00"%"','bold': True}) # Ajout d'un format spécial pour les pourcentages
    worksheet.write(0, 0, "Comptable : "+str(nomComptable)) 
    worksheet.write(0, 1, "Année : "+str(vg.annee))
    legende = ["Répertoire","Nombre de fichiers","Nombre de fichiers incorrects qui nécéssitent une relance",
              "Pourcentage de fichiers incorrects qui nécéssitent une relance",
              "Nombre de fichiers incorrects",
              "Pourcentage de fichiers incorrects","","",
              "Extension incorrecte",
              "ODS ou PDF inexistant", "Nomage incorrect", 
              "Fichier(s) corrompu(s)", "Image(s) non exploitable(s)", 
              "Mauvaise référence"]
    for j in range(len(legende)): # Ecriture de la légende
        worksheet.write(3, j, legende[j])
    for j in range(4, 4 + len(vg.N3)): # Ecriture des répertoires
        worksheet.write(j, 0, vg.N3[j-4])
    for i in range(2): # Ecriture du nombre de fichiers et du nombre de fichiers incorrects avec une erreur grave
        for j in range(len(vg.N3)):
            worksheet.write(j + 4, i + 1, EC[i][j])
    for j in range(len(vg.N3)): # Ecriture du nombre de fichiers incorrects (quelquesoit la gravité de l'erreur)
        worksheet.write(j + 4, 4, EC[2][j]) 
    for i in range(3, len(EC)): # Ecriture du tableau de détail des erreurs
        for j in range(len(vg.N3)):
            worksheet.write(j + 4, i + 5, EC[i][j])
    worksheet.write(len(vg.N3) + 4, 0, "Totaux")
    for i in [1,2,4] + [i + 5 for i in range(3, len(EC))]: # Ecriture des formules de calculs des totaux par colonne
        worksheet.write(len(vg.N3) + 4, i, "=SUM({0}5:{0}{1})".format(chr(65 + i), len(vg.N3) + 4))
        
    worksheet.write(len(vg.N3) + 5, 0, "Pourcentage Totaux")
    for i in [2,4] + [i + 5 for i in range(3, len(EC))]:  # Ecriture des formules de calculs des pourcentages totaux par colonne
        worksheet.write(len(vg.N3) + 5, i, "=IF(B{1} = 0, 0, ROUNDUP({0}{1}/B{1}*100, 0))".format(chr(65 + i), len(vg.N3) + 5), bold_percent)
        
    for j in range(4,len(vg.N3) + 4): # Ecriture des formules de calculs des pourcentages totaux par ligne pour les nombres de fichiers incorrects (avec et sans les erreurs légères)
        worksheet.write(j, 3, "=IF(B{1} = 0, 0 , ROUNDUP({0}{1}/B{1}*100,0))".format(chr(65 + 2), j + 1), bold_percent)
        worksheet.write(j, 5, "=IF(B{1} = 0, 0 , ROUNDUP({0}{1}/B{1}*100,0))".format(chr(65 + 4), j + 1), bold_percent)
        
    worksheet2 = workbook.add_worksheet("Message d'erreur")# On ajoute la page message d'erreur au fichier excel
    legende = ["Repertoire","Nom du fichier","Message d'erreur"]
    for j in range(len(legende)): # On ecrit la legende 
        worksheet2.write(0, j, legende[j]) 
    
    erreur_importante = workbook.add_format({'bold': True, 'font_color': '#9C0006'}) #code couleur rouge et gras pour les erreurs importantes
    erreur_legere = workbook.add_format({'font_color': '#FF6600'}) #code couleur orange pour les erreurs legeres
    zeroformat = workbook.add_format({})
    
    J = 1
    for p in range(len(vg.N3)): # On écrit le tableau en ajoutant des liens clicables pour le dossier et le fichier
        worksheet2.write(J,0, vg.N3[p])
        for i in range(len(EM[p])):
            if EM[p][i][3] == 2: # erreur importante, on colore la case en rouge et on met en gras
                worksheet2.write_url(J + 1 + i, 0, EM[p][i][0], erreur_importante, vg.N3[p])
                worksheet2.write_url(J + 1 + i, 1, EM[p][i][0] + '/' + EM[p][i][1], erreur_importante, EM[p][i][1])
                worksheet2.write(J + 1 + i, 2, EM[p][i][2] ,erreur_importante)
            elif EM[p][i][3] == 1: # erreur legere, on colore la case en orange
                worksheet2.write_url(J + 1 + i, 0, EM[p][i][0], erreur_legere, vg.N3[p])
                worksheet2.write_url(J + 1 + i, 1, EM[p][i][0] + '/' + EM[p][i][1], erreur_legere, EM[p][i][1])
                worksheet2.write(J + 1 + i, 2, EM[p][i][2] ,erreur_legere)
            else: # Ecriture des titres de répertoires
                worksheet2.write_url(J + 1 + i, 0, EM[p][i][0], zeroformat, vg.N3[p])
                worksheet2.write_url(J + 1 + i, 1, EM[p][i][0] + '/' + EM[p][i][1], zeroformat, EM[p][i][1])
                worksheet2.write(J + 1 + i, 2, EM[p][i][2])
        J += len(EM[p]) + 2
    workbook.close()
    return

    
def sauvegarder_analyse_globale_comptables(adresseStockage, ECG, EMG):
    '''Permet de sauvegarder sous format excel l'analyse de tous les comptables donnés d'une année (paramètres globaux : annee, liste_nom)
        *args = adresseStockage : endroit ou stocker le fichier (le répertoire doit déjà exister)
                ECG : Tableau des erreurs de comptage général sous le format :
                    [Nfichier, NFichierFortementIncorrect, NFichierIncorrect, NExtIncorrecte, NDualInexistant, NNomage, NCorrompu, NImage, NReference]
                    chaque element est une liste de même longueur que la liste N3 globale
                EMG : Tableau des comptables ayant au moins un fichier dont l'erreur est importante sous le format :
                    [nom du comptable, nombre d'erreurs]
        *out = Ne renvoit rien
    '''
    ## Ecriture de ECM
    legende = ["Répertoire","Nombre de fichiers","Nombre de fichiers incorrects qui nécéssitent une relance",
              "Pourcentage de fichiers incorrects qui nécéssitent une relance",
              "Nombre de fichiers incorrects",
              "Pourcentage de fichiers incorrects","","",
              "Extension incorrecte",
              "ODS ou PDF inexistant", "Nomage incorrect", 
              "Fichier(s) corrompu(s)", "Image(s) non exploitable(s)", 
              "Mauvaise référence"]
    workbook = xlsxwriter.Workbook(adresseStockage + "/" +"Etude_globale_" + str(vg.annee) +".xlsx") # Création d'un fichier excel pour l'analyse globale
    worksheet = workbook.add_worksheet("Etude globale") # Création d'une page de statistique globale
    bold_percent = workbook.add_format({'num_format': '00"%"','bold': True}) # Création d'un format spécial pour les cases contenant des statistiques
    worksheet.write(0, 0, "Etude de tous les comptables")
    worksheet.write(0, 1, "Année : " + str(vg.annee))
    for j in range(len(legende)): # Ecriture de la legende
        worksheet.write(3, j, legende[j])
    for j in range(4, 4 + len(vg.N3)): # Ecriture du nom des repertoires
        worksheet.write(j, 0, vg.N3[j-4])
    for i in range(2): # Ecriture des colonnes Nombres de fichiers et Nombre de fichiers incorrects qui nécessitent une relance
        for j in range(len(vg.N3)):
            worksheet.write(j + 4, i + 1, ECG[i][j])
    for j in range(len(vg.N3)): # Ecriture de la colonne Nombre de fichiers incorrects (inclus les fichiers qui ont des erreurs moins importantes)
        worksheet.write(j + 4, 4, ECG[2][j]) 
    for i in range(3, len(ECG)): # Ecriture du détail des erreurs
        for j in range(len(vg.N3)):
            worksheet.write(j + 4, i + 5, ECG[i][j])
    worksheet.write(len(vg.N3) + 4, 0, "Totaux")
    for i in [1,2,4] + [i + 5 for i in range(3, len(ECG))]: # Ecriture des formules de calculs des totaux par colonne
        worksheet.write(len(vg.N3) + 4, i, "=SUM({0}5:{0}{1})".format(chr(65 + i), len(vg.N3) + 4))
        
    worksheet.write(len(vg.N3) + 5, 0, "Pourcentage Totaux")
    for i in [2,4] + [i + 5 for i in range(3, len(ECG))]: # Ecriture des formules de calculs des pourcentages totaux par colonne
        worksheet.write(len(vg.N3) + 5, i, "=IF(B{1} = 0, 0, ROUNDUP({0}{1}/B{1}*100, 0))".format(chr(65 + i), len(vg.N3) + 5), bold_percent)
        
    for j in range(4,len(vg.N3) + 4): # Ecriture des formules de calculs des pourcentages totaux par ligne pour les nombres de fichiers incorrects (avec et sans les erreurs légères)
        worksheet.write(j, 3, "=IF(B{1} = 0, 0 , ROUNDUP({0}{1}/B{1}*100,0))".format(chr(65 + 2), j + 1), bold_percent)
        worksheet.write(j, 5, "=IF(B{1} = 0, 0 , ROUNDUP({0}{1}/B{1}*100,0))".format(chr(65 + 4), j + 1), bold_percent)
    
    ## Ecriture de EMG :
    worksheet2 = workbook.add_worksheet("Comptable à relancer") # Création d'une page dans le fichier
    legende = ["Comptable", "Nombre d'erreur graves"] 
    for j in range(len(legende)): # Ecriture de la legende
        worksheet2.write(0, j, legende[j])
    for i in range(2): # Ecriture du tableau EMG
        for j in range(len(EMG)):
            worksheet2.write(j + 1, i, EMG[j][i])
            
    workbook.close()
    return