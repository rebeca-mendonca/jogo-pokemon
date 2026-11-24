import pygame
import sys
import subprocess
import os

pygame.init()#inicializar o pygame

#configurações da tela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.SCALED)
pygame.display.set_caption("CInMons: Destino Cinistro")

clock = pygame.time.Clock()

#fundo de inicio e fundo da placa
fundo_titulo = pygame.image.load("assets/cenarios/tela_inicial.jpg").convert()
fundo_titulo = pygame.transform.scale(fundo_titulo, (LARGURA, ALTURA))

fundo_placa = pygame.image.load("assets/cenarios/Placa_cin.png").convert()
fundo_placa = pygame.transform.scale(fundo_placa, (LARGURA, ALTURA))

#botao, creditos e esc
fonte_botao = pygame.font.Font(None, 44)
fonte_creditos = pygame.font.Font(None, 32)
fonte_esc = pygame.font.Font(None, 26)

#botao jogar
botao_jogar = pygame.Rect(0, 0, 180, 50)
botao_jogar.center = (LARGURA // 2, 315)

#botao voltar da tela da placa
botao_voltar = pygame.Rect(LARGURA - 145, ALTURA - 42, 130, 28)

#botao batalha da tela da placa
botao_batalha = pygame.Rect(0, 0, 180, 50)
botao_batalha.center = (LARGURA // 2, 460)

#frase embaixo
texto_creditos = fonte_creditos.render("@EC2026.2", True, (0, 0, 0))
rect_creditos = texto_creditos.get_rect(center=( LARGURA // 2, 560))

estado_jogo = "TELA_INICIAL"
progresso_zoom = 0.0

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
                    progresso_zoom = 0.0
                    estado_jogo = "ZOOM_PLACA"

            #usando enter ou espaco tbm
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                    progresso_zoom = 0.0
                    estado_jogo = "ZOOM_PLACA"
        elif estado_jogo == "PLACA_CIN":
            #apertar ESC p a tela inicial
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    progresso_zoom = 0.0
                    estado_jogo = "TELA_INICIAL"

            #clique no botao de voltar
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao_voltar.collidepoint(evento.pos):
                    progresso_zoom = 0.0
                    estado_jogo = "TELA_INICIAL"
                elif botao_batalha.collidepoint(evento.pos):
                    pygame.display.quit()
                    try:
                        subprocess.run(
                            [sys.executable, os.path.join(os.path.dirname(__file__), "batalha.py")],
                            cwd=os.path.dirname(__file__)
                        )
                    finally:
                        pygame.display.init()
                        tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.SCALED)
                        pygame.display.set_caption("CInMons: Destino Cinistro")

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

    elif estado_jogo == "ZOOM_PLACA":
        progresso_zoom = min(1.0, progresso_zoom + 0.025) #aumentar prog a cada frame
        t = progresso_zoom * progresso_zoom * (3 - 2 * progresso_zoom) #suavizar começ e fim do movimento p trasncioar bonito

        #ampliando imagem inicial p placa do Cin que ta no lado esquerdo

        escala = 1.0 + 2.6 * t
        fundo_ampliado = pygame.transform.scale(fundo_titulo, (int(LARGURA * escala), int(ALTURA * escala)))
        pos_x = int(t * (LARGURA // 2 - 115 * escala))
        pos_y = int(t * (ALTURA // 2 - 370 * escala))
        tela.blit(fundo_ampliado, (pos_x, pos_y))

        if progresso_zoom > 0.45:
            alpha = int(((progresso_zoom - 0.45) / 0.55) * 255)
            fundo_placa.set_alpha(alpha)
            tela.blit(fundo_placa, (0, 0))

        if progresso_zoom >= 1.0:
            fundo_placa.set_alpha(255)
            estado_jogo = "PLACA_CIN"

    elif estado_jogo == "PLACA_CIN":
        tela.blit(fundo_placa, (0, 0))

        #botao voltar
        mouse_em_cima = botao_voltar.collidepoint(pos_mouse)
        cor_fundo = (225, 65, 50) if mouse_em_cima else (20, 20, 25)
        cor_borda = (255, 220, 120) if mouse_em_cima else (255, 255, 255)

        pygame.draw.rect(tela, cor_fundo, botao_voltar, border_radius=6)
        pygame.draw.rect(tela, cor_borda, botao_voltar, width=2, border_radius=6)

        texto_esc = fonte_esc.render("ESC - Voltar", True, (255, 255, 255))
        tela.blit(texto_esc, texto_esc.get_rect(center=botao_voltar.center))

        #botao batalha
        mouse_em_cima_batalha = botao_batalha.collidepoint(pos_mouse)
        cor_fundo_batalha = (225, 65, 50) if mouse_em_cima_batalha else (180, 35, 35)
        cor_borda_batalha = (255, 220, 120) if mouse_em_cima_batalha else (255, 255, 255)

        pygame.draw.rect(tela, cor_fundo_batalha, botao_batalha, border_radius=8)
        pygame.draw.rect(tela, cor_borda_batalha, botao_batalha, width=2, border_radius=8)

        texto_batalha = fonte_botao.render("BATALHA", True, (255, 255, 255))
        tela.blit(texto_batalha, texto_batalha.get_rect(center=botao_batalha.center))
        

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

    