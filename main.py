import pygame
import math
import numpy as np
pygame.init()

WIDTH , HEIGHT = 800 , 800
WIN = pygame.display.set_mode((WIDTH,HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Black Hole M87 Simulation")


#defining the constants
c = 30
G = 3.54 
particles = []
dt = 0.1


class BlackHole():
    def __init__(self,x,y,m):
        self.pos = pygame.math.Vector2(x,y)
        self.mass = m
        self.radius = (2 * G * self.mass) / (c * c)
    
    def draw(self):
        WIN.fill((255, 255, 255))
        pygame.draw.circle(WIN , (0,0,0) , (self.pos.x , self.pos.y) , (self.radius))
        pygame.draw.circle(WIN, (245,150,0) , (self.pos.x , self.pos.y) , (3 * self.radius)+15  , 30)
        pygame.draw.circle(WIN, (245,240,0) , (self.pos.x , self.pos.y) , (1.5 * self.radius)+10   , 20)

    def pull(self, photon):
        force = self.pos - photon.pos
        r = force.length()
        theta = math.atan2(force.y, force.x)
        fg = (G * self.mass) / (r * r)
        deltaTheta = -fg * (dt / c) * math.sin(photon.theta - theta)
        deltaTheta /= abs(1.0 - 2.0 * G * self.mass / (r * c * c))
        photon.theta += deltaTheta
        photon.vel = pygame.math.Vector2(math.cos(photon.theta), math.sin(photon.theta))
        photon.vel.scale_to_length(c)

        if r <= self.radius + 0.5:
            photon.stop()





class Photon():
    def __init__(self,x,y):
        self.pos = pygame.math.Vector2(x,y)
        self.vel = pygame.math.Vector2(-c,0)
        self.history = []
        self.stopped = False
        self.theta = math.pi

    def stop(self):
        self.stopped = True

    
    def draw(self):
        for i in range(len(self.history) - 1):
            start_pos = (int(self.history[i].x), int(self.history[i].y))
            end_pos = (int(self.history[i+1].x), int(self.history[i+1].y))
            pygame.draw.aaline(WIN, (255, 0, 0), start_pos, end_pos)


    def update(self, m87):
        if not self.stopped:
            self.history.append(self.pos.copy())
            deltaV = self.vel.copy()
            deltaV *= dt
            self.pos += deltaV

        if len(self.history) > 500:
            self.history.pop(0)

        if (
            self.pos.x < 0
            or self.pos.x > WIDTH
            or self.pos.y < 0
            or self.pos.y > HEIGHT
        ):
            self.stop()

start = 0
end = 0 

def main():
    clock = pygame.time.Clock()
    run = True


    m87 = BlackHole(WIDTH / 2, HEIGHT / 2, 10000)

    num_photons = 50
    distance_factor = 1.5  # Adjust this value to increase or decrease the distance between photons
    start = HEIGHT / 2
    end = (HEIGHT / 2) - (m87.radius * 2.6)
    distance = (end - start) / num_photons * distance_factor
    start_y = start - distance / 2
    particles = [Photon(WIDTH - 20, start_y + distance * i) for i in range(num_photons)]


    while run:
        clock.tick(60)  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        WIN.fill((255, 255, 255))
        m87.draw()

        for p in particles:
            m87.pull(p)
            p.update(m87)
            p.draw()

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()