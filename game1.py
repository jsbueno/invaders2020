#! /home/gwidion/apresentacao/pythonbrasil2020/invaders2020/env39/bin/python

import random

import pygame

from pygame import Vector2 as V2

cores = [(255, 0, 0), (255, 255, 0), (255, 128, 0), (192, 128,0), (0, 255,0)]

LARGURA, ALTURA = 640, 480
PASSO = 10
FPS = 30
DELAY = int(1000 / FPS)
TAMANHO = 50


class ExcecaoDoJogo(BaseException):
    pass

class JogadorMorreu(ExcecaoDoJogo):
    pass

class PassouDeFase(ExcecaoDoJogo):
    pass

class JogadorSaiu(ExcecaoDoJogo):
    pass

def iniciar():
    global tela
    tela = pygame.display.set_mode((LARGURA, ALTURA))

class Objeto:
    def __init__(self):
        self.tamanho = 50

    def atualiza(self):
        pass

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.tamanho, self.tamanho)

    def atualiza(self):
        if self.x <= 0:
            self.x = 0
        elif self.x >= (LARGURA - TAMANHO):
            self.x = LARGURA- TAMANHO

        if self.y <= 0:
            self.y = 0
        elif self.y >= (ALTURA - TAMANHO):
            self.y = ALTURA - TAMANHO


class Jogador(Objeto):
    vel_max = 2 * PASSO
    aceleracao = 2

    def __init__(self):
        super().__init__()

        self.pos = V2(0, ALTURA // 2)
        self.vel = V2(0, 0)
        self.acel = V2(0,0)

    @property
    def x(self):
        return self.pos.x
    @x.setter
    def x(self, valor):
        self.pos.x = valor

    y = property((lambda self: self.pos.y), (lambda self, valor: setattr(self.pos, "y", valor)))


    def atualiza(self, events):

        for event in events:
            if event.type == pygame.KEYDOWN:
                tecla = event.key

                if tecla == pygame.K_RIGHT:
                    self.acel.x = self.aceleracao
                if tecla == pygame.K_LEFT:
                    self.acel.x = - self.aceleracao
                if tecla == pygame.K_UP:
                    self.acel.y = - self.aceleracao
                if tecla == pygame.K_DOWN:
                    self.acel.y = self.aceleracao

            if event.type == pygame.KEYUP:
                tecla = event.key
                if tecla in (pygame.K_RIGHT, pygame.K_LEFT):
                    self.acel.x = 0
                if tecla in {pygame.K_UP, pygame.K_DOWN}:
                    self.acel.y = 0

        self.vel += self.acel

        if self.vel.x > self.vel_max:
            self.vel.x = self.vel_max

        if self.vel.y > self.vel_max:
            self.vel.y = self.vel_max

        self.vel *= 1

        self.x += self.vel.x
        self.y += self.vel.y

        super().atualiza()



class Inimigo(Objeto):
    def __init__(self, numero):
        super().__init__()
        self.cor = (192, 0, 192)
        self.x, self.y = (LARGURA - TAMANHO,  ALTURA // 2 + numero * TAMANHO * 2)
        self.cont = 0
        self.vel_x = 0

    def atualiza(self):
        self.cont += 1
        if self.cont < 10:
            self.y -= PASSO
        elif self.cont < 30:
            self.y += PASSO
        else:
            self.cont = -10

        if random.random() < 0.1:
            self.vel_x += random.randrange(-3, +3, 1)

        self.x += self.vel_x

        if self.get_rect().colliderect(jogador.get_rect()):
            raise JogadorMorreu()

        super().atualiza()


def principal():
    global jogador

    executando = True
    indice = 0

    jogador = Jogador()
    inimigos = []

    for i in range(4):
        inimigos.append(Inimigo(i))

    while executando:

        cor = cores[indice]
        indice += 1

        if indice >= len(cores):
            indice = 0
        eventos = pygame.event.get()
        for event in eventos:
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                raise JogadorSaiu()

        jogador.atualiza(eventos)
        for inimigo in inimigos:
            inimigo.atualiza()

        tela.fill((0, 0, 0))

        pygame.draw.rect(tela, cor, jogador.get_rect() )
        for inimigo in inimigos:
            pygame.draw.rect(tela, inimigo.cor, inimigo.get_rect() )
        pygame.display.flip()
        pygame.time.delay(DELAY)


iniciar()
try:
    principal()
except JogadorMorreu:
    print("Você foi morto")
except ExcecaoDoJogo:
    print("O jogo acabou por que você saiu ou passou de fase")
else:
    print("Voce saiu")
finally:
    pygame.quit()
