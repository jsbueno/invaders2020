import random
from pathlib import Path

import pygame


MIDIAS = Path("media")

TAMANHO = (800, 600)
LARGURA, ALTURA = TAMANHO
TAMANHO_TEXTO = 64
ALTURA -= TAMANHO_TEXTO

tela = None

TAMANHO_NAVE = 64


class EventoDoJogo(BaseException):
    pass

class FimDeFase(EventoDoJogo):
    pass

class FimDeJogo(EventoDoJogo):
    pass

class JogadorMorreu(EventoDoJogo):
    pass

class Objeto:

    cor = (255, 255, 255)
    base_image = None
    arquivo_imagem = "NAO EXISTE"

    def __init__(self, x, y, jogo):
        self.x = x
        self.y = y
        self.largura = TAMANHO_NAVE
        self.altura = TAMANHO_NAVE
        self.jogo = jogo
        self.lista = []
        self.carrega_imagem()
        self.cont = 0

    def carrega_imagem(self):
        if self.__class__.__dict__.get("base_image"):
            self.image = self.__class__.base_image
            return

        caminho = MIDIAS / self.arquivo_imagem
        if not caminho.exists():
            self.image = None
            return
        print(f"Lendo do disco: {caminho}")
        imagem = pygame.image.load(str(caminho))
        self.image = pygame.transform.scale(imagem, (self.largura, self.altura))
        self.image.fill(self.cor, special_flags=pygame.BLEND_ADD)
        self.__class__.base_image = self.image
        miniatura = self.__class__.miniatura = pygame.transform.scale(imagem, (32, 32))
        miniatura.fill((255, 255, 255), special_flags=pygame.BLEND_ADD)

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.largura, self.altura)

    def atualiza(self):
        self.cont += 1

    def desenha(self):
        if not self.image:
            pygame.draw.rect(self.jogo.tela, self.cor, (self.x, self.y, self.largura, self.altura))
        else:
            self.jogo.tela.blit(self.image, self.rect)

    def acertado(self, forca):
        self.energia -= forca
        if self.energia <= 0:
            self.morrer()

    def morrer(self):
        try:
            self.lista.remove(self)
        except ValueError:
            pass


class Nave(Objeto):
    cor = (0, 255, 0)
    arquivo_imagem = "ship.png"
    max_energia = 4

    def __init__(self,jogo):
        x=LARGURA // 2
        y=ALTURA - TAMANHO_NAVE
        super().__init__(x, y, jogo)
        self.ultimo_tiro = 0
        self.tempo_entre_tiros = 30
        self.maximo_tiros = 3
        self.energia = self.max_energia

    def atualiza(self):
        super().atualiza()
        teclas = pygame.key.get_pressed()
        if self.cont % 2 != 0:
            return
        if teclas[pygame.K_LEFT]:
            self.x -= self.largura // 2
        if teclas[pygame.K_RIGHT]:
            self.x += self.largura // 2

        if teclas[pygame.K_SPACE]:

            if (
                not self.jogo.tiros_da_nave or
                (self.cont - self.ultimo_tiro) > self.tempo_entre_tiros and
                len(self.lista) < self.maximo_tiros
            ):
                tiro = TiroAmigo(self.x, self.y - self.altura, self.jogo)
                self.ultimo_tiro = self.cont

        if self.x < 0:
            self.x = 0
        elif self.x + self.largura > LARGURA:
            self.x = LARGURA - self.largura

    def morrer(self):
        raise JogadorMorreu()


class Inimigo(Objeto):
    cor = (192, 0, 0)
    forca_do_tiro = 1
    chance_de_tiro = .01
    tempo_entre_tiros = 50
    valor = 100
    energia = 1
    divisor_velocidade = 4

    arquivo_imagem = "invader01_00.png"

    def __init__(self, x, y, jogo):
        super().__init__(x, y, jogo)
        self.lista = jogo.inimigos
        self.max_voltas_na_mesma_linha = 2
        self.voltas_na_mesma_linha = 0

        self.ultimo_tiro = 0

    def atualiza(self):
        super().atualiza()
        if self.cont % self.divisor_velocidade == 0:
            self.x += self.largura // 2
            if self.x + self.largura > LARGURA:
                self.x = 0
                self.voltas_na_mesma_linha += 1
                if self.voltas_na_mesma_linha > self.max_voltas_na_mesma_linha:
                    self.y += self.altura
                    self.voltas_na_mesma_linha = 0

        if self.y + self.altura >= ALTURA:
            raise JogadorMorreu()

        if self.rect.colliderect(self.jogo.nave.rect):
            raise JogadorMorreu()

        if random.random() <= self.chance_de_tiro:
            self.tenta_atirar()

    def tenta_atirar(self):
        qtd = len(self.jogo.tiros_inimigos)
        if qtd >= 3: # self.jogo.fase.max_tiros_inimigos:
            return
        if (self.cont - self.ultimo_tiro) > self.tempo_entre_tiros:
                tiro = TiroInimigo(self.x, self.y + self.altura, self.jogo, self.forca_do_tiro)
                self.ultimo_tiro = self.cont

    def morrer(self):
        self.jogo.pontos += self.valor
        super().morrer()


