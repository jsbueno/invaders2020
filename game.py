import pygame

TAMANHO = (640, 480)
LARGURA, ALTURA = TAMANHO
tela = None

tamanho_nave = 64

x = LARGURA // 2
y = ALTURA - tamanho_nave

def inicio():
    global tela
    tela = pygame.display.set_mode(TAMANHO)

def atualiza():
    global x, y
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and x > 0:
        x -= tamanho_nave // 2
    if teclas[pygame.K_RIGHT] and x < (LARGURA - tamanho_nave):
        x += tamanho_nave // 2


def desenha():
    global x, y, tamanho_nave
    tela.fill((0, 0, 0))
    pygame.draw.rect(tela, (0, 255, 0), (x, y, tamanho_nave, tamanho_nave))

def principal():

    fim_de_jogo = False
    while not fim_de_jogo:
        desenha()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                fim_de_jogo = True
            #if evento.type == pygame.KEYDOWN:
            #    atualiza(evento)
        atualiza()
        pygame.display.flip()
        pygame.event.pump()
        pygame.time.delay(30)

inicio()
principal()
pygame.quit()
