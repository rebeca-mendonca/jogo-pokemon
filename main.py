import pygame
import sys

pygame.init()#inicializar o pygame

#configurações da tela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.SCALED)
pygame.display.set_caption("CInMons: Destino Cinistro")

clock = pygame.time.Clock()

#fundo de inicio
fundo_titulo = pygame.image.load("assets/cenarios/tela_inicial.jpg").convert()
fundo_titulo = pygame.transform.scale(fundo_titulo, (LARGURA, ALTURA))

#botao
fonte_botao = pygame.font.Font(None, 44)
fonte_creditos = pygame.font.Font(None, 32)

#botao jogar
botao_jogar = pygame.Rect(0, 0, 180, 50)
botao_jogar.center = (LARGURA // 2, 315)

#frase em baixo
texto_creditos = fonte_creditos.render("@EC2026.2", True, (0, 0, 0))
rect_creditos = texto_creditos.get_rect(center=( LARGURA // 2, 560))

estado_jogo = "TELA_INICIAL"

#loop principal do jogo
rodando = True
while rodando:
    pos_mouse = pygame.mouse.get_pos()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if estado_jogo == "TELA_INICIAL":
            #clique no jogar (dps quero fazer passar o mouse em cima do jogar e mudar de cor)
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao_jogar.collidepoint(evento.pos):
                    estado_jogo = "PLACA_CIN"

            #usando enter ou espaco tbm
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                    estado_jogo = "PLACA_CIN"

    #desenho da tela
    if estado_jogo == "TELA_INICIAL":
        tela.blit(fundo_titulo, (0, 0))

        #passando o mouse e mudando o jogar
        mouse_em_cima = botao_jogar.collidepoint(pos_mouse)
        cor_fundo = (225, 65, 50) if mouse_em_cima else (180, 35, 35)
        cor_borda = (255, 220, 120) if mouse_em_cima else (255, 255, 255)

        pygame.draw.rect(tela, cor_fundo, botao_jogar, border_radius=8)
        pygame.draw.rect(tela, cor_borda, botao_jogar, width=2, border_radius=8)

        texto_jogar = fonte_botao.render("JOGAR", True, (255, 255, 255))
        rect_jogar = texto_jogar.get_rect(center=botao_jogar.center)
        tela.blit(texto_jogar, rect_jogar)

        #"@EC2026.2" em preto no gramado
        tela.blit(texto_creditos, rect_creditos)

    elif estado_jogo == "PLACA_CIN":
        tela.fill((25, 25, 35))
        aviso = fonte_botao.render("Tela da Placa do CIn", True, (255, 255, 255))
        tela.blit(aviso, aviso.get_rect(center=(120, 80)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

    