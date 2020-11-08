import pygame

TAMANHO = (800, 600)
LARGURA, ALTURA = TAMANHO
tela = None

TAMANHO_NAVE = 64



class Objeto:

    cor = (255, 255, 255)

    def __init__(self, x, y, jogo):
        self.x = x
        self.y = y
        self.largura = TAMANHO_NAVE
        self.altura = TAMANHO_NAVE
        self.jogo = jogo

    def atualiza(self):
        pass

    def desenha(self):
        pygame.draw.rect(self.jogo.tela, self.cor, (self.x, self.y, self.largura, self.altura))


class Nave(Objeto):
    cor = (0, 255, 0)
    def atualiza(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.x -= self.largura // 2
        if teclas[pygame.K_RIGHT]:
            self.x += self.largura // 2
        if self.x < 0:
            self.x = 0
        elif self.x + self.largura > LARGURA:
            self.x = LARGURA - self.largura


class Inimigo(Objeto):
    cor = (192, 0, 0)

    cont = 0

    def atualiza(self):
        if self.cont % 4 == 0:
            self.x += self.largura // 2
            if self.x + self.largura > LARGURA:
                self.x = 0
        self.cont += 1


class Jogo:

    def __init__(self):
        self.tela = pygame.display.set_mode(TAMANHO)

    def principal(self):

        self.nave = Nave(x=LARGURA // 2, y=ALTURA - TAMANHO_NAVE, jogo=self)
        self.inimigos = []
        self.tiros_da_nave = []
        self.tiros_inimigos = []

        total_inimigos = 7

        for i in range(total_inimigos):
            inimigo = Inimigo(
                x = i * (LARGURA / total_inimigos),
                y = TAMANHO_NAVE,
                jogo = self
            )
            self.inimigos.append(inimigo)

        fim_de_jogo = False

        while not fim_de_jogo:

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT or evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    fim_de_jogo = True
                #if evento.type == pygame.KEYDOWN:
                #    atualiza(evento)
            self.nave.atualiza()
            for inimigo in self.inimigos:
                inimigo.atualiza()

            self.tela.fill((0, 0, 0))

            self.nave.desenha()
            for inimigo in self.inimigos:
                inimigo.desenha()

            pygame.display.flip()
            pygame.event.pump()
            pygame.time.delay(30)

jogo = Jogo()

jogo.principal()

pygame.quit()
