#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

from tkinter import *
fields = []

def fetch(entries):
   for entry in entries:
      field = entry[0]
      text  = entry[1].get()
      print('%s: "%s"' % (field, text)) 

def save(entries):
   for entry in entries:
      field = entry[0]
      text  = entry[1].get()

def makeform(root, fields):
   entries = []
   for idx,field in enumerate(fields):
      lab = Label(root, width=15, text=field, anchor='w')
      ent = Entry(root)
      lab.grid(row=idx, column=0)
      ent.grid(row=idx, column=1)
      # liste des couleurs
      lst1 = ['Red','Green','Blue']
      var1 = StringVar()
      Drop = OptionMenu(root,var1,*lst1)
      Drop.grid(row=idx, column=2)
      entries.append((field, ent))
   return entries

def suivant():
   nb_joueurs = int(Entry1.get())
   print(nb_joueurs)
   for k in range(0,nb_joueurs):
      fields.append("Joueur"+str(k+1))
   ents = makeform(root, fields)
   root.bind('<Return>', (lambda event, e=ents: fetch(e)))  # a changer
   b1.grid_forget()
   Entry1.grid_forget()
   Lbl1.grid_forget()
   b2 = Button(root, text='Jouer',command=(lambda e=ents: fetch(e)))
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


 