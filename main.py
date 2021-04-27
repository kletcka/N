import pygame
import PIL
import os
from PIL import Image, ImageDraw, ImageTk
import random
import math
import threading
import time
pygame.init()
clock = pygame.time.Clock()
WIDTH = 1200
HEIGHT = 512
screen = pygame.display.set_mode((WIDTH, HEIGHT))
done = False
pygame.font.init()
image = Image.new("RGB", (512,512), (177,34,45))
draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования
width = image.size[0]  # Определяем ширину
height = image.size[1]  # Определяем высоту
pix = image.load() 
size = 400
n = 2
angle = 60
cx = 40
cy = 140
clicks = 0
cur_clicks = 0
iterations = 0 
cps = 0
event = threading.Event()
up1_b = 0
up2_b = 0
up3_b = 0
up4_b = 0
myfont = pygame.font.SysFont(None, 30)


def forward(size):
    global angle, cx, cy

    angle = angle%360
    ang = (angle) * 3.14 / 180.0
    cx1 = cx + size * math.cos(ang)
    cy1 = cy + size * math.sin(ang)
    draw.line((cx, cy, cx1, cy1), width=1)
    cx=cx1
    cy=cy1



def koch_curve(size, n):
    global angle, cur_clicks, clicks, iterations
    if n == 0:
        forward(size)
        while cur_clicks//1==clicks:
            continue
        clicks = cur_clicks
        iterations += 1


    else:
        koch_curve(size / 3, n - 1)
        angle+=60
        koch_curve(size / 3, n - 1)
        angle-=120
        koch_curve(size / 3, n - 1)
        angle+=60
        koch_curve(size / 3, n - 1)
 
 
def draw_koch_snowflake(size, n):
    global angle, draw, width, height, pix, cx, cy, image, clicks, cur_clicks
    while True:
        for i in range(3):
            koch_curve(size, n)
            angle-=120
        n+=1
        image = Image.new("RGB", (512,512), (177,34,45))
        draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования
        width = image.size[0]  # Определяем ширину
        height = image.size[1]  # Определяем высоту
        pix = image.load() 
        cx = 40
        cy = 140
        clicks = 0
        cur_clicks = 0
    
def pilImageToSurface(pilImage):
    return pygame.image.fromstring(
        pilImage.tobytes(), pilImage.size, pilImage.mode).convert()
def delta():
    draw_koch_snowflake(size, n)
thr = threading.Thread(target = delta)
thr.start()

def up():
    global cur_clicks, cps
    while True:
        cur_clicks += cps/100
        time.sleep(1)


thr1 = threading.Thread(target = up)
thr1.start()

while not done:

    screen.fill((177,34,45))
    clock.tick(60)
    pygameSurface = pilImageToSurface(image)
    up1 = pygame.image.load('calc.png')
    up2 = pygame.image.load('school.png')
    up3 = pygame.image.load('ai.png')
    up4 = pygame.image.load('manuscript.png')
    textsurface = myfont.render(f"Bought: {up1_b}, price: {100*((up1_b+1)**2)}", False, (255, 255, 255))
    textsurface1 = myfont.render(f"Bought: {up2_b}, price: {1000*((up2_b+1)**2)}", False, (255, 255, 255))
    textsurface2 = myfont.render(f"Bought: {up3_b}, price: {10000*((up3_b+1)**3)}", False, (255, 255, 255))
    textsurface3 = myfont.render(f"Bought: {up4_b}, price: {100000*((up4_b+1)**5)}", False, (255, 255, 255))
    textsurface4 = myfont.render(f"Coins: {iterations}", False, (255, 255, 255))
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            done = True
        if i.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if pygameSurface.get_rect().collidepoint(pos):
                cur_clicks+=0.1
                cur_clicks = int(cur_clicks*10 + (0.5 if cur_clicks*10 > 0 else -0.5))/10
            if up1.get_rect(center = (640, 64)).collidepoint(pos):
                if iterations >= 100*((up1_b+1)**2):
                    cps += 1
                    iterations -= 100*((up1_b+1)**2)
                    up1_b += 1

            if up2.get_rect(center = (640, 192)).collidepoint(pos):
                if iterations >= 1000*((up2_b+1)**2):
                    cps += 2
                    iterations -= 1000*((up2_b+1)**2)
                    up2_b += 1
            if up3.get_rect(center = (640, 320)).collidepoint(pos):
                if iterations >= 10000*((up3_b+1)**3):
                    cps += 10
                    iterations -= 10000*((up3_b+1)**3)
                    up3_b += 1
            if up4.get_rect(center = (640, 448)).collidepoint(pos):
                if iterations >= 100000*((up4_b+1)**5):
                    cps += 100
                    iterations -= 100000*((up4_b+1)**5)
                    up4_b += 1
    screen.blit(pygameSurface, pygameSurface.get_rect(center = (256, 256)))
    screen.blit(up1, up1.get_rect(center = (640, 64)))
    screen.blit(textsurface, (775, 58))
    screen.blit(up2, up2.get_rect(center = (640, 192))) 
    screen.blit(textsurface1, (775, 58+128)) 
    screen.blit(up3, up3.get_rect(center = (640, 320))) 
    screen.blit(textsurface2, (775, 58+128+128))
    screen.blit(up4, up4.get_rect(center = (640, 448))) 
    screen.blit(textsurface3, (775, 58+128+128+128))
    screen.blit(textsurface4, (20, 480))
    pygame.display.flip()

pygame.quit()