class InimigoBoss(Inimigo):
    cor = (255, 192, 0)
    forca_do_tiro = 3
    chance_de_tiro = .05
    valor = 1000
    energia = 5
    divisor_velocidade = 8


class Tiro(Objeto):
    divisor_velocidade = 2

    def __init__(self, x, y, jogo):

        super().__init__(x, y, jogo)
        self.x += self.largura // 2 - self.largura // 16
        self.largura = self.largura // 8

    def adiciona_ao_jogo(self):
        self.lista.append(self)



class TiroAmigo(Tiro):

    def __init__(self, x, y, jogo):

        super().__init__(x, y, jogo)
        self.lista = self.jogo.tiros_da_nave
        self.adiciona_ao_jogo()


    def atualiza(self):
        super().atualiza()
        if not self.cont % self.divisor_velocidade:
            self.y -= self.altura // 2
        if self.y <= 0:
            self.morrer()
        for inimigo in self.jogo.inimigos:
            if self.rect.colliderect(inimigo.rect):
                inimigo.acertado(1)
                self.morrer()

class TiroInimigo(Tiro):
    cor = 255, 255, 212
    divisor_velocidade = 4

    def __init__(self, x, y, jogo, forca=1):
        super().__init__(x, y, jogo)
        self.lista = self.jogo.tiros_inimigos
        self.forca = forca
        self.adiciona_ao_jogo()


    def atualiza(self):
        super().atualiza()
        if not self.cont % self.divisor_velocidade:
            self.y += self.altura // 2
        if self.y >= ALTURA:
            self.morrer()
        if self.rect.colliderect(self.jogo.nave.rect):
            self.jogo.nave.acertado(self.forca)
            self.morrer()


class Jogo:

    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode(TAMANHO)
        self.fonte = pygame.font.Font(str(MIDIAS / "3270-Regular.ttf"), TAMANHO_TEXTO)

        self.pontos = 0
        self.fase = 0
        self.vidas = 3


    def principal(self):
        while True:
            self.inicializa_fase()
            try:
                while True:
                    self.laco_principal()
            except JogadorMorreu:
                print("Jogador morreu")
                self.vidas -= 1
                print(f"Vidas restantes: {self.vidas}")
                if self.vidas <= 0:
                    raise FimDeJogo()
            except FimDeFase:
                self.fase += 1

    def laco_principal(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                raise FimDeJogo()

        self.tela.fill((0, 0, 0))

        for elemento in self.inimigos + self.tiros_da_nave + self.tiros_inimigos:
            elemento.atualiza()
            elemento.desenha()
        self.nave.atualiza()
        self.nave.desenha()
        self.atualiza_informacoes()

        if not self.inimigos:
            raise FimDeFase()

        pygame.display.flip()
        pygame.event.pump()
        pygame.time.delay(30)


    def inicializa_fase (self):

        inimigos_por_fase = {
            0: 21,
            1: 28,
            2: 28,
            3: 35,
            4: 35,
            5: 42,
        }

        self.nave = Nave(jogo=self)
        self.inimigos = []
        self.tiros_da_nave = []
        self.tiros_inimigos = []

        try:
            total_inimigos = inimigos_por_fase[self.fase]
        except KeyError:
            print("Voce venceu a última fase - parabéns!")
            raise FimDeJogo()
        inimigos_por_linha = 7
        espaco_para_cada_nave = (LARGURA / inimigos_por_linha)

        for i in range(total_inimigos):
            linha_dos_inimigos = i // inimigos_por_linha

            x = (i % inimigos_por_linha) * espaco_para_cada_nave + (linha_dos_inimigos % 2) * (espaco_para_cada_nave // 2)

            y = TAMANHO_NAVE * (1 + linha_dos_inimigos)
            inimigo = Inimigo(x, y, jogo)
            self.inimigos.append(inimigo)

        if self.fase >= 1:
            self.inimigos.append(InimigoBoss(0, 0, jogo))

    def atualiza_informacoes(self):

        # pontos
        texto_pontos = self.fonte.render(f"{self.pontos:05d}", False, (0, 255,0))
        self.tela.blit(texto_pontos, (LARGURA - texto_pontos.get_width(), ALTURA))

        # Miniaturas com as vidas
        naves_vida = pygame.Surface((32 * self.vidas, 32))

        for i in range(self.vidas):
            naves_vida.blit(Nave.miniatura, (i * 32, 0))
        self.tela.blit(naves_vida, (0, ALTURA))

        # Barra de energia:
        esquerda = LARGURA // 4
        topo = ALTURA + 8
        largura = LARGURA // 4

        energia = self.nave.energia / self.nave.max_energia
        cor = (0, 255, 0) if energia > 0.6 else (255, 255, 0) if energia > 0.3 else (255, 0, 0)

        pygame.draw.rect(self.tela, cor, (esquerda, topo, int(energia * largura), TAMANHO_TEXTO // 2))
        pygame.draw.rect(self.tela, (255, 255, 255), (esquerda, topo, largura, TAMANHO_TEXTO // 2), width=3)


try:
    jogo = Jogo()
    jogo.principal()
except FimDeJogo:
    print(f"Jogo encerrado: total de pontos {jogo.pontos}")
finally:
    pygame.quit()
