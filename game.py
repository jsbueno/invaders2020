import pygame

TAMANHO = (640, 480)
tela = None

def inicio():
    global tela
    tela = pygame.display.set_mode(TAMANHO)

def desenha():
    pygame.draw.rect(tela, (0, 255, 0), (50, 50, 200, 150))

def principal():

    fim_de_jogo = False
    while not fim_de_jogo:
        desenha()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                fim_de_jogo = True

        pygame.display.flip()
        pygame.event.pump()
        pygame.time.delay(30)

inicio()
principal()
pygame.quit()
