#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

import functools
import pygame
from pygame.locals import *
import Risk
import glob

PATH_IMG='Pictures/'
PATH_MAP='Pictures/Maps/'
MAP_IMG='Risk_game_map_fixed.bmp'
f_w=1280
f_h=800

green=(0,255,0)
lgreen=(0,200,0)
red=(255,0,0)
black=(0,0,0)
grey=(100,100,100)
lgrey=(125,125,125)
blue=(0,0,250)

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

	smallText = pygame.font.Font("freesansbold.ttf",16)
	textSurf, textRect = text_objects(msg, smallText)
	textRect.center = ( (x+(w/2)), (y+(h/2)) )
	fenetre.blit(textSurf, textRect)

def color_surface(surface,color):
	for x in range(0,surface.get_width()):
		for y in range(0,surface.get_height()):
			if surface.get_at((x,y))!=(0,0,0):
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
	smallText = pygame.font.Font("freesansbold.ttf",16)
	for sprite in sprites:
		pays=Map.pays[sprite.id-1]
		textSurf, textRect = text_objects(str(pays.nb_troupes), smallText)
		textRect.center = sprite.bounds.center
		textes.append([textSurf, textRect])

def display_win(final_layer,players):
	bigText = pygame.font.Font("freesansbold.ttf",42)
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
	bigText = pygame.font.Font("freesansbold.ttf",42)
	marge=50
	pos=(200,200)
	add_text(final_layer,'ESC : exit game',pos,bigText,colormap.white)
	pos=(pos[0],pos[1]+marge)
	add_text(final_layer,'n : next phase',pos,bigText,colormap.white)
	pos=(pos[0],pos[1]+marge)
	add_text(final_layer,'p : next player turn',pos,bigText,colormap.white)
	pos=(pos[0],pos[1]+marge)
	add_text(final_layer,'h : show/hide help menu',pos,bigText,colormap.white)

def display_hud(t_hud,turns,pos):
	smallText = pygame.font.Font("freesansbold.ttf",16)
	marge=20
	col=[0,300,600,700]
	row=pos[1]
	#partie joueur
	textSurf, textRect = text_objects('Tour : '+str(turns.num), smallText)
	textRect.topleft = pos
	t_hud.append([textSurf, textRect])
	textSurf, textRect = text_objects('Joueur : '+turns.players[turns.player_turn-1].name, smallText,turns.players[turns.player_turn-1].color)
	pos=(pos[0],pos[1]+marge)
	textRect.topleft = pos
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

	#partie objectifs
	textSurf, textRect = text_objects('Objectif(s) ', smallText)
	pos=(col[1],row)
	textRect.topleft = pos
	t_hud.append([textSurf, textRect])
	try:
		textSurf, textRect = text_objects(str(turns.players[turns.player_turn-1].obj.description), smallText)
	except AttributeError:
		pass
	pos=(col[1],row+marge)
	textRect.topleft = pos
	t_hud.append([textSurf, textRect])
	try:
		textSurf, textRect = text_objects('Statut : '+str(turns.players[turns.player_turn-1].obj.get_state()), smallText)
	except AttributeError:
		pass
	pos=(col[1],row+2*marge)
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

