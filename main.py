import pygame
import sys
import subprocess
import os
from constants import LARGURA, ALTURA, FPS
from classes.ui_telas import GerenciadorTelas
from classes.jogador import Jogador

pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.SCALED)
pygame.display.set_caption("CInMons: Destino Cinistro")
clock = pygame.time.Clock()

ui = GerenciadorTelas()
jogador = Jogador()
estado_jogo = "TELA_INICIAL"

rodando = True
while rodando:
    pos_mouse = pygame.mouse.get_pos()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if estado_jogo == "TELA_INICIAL":
            estado_jogo = ui.eventos_tela_inicial(evento)

        elif estado_jogo == "PLACA_CIN":
            estado_jogo = ui.eventos_placa_cin(evento)
            if estado_jogo == "HISTORIA_INICIAL":
                #salva nome e personagem escolhidos no objeto jogador
                jogador.nome = ui.nome_jogador
                jogador.genero = ui.personagem_escolhido

        elif estado_jogo == "HISTORIA_INICIAL":
            if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                estado_jogo = "MAPA"

        elif estado_jogo == "MAPA":
            jogador.movimento(evento)
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                estado_jogo = ui.abrir_guia_pausa()

        elif estado_jogo == "GUIA_PAUSA":
            estado_jogo = ui.eventos_guia_pausa(evento)

    #desenho das telas
    if estado_jogo == "TELA_INICIAL":
        ui.desenhar_tela_inicial(tela, pos_mouse)

    elif estado_jogo == "ZOOM_PLACA":
        estado_jogo = ui.desenhar_zoom_placa(tela)

    elif estado_jogo == "PLACA_CIN":
        ui.desenhar_placa_cin(tela, pos_mouse)

    #historia e mapa provisorios, até a amanda e a lara acrescentarem, quero apenas testar o confirmar e a pausa
    elif estado_jogo == "HISTORIA_INICIAL":
        tela.fill((20, 22, 32))
        txt1 = ui.fonte_titulo_caixa.render(f"Bem-vindo(a) ao CIn, {jogador.nome}!", True, (255, 220, 110))
        txt2 = ui.fonte_texto_caixa.render("Prof. Byte precisa da sua ajuda! (Pressione ENTER para ir ao mapa)", True, (245, 245, 245))
        tela.blit(txt1, txt1.get_rect(center=(LARGURA // 2, ALTURA // 2 - 20)))
        tela.blit(txt2, txt2.get_rect(center=(LARGURA // 2, ALTURA // 2 + 20)))

    elif estado_jogo == "MAPA":
        jogador.velocidade()
        tela.fill((30, 55, 40))
        jogador.draw_player(tela)

        hud = ui.fonte_texto_caixa.render(
            f"ESC: pausa e menu",
            True,
            (255, 255, 255),
        )
        tela.blit(hud, (20, 20))

    elif estado_jogo == "GUIA_PAUSA":
        tela.fill((30, 55, 40)) #fundo provisorio enquanto o mapa nao entra por baixo
        jogador.draw_player(tela)
        ui.desenhar_guia_pausa(tela, pos_mouse)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()