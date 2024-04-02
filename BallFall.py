import pygame
import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import ode
import random
from datetime import datetime

pygame.init()
win_width = 640
win_height = 640
screen = pygame.display.set_mode((win_width, win_height))  # Top left corner is (0,0)
pygame.display.set_caption('Ball Fall')



# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#Constances
gravity = -9.8
dt = 0.05
mass = 1
radius = 1
COR = 1


#clock
clock = pygame.time.Clock()

#balls


class Ball:
    def __init__(self, pos, mass, color, radius):
        self.pos = np.array(pos)
        self.vel = np.array([0,0])

        self.t = 0

        self.radius = radius
        self.color = color
        self.mass = mass

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)

    def set_pos(self, pos):
        self.pos = np.array(pos)

    def set_vel(self, vel):
        self.vel = np.array(vel)

    def update(self, dt):
    
    def f(self):


class Triangle:
    def __init__(self, pos):
        self.pos = np.array(pos)

    
    def draw(self):
        pygame.draw.t(screen, self.color, self.pos, self.radius) #position needs to be a list of 3 coords [(x,y), (x2,y2), (x3,y3)]


class bigBall:
    def __init__(self, pos, color, radius):
        self.pos = np.array(pos)
        self.radius = radius
        self.color = color

    def set_pos(self, pos):
        self.pos = np.array(pos)
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)



def Collision_detection(activeballs):
    for i in range(activeballs.len()):

        #wall collision
        if activeballs.x <= 0:
            #screen edge
        elif activeballs.x >= 640:
            #other edge

        #object collision
        if activeballs[i].x == 1:
            #triangle collision
        else:
            #ball collsions

        
def make_ball(active):
    x = 320 # set to random in a range
    y = 620
    pos = np.array([x,y])
    active.append(Ball(pos,mass, WHITE, radius))




def main():
    activeballs = [Ball]

    
if __name__ == '__main__':
    main()
