#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
import random
import copy

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
	def __init__(self,id,Map,turns):
		self.id=id
		self.nb_troupes=0
		self.name=""
		self.pays=[]
		self._bonus=0
		self._sbyturn=0
		self._isalive=True
		self.color=(0,0,0)
		self.map=Map
		self.turns=turns
		self.obj=None
		self.cards=[]
		self.win_land=False

	def use_best_cards(self):
		#TODO empecher l'utilisation si on est pas dans le tour de déploiment
		if self.turns.list_phase[self.turns.phase]=='placement':
			nb_s=[x for x in self.cards if x.type==x.types[0]]
			nb_h=[x for x in self.cards if x.type==x.types[1]]
			nb_c=[x for x in self.cards if x.type==x.types[2]]
			if len(nb_s)>0 and len(nb_h)>0 and len(nb_c)>0:#si triplé déparaillé
				self.use_cards([nb_s[0],nb_h[0],nb_c[0]])
			elif len(nb_c)>2:#si canon
				self.use_cards([nb_c[0],nb_c[1],nb_c[2]])
			elif len(nb_h)>2:#si cavalier
				self.use_cards([nb_h[0],nb_h[1],nb_h[2]])
			elif len(nb_s)>2:#si soldats
				self.use_cards([nb_s[0],nb_s[1],nb_s[2]])
			else:#sinon pas de combi possible
				#TODO raise
				print('Pas de combianaison disponibles')
		else:#TODO raise
			print('On peut positionner que pendant la phase de placement')

	#take only 3 cards in input
	def use_cards(self,cards):
		#triplé
		if cards[0].type==cards[1].type and cards[1].type==cards[2].type and cards[0].type==cards[2].type:
			self.nb_troupes+=cards[0].bonus
			self.cards.remove(cards[0])
			self.cards.remove(cards[1])
			self.cards.remove(cards[2])
		#deparaillé
		elif cards[0].type!=cards[1].type and cards[1].type!=cards[2].type and cards[0].type!=cards[2].type:
			self.nb_troupes+=cards[0].max_bonus
			self.cards.remove(cards[0])
			self.cards.remove(cards[1])
			self.cards.remove(cards[2])

	def del_card(self,card_index):
		self.cards.pop(card_index)

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

	@property
	def isalive(self):
		if len(self.pays)>0:
			return True
		else:
			#TODO
			#print(self.name+" is dead")
			#self.turns.ordre.remove(self.id_player)
			return False

#types de définition des missions à effectuer par les joueurs
class Goal():
	def __init__(self,Map,turns):
		self.turns=turns
		self.types=['capture continents','capture pays','destroy']
		self.map=Map
		self.randrange=[[0,1,2,3,4,5],[],[x for x in range(1,turns.nb_players+1)]]

