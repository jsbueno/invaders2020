#! /home/gwidion/apresentacao/pythonbrasil2020/invaders2020/env39/bin/python

import random

import pygame

from pygame import Vector2 as V2



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



class Objeto:
    tamanho = V2(50, 50)

    imagem = None

    def __init__(self, jogo, pos=None, vel=None):
        self.jogo = jogo
        if pos is None:
            pos = V2(0, 0)
        if vel is None:
            vel = V2(0, 0)
        self.pos = pos
        self.vel = vel
        self.limite_direito = LARGURA - self.tamanho.x

    x = property((lambda self: self.pos.x), (lambda self, valor: setattr(self.pos, "x", valor)))
    y = property((lambda self: self.pos.y), (lambda self, valor: setattr(self.pos, "y", valor)))

    def atualiza(self):
        pass

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.tamanho.x, self.tamanho.y)

    def atualiza(self):
        self.pos += self.vel

        if self.x <= 0:
            self.x = 0
        elif self.x >= self.limite_direito:
            self.x = self.limite_direito

        if self.y <= 0:
            self.y = 0
        elif self.y >= (ALTURA - TAMANHO):
            self.y = ALTURA - TAMANHO

    def desenha(self):
        pygame.draw.rect(self.jogo.tela, self.cor, self.get_rect())

class Jogador(Objeto):
    vel_max = PASSO
    aceleracao = 2
    cores = [(255, 0, 0), (255, 255, 0), (255, 128, 0), (192, 128,0), (0, 255,0)]

    def __init__(self, jogo):
        super().__init__(jogo, pos=V2(0, ALTURA // 2))

        self.acel = V2(0,0)
        self.indice = 0

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
                if tecla == pygame.K_SPACE:
                    self.jogo.tiros.append(Tiro(self.jogo, self.pos + V2(self.tamanho.x,  self.tamanho.y // 2)))

            if event.type == pygame.KEYUP:
                tecla = event.key
                if tecla in (pygame.K_RIGHT, pygame.K_LEFT):
                    self.acel.x = 0
                if tecla in {pygame.K_UP, pygame.K_DOWN}:
                    self.acel.y = 0

        self.vel += self.acel

        if abs(self.vel.x) > self.vel_max:
            self.vel.x = self.vel_max * (-1 if self.vel.x < 0 else 1)

        if abs(self.vel.y) > self.vel_max:
            self.vel.y = self.vel_max * (-1 if self.vel.y < 0 else 1)

        self.vel *= 1

        super().atualiza()

        self.cor = self.cores[self.indice]
        self.indice = (self.indice + 1) % len(self.cores)


class Tiro(Objeto):
    vel_inicial = V2(1.5 * PASSO, 0)
    altura = TAMANHO / 5
    cor = (0, 192, 255)
    tamanho = V2(TAMANHO // 2, altura)

    def __init__(self, jogo, pos):
        super().__init__(jogo, pos, vel=self.vel_inicial)
        self.limite_direito = LARGURA + 1

    def atualiza(self):
        super().atualiza()

        if self.x >= LARGURA:
            self.remove()

        for inimigo in self.jogo.inimigos:
            rect = self.get_rect()
            if rect.colliderect(inimigo.get_rect()):
                inimigo.acertado(self)
                self.remove()

    def remove(self):
        self.jogo.tiros.remove(self)

    def get_rect(self):
        x = int(self.pos.x)
        y = int(self.pos.y - self.altura / 2)
        return pygame.Rect (x, y, TAMANHO // 2, self.altura)



class Inimigo(Objeto):
    def __init__(self, jogo, numero):
        pos = V2(LARGURA - TAMANHO,  ALTURA // 2 + numero * TAMANHO * 2)
        super().__init__(jogo, pos)
        self.cor = (192, 0, 192)
        self.cont = 0
        self.vel = V2(0, 0)

    def atualiza(self):
        self.cont += 1
        if self.cont < 10:
            self.vel.y = 10
        elif self.cont < 30:
            self.vel.y = -10
        else:
            self.cont = -10

        if random.random() < 0.1:
            self.vel.x += random.randrange(-3, +3, 1)

        if self.get_rect().colliderect(self.jogo.jogador.get_rect()):
            raise JogadorMorreu()

        super().atualiza()

    def acertado(self, objeto):
        self.remove()

    def remove(self):
        self.jogo.inimigos.remove(self)


class Jogo:

    def __init__(self):

        self.tela = pygame.display.set_mode((LARGURA, ALTURA))

    def principal(self):


        self.jogador = Jogador(self)
        self.inimigos = []

        for i in range(4):
            self.inimigos.append(Inimigo(self, i))

        self.tiros = []

        executando = True
        while executando:

            eventos = pygame.event.get()
            for event in eventos:
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    raise JogadorSaiu()

            self.jogador.atualiza(eventos)
            for inimigo in self.inimigos:
                inimigo.atualiza()
            for tiro in self.tiros:
                tiro.atualiza()

            self.desenha_fundo()

            self.jogador.desenha()
            for inimigo in self.inimigos:
                inimigo.desenha()

            for tiro in self.tiros:
                tiro.desenha()

            pygame.display.flip()
            pygame.time.delay(DELAY)

    def desenha_fundo(self):
        self.tela.fill((0, 0, 0))


jogo = Jogo()
try:
    jogo.principal()
except JogadorMorreu:
    print("Você foi morto")
except ExcecaoDoJogo:
    print("O jogo acabou por que você saiu ou passou de fase")
else:
    print("Voce saiu")
finally:
    pygame.quit()
