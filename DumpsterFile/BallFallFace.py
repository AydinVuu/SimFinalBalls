import pygame
import sys
import numpy as np
import math
from pygame import mixer
import random

mixer.init()
mixer.music.load('peghit.ogg')


pygame.display.set_caption('Ball Fall')

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Constants
gravity = -9.8
dt = 0.05
mass = 1
radius = random.randint(10, 30)
color = (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))
big_ball_color = (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))
triangle_color = (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))

# Elasticity of all objects
COR = 0.7

# randomize for different types of balls
# change mass constant to a gravity multiplier
# radius multiplier as well
# have one normal ball with default gravity and radius
# random ball spawns use lab 6
# when balls below line, check for x coord to assign points
# if we goated add spin

# clock
clock = pygame.time.Clock()


class Ball:
    def __init__(self, position, velocity, radius, color, mass=1):
        self.set_pos(position)
        self.set_vel(velocity)
        self.radius = radius
        self.mass = mass
        self.color = color
    def set_pos(self, pos):
        self.position = np.array(pos, dtype=float)

    def set_vel(self, vel):
        self.velocity = np.array(vel, dtype=float)

    def update(self, dt):
        k1v = dt * self.acceleration(self.position, self.velocity)
        k1x = dt * self.velocity
        k2v = dt * self.acceleration(self.position + 0.5 * k1x, self.velocity + 0.5 * k1v)
        k2x = dt * (self.velocity + 0.5 * k1v)
        k3v = dt * self.acceleration(self.position + 0.5 * k2x, self.velocity + 0.5 * k2v)
        k3x = dt * (self.velocity + 0.5 * k2v)
        k4v = dt * self.acceleration(self.position + k3x, self.velocity + k3v)
        k4x = dt * (self.velocity + k3v)
        self.velocity += (1/6) * (k1v + 2 * k2v + 2 * k3v + k4v)
        self.position += (1/6) * (k1x + 2 * k2x + 2 * k3x + k4x)

    def acceleration(self, position, velocity):
        return np.array([0, gravity])

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), self.radius)
    def __del__(self):
        pass
#Code by Paul Panzer (December 7th, 2017) Array of coordinates between two points
#URL: https://stackoverflow.com/questions/47704008/fastest-way-to-get-all-the-points-between-two-x-y-coordinates-in-python
def connect(ends):
    d0, d1 = np.abs(np.diff(ends, axis=0))[0]
    if d0 > d1: 
        return np.c_[np.linspace(ends[0, 0], ends[1, 0], d0+1, dtype=np.int32),
                     np.round(np.linspace(ends[0, 1], ends[1, 1], d0+1))
                     .astype(np.int32)]
    else:
        return np.c_[np.round(np.linspace(ends[0, 0], ends[1, 0], d1+1))
                     .astype(np.int32),
                     np.linspace(ends[0, 1], ends[1, 1], d1+1, dtype=np.int32)]


class Triangle:
    def __init__(self, screen, pos, color):
        # pos format [[x,y],[x2,y2],[x3,y3]]
        self.screen = screen
        self.pos = pos  # order will top vertice, right vertice, left vertice
        self.color = color
        rp = np.array([pos[0], pos[1]])
        lp = np.array([pos[0], pos[2]])
        self.rightedge = connect(rp)
        self.leftedge = connect(lp)
        # the angle from the center of the ball that will hit the edges of the triangle
        self.langle = math.atan2((pos[0][0] - pos[1][0]), -(pos[0][1] - pos[1][1]))
        self.rangle = math.atan2(-(pos[0][0] - pos[2][0]), (pos[0][1] - pos[2][1]))
        # find

    def draw(self):
        pygame.draw.polygon(screen, self.color, self.pos)  # position needs to be a list of 3 coords [[x,y],[x2,y2],[x3,y3]]


class BigBall:
    def __init__(self, screen, pos, color, radius):
        self.screen = screen
        self.pos =pos
        self.radius = radius
        self.color = color

    def set_pos(self, pos):
        self.pos = np.array(pos)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)