#def des missions
class Objective():
	def __init__(self,goal,player):
		self.goal=goal
		self.type=self.goal.types[random.randint(0,len(self.goal.types)-1)]
		self.player=player
		self._description=''
		self.gen_obj()

	def gen_obj(self):
		if self.type=='capture continents':
			self.continents=[]
			self.other_cont=False
			self.nbtroupes=1
			r_choice=random.choice(self.goal.randrange[0])
			self.goal.randrange[0].remove(r_choice) #on enleve la combinaison choisi pour eviter les doublons de missions
			if r_choice==0:
				self.continents.append(self.goal.map.continents[4])
				self.continents.append(self.goal.map.continents[5])
				self.other_cont=True
			elif r_choice==1:
				self.continents.append(self.goal.map.continents[4])
				self.continents.append(self.goal.map.continents[2])
				self.other_cont=True
			elif r_choice==2:
				self.continents.append(self.goal.map.continents[1])
				self.continents.append(self.goal.map.continents[0])
			elif r_choice==3:
				self.continents.append(self.goal.map.continents[1])
				self.continents.append(self.goal.map.continents[5])
			elif r_choice==4:
				self.continents.append(self.goal.map.continents[3])
				self.continents.append(self.goal.map.continents[2])
			elif r_choice==5:
				self.continents.append(self.goal.map.continents[3])
				self.continents.append(self.goal.map.continents[0])
		if self.type=='capture pays':
			r_choice=random.randint(0,1)
			if r_choice==0:
				self.nbpays=18
				self.nbtroupes=2
			if r_choice==1:
				self.nbpays=24
				self.nbtroupes=1
		if self.type=='destroy':
			randrange_excl=copy.copy(self.goal.randrange[2])
			try:
				randrange_excl.remove(self.player.id)#exclude himself
			except ValueError:
				pass #player deja remove de la list
			if len(randrange_excl)==0:
				print('erreur de merde')
			try:
				randid=random.choice(randrange_excl)
				print(self.goal.randrange[2],randrange_excl,randid)
				self.goal.randrange[2].remove(randid)#on enleve la combinaison pour eviter les doublons de mission
				self.target=self.goal.turns.players[randid-1] 
			except IndexError: #le seul joueur attaquable est lui mm
				self.type=self.goal.types[random.randint(0,1)]#on choisi une autre mission
				self.gen_obj()
			
	@property
	def description(self):
		if self.type=='capture continents':
			tmp_str='Capturer'
			for i in range(0,len(self.continents)):
				tmp_str+=' '+str(self.continents[i].name)
			if self.other_cont:
				tmp_str+=' and another cont'
			return tmp_str
		elif self.type=='capture pays':
			tmp_str = 'Capturer '+str(self.nbpays)+' pays' 
			if self.nbtroupes>1:
				tmp_str+=' avec '+str(self.nbtroupes)+' soldats'
			return tmp_str
		elif self.type=='destroy':
			if self.target.name=='':
				return 'Detruire '+str(self.target.id)
			else:
				return 'Detruire '+str(self.target.name)

	def get_state(self):
		if self.type=='capture pays':
			return self.capture_pays(self.nbpays,self.nbtroupes)
		if self.type=='capture continents':
			return self.capture_continents(self.continents,self.nbtroupes)
		if self.type=='destroy':
			return self.destroy_player(self.target)		

	def capture_pays(self,nb_pays,nb_troupes):
		nb_occupe=0
		for p in self.goal.map.pays:
			if p.nb_troupes>nb_troupes-1 and p.id_player==self.player.id:
				nb_occupe+=1
		if nb_occupe>nb_pays-1:
			self.goal.turns.game_finish=True
			return True
		else:
			return False

	def capture_continents(self,continents,nb_troupes):
		nb_occupe=0
		for c in continents:
			cont_occupe=True
			for p in c.pays:
				if p.nb_troupes<nb_troupes or p.id_player!=self.player.id:
					cont_occupe=False
			if cont_occupe==True:
				nb_occupe+=1
		if self.other_cont:
			#player must have another continent
			additionnal_cont=0
			other_conts=[x for x in self.goal.map.continents if x not in continents]
			for c in other_conts:
				cont_occupe=True
				for p in c.pays:
					if p.nb_troupes<nb_troupes or p.id_player!=self.player.id:
						cont_occupe=False
				if cont_occupe==True:
					additionnal_cont+=1
		if nb_occupe == len(continents):
			if self.other_cont and additionnal_cont>0:
				self.goal.turns.game_finish=True
				return True
			elif not self.other_cont:
				self.goal.turns.game_finish=True
				return True
			else:
				return False
		else:
			return False

	def destroy_player(self,player):
		if not player.isalive:
			self.goal.turns.game_finish=True
			return True
		else:
			return False

class Card():
	def __init__(self):
		self.types=['Soldat','Cavalier','Canon']
		bonus=[5,8,10,12]
		rand=random.randint(0,2)
		self.type=self.types[rand]
		self.bonus=bonus[rand]
		print(self.bonus)
		self.max_bonus=bonus[-1]
	def __repr__(self):
		return str(self.type)

