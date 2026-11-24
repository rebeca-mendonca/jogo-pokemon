import pygame
import sys
import subprocess
import os
from constants import LARGURA, ALTURA, FPS
from classes.ui_telas import GerenciadorTelas

pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.SCALED)
pygame.display.set_caption("CInMons: Destino Cinistro")
clock = pygame.time.Clock()

ui = GerenciadorTelas()
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
            if estado_jogo == "ABRIR_BATALHA":
                pygame.display.quit()
                try:
                    caminho_batalha = os.path.join(os.path.dirname(__file__), "classes", "batalha.py")
                    subprocess.run([sys.executable, caminho_batalha], cwd=os.path.dirname(__file__))
                finally:
                    pygame.display.init()
                    tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.SCALED)
                    pygame.display.set_caption("CInMons: Destino Cinistro")
                    estado_jogo = "PLACA_CIN"

        elif estado_jogo == "GUIA_PAUSA":
            estado_jogo = ui.eventos_guia_pausa(evento)

    #desenho das telas
    if estado_jogo == "TELA_INICIAL":
        ui.desenhar_tela_inicial(tela, pos_mouse)

    elif estado_jogo == "ZOOM_PLACA":
        estado_jogo = ui.desenhar_zoom_placa(tela)

    elif estado_jogo == "PLACA_CIN":
        ui.desenhar_placa_cin(tela, pos_mouse)

    elif estado_jogo == "GUIA_PAUSA":
        tela.fill((30, 55, 40)) #fundo provisorio enquanto o mapa nao entra por baixo
        ui.desenhar_guia_pausa(tela, pos_mouse)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()