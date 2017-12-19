#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

import functools
import pygame
from pygame.locals import *
import Risk
import glob
import pickle 

PATH_IMG='Pictures/'
PATH_MAP='Pictures/Maps/'
PATH_BCK='Pictures/Backgrounds/'
PATH_DCE='Pictures/Dices/'
MAP_IMG='Risk_game_map_fixed_greylevel.png'
MAP_LVL='Risk_game_map_fixed_greylevel.png'
BCK_IMG='background5.jpg'
BAR_IMG='barre.png'
DHE_IMG='tete-de-mort.png'
POLICE_NAME='freesansbold.ttf'
POLICE_SIZE=16
DICE_SIZE=25
f_w=1280
f_h=800

class ColorMap():
	def __init__(self):
		self.green=(0,255,0)
		self.red=(255,0,0)
		self.blue=(0,0,255)
		self.white=(255,255,255)
		self.black=(0,0,0)
		self.grey=(100,100,100)
		self.yellow=(255,255,0)
		self.purple=(255,0,255)
		self.cian=(0,255,255)
		self.dark_purple=(127,0,255)
		self.dark_green=(0,170,0)
		self.dark_red=(170,0,0)
		self.dark_blue=(0,0,170)

#a mettre dans une classe
def text_objects(text, font,color=(0,0,0)):
	textSurface = font.render(text, True, color)
	return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if x+w > mouse[0] > x and y+h > mouse[1] > y:
		pygame.draw.rect(fenetre, ac,(x,y,w,h))
		if click[0] == 1 and action != None:
			Win.fonctions.append(action)
	else:
		pygame.draw.rect(fenetre, ic,(x,y,w,h))

	smallText = pygame.font.Font(POLICE_NAME,POLICE_SIZE)
	textSurf, textRect = text_objects(msg, smallText)
	textRect.center = ( (x+(w/2)), (y+(h/2)) )
	fenetre.blit(textSurf, textRect)

def color_surface(surface,color):
	for x in range(0,surface.get_width()):
		for y in range(0,surface.get_height()):
			if surface.get_at((x,y))!=(0,0,0):
				surface.set_at((x,y),color)

#not used right now
def color_surface_map(surface,color,map_color):
	for x in range(0,surface.get_width()):
		for y in range(0,surface.get_height()):
			if surface.get_at((x,y))==map_color:
				surface.set_at((x,y),color)
