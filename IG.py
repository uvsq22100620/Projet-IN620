##### Interface Graphique #####

#pip install customtkinter
#pip install customtkinter --upgrade

import customtkinter as ctk
import tkinter as tk

def comptePasDiese(liste):
    """ Renvoie le nombre d'éléments qui ne sont pas des dièses dans une liste"""

    nb = 0

    for elt in liste:
        if elt != '#':
            nb += 1

    return nb


def affichage_registres(config_registres):
    """ Prend en entrée un dictionnaire des états des registres après l'exécution d'une instruction et affiche ces registres"""
    
    global app_P1

    # Calcul de la taille maximale des registres (tous confondus)
    #max_elts_dans_un_registre = 0
##### dire qu'on sait comment adapter la taille et tout (discussion discord 04/04 19h)
    #for config in listes_config_registres:
    #    max_elts_dans_un_registre = max(max_elts_dans_un_registre, comptePasDiese(dico_elt_RAM['registres_i']))
    #    max_elts_dans_un_registre = max(max_elts_dans_un_registre, comptePasDiese(dico_elt_RAM['registres_r']))
    #    max_elts_dans_un_registre = max(max_elts_dans_un_registre, comptePasDiese(dico_elt_RAM['registres_o']))
    
    longueur_registres = 500
    largeur_registres = 25

    canvas = ctk.Canvas(app_P1, width=700, height=550, bg="lightgrey")
    canvas.pack()

    reg_i = canvas.create_rectangle(20, 20, 20+longueur_registres, 20+largeur_registres, fill='green')
    reg_r = canvas.create_rectangle(60, 20, 60+longueur_registres, 60+largeur_registres)
    reg_o = canvas.create_rectangle(100, 20, 20+longueur_registres, 20+largeur_registres)

    return

def lance_app_P1():

    global app_P1

    app_P1 = ctk.CTk()
    app_P1.geometry("700x550")
    app_P1.title("Simulation de l'exécution d'une machine RAM")
    longueur_registres = 500
    largeur_registres = 25

    canvas = tk.Canvas(app_P1, width=700, height=550, bg="lightgrey")
    canvas.pack()

    reg_i = canvas.create_rectangle(20, 20, 20+longueur_registres, 20+largeur_registres, fill='green')
    reg_r = canvas.create_rectangle(60, 20, 60+longueur_registres, 60+largeur_registres, fill='green')
    reg_o = canvas.create_rectangle(100, 20, 20+longueur_registres, 20+largeur_registres, fill='green')

    #affichage_registres([0])

    app_P1.mainloop()

def lance_app_P2():

    app_P2 = ctk.CTk()
    app_P2.geometry("700x550")
    app_P2.title("Simulation d'un automate à pile avec une machine RAM")

    app_P2.mainloop()

def lance_app_P3():

    app_P3 = ctk.CTk()
    app_P3.geometry("700x550")
    app_P3.title("Optimisation de la machine RAM")

    app_P3.mainloop()


def lance_app_accueil():

    # Création de l'application
    app_accueil = ctk.CTk()
    app_accueil.geometry("420x190")
    app_accueil.title("Projet_IN-620")

    # Affichage du label du choix
    l_choisissez = ctk.CTkLabel(app_accueil, text="Choisissez une partie du projet")
    l_choisissez.grid(row=0, column=0)

    # Affichage des 3 boutons pour basculer sur les autres applications
    b_choixP1 = ctk.CTkButton(app_accueil, text="Simulation de l'exécution d'une machine RAM", command=lance_app_P1)
    b_choixP2 = ctk.CTkButton(app_accueil, text="Simulation d'un automate à pile avec une machine RAM", command=lance_app_P2)
    b_choixP3 = ctk.CTkButton(app_accueil, text="Optimisation de la machine RAM", command=lance_app_P3)
    b_choixP1.grid(row=1, column=0, padx=20, pady=10)
    b_choixP2.grid(row=2, column=0, padx=20, pady=10)
    b_choixP3.grid(row=3, column=0, padx=20, pady=10)

    app_accueil.mainloop()

    return


# Appel de la fonction pour démarrer l'application
#lance_app_accueil()