class Turns():
	def __init__(self,nb_players,M):
		self.game_finish=False
		self.num=0
		self.nb_players=nb_players
		self.ordre=list(range(1,nb_players+1))
		random.shuffle(self.ordre)
		self.nb_pays=M.nb_pays
		self.players=[]
		#generation des joueurs
		for k in range(0,nb_players):
			self.players.append(Player(k+1,M,self))
		#affectation des objectifs aprés que tous les joueurs soient crées
		self.goal=Goal(M,self)
		for k in range(0,nb_players):
			self.players[k].obj=Objective(self.goal,self.players[k])
		self.id_ordre=0
		self.map=M
		self.list_phase=['placement','attaque','deplacement']
		self.phase=0
		self._player_turn=self.ordre[self.id_ordre]

	def next(self):
		if self.players[self.player_turn-1].nb_troupes>0:
			raise ValueError('Need to deploy',self.players[self.player_turn-1].nb_troupes)
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
				#mise a jour du booleen de pays capture
				self.players[self.player_turn-1].win_land=False
				if self.id_ordre==0:
					self.num+=1
					self.phase=0
					#mise a jour du nombre de troupes dispos : renforts de débuts de tour
					self.players[self.player_turn-1].nb_troupes+=self.players[self.player_turn-1].sbyturn
		else:
			self.phase=(self.phase+1)%len(self.list_phase)
			if self.phase == 0 :
				self.id_ordre=(self.id_ordre+1)%len(self.ordre)
				#mise a jour du booleen de pays capture
				self.players[self.player_turn-1].win_land=False
				#mise a jour du nombre de troupes dispos : renforts de débuts de tour
				self.players[self.player_turn-1].nb_troupes+=self.players[self.player_turn-1].sbyturn
				if self.id_ordre==0:
					self.num+=1
		print('tour numero :', self.num,'ordre',self.ordre,'joueur tour', self.ordre[self.id_ordre])
		print(self.list_phase[self.phase])

	def next_player(self):
		# if self.players[self.player_turn-1].nb_troupes>0:
		# 	raise ValueError('Need to deploy',self.players[self.player_turn-1].nb_troupes)
		if self.num==0: #phase de placement initiale
			self.id_ordre=(self.id_ordre+1)%len(self.ordre)
			if self.id_ordre==0:
				self.num+=1
				self.phase=(self.phase+1)%len(self.list_phase)
		elif self.num==1:#on saute la phase de placement
			self.phase=1
			self.id_ordre=(self.id_ordre+1)%len(self.ordre)
			#mise a jour du booleen de pays capture
			self.players[self.player_turn-1].win_land=False
			if self.id_ordre==0:
				self.num+=1
				self.phase=0
				#mise a jour du nombre de troupes dispos : renforts de débuts de tour
				self.players[self.player_turn-1].nb_troupes+=self.players[self.player_turn-1].sbyturn

		else:
			#on passe au tours du joueur suivant
			self.id_ordre=(self.id_ordre+1)%len(self.ordre)
			self.phase=0
			#mise a jour du booleen de pays capture
			self.players[self.player_turn-1].win_land=False
			#mise a jour du nombre de troupes dispos : renforts de débuts de tour
			self.players[self.player_turn-1].nb_troupes+=self.players[self.player_turn-1].sbyturn
			if self.id_ordre==0:
				self.num+=1

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
			#throw execption
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
		pertes=[0,0,d_a,d_b]     						#[pertes de l'attaquant, deffenseur]
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
		res_l=[]
		while(True):
			if nb_attaquants>2:
				dice_atck=3
			elif nb_attaquants>1:
				dice_atck=2
			elif nb_attaquants>0:
				dice_atck=1
			else:
				#throw exception pas assez de troupes pour attaquer
				raise ValueError('not enough troops :',nb_attaquants)
			if pays_d.nb_troupes>1:
				dice_def=2
			elif pays_d.nb_troupes>0:
				dice_def=1
			res=self.throw_dices(dice_atck,dice_def)
			print(res)
			res_l.append(res)
			pays_a.nb_troupes-=res[0]
			nb_attaquants-=res[0]
			pays_d.nb_troupes-=res[1]

			if nb_attaquants==0: #l'attaque a echoué
				return False,res_l
			elif pays_d.nb_troupes==0: #le pays est capturé
				#mise a jour de la liste des pays de chaque joueurs
				self.players[pays_a.id_player-1].pays.append(pays_d.id)
				self.players[pays_d.id_player-1].pays.remove(pays_d.id)
				#on change le player id 
				pays_d.id_player=pays_a.id_player
				#deplacement automatique du nombre de troupes attaquante au dernier lancer de dés (1,2,3)
				self.deplacer(pays_a,pays_d,dice_atck)
				#on donne une carte au joueur attaquant si c'est son premier territoire capturé ce tour
				if self.players[pays_a.id_player-1].win_land==False:
					self.players[pays_a.id_player-1].win_land=True
					#si le joueur a plus de 5 cartes il doit se défausse
					if len(self.players[pays_a.id_player-1].cards)>4:
						self.players[pays_a.id_player-1].del_card(0)
						#TODO raise ValueError('Too much cards',len(self.players[pays_a.id_player-1].cards))
					self.players[pays_a.id_player-1].cards.append(Card())
					#print(self.players[pays_a.id_player-1].cards)
				return True,res_l  #success

	def deplacer(self,pays_ori,pays_dest,nb_troupes):
		pays_ori.nb_troupes-=nb_troupes
		pays_dest.nb_troupes+=nb_troupes

	def placer(self,pays,nb_troupes):
		#le player qui place voit son compteur décroitre
		player=next((p for p in self.players if p.id == pays.id_player), None)
		if(player.nb_troupes-nb_troupes<=0):
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
			self.continents.append(Continent(['Venezuela','Bresil','Perou','Argentine']
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
			self.continents[0].pays[4].voisins=[1,2,3,17,36,38]
			self.continents[0].pays[5].voisins=[1,2,4]
			self.continents[1].pays[0].voisins=[8,12,25]
			self.continents[1].pays[1].voisins=[7,12,13,15]
			self.continents[1].pays[2].voisins=[15,10,19]#Am centrale
			self.continents[1].pays[3].voisins=[9,15,13,14]#10
			self.continents[1].pays[4].voisins=[12,13,14,33]
			self.continents[1].pays[5].voisins=[7,8,13,11]
			self.continents[1].pays[6].voisins=[8,15,10,14,11,12]
			self.continents[1].pays[7].voisins=[10,13,11]
			self.continents[1].pays[8].voisins=[9,10,8,13]
			self.continents[2].pays[0].voisins=[17,18]
			self.continents[2].pays[1].voisins=[16,18,19,5]
			self.continents[2].pays[2].voisins=[16,17,19]
			self.continents[2].pays[3].voisins=[18,17,9]#Argentine
			self.continents[3].pays[0].voisins=[21,22,26,30,37]#20
			self.continents[3].pays[1].voisins=[20,22,28,27,29,30]
			self.continents[3].pays[2].voisins=[20,21,26,28]
			self.continents[3].pays[3].voisins=[29,27,25,31]
			self.continents[3].pays[4].voisins=[27,25]
			self.continents[3].pays[5].voisins=[31,23,27,24,7]
			self.continents[3].pays[6].voisins=[20,22,37,2,3]
			self.continents[3].pays[7].voisins=[24,21,29,25,23]
			self.continents[3].pays[8].voisins=[21,22,40]
			self.continents[3].pays[9].voisins=[30,21,23,31,27]
			self.continents[3].pays[10].voisins=[20,21,29,37]#30
			self.continents[3].pays[11].voisins=[29,23,25]
			self.continents[4].pays[0].voisins=[33,35,34,38]
			self.continents[4].pays[1].voisins=[32,35,11]
			self.continents[4].pays[2].voisins=[32,35,37,36,38]
			self.continents[4].pays[3].voisins=[37,32,33,34]
			self.continents[4].pays[4].voisins=[38,34,37,3,26,5]
			self.continents[4].pays[5].voisins=[35,34,36,20,26,30]
			self.continents[4].pays[6].voisins=[32,34,36,5]
			self.continents[5].pays[0].voisins=[42,41]
			self.continents[5].pays[1].voisins=[42,41,28]#40
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