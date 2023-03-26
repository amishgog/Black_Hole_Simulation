import pygame
import math
import numpy as np
pygame.init()

WIDTH , HEIGHT = 800 , 800
WIN = pygame.display.set_mode((WIDTH,HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Black Hole M87 Simulation")


#defining the constants
c = 30
G = 4 
particles = []
dt = 0.05


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

    def pull(self , photon):
        force = pygame.math.Vector2(self.pos - photon.pos)
        r = force.magnitude()
        fg = (G * self.mass) / (r * r)
        norm_force = math.sqrt((force.x * force.x) + (force.y * force.y))
        normalized_force = (force.x / norm_force  , force.y / norm_force)
        force_app = pygame.math.Vector2(normalized_force[0] * fg , normalized_force[1] * fg)
        photon.vel += force_app
        norm_vel = math.sqrt((photon.vel.x * photon.vel.x) + (photon.vel.y * photon.vel.y))
        normalized_vel = (photon.vel.x / norm_vel  , photon.vel.y / norm_vel)
        velocity = pygame.math.Vector2(normalized_vel[0] * c , normalized_vel[1] * c)
        photon.vel = velocity

        if r <= (self.radius + 0.5):
            photon.stop()




class Photon():
    def __init__(self,x,y):
        self.pos = pygame.math.Vector2(x,y)
        self.vel = pygame.math.Vector2(-c,0)
        self.history = []
        self.stopped = False

    def stop(self):
        self.stopped = True

    
    def draw(self):
        for i in range(len(self.history)-1):
            start_pos = (int(self.history[i].x), int(self.history[i].y))
            end_pos = (int(self.history[i+1].x), int(self.history[i+1].y))
            pygame.draw.aaline(WIN, (255, 0, 0), start_pos, end_pos)

    
    def update(self):
        if (not self.stopped):
            self.history.append(self.pos.copy())
            deltaV = self.vel.copy()
            deltaV = (deltaV * dt) 
            self.pos = self.pos + deltaV


        if len(self.history) > 700:
            self.history.pop(0)


start = 0
end = 0 

def main():
    clock = pygame.time.Clock()
    run = True


    m87 = BlackHole(400, 400, 2000)


    start = HEIGHT / 2
    end = (HEIGHT / 2) - m87.radius
    particles = [Photon(WIDTH - 20, y) for y in np.linspace(0, end, 30)]

    pygame.draw.line(WIN , (0,0,0) , (0, start) , (WIDTH, start) , 1)

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        WIN.fill((255, 255, 255))
        m87.draw()

        for p in particles:
            m87.pull(p)
            p.update()
            p.draw()

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
