#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
import random

class Continent():
	def __init__(self,pays,bonus,name,Map):
		self.bonus=bonus
		self.name=name
		self.pays=[]
		for p in pays:
			P=Pays(p,name,Map)
			self.pays.append(P)
			Map.pays.append(P)
		self.nb_pays=len(self.pays)

class Pays():
	def __init__(self,name,continent,Map):
		Map.nb_pays=Map.nb_pays+1
		self.id=Map.nb_pays
		self.name=name
		self.continent=continent
		self.id_player=0
		self.nb_troupes=0
		self.voisins=[]

	def voisins(self,pays):
		for p in pays:
			self.voisins.append(p)

	def print_carac(self):
		print(self.id,self.name,self.continent,self.id_player,self.nb_troupes,self.voisins)

class Player():
	def __init__(self,id,Map):
		self.id=id
		self.nb_troupes=0
		self.name=""
		self.pays=[]
		self._bonus=0
		self._sbyturn=0
		self.color=(0,0,0)
		self.map=Map

	def print_carac(self):
		print(self.id,self.name,self.nb_troupes,self.sbyturn,self.pays)

	@property
	def sbyturn(self):				#mise a jour des qu'on l'apelle
		return max(3,len(self.pays)//3+self.bonus)

	@property
	def bonus(self):				#mise a jour des qu'on l'apelle
		b=0
		for c in self.map.continents:
			player_have_cont=True
			for pays in c.pays:
				if pays.id not in self.pays:
					player_have_cont=False
					break
			if player_have_cont:
				b+=c.bonus
		return b

class Objectifs():
	def __init__(self):
		self.types=['capture continents','capture pays','destroy']

	def capture_pays(nb_pays,nb_troupes):
		pass
		nb_occupe=0
		for p in pays_joueur:
			if p.nb_troupes>nb_troupes-1 and p.id_player==joueur.id:
				nb_occupe++
		if nb_occupe>nb_pays-1:
			return True
		else
			return False

	def destroy_player(player)
		if not player.isalive():
			




class CartesBonus():
	def __init__(self,nb_cartes):
		self.nb_cartes=nb_cartes
		self.types=['Soldat','Cavalier','Canon']
		self.bonus=[5,8,10,12]

class Turns():
	def __init__(self,nb_players,M):
		self.num=0
		self.nb_players=nb_players
		self.ordre=list(range(1,nb_players+1))
		random.shuffle(self.ordre)
		self.nb_pays=M.nb_pays
		self.players=[]
		for k in range(0,nb_players):
			self.players.append(Player(k+1,M))
		self.id_ordre=0
		self.map=M
		self.list_phase=['placement','attaque','deplacement']
		self.phase=0
		self._player_turn=self.ordre[self.id_ordre]

	def next(self):
		if self.num==0: #phase de placement initiale
			self.id_ordre=(self.id_ordre+1)%len(self.ordre)
			if self.id_ordre==0:
				self.num+=1
				self.phase=(self.phase+1)%len(self.list_phase)
		elif self.num==1:#on saute la phase de placement
			self.phase=(self.phase+1)%len(self.list_phase)
			if self.phase == 0 :
				self.phase+=1
				self.id_ordre=(self.id_ordre+1)%len(self.ordre)
				if self.id_ordre==0:
					self.num+=1
					self.phase=0
					#mise a jour du nombre de troupes dispos : renforts de débuts de tour
					self.players[self.player_turn-1].nb_troupes+=self.players[self.player_turn-1].sbyturn
		else:
			self.phase=(self.phase+1)%len(self.list_phase)
			if self.phase == 0 :
				self.id_ordre=(self.id_ordre+1)%len(self.ordre)
				#mise a jour du nombre de troupes dispos : renforts de débuts de tour
				self.players[self.player_turn-1].nb_troupes+=self.players[self.player_turn-1].sbyturn
				if self.id_ordre==0:
					self.num+=1
		print('tour numero :', self.num,'ordre',self.ordre,'joueur tour', self.ordre[self.id_ordre])
		print(self.list_phase[self.phase])

	def start_deploy(self):
		if self.nb_players==3:
			nb_troupes=35
		elif self.nb_players==4:
			nb_troupes=30
		elif self.nb_players==5:
			nb_troupes=25
		elif self.nb_players==6:
			nb_troupes=20
		else:
			print('Nombre de players invalide')
		for p in self.players:
			p.nb_troupes=nb_troupes

	def distrib_pays(self,pays):
		lst_id_pays=[]
		for k in pays:
			lst_id_pays.append(k.id)
		random.shuffle(lst_id_pays)
		n=self.nb_pays//self.nb_players
		for idx,i in enumerate(range(0, len(lst_id_pays),n)):
			if idx<self.nb_players:
				self.players[idx].pays=lst_id_pays[i:i+n]
			else:
				for pays_restant in lst_id_pays[i:i+n]:		#les pays restant sont attribue aleatoirement variante avec un neutre ???
					self.players[random.randint(0,self.nb_players-1)].pays.append(pays_restant)
		for p in self.players:
			for pays in p.pays:
				self.map.pays[pays-1].id_player=p.id
				self.map.pays[pays-1].nb_troupes=1 #minimum de un soldat sur tout territoire
				p.nb_troupes-=1
		return lst_id_pays     #debug

	def throw_dices(self,atck,defense):
		d_a=[]
		d_b=[]
		pertes=[0,0]     						#[pertes de l'attaquant, deffenseur]
		for k in range(0,atck):
			d_a.append(random.randint(1,6))
		d_a.sort(reverse=True)
		for k in range(0,defense):
			d_b.append(random.randint(1,6))
		d_b.sort(reverse=True)
		for k in range(0,min(atck,defense)):
			if d_b[k]<d_a[k]:					#l'attaquant gagne
				pertes[1]=pertes[1]+1
			else:
				pertes[0]=pertes[0]+1
		return pertes

	def attaque(self,pays_a,pays_d,nb_attaquants):
		while(True):
			if nb_attaquants>2:
				dice_atck=3
			elif nb_attaquants>1:
				dice_atck=2
			elif nb_attaquants>0:
				dice_atck=1
			if pays_d.nb_troupes>1:
				dice_def=2
			elif pays_d.nb_troupes>0:
				dice_def=1
			res=self.throw_dices(dice_atck,dice_def)
			print(res)
			pays_a.nb_troupes-=res[0]
			nb_attaquants-=res[0]
			pays_d.nb_troupes-=res[1]

			if nb_attaquants==0: #l'attaque a echoué
				return False
			elif pays_d.nb_troupes==0: #le pays est capturé
				#mise a jour de la liste des pays de chaque joueurs
				self.players[pays_a.id_player-1].pays.append(pays_d.id)
				self.players[pays_d.id_player-1].pays.remove(pays_d.id)
				#on change le player id 
				pays_d.id_player=pays_a.id_player
				#deplacement automatique du minimum
				self.deplacer(pays_a,pays_d,1)
				return True   #success

	def deplacer(self,pays_ori,pays_dest,nb_troupes):
		pays_ori.nb_troupes-=nb_troupes
		pays_dest.nb_troupes+=nb_troupes

	def placer(self,pays,nb_troupes):
		#le player qui place voit son compteur décroitre
		player=next((p for p in self.players if p.id == pays.id_player), None)
		if(player.nb_troupes-nb_troupes<0):
			print('pas assez de troupes')
			pays.nb_troupes+=player.nb_troupes
			player.nb_troupes-=player.nb_troupes
			self.next()
		else:
			player.nb_troupes-=nb_troupes
			pays.nb_troupes+=nb_troupes

	def print_players(self):
		for p in self.players:
			p.print_carac()

	@property
	def player_turn(self):				#mise a jour des qu'on l'apelle
		return self.ordre[self.id_ordre]

class Map():
	def __init__(self,name):
		self.name=name
		self.pays=[]  
		self.continents=[]
		self.nb_pays=0
		if name=='Terre':
			self.continents.append(Continent(['Congo','Affrique de l\'Est','Egypte','Madagascar','Afrique du Nord','Afrique du Sud']
											,3,'Afrique',self))
			self.continents.append(Continent(['Alaska','Alberta','Amerique Centrale','Etats de l\'Est','Groenland','Territoires du Nord-Ouest','Ontario','Quebec','Etats de l\'Ouest']
											,5,'Amerique du Nord',self))
			self.continents.append(Continent(['Argentine','Bresil','Perou','Venezuela']
											,2,'Amerique du Sud',self))
			self.continents.append(Continent(['Afghanistan','Chine','Inde','Tchita','Japon','Kamchatka','Moyen-Orient','Mongolie','Siam','Siberie','Oural','Yakoutie']
											,7,'Asie',self))
			self.continents.append(Continent(['Grande-Bretagne','Islande','Europe du Nord','Scandinavie','Europe du Sud','Ukraine','Europe Occidentale']
											,5,'Europe',self))
			self.continents.append(Continent(['Australie Orientale','Indonésie','Nouvelle-Guinée','Australie Occidentale']
											,2,'Oceanie',self))
			self.continents[0].pays[0].voisins=[2,5,6]
			self.continents[0].pays[1].voisins=[1,3,4,5,26]
			self.continents[0].pays[2].voisins=[2,5,36,26]
			self.continents[0].pays[3].voisins=[2,6]
			self.continents[0].pays[4].voisins=[1,2,3,17,38]
			self.continents[0].pays[5].voisins=[1,2,4]
			self.continents[1].pays[0].voisins=[8,12,25]
			self.continents[1].pays[1].voisins=[7,12,13,15]
			self.continents[1].pays[2].voisins=[15,10,16]
			self.continents[1].pays[3].voisins=[9,15,13,14]
			self.continents[1].pays[4].voisins=[12,13,14,33]
			self.continents[1].pays[5].voisins=[7,8,13,11]
			self.continents[1].pays[6].voisins=[8,15,10,14,11,12]
			self.continents[1].pays[7].voisins=[10,13,11]
			self.continents[1].pays[8].voisins=[9,10,8,13]
			self.continents[2].pays[0].voisins=[17,18]
			self.continents[2].pays[1].voisins=[16,18,19,5]
			self.continents[2].pays[2].voisins=[16,17,19]
			self.continents[2].pays[3].voisins=[18,17,9]
			self.continents[3].pays[0].voisins=[21,22,26,30,37]
			self.continents[3].pays[1].voisins=[20,22,28,27,29,30]
			self.continents[3].pays[2].voisins=[20,21,26,28]
			self.continents[3].pays[3].voisins=[29,27,25,31]
			self.continents[3].pays[4].voisins=[27,25]
			self.continents[3].pays[5].voisins=[31,23,27,24,7]
			self.continents[3].pays[6].voisins=[20,22,37,2,3]
			self.continents[3].pays[7].voisins=[24,21,29,25,23]
			self.continents[3].pays[8].voisins=[21,22,40]
			self.continents[3].pays[9].voisins=[30,21,23,31,27]
			self.continents[3].pays[10].voisins=[20,21,29,37]
			self.continents[3].pays[11].voisins=[29,23,25]
			self.continents[4].pays[0].voisins=[33,35,34,38]
			self.continents[4].pays[1].voisins=[32,35,11]
			self.continents[4].pays[2].voisins=[32,35,37,36,38]
			self.continents[4].pays[3].voisins=[37,32,33,34]
			self.continents[4].pays[4].voisins=[38,34,37,3,26]
			self.continents[4].pays[5].voisins=[35,34,36,20,26,30]
			self.continents[4].pays[6].voisins=[32,34,36,5]
			self.continents[5].pays[0].voisins=[42,41]
			self.continents[5].pays[1].voisins=[42,41,28]
			self.continents[5].pays[2].voisins=[42,40,39]
			self.continents[5].pays[3].voisins=[39,41,40]

	def print_pays(self):
		for pays in self.pays:
			pays.print_carac()

	def chemin_exist(self,pays_joueur,pays1,pays2):
		pays_reachable=[]
		if pays1.id in pays_joueur:
			pays_reachable.append(pays1.id)
			self.parcours_profondeur(pays1,pays_joueur,pays_reachable)
			if pays2.id in pays_reachable:
				print('un chemin existe')
				return True
			else:
				print('pas de chemin')
				return False
		else:
			print('Le pays n\'est pas au joueur')
			return False

	def parcours_profondeur(self,pays,pays_joueur,pays_reachable):
		for p_id in pays.voisins:
			if p_id in pays_joueur and p_id not in pays_reachable:
				pays_reachable.append(p_id)
				self.parcours_profondeur(self.pays[p_id-1],pays_joueur,pays_reachable)

class Check():
	def __init__(self):
		self.totalcheck=0

	def pays_unicite(self,pays):
		self.a=a

if __name__ == '__main__':
	print("== Tests unitaires ==")
	M=Map('Terre')
	Continents=M.continents
	Europe=Continents[4]
	print(Europe.bonus)
	print(Europe.nb_pays)
	for P in T.players:
		print(P.pays,P.id)

	print("== Tests attaque ==")
	T=Turns(4,M)
	r=T.throw_dices(1,2)
	print(r[0:2])
	print("== Tests ordre ==")
	print(T.ordre)

	print("== Tests round 0 ==")
	T.start_deploy()
	print(T.distrib_pays(M.pays))
	T.print_players()
	M.print_pays()