def display_continent(turns,temp_layer,sprites_pays_masque):
	c=turns.map.continents[3]
	for p in c.pays:
		temp_layer.append(next((x.map_pays for x in sprites_pays_masque if x.id == p.id), None))

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
		self.game=GamePara()
		self.turns=turns
		self.players=turns.players
		self.map=turns.map
		self.textes=[]#liste des textes de troupes pour les fusionner aprés les surfaces
		self.tmp=[]#liste des spirtes temporaires
		self.t_hud=[]#liste des textes HUD
		self.final_layer=[]#derniere couche d'affichage, utilisé pour le winning screen et le menu d'aide

	def color_players(self,sprites):
		for pl in self.players:
			for pays in pl.pays:
				#print(pl.id,pays,sprites[pays-1].name_pays)
				sprite=next((s for s in sprites if s.id == pays), None)
				color_surface(sprite,pl.color,255)
				#print(sprite.id,pays)

	def afficher(self,fonction=None):
		colormap=ColorMap()
		afficher=1
		select=False
		sprite_select=-1
		glob_pays=glob.glob(PATH_MAP+"*.png")
		sprites_pays=[]
		help_menu=False
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
		#affichage des troupes
		display_troupes(self.textes,sprites_pays,self.map)

		while afficher:
			for event in pygame.event.get():
				if event.type == QUIT:
					afficher=0
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						afficher = 0
					if event.key == K_n:
						self.turns.next()
						self.tmp=[]
						select=False
						sprite_select=0
					if event.key == K_p:
						self.turns.next_player()
						self.tmp=[]
						select=False
						sprite_select=0
					if event.key == K_w:
						self.turns.game_finish=True
					if event.key == K_h:
						help_menu = not help_menu
			for surface in self.surfaces:
				self.fenetre.blit(surface[0],surface[1])
			for sprite in sprites_pays:
				self.fenetre.blit(sprite.map_pays,(0,0))
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
			if self.turns.game_finish==True:
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
					#display_help(self.final_layer,colormap)
					self.tmp=[]
					display_continent(self.turns,self.tmp,sprites_pays_masque)
				else:
					self.final_layer=[]

			#pygame.display.flip()
			mouse = pygame.mouse.get_pos()
			#print(self.fenetre.get_at((mouse[0], mouse[1])))
			#boucle de survole des pays
			for idx,sprite in enumerate(sprites_pays):
				if sprite.bounds.x<mouse[0]<sprite.bounds.x+sprite.bounds.width and sprite.bounds.y<mouse[1]<sprite.bounds.y+sprite.bounds.height: 
					if sprite.map_pays.get_at((mouse[0],mouse[1])) != (0,0,0):
						#print(sprite.id)
						#masque quand passage de la souris crée à la volé
						# if sprite.id != sprite_select:
						# 	sprite_bis=SpritePays(sprite.map_pays.copy(),"00.png") #pas propre
						# 	color_surface(sprite_bis,(1,1,1),150)
						# 	self.fenetre.blit(sprite_bis.map_pays,(0,0))
						# 	pygame.display.flip()
						if sprite.id != sprite_select:
							self.fenetre.blit(sprites_pays_masque[idx].map_pays,(0,0))
							pygame.display.flip()
						click=pygame.mouse.get_pressed()
						if self.turns.list_phase[self.turns.phase] == 'placement':
							if click[0]==1:
								pays=next((p for p in self.map.pays if p.id == sprite.id), None) 
								if pays.id_player==self.turns.player_turn:
									#mise a jout du nombre de troupes
									self.turns.placer(pays,10)
								else:
									print('pays n\'appartenant pas au joueur')
						elif self.turns.list_phase[self.turns.phase] == 'attaque':
							if click[0]==1 and not select:
								pays1=next((p for p in self.map.pays if p.id == sprite.id), None)
								if pays1.id_player==self.turns.player_turn:
									self.tmp.append(sprites_pays_masque[idx].map_pays)
									select=True 
									sprite_select=sprite.id
							elif click[0]==1:
								pays2=next((p for p in self.map.pays if p.id == sprite.id), None)
								if pays2.id_player!=self.turns.player_turn and pays2.id in pays1.voisins:
									try:
										atck=self.turns.attaque(pays1,pays2,pays1.nb_troupes-1)
									except ValueError as e:
										print(e.args)
										atck=False
									select=False
									self.tmp=[]
									if atck:
										color_surface(sprite,self.turns.players[self.turns.player_turn-1].color,255)
						elif self.turns.list_phase[self.turns.phase] == 'deplacement':
							if click[0]==1 and not select:
								pays1=next((p for p in self.map.pays if p.id == sprite.id), None)
								self.tmp.append(sprites_pays_masque[idx].map_pays)
								select=True 
								sprite_select=sprite.id
							elif click[0]==1:
								pays2=next((p for p in self.map.pays if p.id == sprite.id), None)
								chemin=self.map.chemin_exist(self.turns.players[self.turns.player_turn-1].pays,pays1,pays2)
								select=False
								sprite_select=0
								self.tmp=[]
								if chemin and pays2.id != pays1.id:
									self.turns.deplacer(pays1,pays2,pays1.nb_troupes-1)
									self.turns.next()
						#affichage des troupes
						self.textes=[]
						display_troupes(self.textes,sprites_pays,self.map)
						break
			#HUD
			#print('tour numero :', self.num,'ordre',self.ordre,'joueur tour', self.ordre[self.id_ordre])
			#print(self.list_phase[self.phase])
			self.t_hud=[]
			display_hud(self.t_hud,self.turns,(10,sprites_pays[0].map_pays.get_height()+10))
			pygame.display.flip()


