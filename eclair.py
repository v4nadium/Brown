#! /usr/bin/env python
# -*- coding:Utf-8 -*-
# lichtenberg
# GPL - baptiste.paris.v@gmail.com
from pygame import *;
init(); # (6, 0)
from pygame.locals import *;
from math import sin, cos, tan, atan, pi, hypot, sqrt;
from random import random, randint;
from time import sleep, time;
from sys import argv;


X = 1300; Y = 700;
if len(argv) > 2:
	X = int(argv[-2])
	Y = int(argv[-1]);

if (X == 1920) and (Y == 1080): MODE = FULLSCREEN;
else:				MODE = RESIZABLE ;

SIZE = (X, Y);
CENTER = (X/2, Y/2);

s = display.set_mode(SIZE, MODE);

def barycentre(particles, ref):
	"""Renvoie le barycentre d'une distribution de particules pondérées.
	Coordonées calculées à partir d'une particule de référence,
	mais données de manière absolue."""
	x = y = 0;
	c = 0;
	for p in particles:
		x += p.charge * (ref.x - p.x);
		y += p.charge * (ref.y - p.y);
		c += p.charge;
#	relativ = (x/c, y/c);
	absol = (ref.x - x/c, ref.y - y/c);
	return Particle(absol[0], absol[1], c, (255,0,0), False);

class Particle:
	def __init__(self, x, y, charge, color=(255, 255, 255), mobile=True):
		self.x = x;
		self.y = y;
		self.charge =charge;
		self.oldx = x;
		self.oldy = y;
		self.mobile = mobile;
		
		self.color = color;
		
	def angle(self, autre):
		try:
			angle = atan( (self.y - autre.y) / (self.x - autre.x) );
			return angle;
		except ZeroDivisionError:
			#print "Error calculating angle: Same position."
			return 0;
	
	def move(self, particle):
		### si la particule est statique: on arrête là
		if not self.mobile: return;
		### sauve coordonnées
		self.oldx = self.x;
		self.oldy = self.y;
		
		### calcul de l'angle avec l'autre particule
		fixed_angle = self.angle(particle);
		stochastic_angle = 2*(0.5-random()) * 0.8; # angle random

		angle = fixed_angle + stochastic_angle;
		
		### distance à la particule
		distance = hypot( (self.x - particle.x), (self.y - particle.y) )/3.0;
		if  distance == 0:
			distance =1;
		### loi du mouvement par rapport à la particule
		#bug de déplacement si self.x < particle.x
		if self.x < particle.x:	o = -1;
		else:					o = +1;
		
		self.x = self.x + o * self.charge * cos(angle) /(distance+1);
		self.y = self.y + o * self.charge * sin(angle) /(distance+1);
		

	
	def render(self, screen=s):
		X, Y = int(self.x), int(self.y)
		line = draw.line(screen, self.color, (int(self.oldx), int(self.oldy)), (X, Y), int(sqrt(self.charge)));
		###TODO Si la particule croise un chemin d'une autre particule elle disparaît
		# out
		if (X > SIZE[0]-1 or X < 1) or (Y > SIZE[1]-1 or Y < 1 ):
			self.mobile = False;
		# collision
#		elif screen.get_at((X, Y))[0] == (0,0):
#			self.mobile = False;


# une figure
def discharge(particles_list, screen=s):
	for p in particles_list:
		p.render();
	n = 0;
	while len(particles_list) > 5:
		for p in particles_list:
			# enlever toutes les particules fixes
			if not p.mobile:
				particles_list.remove(p);
				break;
			# crée une liste des toutes les particules sans l'actuelle
			TEMP = list(particles_list);
			TEMP.remove(p);
			### 1°) calcul des interaction avec le barycentre des charges (0.01s plus lent mais joli)
#			b = barycentre(TEMP, p);
#			p.move(b);
			
			### 2°) Calcul des interactions avec toutes les autres charges (un peu plus dégueu')
			olx, oly = p.x, p.y; # sauvegarde des coord. pour bug de lignes discontinues
			for a in TEMP:
				p.move(a);
			p.oldx, p.oldy = olx, oly;

#			p_olist = particles_list; p_olist.remove(p);
#			for p_o in p_olist:
#				if p.x - p_o.x < 100 and p.y - p_o.y < 100:
#					p.move(p_o);
			
			# Affichage
			p.color = [230-n*230/150, 245-n*245/150, 255-n*220/150];
			p.render();

			if random() < (2**(n))*0.1 and p.mobile: # séparation d'une particle mobile chargée (10% chance)
				if p.charge < 1:
					particles_list.remove(p);
					continue;
				loss = randint(1, p.charge);
				particles_list.append( Particle(p.x, p.y, p.charge-loss, p.color) );
				p.charge -= loss;


		


#		B = barycentre(particles_list, Particle(0,0,0));
#		B.render();
#		sleep(0.01);
		sleep(0.005);
		display.flip();


### MAIN LOOP
fixed = False;
while True:
	# liste de n particules
	if not fixed: n = randint(2,6);

	# events loop
	for evt in event.get():
		if evt.type == MOUSEBUTTONDOWN or evt.type == QUIT:
			exit();
		### réinitialiser la taille de la fenêtre:
		elif evt.type == VIDEORESIZE:
			X = evt.w;
			Y = evt.h;
		elif evt.type == KEYDOWN:
			if   evt.key == K_KP_MINUS:
				if n > 15:
					n -= 10;
					fixed = True;
			elif evt.key == K_KP_PLUS:
				if n < 200:
					n += 10
					fixed = True;
			elif evt.key == K_KP3:
				n = 3;
				fixed = True;
			elif evt.key == K_KP0:
				fixed = False;
			
			elif evt.key == K_q:
				exit(0);
	
	### FOND
	s.fill((0,0,0));
	### NUAGE
	draw.circle(s, (30,30,50), (SIZE[0]/3, -100), 500)
	draw.circle(s, (30,30,50), (SIZE[0]*2/3, -200), 400)
	draw.circle(s, (30,30,50), (SIZE[0]*3/3, -400), 800)
	draw.circle(s, (30,30,50), (0, 0), 500)



	### TODO : mieux répartir les charges autour du point de départ (p.ex à certains multiples de pi/6 ± random)
	x_rand = randint(1,6) * X/6;
	draw.circle(s, 3*[255], (x_rand, Y/6), 10)
	x = lambda c,n: x_rand + 10*cos(c*pi/(n/4.0) + (random()-0.5)/8.0);
	y = lambda c,n: Y/6 + 10*sin(c*pi/(n/4.0) + (random()-0.5)/8.0);
	
	PARTICLES = [ Particle(x(c,n), y(c,n), randint(20,80)) for c in range(n) ];
	
	tstart = time();
	discharge(PARTICLES); # <<<<< what's important
	if time() - tstart < 1:
		continue;
	
	display.flip();
	sleep(1);

	




