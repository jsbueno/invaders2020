import pygame

tela = pygame.display.set_mode((640, 480))

cores = [(255, 0, 0), (255, 255, 0), (255, 128, 0), (192, 128,0), (0, 255,0)]

executando = True

indice = 0

x = 0

while executando:

    cor = cores[indice]
    indice = indice + 1

    if indice >= len(cores):
        indice = 0

    x = x + 20
    if x >= 640:
         x = 0

    tela.fill((0, 0, 0))
    pygame.draw.rect(tela, cor, (x, 50, 200, 200))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            executando = False

    pygame.time.delay(50)
