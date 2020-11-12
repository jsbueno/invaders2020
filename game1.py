#! /home/gwidion/apresentacao/pythonbrasil2020/invaders2020/env39/bin/python

import pygame

cores = [(255, 0, 0), (255, 255, 0), (255, 128, 0), (192, 128,0), (0, 255,0)]

LARGURA, ALTURA = 640, 480
PASSO = 10
FPS = 30
DELAY = int(1000 / FPS)
TAMANHO = 50


def iniciar():
    global tela
    tela = pygame.display.set_mode((LARGURA, ALTURA))


x = y = vel_x = vel_y = 0

x_i, y_i =  (LARGURA - TAMANHO,  ALTURA // 2)
cor_i = (192, 0, 192)
cont_i = 0

def atualiza_i():
    global x_i, y_i, cont_i
    cont_i += 1
    if cont_i < 10:
        y_i -= PASSO
    elif cont_i < 30:
        y_i += PASSO
    else:
        cont_i = -10


def atualiza(events):
    global x, y, vel_x, vel_y

    for event in events:
        if event.type == pygame.KEYDOWN:
            tecla = event.key

            if tecla == pygame.K_RIGHT:
                vel_x += PASSO
            if tecla == pygame.K_LEFT:
                vel_x += -PASSO
            if tecla == pygame.K_UP:
                vel_y = -PASSO
            if tecla == pygame.K_DOWN:
                vel_y = PASSO

        if event.type == pygame.KEYUP:
            tecla = event.key
            if tecla == pygame.K_RIGHT or tecla == pygame.K_LEFT:
                vel_x = 0
            if tecla in {pygame.K_UP, pygame.K_DOWN}:
                vel_y = 0

    x += vel_x
    y += vel_y

    if x <= 0:
        x = 0
    elif x >= (LARGURA - TAMANHO):
        x = LARGURA- TAMANHO

    if y <= 0:
        y = 0
    elif y >= (ALTURA - TAMANHO):
        y = ALTURA - TAMANHO



def principal():
    executando = True
    indice = 0

    while executando:

        cor = cores[indice]
        indice += 1

        if indice >= len(cores):
            indice = 0
        eventos = pygame.event.get()
        for event in eventos:
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                executando = False

        atualiza(eventos)
        atualiza_i()

        tela.fill((0, 0, 0))

        pygame.draw.rect(tela, cor, (x, y, TAMANHO, TAMANHO))
        pygame.draw.rect(tela, cor_i, (x_i, y_i, TAMANHO, TAMANHO))
        pygame.display.flip()
        pygame.time.delay(DELAY)


iniciar()
principal()