#useless?
def colorize(image, newColor):
    # zero out RGB values
    image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    # add in new RGB values
    image.fill(newColor[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

def color_surface(sprite,color,alpha):
	for x in range(0,sprite.bounds.width):
		for y in range(0,sprite.bounds.height):
			if sprite.map_pays.get_at((sprite.bounds.x+x,sprite.bounds.y+y))!=(0,0,0):
				sprite.map_pays.set_at((sprite.bounds.x+x,sprite.bounds.y+y),color)
				sprite.map_pays.set_alpha(alpha)

def add_text(layer,message,pos,font,color=(0,0,0)):
	textSurf, textRect = text_objects(message, font,color)
	textRect.topleft = pos
	layer.append([textSurf, textRect])

def display_troupes(textes,sprites,Map):
	smallText = pygame.font.Font(POLICE_NAME,POLICE_SIZE)
	for sprite in sprites:
		pays=Map.pays[sprite.id-1]
		textSurf, textRect = text_objects(str(pays.nb_troupes), smallText)
		textRect.center = sprite.bounds.center
		textes.append([textSurf, textRect])

def display_win(final_layer,players):
	bigText = pygame.font.Font(POLICE_NAME,42)
	marge=50
	pos=(200,200)
	for p in players:
		if p.obj.get_state()==True:
			p_win=p
			#player win
			textSurf, textRect = text_objects(p_win.name+' win', bigText,p_win.color)
			textRect.topleft = pos
			pos=(pos[0],pos[1]+marge)
			final_layer.append([textSurf, textRect])
			#objective
			textSurf, textRect = text_objects('Objective '+p_win.obj.description, bigText,p_win.color)
			textRect.topleft = pos
			pos=(pos[0],pos[1]+marge)
			final_layer.append([textSurf, textRect])

def display_help(final_layer,colormap):
	bigText = pygame.font.Font(POLICE_NAME,42)
	marge=50
	pos=(200,200)
	add_text(final_layer,'ESC : exit game',pos,bigText,colormap.white)
	pos=(pos[0],pos[1]+marge)
	add_text(final_layer,'n : next phase',pos,bigText,colormap.white)
	pos=(pos[0],pos[1]+marge)
	add_text(final_layer,'p : next player turn',pos,bigText,colormap.white)
	pos=(pos[0],pos[1]+marge)
	add_text(final_layer,'h : show/hide help menu',pos,bigText,colormap.white)
	pos=(pos[0],pos[1]+marge)
	add_text(final_layer,'d : show/hide quest',pos,bigText,colormap.white)
	pos=(pos[0],pos[1]+marge)
	add_text(final_layer,'u : use your cards',pos,bigText,colormap.white)

def display_hud(nb_units,t_hud,turns,pos,hide):
	smallText = pygame.font.Font(POLICE_NAME,POLICE_SIZE)
	marge=20
	col=[100,400,700,1000]
	row=pos[1]
	#partie joueur
	textSurf, textRect = text_objects('Tour : '+str(turns.num), smallText)
	textRect.topleft = pos
	t_hud.append([textSurf, textRect])
	textSurf, textRect = text_objects('Joueur : ',smallText)
	pos=(pos[0],pos[1]+marge)
	textRect.topleft = pos
	t_hud.append([textSurf, textRect])
	textSurf, textRect = text_objects(turns.players[turns.player_turn-1].name, smallText,turns.players[turns.player_turn-1].color)
	textRect.topleft = (pos[0]+70,pos[1])#pas propre
	t_hud.append([textSurf, textRect])
	textSurf, textRect = text_objects('Phase : '+turns.list_phase[turns.phase], smallText)
	pos=(pos[0],pos[1]+marge)
	textRect.topleft = pos
	t_hud.append([textSurf, textRect])
	textSurf, textRect = text_objects('Soldats par tours : '+str(turns.players[turns.player_turn-1].sbyturn), smallText)
	pos=(pos[0],pos[1]+marge)
	textRect.topleft = pos
	t_hud.append([textSurf, textRect])
	textSurf, textRect = text_objects('Soldats a deployer : '+str(turns.players[turns.player_turn-1].nb_troupes), smallText)
	pos=(pos[0],pos[1]+marge)
	textRect.topleft = pos
	t_hud.append([textSurf, textRect])
	textSurf, textRect = text_objects('Soldats selectionnes : '+str(nb_units), smallText)
	pos=(pos[0],pos[1]+marge)
	textRect.topleft = pos
	t_hud.append([textSurf, textRect])

	#partie objectifs
	textSurf, textRect = text_objects('Objectif(s) ', smallText)
	pos=(col[1],row)
	textRect.topleft = pos
	t_hud.append([textSurf, textRect])
	if hide==False:
		try:
			textSurf, textRect = text_objects(str(turns.players[turns.player_turn-1].obj.description), smallText)
		except AttributeError as e:
			print (e.args)
		pos=(col[1],row+marge)
		textRect.topleft = pos
		t_hud.append([textSurf, textRect])
		try:
			textSurf, textRect = text_objects('Statut : '+str(turns.players[turns.player_turn-1].obj.get_state()), smallText)
		except AttributeError as e:
			print (e.args)
		pos=(col[1],row+2*marge)
		textRect.topleft = pos
		t_hud.append([textSurf, textRect])

	#partie cartes
	textSurf, textRect = text_objects('Cartes ', smallText)
	pos=(col[1],row+3*marge)
	textRect.topleft = pos
	t_hud.append([textSurf, textRect])
	if hide==False:
		textSurf, textRect = text_objects(str(turns.players[turns.player_turn-1].cards), smallText)
		pos=(col[1],row+4*marge)
		textRect.topleft = pos
		t_hud.append([textSurf, textRect])

	#partie bonus des continents
	pos=(col[3],row)
	textSurf, textRect = text_objects('Bonus Continents', smallText)
	textRect.topleft = pos
	t_hud.append([textSurf, textRect])
	for idx,c in enumerate(turns.map.continents):
		pos=(col[3],row+(idx+1)*marge)
		textSurf, textRect = text_objects(c.name+' '+str(c.bonus), smallText)
		textRect.topleft = pos
		t_hud.append([textSurf, textRect])

def display_continent(cont,temp_layer,sprites_pays_masque):
	for p in cont.pays:
		temp_layer.append(next((x.map_pays for x in sprites_pays_masque if x.id == p.id), None))

def save_game(obj_lst):
	# Saving the objects:
	with open('saved_game', 'wb') as f:
		pickle.dump(obj_lst, f)
		print('Game saved')

def restore_game(obj_lst):
	# Getting back the objects:
	with open('saved_game','rb') as f:
		obj_lst=pickle.load(f)
		print('Game restored')

class GamePara():
	def __init__(self):
		self.nb_joueurs=0
		self.tour=0
		self.joueurs=[]

class SpritePays():
	def __init__(self,surface,name_id):
		self.map_pays=surface
		self.name_pays=''
		self.id=int(name_id[-6:-4])#pas tres propre
		self.bounds=surface.get_bounding_rect()

class CurrentWindow():
	def __init__(self,fenetre,turns):
		self.fenetre=fenetre
		self.fonctions=[]	#liste de l'ensemble des fonctions a exécuter
		self.surfaces=[] #liste de l'ensemble des surfaces à afficher
		self.dices=[] #liste de l'ensemble des surfaces dices
		self.game=GamePara()
		self.turns=turns
		self.players=turns.players
		self.map=turns.map
		self.textes=[]#liste des textes de troupes pour les fusionner aprés les surfaces
		self.tmp=[]#liste des sprites temporaires
		self.t_hud=[]#liste des textes HUD
		self.final_layer=[]#derniere couche d'affichage, utilisé pour le winning screen et le menu d'aide
		self._nb_units=25 #pas propre
		self.pays_select=None #pays selectionné

	@property
	def nb_units(self):
		if self.turns.phase==0:#regles du getter pendant la phase de deploiment
			return min(self._nb_units,self.players[self.turns.player_turn-1].nb_troupes)#le joueur ne peut pas selectionner plus de troupes qu'il n'en possede 
		else:
			return self._nb_units

	@nb_units.setter #attention incompatible tel quel python 2, necessite d'heriter de la class objet
	def nb_units(self, value):
		if self.turns.phase==0:#regles du setter pendant la phase de deploiment
			if value<1:
				self._nb_units = 1
				raise ValueError('Too few troops',value)
			elif value>self.players[self.turns.player_turn-1].nb_troupes:
				self._nb_units = self.players[self.turns.player_turn-1].nb_troupes
				raise ValueError('Too much troops',value)
		else:#regles du setter pendant les autres phases
			if value<0:
				self._nb_units = 0
				raise ValueError('Too few troops',value)
			elif value>self.pays_select.nb_troupes-1:
				self._nb_units = self.pays_select.nb_troupes-1#on ne peut attaquer/deplacer que avec n-1 troupes
				raise ValueError('Too much troops',value)
		self._nb_units = value

	def color_players(self,sprites):
		for pl in self.players:
			for pays in pl.pays:
				#print(pl.id,pays,sprites[pays-1].name_pays)
				sprite=next((s for s in sprites if s.id == pays), None)
				color_surface(sprite,pl.color,255)
				#print(sprite.id,pays)

	def start_game(self):
		self.surfaces=[]
		#fond bleue
		# background = pygame.Surface(fenetre.get_size())
		# background = background.convert()
		# background.fill(blue)
		#fond personnalisé
		background=pygame.image.load(PATH_BCK+BCK_IMG).convert()
		coeff=f_w/background.get_width() #adapte l'image selon la largeur
		w=int(coeff*background.get_width())
		h=int(coeff*background.get_height())
		background=pygame.transform.scale(background,(w,h))

		#map
		map_monde=pygame.image.load(PATH_IMG+MAP_IMG).convert_alpha()
		coeff=f_w/map_monde.get_width()#adapte l'image selon la largeur
		w=int(coeff*map_monde.get_width())
		h=int(coeff*map_monde.get_height())
		map_monde=pygame.transform.scale(map_monde,(w,h))

		#HUD barre
		barre=pygame.image.load(PATH_IMG+BAR_IMG).convert_alpha()
		barre=pygame.transform.scale(barre,(f_w,f_h-h))

		self.fonctions=[]
		self.surfaces.extend([[background,(0,0)],[barre,(0,h)],[map_monde,(0,0)]])

	def afficher(self,fonction=None):
		colormap=ColorMap()
		afficher=1
		select=False
		atck_winmove=False
		sprite_select=-1
		glob_pays=glob.glob(PATH_MAP+"*.png")
		sprites_pays=[]
		help_menu=False
		id_c=0
		hide=True
		#sprites de passage
		sprites_pays_masque=[]
		#chagement des sprites de pays
		for idx,fl in enumerate(glob_pays):
			s=pygame.image.load(fl).convert()
			coeff=f_w/s.get_width()
			s=pygame.transform.scale(s,(int(coeff*s.get_width()),int(coeff*s.get_height())))
			sp=SpritePays(s,fl)
			sp_masque=SpritePays(s.copy(),fl)
			color_surface(sp_masque,(1,1,1),150)
			sprites_pays.append(sp)
			sprites_pays_masque.append(sp_masque)

		#colorisation des pays selon les couleurs des joueurs
		self.color_players(sprites_pays)
		for idx, spr in enumerate(sprites_pays):#pas super propre
			if idx==0:
				merged_pays = spr.map_pays.copy()
			else:
				merged_pays.blit(spr.map_pays, (0, 0))

		#affichage des troupes
		display_troupes(self.textes,sprites_pays,self.map)

		while afficher:
			for event in pygame.event.get():
				if event.type == QUIT:
					afficher=0
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						afficher = 0
					elif event.key == K_n:
						try:
							self.turns.next()
						except ValueError as e:
							print(e.args)
						self.tmp=[]
						select=False
						sprite_select=0
					elif event.key == K_p:
						try:
							self.turns.next_player()
						except ValueError as e:
							print(e.args)
						self.tmp=[]
						select=False
						sprite_select=0
					elif event.key == K_w:#a enlever, debug func
						self.turns.game_finish=True
					elif event.key == K_h:
						help_menu = not help_menu
					elif event.key == K_c:
						self.tmp=[]
						display_continent(self.turns.map.continents[id_c],self.tmp,sprites_pays_masque)
						id_c=(id_c+1)%len(self.turns.map.continents)
					elif event.key == K_u:#utilisation des cartes
						self.turns.players[self.turns.player_turn-1].use_best_cards()
					elif event.key == K_d:#affichage/masquage des objectifs du joueurs
						hide = not hide
					elif event.key == K_s:#sauvegarde
						save_game(self)
					elif event.key == K_r:#restoration
						restore_game(self.turns)
				elif event.type == MOUSEBUTTONDOWN:
					try:
						if event.button==3: #rigth click to unselect
							self.tmp=[]
							select=False
							sprite_select=0
						elif event.button==4:#scroll wheel up
							self.nb_units+=1
						elif event.button==5:#scroll wheel down
							if self.nb_units>0:
								self.nb_units-=1
					except AttributeError as e:
						print('You should select a country first')
					except ValueError as e:
						print(e.args)

			for surface in self.surfaces:
				self.fenetre.blit(surface[0],surface[1])
			for dice in self.dices:
				self.fenetre.blit(dice[0],dice[1])
			#for sprite in sprites_pays:
			#	self.fenetre.blit(sprite.map_pays,(0,0))
			self.fenetre.blit(merged_pays,(0,0))
			for tmp in self.tmp:
				self.fenetre.blit(tmp,(0,0))
			for texte in self.textes:
				self.fenetre.blit(texte[0],texte[1])
			for t in self.t_hud:
				self.fenetre.blit(t[0],t[1])
			for final in self.final_layer:
				self.fenetre.blit(final[0],final[1])
			if self.fonctions != []:
				for f in self.fonctions:
					f()				#fonctions d'affichage

			#Ecran de victoire lorsqu'un joueur gagne
			if self.turns.players[self.turns.player_turn-1].obj.get_state()==True: #pas propre
				self.final_layer=[]
				win_screen = pygame.Surface(self.fenetre.get_size())
				win_screen = win_screen.convert()
				win_screen.fill(colormap.black)
				win_screen.set_alpha(180)
				self.final_layer.append([win_screen,(0,0)])
				display_win(self.final_layer,self.players)
			else:
				#ecran d'aide
				if help_menu:
					self.final_layer=[]
					win_screen = pygame.Surface(self.fenetre.get_size())
					win_screen = win_screen.convert()
					win_screen.fill(colormap.black)
					win_screen.set_alpha(180)
					self.final_layer.append([win_screen,(0,0)])
					display_help(self.final_layer,colormap)
				else:
					self.final_layer=[]

			#pygame.display.flip()
			mouse = pygame.mouse.get_pos()
			#print(self.fenetre.get_at((mouse[0], mouse[1])))
			#boucle de survole des pays
			#for idx,sprite in enumerate(sprites_pays):
				#if sprite.bounds.x<mouse[0]<sprite.bounds.x+sprite.bounds.width and sprite.bounds.y<mouse[1]<sprite.bounds.y+sprite.bounds.height: 
			try:
				mouse_color=self.surfaces[2][0].get_at((mouse[0],mouse[1]))
			except IndexError as e:
				pass #pas propre
				#print(e.args)

			try:
				if mouse_color != (0,0,0,0) and mouse_color != (0,0,0,255):
				#if sprite.map_pays.get_at((mouse[0],mouse[1])) != (0,0,0):
					id_pays_tmp=mouse_color[0]-100
					#print(id_pays_tmp)
					sp_msq=next((sp for sp in sprites_pays_masque if sp.id == id_pays_tmp), None)
					#print(sp_msq.id) 
					#print(sprite.id)
					#masque quand passage de la souris crée à la volé
					# if sprite.id != sprite_select:
					# 	sprite_bis=SpritePays(sprite.map_pays.copy(),"00.png") #pas propre
					# 	color_surface(sprite_bis,(1,1,1),150)
					# 	self.fenetre.blit(sprite_bis.map_pays,(0,0))
					# 	pygame.display.flip()
					if id_pays_tmp != sprite_select:
						self.fenetre.blit(sp_msq.map_pays,(0,0))
						pygame.display.update(sp_msq.map_pays.get_rect())
						#pygame.display.update(sp_msq.bounds)
					click=pygame.mouse.get_pressed()
					if self.turns.list_phase[self.turns.phase] == 'placement':
						#for event in pygame.event.get():
							#if event.type == pygame.MOUSEBUTTONDOWN:
							if click[0]==1:
								pays=next((p for p in self.map.pays if p.id == id_pays_tmp), None) 
								if pays.id_player==self.turns.player_turn:
									#mise a jout du nombre de troupes
									self.turns.placer(pays,self.nb_units)
									pygame.time.wait(100) #pas propre
									# try:
									# 	self.nb_units=self.players[self.turns.player_turn-1].nb_troupes
									# except ValueError as e:
									# 	print(e.args)
								else:
									#raise error
									print('pays n\'appartenant pas au joueur')
					elif self.turns.list_phase[self.turns.phase] == 'attaque':
						if click[0]==1 and not select: #selection du pays attaquant 
							pays1=next((p for p in self.map.pays if p.id == id_pays_tmp), None)
							self.pays_select=pays1
							if pays1.id_player==self.turns.player_turn and pays1.nb_troupes>1:
								self.nb_units=pays1.nb_troupes-1
								self.tmp.append(sp_msq.map_pays)
								select=True 
								sprite_select=id_pays_tmp
						elif click[0]==1:#selection du pays attaqué
							pays2=next((p for p in self.map.pays if p.id == id_pays_tmp), None)
							if atck_winmove and pays2 == pays_atck and pays1.nb_troupes>1:#mouvement gratuit apres attaque reussi
								self.turns.deplacer(pays1,pays2,self.nb_units)
								select=False
								self.tmp=[]
								atck_winmove=False
							elif atck_winmove:
								select=False
								self.tmp=[]
								atck_winmove=False
							elif pays2.id_player!=self.turns.player_turn and pays2.id in pays1.voisins:
								try:
									self.dices=[]		 #on efface les ancians sprites des dice								
									atck,res_l=self.turns.attaque(pays1,pays2,self.nb_units)
									print(res_l)
									for idx,res in enumerate(res_l):
										roll_dices(self,res[0],res[2],600,sprites_pays[0].map_pays.get_height()+10+idx*DICE_SIZE*1.1)#pas propre
										roll_dices(self,res[1],res[3],800,sprites_pays[0].map_pays.get_height()+10+idx*DICE_SIZE*1.1)
									pygame.time.wait(100) #pas propre
									#print(res)
								except ValueError as e:
									print(e.args)
									atck=False
									select=False
									self.tmp=[]
								if atck:
									sprite=next((s for s in sprites_pays if s.id == id_pays_tmp), None)
									color_surface(sprite,self.turns.players[self.turns.player_turn-1].color,255)
									merged_pays.blit(sprite.map_pays,(0,0))
									atck_winmove=True
									pays_atck=pays2
									self.nb_units=pays1.nb_troupes-1
								else:
									select=False
									self.tmp=[]
					elif self.turns.list_phase[self.turns.phase] == 'deplacement':
						if click[0]==1 and not select:
							pays1=next((p for p in self.map.pays if p.id == id_pays_tmp), None)
							self.pays_select=pays1
							if pays1.id_player==self.turns.player_turn and pays1.nb_troupes>1:
								self.nb_units=pays1.nb_troupes-1
								self.tmp.append(sp_msq.map_pays)
								select=True 
								sprite_select=id_pays_tmp
						elif click[0]==1:
							pays2=next((p for p in self.map.pays if p.id == id_pays_tmp), None)
							chemin=self.map.chemin_exist(self.turns.players[self.turns.player_turn-1].pays,pays1,pays2)
							select=False
							sprite_select=0
							self.tmp=[]
							if chemin and pays2.id != pays1.id:
								self.turns.deplacer(pays1,pays2,self.nb_units)
								self.turns.next()
					#affichage des troupes
					self.textes=[]
					display_troupes(self.textes,sprites_pays,self.map)
					#break
			except ValueError as e:
				pass #pas propre

			#HUD
			#print('tour numero :', self.num,'ordre',self.ordre,'joueur tour', self.ordre[self.id_ordre])
			#print(self.list_phase[self.phase])
			self.t_hud=[]
			display_hud(self.nb_units,self.t_hud,self.turns,(75,sprites_pays[0].map_pays.get_height()+10),hide)
			pygame.display.flip()

def menu(Win):
	#useless?
	barre=pygame.image.load(PATH_IMG+BAR_IMG).convert()
	r1=Win.fenetre.blit(barre,(0,0))
	Win.surfaces.extend([[barre,r1]])

#affichage des dés(résultats) +têtes de morts pour les pertes
def roll_dices(Win,pertes,number,x,y):
	L=[]
	for idx,d in enumerate(number):
		de=pygame.image.load(PATH_DCE+str(d)+".png").convert_alpha()
		resize_de=pygame.transform.scale(de,(DICE_SIZE,DICE_SIZE)) #resize des dices
		L.append([resize_de,Win.fenetre.blit(resize_de,(idx*DICE_SIZE*1.1+x,y))])

	for idx_p in range(0,pertes):
		deadhead=pygame.image.load(PATH_DCE+DHE_IMG).convert_alpha()
		resize_dh=pygame.transform.scale(deadhead,(DICE_SIZE,DICE_SIZE)) #resize des deadhead
		L.append([resize_dh,Win.fenetre.blit(resize_dh,(x-(idx_p+1)*DICE_SIZE*1.1,y))])
	Win.dices.extend(L) 

def menu_but(Win):
	#useless
	colors=ColorMap()
	#button('Start',150,150,100,50,colors.grey,colors.black,start_game)
	func=functools.partial(roll_dices,Win,[5,4,4],0,0)		#generation d'une nouvelle fonction avec les agruments
	button('Roll1',f_w/2,f_h/2,100,50,colors.grey,colors.black,func)
	func=functools.partial(roll_dices,Win,[1,6],0,0)		
	button('Roll2',300,300,100,50,colors.black,colors.black,func)

if __name__ == '__main__':
	import Risk
	from Risk import *
	print("== Tests unitaires ==")
	M=Map('Terre')
	Continents=M.continents
	T=Turns(3,M)
	T.start_deploy()
	print(T.distrib_pays(M.pays))
	T.print_players()
	#M.print_pays()
	Colors=ColorMap()
	T.players[0].color=Colors.dark_purple
	T.players[1].color=Colors.dark_green
	T.players[2].color=Colors.dark_red
	# T.players[3].color=Colors.white
	# T.players[4].color=Colors.yellow
	# T.players[5].color=Colors.cian
	T.players[0].name='nico'
	T.players[1].name='nono'
	T.players[2].name='jojo'
	# T.players[3].name='wis'
	# T.players[4].name='gogor'
	# T.players[5].name='pilou'
	# T.players[3].color=grey

	pygame.init()
	clock = pygame.time.Clock()
	fenetre = pygame.display.set_mode((f_w, f_h))
	Win=CurrentWindow(fenetre,T)
	Win.game.nb_joueurs=3
	Win.game.joueurs=['nico','nono','jojo']
	#menu_but(Win)							#affiche ini ? useless ?
	Win.fonctions.append(Win.start_game)		#fonctions ini 
	clock.tick(60)

	Win.afficher()	#on rentre dans la boucle while d'affichage
