import pygame

TAMANHO = (640, 480)

tela = pygame.display.set_mode(TAMANHO)


pygame.draw.rect(tela, (0, 255, 0), (50, 50, 200, 150))

pygame.display.flip()

for i in range(100):
    pygame.event.pump()
    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
