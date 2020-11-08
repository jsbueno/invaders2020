import pygame

TAMANHO = (640, 480)
tela = None

def inicio():
    global tela
    tela = pygame.display.set_mode(TAMANHO)

def desenha():
    pygame.draw.rect(tela, (0, 255, 0), (50, 50, 200, 150))

def principal():
    desenha()
    for i in range(100):
        pygame.event.pump()
        pygame.display.flip()
        pygame.time.delay(100)

inicio()
principal()
pygame.quit()