def menu(Win):
	barre=pygame.image.load(PATH_IMG+"barre.png").convert()
	r1=Win.fenetre.blit(barre,(0,0))
	Win.surfaces.extend([[barre,r1]])

def roll_dices(number,x,y):
	L=[]
	for idx,d in enumerate(number):
		de=pygame.image.load(PATH_IMG+str(d)+".png").convert()
		L.append([de,Win.fenetre.blit(de,(idx*125,0))])
	Win.surfaces.extend(L) 

def start_game():
	Win.surfaces=[]
	#fond bleue
	background = pygame.Surface(fenetre.get_size())
	background = background.convert()
	background.fill(blue)
	#map
	map_monde=pygame.image.load(PATH_IMG+MAP_IMG).convert()
	coeff=f_w/map_monde.get_width()
	w=int(coeff*map_monde.get_width())
	h=int(coeff*map_monde.get_height())
	map_monde=pygame.transform.scale(map_monde,(w,h))
	barre=pygame.image.load(PATH_IMG+"barre.png").convert()
	Win.fonctions=[]
	Win.surfaces.extend([[background,(0,0)],[barre,(0,h)],[map_monde,(0,0)]])

def menu_but():
	#useless
	button('Start',150,150,100,50,grey,lgrey,start_game)
	func=functools.partial(roll_dices,[5,4,4],0,0)		#generation d'une nouvelle fonction avec les agruments
	button('Roll1',f_w/2,f_h/2,100,50,grey,lgrey,func)
	func=functools.partial(roll_dices,[1,6],0,0)		
	button('Roll2',300,300,100,50,grey,lgrey,func)

if __name__ == '__main__':
	import Risk
	from Risk import *
	print("== Tests unitaires ==")
	M=Map('Terre')
	Continents=M.continents
	T=Turns(6,M)
	T.start_deploy()
	print(T.distrib_pays(M.pays))
	T.print_players()
	#M.print_pays()
	Colors=ColorMap()
	T.players[0].color=Colors.dark_purple
	T.players[1].color=Colors.dark_green
	T.players[2].color=Colors.dark_red
	T.players[3].color=Colors.white
	T.players[4].color=Colors.yellow
	T.players[5].color=Colors.cian
	T.players[0].name='nico'
	T.players[1].name='nono'
	T.players[2].name='jojo'
	T.players[3].name='wis'
	T.players[4].name='gogor'
	T.players[5].name='pilou'
	# T.players[3].color=grey

	pygame.init()
	clock = pygame.time.Clock()
	fenetre = pygame.display.set_mode((f_w, f_h))
	Win=CurrentWindow(fenetre,T)
	Win.game.nb_joueurs=3
	Win.game.joueurs=['nico','nono','jojo']
	menu(Win)							#affiche ini
	Win.fonctions.append(start_game)		#fonctions ini
	clock.tick(60)
	

	Win.afficher()	#on rentre dans la boucle while d'affichage

