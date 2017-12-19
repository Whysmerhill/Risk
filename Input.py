#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

from tkinter import *
#Imports de porc
import Risk
from Risk import *
import GUI
from GUI import *

fields = []
PLAYERS_COLORS=['red','green','blue','yellow','purple','cian']
MAX_NB_PLAYERS=6
MIN_NB_PLAYERS =3
CLOCK_TICK=60 #refresh rate

def fetch(entries):
   for entry in entries:
      field = entry[0]
      text = entry[1].get()
      color=entry[2].get()
      print('%s: "%s" %s' % (field, text,color))

def correspondance_colors(nameofcolor,colormap):
   if nameofcolor =='red':
      return colormap.red
   elif nameofcolor=='green':
      return colormap.green
   elif nameofcolor=='blue':
      return colormap.blue
   elif nameofcolor=='yellow':
      return colormap.yellow
   elif nameofcolor=='purple':
      return colormap.purple
   elif nameofcolor=='cian':
      return colormap.cian

def launch_game(entries):
   #on verifie que deux joueurs n'ont pas la meme couleur, pas de nom vide
   try:
      players_names=[]
      players_colors=[]
      for entry in entries:
         players_names.append(entry[1].get())
         if entry[1].get()=='':
            raise ValueError('Vous devez choisir un nom de joeur')
         players_colors.append(entry[2].get())
      seen = set()
      uniq = []
      for c in players_colors:
         if c not in seen:
           uniq.append(c)
           seen.add(c)
      if not len(uniq)==len(players_names):
         raise ValueError('Vous devez choisir une couleur différente pour chaque joeur:')
   except ValueError as e:
         print (e.args)
   else:
      root.destroy() #exiting the players choicd window

      print("== Game launched ==")
      M=Map('Terre')
      Continents=M.continents
      nb_players=len(players_names)
      T=Turns(nb_players,M)
      T.start_deploy()
      print(T.distrib_pays(M.pays))
      T.print_players()
      #M.print_pays()
      colors=ColorMap()
      for idx,play_name in enumerate(players_names):
         T.players[idx].color=correspondance_colors(players_colors[idx],colors)
         T.players[idx].name=play_name

      pygame.init()
      clock = pygame.time.Clock()
      fenetre = pygame.display.set_mode((f_w, f_h))
      Win=CurrentWindow(fenetre,T)
      Win.game.nb_joueurs=nb_players
      Win.game.joueurs=players_names
      menu(Win)                     #affiche ini
      Win.fonctions.append(Win.start_game)    #fonctions ini
      clock.tick(CLOCK_TICK)

      Win.afficher() #on rentre dans la boucle while d'affichage


def save(entries):
   for entry in entries:
      field = entry[0]
      text  = entry[1].get()

def check_colors(entries,lst1):
   for entry in entries:
      if entry[2].get() in lst1: lst1.remove(entry[2].get())   

def makeform(root, fields):
   entries = []
   for idx,field in enumerate(fields):
      lab = Label(root, width=15, text=field, anchor='w')
      ent = Entry(root)
      lab.grid(row=idx, column=0)
      ent.grid(row=idx, column=1)
      # liste des couleurs
      lst1 = PLAYERS_COLORS
      #Couleurs deja selectionnees

      var1 = StringVar()
      Drop = OptionMenu(root,var1,*lst1)
      Drop.grid(row=idx, column=2,sticky="ew") # make option menu with uniform width for all the rows 
      entries.append((field, ent,var1))
   return entries

def suivant():
   nb_joueurs = int(Entry1.get())
   if nb_joueurs<MIN_NB_PLAYERS:
      print("Minimum players number is "+str(MIN_NB_PLAYERS))
      nb_joueurs=MIN_NB_PLAYERS
   elif nb_joueurs>MAX_NB_PLAYERS:
      print("Maximum players number is "+str(MAX_NB_PLAYERS))
      nb_joueurs=MAX_NB_PLAYERS
   else:
      print(nb_joueurs)
   for k in range(0,nb_joueurs):
      fields.append("Joueur"+str(k+1))
   ents = makeform(root, fields)
   root.bind('<Return>', (lambda event, e=ents: fetch(e)))  # je comprends rien a ce que je fais
   b1.grid_forget()
   Entry1.grid_forget()
   Lbl1.grid_forget()
   b2 = Button(root, text='Jouer',command=lambda e=ents: launch_game(e)) 
   b2.grid(row=20, column=0)#pas prore
   b3.grid(row=20, column=1)#pas propre
   
if __name__ == '__main__':
   root = Tk()
   root.title("Risk")

   Lbl1 = Label(root, text="Nombre de joueurs:")
   Lbl1.grid(row=0, column=0,columnspan=2)
   Entry1 = Entry(root, bd =1)
   Entry1.grid(row=1, column=0,columnspan=2)

   b1 = Button(root, text='Suivant',command=suivant)
   b1.grid(row=2, column=0)
    
   b3 = Button(root, text='Quit', command=root.quit)
   b3.grid(row=2, column=1)
   root.mainloop()


 