# -*- coding: utf-8 -*-
# Fichier IOfonction.py
# Contient toutes les fonctions qui accèdent à des documents externes au code
import io
import PyPDF2

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage 

def lire_csv(adresse, nom):
    '''lit un csv basique et renvoit le résultat sous forme de tableau'''
    flux = open(adresse + '/' + nom + '.csv', 'r')
    texte = flux.read()
    L = texte.split("\n")
    T = []
    for l in L:
        T.append(l.split(";"))
    return T
    
def lecture_base(adresse, nom):
    '''Lecture de la base des comptables sous format txt'''
    flux = open(adresse + '/' + nom + ".txt", "r")
    L = flux.read().splitlines()
    flux.close()
    return L


def ecrire_csv(adresse, nom, T):
    '''permet d'écrire un tableau dans un csv (nom sans extension) peu importe le format des colonnes'''
    flux = open(adresse + "/" + nom + ".csv", "w")
    for t in T:
        ligne = ''
        for element in t:
            ligne += str(element) + ';'
        ligne = ligne[:len(ligne)-1] + '\n'
        flux.write(ligne)
    flux.close()
    return


def pdf_non_vide(adresse):
    '''Renvoit un boléen pour savoir si le texte est non vide uniquement dans les 5 premieres pages'''
    try : 
        flux = open(adresse, 'rb')
        DocPDF = PyPDF2.PdfFileReader(flux)
        n = min(DocPDF.numPages, 3)
        for i in range(n):
            if len(DocPDF.getPage(i).extractText()) > 0:
                flux.close()            
                return (True, True)
        flux.close()
        return (True, False)
    except:
        return (False, '')
 
 
def est_dans(L,M):
    '''Indique les elements de L dont l'info est contenue dans M'''
    B = []
    for i in range(len(L)):
        est_dedans = False
        for j in range(len(M)):
            if L[i] in M[j]:
                est_dedans = True
                B.append([i,j])
                break
        if not est_dedans:
            B.append([i,-1])
    return B 
    
def recherche_mot(adresse, mot, rev = False):
    '''Renvoit un boleen qui indique si le mot est dans le pdf uniquement dans les 5 premieres pages'''
    mot2 = ''.join(mot)
    try : 
        flux = open(adresse, 'rb')
        DocPDF = PyPDF2.PdfFileReader(flux)
        if not(rev):
            I = [i for i in range(min(DocPDF.numPages, 4))]
        else: 
            I = [i for i in range(DocPDF.numPages - 3, DocPDF.numPages)]
            
        for i in I:
            page = DocPDF.getPage(i)
            try :
                rot = 270 - page.get('/Rotate')
                page.rotateClockwise(rot)
            except :
                    rot = 0
            L = page.extractText().split( )
            # Recherche du mot lorsque la page est bien construite   
            for p in range(len(L) - len(mot)):
                if L[p:p + len(mot)] == mot:
                    flux.close()
                    return True
            # Si la page est mal construite, le mot sera dans le texte mais il n'y aura pas d'espace, on le repere, et on utilise convert_pdf_txt sur la page concernée
            if i  > 0:
                for el in L:
                    if mot2 == el:
                        return True
                    for p in range(len(el) - len(mot2) + 1):
                        if el[p:p + len(mot2)] == mot2:
                            for rot in range(0,360,90):
                                texte = convert_pdf_to_txt(adresse, i, rot)
                                L = texte.split( )
                                for p in range(len(L) - len(mot) + 1):
                                    if L[p:p + len(mot)] == mot:
                                        return True
                            return False
        return False
    except IOError:
        return False
   
   
def convert_pdf_to_txt(adresse,i, rot = 0):
    '''Converti une page pdf en texte (méthode lente mais précise)'''
    flux = open(adresse, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pagenos = set([i])
    for page in PDFPage.get_pages(flux, pagenos = pagenos):
        page.rotate = rot
        interpreter.process_page(page)
    text = retstr.getvalue()
    device.close()
    retstr.close()
    flux.close()
    return text
