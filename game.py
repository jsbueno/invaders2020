import pygame

TAMANHO = (800, 600)
LARGURA, ALTURA = TAMANHO
tela = None

tamanho_nave = 64

x = LARGURA // 2
y = ALTURA - tamanho_nave

x_i = 0
y_i = tamanho_nave
cont_i = 0

def inicio():
    global tela
    tela = pygame.display.set_mode(TAMANHO)

def atualiza():
    global x, y
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        x -= tamanho_nave // 2
    if teclas[pygame.K_RIGHT]:
        x += tamanho_nave // 2
    if x < 0:
        x = 0
    elif x + tamanho_nave > LARGURA:
        x = LARGURA - tamanho_nave

def desenha():
    pygame.draw.rect(tela, (0, 255, 0), (x, y, tamanho_nave, tamanho_nave))

def atualiza_i():
    global x_i, y_i, cont_i
    if cont_i % 4 == 0:
        x_i += tamanho_nave // 2
        if x_i + tamanho_nave > LARGURA:
            x_i = 0
    cont_i += 1

def desenha_i():
    pygame.draw.rect(tela, (192, 0, 0), (x_i, y_i, tamanho_nave, tamanho_nave))

def principal():

    fim_de_jogo = False
    while not fim_de_jogo:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                fim_de_jogo = True
            #if evento.type == pygame.KEYDOWN:
            #    atualiza(evento)
        atualiza()
        atualiza_i()
        tela.fill((0, 0, 0))
        desenha()
        desenha_i()

        pygame.display.flip()
        pygame.event.pump()
        pygame.time.delay(30)

inicio()
principal()
pygame.quit()