def Collision_detection(activeballs, bigballs, triangles):
    for ball in activeballs:

        # Wall collision
        if (ball.position[0] - ball.radius) <= 0:
            # Left wall
            mixer.music.play()
            ball.position[0] = ball.radius
            ball.velocity[0] *= -COR
        elif (ball.position[0] + ball.radius) >= screen_width:
            # Right wall
            mixer.music.play()
            ball.position[0] = screen_width - ball.radius
            ball.velocity[0] *= -COR

        # Object collision
        # Check if the ball is on the left side of the screen
        for triangle in triangles:
            if ball.position[0] + radius >= triangle.pos[2][0] and ball.position[0] - radius <= triangle.pos[1][0]:
                # Check collision with triangle
                disx = ball.position[0] - triangle.pos[0][0]
                disy = ball.position[1] - triangle.pos[0][1]

                distance = math.sqrt(disx**2 + disy**2)

                
                
                if distance <= ball.radius:
                    mixer.music.play()
                    #Ball on stationary
                    relative_velocity = ball.velocity - np.array([0, 0]) 
                    #Bounce
                    normal_vector = np.array([disx, disy]) / distance
                    dot_product = np.dot(relative_velocity, normal_vector)
                    impulse = (2 * dot_product)
                    ball.velocity -= impulse * normal_vector
                
                elif ball.position[0] >= triangle.pos[0][0]: #right side

                    for j in range(len(triangle.rightedge)):
                        
                        if triangle.rightedge[j][0] == round(ball.position[0] + (radius * math.cos(triangle.rangle))):
                            
                            if triangle.rightedge[j][1] < (ball.position[1] - (radius * math.sin(triangle.rangle))) and ((ball.position[1] - (radius * math.sin(triangle.rangle))) < triangle.pos[1][1]):
                                mixer.music.play()
                                #Ball on stationary
                                relative_velocity = ball.velocity - np.array([0, 0]) 
                                #Bounce
                                normal_vector = np.array([-(radius * math.cos(triangle.rangle)), (radius * math.sin(triangle.rangle))]) / radius
                                dot_product = np.dot(relative_velocity, normal_vector)
                                impulse = (2 * dot_product)
                                ball.velocity -= impulse * normal_vector
                                
                                for l in range(len(triangle.rightedge)):
                                    if triangle.rightedge[l][1] == round(ball.position[1] - (radius * math.sin(triangle.rangle))):
                                        index = round((l + j)/2)
                                        disxr = (ball.position[0] + (radius * math.cos(triangle.rangle))) - triangle.rightedge[index][0]
                                        disyr = (ball.position[1] - (radius * math.sin(triangle.rangle))) - triangle.rightedge[index][1]
                                        distancer = math.sqrt(disxr**2 + disyr**2)
                                        ball.position[0] += distancer*(-(math.cos(triangle.rangle)))
                                        ball.position[1] += distancer*(math.sin(triangle.rangle))

                    disx2 = ball.position[0] - triangle.pos[1][0]
                    disy2 = ball.position[1] - triangle.pos[1][1]

                    distance2 = math.sqrt(disx2**2 + disy2**2)
                    if distance2 <= ball.radius:
                        mixer.music.play()
                        #Ball on stationary
                        relative_velocity = ball.velocity - np.array([0, 0]) 
                        #Bounce
                        normal_vector = np.array([disx2, disy2]) / distance2
                        dot_product = np.dot(relative_velocity, normal_vector)
                        impulse = (2 * dot_product)
                        ball.velocity -= impulse * normal_vector


                elif ball.position[0] <= triangle.pos[0][0]: #left side

                    for k in range(len(triangle.leftedge)):

                        if triangle.leftedge[k][0] == round(ball.position[0] + (radius * math.cos(triangle.langle))):


                            if (triangle.leftedge[k][1] < (ball.position[1] - (radius * math.sin(triangle.langle)))) and ((ball.position[1] - (radius * math.sin(triangle.langle))) < triangle.pos[2][1]):

                                mixer.music.play()
                                #Ball on stationary
                                relative_velocity = ball.velocity - np.array([0, 0]) 

                                #Bounce
                                normal_vector = np.array([-(radius * math.cos(triangle.langle)), (radius * math.sin(triangle.langle))]) / radius
                                dot_product = np.dot(relative_velocity, normal_vector)
                                impulse = (2 * dot_product)
                                ball.velocity -= impulse * normal_vector
                                for l in range(len(triangle.leftedge)):
                                    if triangle.leftedge[l][1] == round(ball.position[1] - (radius * math.sin(triangle.langle))):
                                        index = round((l + k)/2)
                                        disxr = (ball.position[0] + (radius * math.cos(triangle.langle))) - triangle.leftedge[index][0]
                                        disyr = (ball.position[1] - (radius * math.sin(triangle.langle))) - triangle.leftedge[index][1]
                                        distancer = math.sqrt(disxr**2 + disyr**2)
                                        ball.position[0] += distancer*(-(math.cos(triangle.langle)))
                                        ball.position[1] += distancer*(math.sin(triangle.langle))

                    disx3 = ball.position[0] - triangle.pos[2][0]
                    disy3 = ball.position[1] - triangle.pos[2][1]

                    distance3 = math.sqrt(disx3**2 + disy3**2)
                    if distance3 <= ball.radius:
                        mixer.music.play()
                        #Ball on stationary
                        relative_velocity = ball.velocity - np.array([0, 0]) 
                        #Bounce
                        normal_vector = np.array([disx3, disy3]) / distance3
                        dot_product = np.dot(relative_velocity, normal_vector)
                        impulse = (2 * dot_product)
                        ball.velocity -= impulse * normal_vector

        else:
            for bigball in bigballs:
                #Ball collision with big ball
                disx = ball.position[0] - bigball.pos[0]
                disy = ball.position[1] - bigball.pos[1]
                distance = math.sqrt(disx**2 + disy**2)

                if distance < (ball.radius + bigball.radius):
                    mixer.music.play()
                    #Ball on stationary
                    relative_velocity = ball.velocity - np.array([0, 0]) 
                    #Bounce
                    normal_vector = np.array([disx, disy]) / distance
                    dot_product = np.dot(relative_velocity, normal_vector)
                    impulse = (2 * dot_product)
                    ball.velocity -= impulse * normal_vector
                

