import pygame

TAMANHO = (800, 600)
LARGURA, ALTURA = TAMANHO
tela = None

TAMANHO_NAVE = 64


def inicio():
    global tela
    tela = pygame.display.set_mode(TAMANHO)


class Objeto:

    cor = (255, 255, 255)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tamanho = TAMANHO_NAVE

    def atualiza(self):
        pass

    def desenha(self):
        pygame.draw.rect(tela, self.cor, (self.x, self.y, self.tamanho, self.tamanho))


class Nave(Objeto):

    def atualiza(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.x -= self.tamanho // 2
        if teclas[pygame.K_RIGHT]:
            self.x += self.tamanho // 2
        if self.x < 0:
            self.x = 0
        elif self.x + self.tamanho > LARGURA:
            self.x = LARGURA - self.tamanho

class Inimigo(Objeto):

    cont = 0

    def atualiza(self):
        if self.cont % 4 == 0:
            self.x += self.tamanho // 2
            if self.x + self.tamanho > LARGURA:
                self.x = 0
        self.cont += 1


def principal():

    nave = Nave(x=LARGURA // 2, y=ALTURA - TAMANHO_NAVE)
    inimigo = Inimigo(x=0, y = TAMANHO_NAVE)

    fim_de_jogo = False

    while not fim_de_jogo:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                fim_de_jogo = True
            #if evento.type == pygame.KEYDOWN:
            #    atualiza(evento)
        nave.atualiza()
        inimigo.atualiza()

        tela.fill((0, 0, 0))

        nave.desenha()
        inimigo.desenha()

        pygame.display.flip()
        pygame.event.pump()
        pygame.time.delay(30)

inicio()
principal()
pygame.quit()
