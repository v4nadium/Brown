#! /usr/bin/env python
# -*- coding:Utf-8 -*-
# gazelle.py
# GPL - baptiste.paris.v@gmail.com
# Pas optimisé du tout.

try:
	from pygame import *;
	init(); # (6, 0)
	from pygame.locals import *;
except ImportError:
	print "Le module <Pygame> doit être installé.\nDebian:\t# apt install python-pygame\n"
	exit("/!\ Missing module");

from math import sin, cos, atan, pi, radians;
from random import random, randint; # random(): nombre aléatoire [0,1[ ; randint(a, b): entier aléatoire [|a, b|]
from time import sleep; # sleep(n): faire des pauses de n secondes
from os.path import isfile; # isfile("fichier.txt"): vérifier l'existence d'un fichier "fichier.txt"
sgn = lambda x:abs(x)/x; # sgn(x): signe du nombre x


X, Y = SIZE = (1500, 800); # taille de l'écran
Cx, Cy = C = (SIZE[0]/2, SIZE[1]/2); # centre
# création de l'écran de taille <SIZE>
s = display.set_mode(SIZE);

### COULEURS
rouge  = (255,  0,  0);
vert   = (  0,255,  0);
fond   = (230,175, 50);
animal = (185,125,  0);
blanc  = (255,255,255);

# scaling
H = 6; # pour pouvoir voir quelque chose...



class Animal:
	def __init__(self, x, y, angle_max, color=(255,255,255)):
		# coordonnées
		self.x = float(x);
		self.y = float(y);
		
		# coordonnées de la position précédante
		self.oldx = float(x-1); # "x-1" <-- ZeroDivisionError
		self.oldy = float(y);
		self.prevangle = 0; # angle au tour précédant

		self.color = color;

		self.angle_max = radians(angle_max); # angle entré en °, converti en rad

	def move(self, angle, length=1):
		# mémoriser l'angle
		self.prevangle = atan( (self.y - self.oldy) / (self.x - self.oldx) );
		
		# mémoriser les anciennes coordonnées
		self.oldx, self.oldy = self.x, self.y;
		
		# nouvelles coordonnées
		self.x = self.x + length * H * cos(angle);
		self.y = self.y + length * H * sin(angle);
	
	def render(self, screen=s):
		# matérialiser la trajectoire par une ligne entre la position précédante et l'actuelle
		draw.line(screen, self.color, (self.oldx, self.oldy), (self.x, self.y), H);


def step(gazelle, guepard, odd=False):
	### angle entre les deux animaux
	angle_GaGue = atan( (guepard.y - gazelle.y) / (guepard.x - gazelle.x) * sgn(gazelle.x - guepard.x) );
	
	### le guépard suit la gazelle
	# courbe du chien...
	if abs(angle_GaGue) < guepard.angle_max + guepard.prevangle:
		guepard.move(angle_GaGue);
	# ...limitée : trop haut --> -angle_max
	elif angle_GaGue - guepard.prevangle < 0:
		guepard.move( guepard.prevangle - guepard.angle_max);
	# trop bas --> +angle max
	else:
		guepard.move(guepard.prevangle + guepard.angle_max);
	
	guepard.render();


	### /!\ BIDOUILLE: la gazelle ne joue pas si odd
	if odd: return;
	
	# "else:"
	
	angle_fuite = angle_GaGue + 2 * (random() - 0.5) * gazelle.angle_max; # ça marche bien avec ces valeurs
	
	length = 3 # longueur des sauts de la gazelle

	### la gazelle fuit le guépard
	if abs(angle_fuite) < gazelle.angle_max:
		gazelle.move(angle_fuite, length);
	elif angle_fuite < 0:
		gazelle.move(-gazelle.angle_max, length);
	else:
		gazelle.move(gazelle.angle_max, length);
	
	
	gazelle.render();
	

def fuite(gazelle, guepard):
	i = 0; # compteur de tours
	
	### tant que les deux animaux sont dans l'écran:
	while gazelle.x < SIZE[0] and guepard.x < SIZE[0] and guepard.y < SIZE[1] and guepard.y > 0:
		i+=1;
		
		# le guépard fait 8 pas (de longueur 1) et la gazelle fait 1 saut de longueur 3
		step(gazelle, guepard, i % 8 );
#		sleep(0.01);
		# ligne entre le guépard et la gazelle
#		draw.line(s, (100,100,100), (guepard.x, guepard.y), (gazelle.x, gazelle.y));#XXX

		# si attrapée <=> distance inférieure à H :
		if abs(guepard.x - gazelle.x) < H and abs(guepard.y - gazelle.y) < H :
			draw.circle(s, rouge, (int(gazelle.x), int(gazelle.y)), 2*H);
			display.flip(); sleep(0.3);
			# petit effet de sang sympa
#			for i in range(5):
#				X = randint(-2*H, 5*H);
#				Y = randint(-3*H, 3*H);
#				R = randint(H, 3*H)/2;
#				draw.circle(s, (255,0,0), (int(gazelle.x)+X, int(gazelle.y)+Y), R);
#				display.flip(); sleep(0.3);
			return 1; # killed
		
		# si le guépard a dépassé la gazelle <=> fuite:
		elif guepard.x > gazelle.x :
			draw.circle(s, vert, (int(gazelle.x), int(gazelle.y)), 2*H);
			display.flip();
			
			# gazelle immobile
			gazelle.move = lambda x,y:0 
			S = sgn(guepard.y - gazelle.y);
			
			# /!\ BIDOUILLE: continuer la course du chien limitée pendant 50 pas
			for k in xrange(50):
				guepard.move(guepard.prevangle - guepard.angle_max * S );
				guepard.render();
				display.flip();
				sleep(0.01);
			return 0; # ¬ killed
			
		
		display.flip();
		sleep(0.01);

	sleep(1);
	return 0;
		
# variables pour les stats
total = 0;
kills = 0;

while True:
	# peindre le fond couleur "savane"
	s.fill(fond);
	
	# définir les animaux
	gazelle = Animal(randint(Cx-100,Cx+100)	, randint(Cy-50,Cy+50), 60);
	guepard = Animal(50, randint(Cy-50,Cy+50), 1.7	, animal);


	total += 1;
	kills += fuite(gazelle, guepard); # +1 si killed, 0 si fuite
	
	# events loop <=> appuyer sur une touche du clavier ou un bouton de la souris ou encore la croix de la fenêtre pour quitter le programme
	for evt in event.get():
		if evt.type == MOUSEBUTTONDOWN or evt.type == KEYDOWN or evt.type == QUIT:
			# noter le poucentage de kills en fonction des angles choisis.
			f = open('gazelle.log', 'a');
			with f:
				f.write(str(gazelle.angle_max) + '\t' + str(guepard.angle_max) + '\t' + str(float(kills)/total) + '\t' + str(float(total)) + '\n');
			exit();
	
	
	
