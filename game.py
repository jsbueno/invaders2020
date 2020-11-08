import pygame

TAMANHO = (640, 480)
tela = None

tamanho_nave = 64

x, y = TAMANHO[0] // 2, TAMANHO[1] - tamanho_nave

def inicio():
    global tela
    tela = pygame.display.set_mode(TAMANHO)

def atualiza(evento):
    global x, y
    if evento.key == pygame.K_LEFT:
        x -= tamanho_nave
    elif evento.key == pygame.K_RIGHT:
        x += tamanho_nave

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
            if evento.type == pygame.KEYDOWN:
                atualiza(evento)

        pygame.display.flip()
        pygame.event.pump()
        pygame.time.delay(30)

inicio()
principal()
pygame.quit()
