#! /usr/bin/env python
# -*- coding:Utf-8 -*-
# brown
# GPL - baptiste.paris.v@gmail.com
from pygame import *; init();
from pygame.locals import *;

from random import random, randint;
from time import sleep;
from math import sin, cos, pi, sqrt;

# COLORS
black = (0,0,0);
white = (255,255,255);

# SCREEN (full)
SIZE = (1366,720);
CENTER = (SIZE[0]/2, SIZE[1]/2);

s = display.set_mode(SIZE);
s.fill(3*[255]);

def barycentre(particles, ref):
	"""Renvoie le barycentre d'une distribution de particules.
	Coordonées calculées à partir d'une particule de référence,
	mais données de manière absolue."""
	x = y = 0;
	c = 0;
	for p in particles:
		x += (ref[0] - p[0]);
		y += (ref[1] - p[1]);
		c += 1;
	absol = (ref[0] - x/c, ref[1] - y/c);
	return absol;


def brown(start=CENTER, maxlength=4, color=black):
	angle = 2*pi*random();
	length = randint(1, maxlength);
	x = start[0] + length * sin(angle);
	y = start[1] + length * cos(angle);
	end = (x,y);
	draw.line(s, color, start, end, 4);
	return end;

def wander(steps=100, maxlength=4, color=black):
	prev = CENTER;
	pos = [];
	for i in xrange(steps):
		pos.append(prev)
		prev = brown(prev, maxlength, color);
		
		display.flip();
		
		b = s.copy(); # copy screen
		b.set_alpha(254); # and dim
		s.fill(white); # reset screen
		s.blit(b, (0,0)); # paste dimmed copy of previous screen
		

	b = barycentre(pos, pos[0]);
	return steps, sqrt((prev[0]-CENTER[0])**2+(prev[1]-CENTER[1])**2), b[0]-CENTER[0], b[1]-CENTER[1];

def demo(times=20, pathlength=200, maxsteplength=20):
	deviations = [];
	for i in xrange(times):
		pathlength = randint(100, 1000);
		print pathlength
		
		randcolor = [ int(random()*255) for i in range(3) ];
		deviations.append(wander(pathlength, maxsteplength, randcolor));
		s.fill(3*[255]);
		b = s.copy(); # copy screen
		b.set_alpha(180); # and dim
		s.fill(white); # reset screen
		s.blit(b, (0,0)); # paste dimmed copy of previous screen

		# events loop
		for evt in event.get():
			if evt.type == QUIT:
				f = open('brown.log', 'a');
				with f:
					for l in deviations:
						for e in l:
							f.write(str(e) + '\t')
						f.write('\n');
				exit();
	f = open('brown.log', 'a');
	with f:
		for l in deviations:
			for e in l:
				f.write(str(e) + '\t')
			f.write('\n');
		
demo(30, 300);


