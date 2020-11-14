#! /home/gwidion/apresentacao/pythonbrasil2020/invaders2020/env39/bin/python

from pathlib import Path
import random

from pygame import Vector2 as V2
import pygame




LARGURA, ALTURA = 640, 480
PASSO = 10
FPS = 30
DELAY = int(1000 / FPS)
TAMANHO = 50

CAMINHO_IMAGENS = Path("media")

class ExcecaoDoJogo(BaseException):
    pass

class JogadorMorreu(ExcecaoDoJogo):
    pass

class PassouDeFase(ExcecaoDoJogo):
    pass

class JogadorSaiu(ExcecaoDoJogo):
    pass

IMAGENS = {}

class Objeto:
    tamanho = V2(50, 50)

    imagem = None
    arq_imagem = "nao existe"
    redutor = 1

    def __init__(self, jogo, pos=None, vel=None):
        self.carrega_imagem()
        self.jogo = jogo
        if pos is None:
            pos = V2(0, 0)
        if vel is None:
            vel = V2(0, 0)
        self.pos = pos
        self.vel = vel
        self.limite_direito = LARGURA - self.tamanho.x

    def carrega_imagem(self):
        cls = type(self)
        if not cls in IMAGENS:
            # le imagem do disco!
            caminho = CAMINHO_IMAGENS / self.arq_imagem
            if caminho.exists():
                imagem = pygame.image.load(str(caminho))
                IMAGENS[cls] = pygame.transform.scale(
                    imagem,
                    (int(self.tamanho.x), int(self.tamanho.y))
                )

        self.imagem = IMAGENS.get(cls, None)


    x = property((lambda self: self.pos.x), (lambda self, valor: setattr(self.pos, "x", valor)))
    y = property((lambda self: self.pos.y), (lambda self, valor: setattr(self.pos, "y", valor)))

    def atualiza(self):
        pass

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.tamanho.x, self.tamanho.y)

    def atualiza(self):
        if self.jogo.tick % self.redutor == 0:
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
        if self.imagem:
            imagem = self.imagem.copy()
            imagem.fill(self.cor, special_flags=pygame.BLEND_ADD)
            self.jogo.tela.blit(imagem, self.get_rect())
        else:
            pygame.draw.rect(self.jogo.tela, self.cor, self.get_rect())

class Jogador(Objeto):
    vel_max = PASSO
    aceleracao = 2
    cores = [(255, 0, 0), (255, 255, 0), (255, 128, 0), (192, 128,0), (0, 255,0)]

    arq_imagem = "ship_h.png"
    max_energia = 100


    def __init__(self, jogo):
        super().__init__(jogo, pos=V2(0, ALTURA // 2))

        self.acel = V2(0,0)
        self.indice = 0
        self.energia = self.max_energia

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

        rect = self.get_rect()
        if rect.collidelist(self.jogo.chao) != -1:
            self.cor = (255, 0, 0)
            self.energia -= 1

        if self.energia == 0:
            raise JogadorMorreu()


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

    arq_imagem = "invader01_00.png"
    redutor = 4

    def __init__(self, jogo, pos):
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
        if self.x == 0:
            self.remove()

    def acertado(self, objeto):
        self.remove()

    def remove(self):
        self.jogo.inimigos.remove(self)


class Fase:
    comprimento = LARGURA * 10
    velocidade = 10
    max_inimigos = 6
    def __init__(self, jogo):
        self.jogo = jogo
        self.cor = (255, 255, 255)
        self.pos = 0
        desnivel_max = 2 * TAMANHO
        self.data = []
        ultima_altura = 0
        altura_maxima = ALTURA * 0.75
        for x in range(0, self.comprimento, TAMANHO):
            altura = ultima_altura + random.randrange(
                -desnivel_max, desnivel_max + TAMANHO, TAMANHO)
            if altura < 0:
                altura = 0
            if altura >= altura_maxima:
                altura = altura_maxima
            self.data.append(altura)
            ultima_altura = altura

    def add_inimigos(self):
        if len(self.jogo.inimigos) >= self.max_inimigos:
            return
        if random.random() < 1 / 15:
            inimigo = Inimigo(self.jogo, pos=V2(LARGURA, random.randrange(0, ALTURA, TAMANHO)))
            self.jogo.inimigos.append(inimigo)

class Jogo:

    def __init__(self):

        self.tela = pygame.display.set_mode((LARGURA, ALTURA))

    def principal(self):


        self.jogador = Jogador(self)
        self.inimigos = []

        self.tiros = []
        self.chao = []

        executando = True
        self.tick = 0
        self.fase = Fase(self)
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
            self.fase.add_inimigos()

            self.desenha_fundo()

            self.jogador.desenha()
            for inimigo in self.inimigos:
                inimigo.desenha()

            for tiro in self.tiros:
                tiro.desenha()

            pygame.display.flip()
            pygame.time.delay(DELAY)
            self.tick += 1

    def desenha_fundo(self):
        self.tela.fill((0, 0, 0))
        blocos_por_tela = LARGURA // TAMANHO
        pos_x = self.tick // self.fase.velocidade
        self.chao = []
        for x in range(pos_x, blocos_por_tela + pos_x):
            altura_bloco = self.fase.data[x]
            esquerda_bloco = (x - pos_x) * TAMANHO

            bloco_de_chao = pygame.Rect(
                esquerda_bloco,
                ALTURA - altura_bloco,
                TAMANHO, altura_bloco
            )
            self.chao.append(bloco_de_chao)
            pygame.draw.rect(
                self.tela,
                self.fase.cor,
                bloco_de_chao
            )



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