def make_ball(active, Total):
    x = 320  # set to random in a range
    y = 620
    pos = np.array([x, y])
    active.append(Ball(pos, mass, WHITE, radius))
    Total.append(Ball(pos, mass, WHITE, radius))


screen_width = 1000
screen_height = 800
gravity = 9.8
left_boundary = 100
right_boundary = 700

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ball Falling")

my_font = pygame.font.SysFont('Comic Sans MS', 30)

delta_t = 0.05
initial_position = [screen_width // 2, 0]
initial_velocity = [0,0]

ball = Ball(initial_position, initial_velocity, radius, color)
bigball = BigBall(screen, [650, 380], big_ball_color, 60)
bigball2 = BigBall(screen,[350,380], big_ball_color, 60)
bigballs = [bigball,bigball2]
tripoints = np.array([[500,380],[590,530],[410,530]])
triangle = Triangle(screen, tripoints, triangle_color)
triangles = [triangle]
is_ball_dropped = False
clock = pygame.time.Clock()
active = [ball]

score = 0

while True:
    Scoretext = "Score: %i" % score
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                is_ball_dropped = True
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and not is_ball_dropped:
        if active[0].position[0] - 3 >= left_boundary:
            active[0].position[0] -= 3
    if keys[pygame.K_d] and not is_ball_dropped:
        if active[0].position[0] + 3 <= right_boundary:
            active[0].position[0] += 3

    if is_ball_dropped:
        for ball in active:
            active[0].update(delta_t)
            Collision_detection(active,bigballs,triangles)
    
    if (ball.position[1] - radius) > screen_height + 50 :
        x_segment = min(max((ball.position[0] - left_boundary) // ((right_boundary - left_boundary) // 5), 0), 4)
        if x_segment == 2:  
            score += 300
        elif x_segment == 1 or x_segment == 3: 
            score += 200
        else:  
            score += 100

        Scoretext = "Score: %i" % score

        # Reset ball parameters and set is_ball_dropped to False
        radius = random.randint(10, 30)
        color = (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))

        active.remove(active[0])
        active.append(Ball(initial_position, initial_velocity, radius, color))
        is_ball_dropped = False

    text_surface = my_font.render(Scoretext, False, (0, 0, 0))
    screen.fill((255, 255, 255))
    screen.blit(text_surface, (0,0))
    for ball in active:
        active[0].draw(screen)
    for bigball in bigballs:
        bigball.draw()
    for triangle in triangles:
        triangle.draw()
    
    pygame.display.flip()
    clock.tick(60)
