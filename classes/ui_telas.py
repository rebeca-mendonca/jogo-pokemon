import pygame
from pathlib import Path
from constants import (
    LARGURA,
    ALTURA,
    COR_FUNDO_CAIXA,
    COR_BORDA_CAIXA,
    COR_TITULO,
    COR_TEXTO,
    COR_VERDE_ACAO,
    PAGINAS_AJUDA,
)
from utils.helpers import desenhar_texto_quebrado, desenhar_pagina_controles


class GerenciadorTelas:
    def __init__(self):
        base_pasta = Path(__file__).resolve().parent.parent
        caminho_tela_inicial = base_pasta / "assets" / "imagens" / "cenarios" / "tela_inicial.png"
        caminho_placa = base_pasta / "assets" / "imagens" / "cenarios" / "Placa_cin.png"

        self.fundo_titulo = pygame.image.load(caminho_tela_inicial).convert()
        self.fundo_titulo = pygame.transform.scale(self.fundo_titulo, (LARGURA, ALTURA))

        self.fundo_placa = pygame.image.load(caminho_placa).convert()
        self.fundo_placa = pygame.transform.scale(self.fundo_placa, (LARGURA, ALTURA))

        #fontes
        self.fonte_botao = pygame.font.Font(None, 48)
        self.fonte_creditos = pygame.font.Font(None, 36)
        self.fonte_esc = pygame.font.Font(None, 26)
        self.fonte_titulo_caixa = pygame.font.Font(None, 34)
        self.fonte_texto_caixa = pygame.font.Font(None, 27)
        self.fonte_tecla = pygame.font.Font(None, 18)
        self.fonte_nav = pygame.font.Font(None, 30)

        #botoes da tela inicial e placa
        self.botao_jogar = pygame.Rect(0, 0, 220, 60)
        self.botao_jogar.center = (LARGURA // 2, 336)

        self.botao_voltar = pygame.Rect(LARGURA - 145, ALTURA - 42, 130, 28)

        #botao temporario de batalha na placa (mateus)
        self.botao_batalha = pygame.Rect(0, 0, 180, 50)
        self.botao_batalha.center = (LARGURA // 2, 460)

        self.texto_creditos = self.fonte_creditos.render("@EC2026.2", True, (0, 0, 0))
        self.rect_creditos = self.texto_creditos.get_rect(center=(LARGURA // 2, 596))

        self.caixa_dialogo = pygame.Rect(278, 332, 404, 220)
        self.btn_voltar_pag = pygame.Rect(self.caixa_dialogo.left + 16, self.caixa_dialogo.bottom - 44, 68, 30)
        self.btn_avancar_pag = pygame.Rect(self.caixa_dialogo.right - 84, self.caixa_dialogo.bottom - 44, 68, 30)

        self.progresso_zoom = 0.0
        self.indice_guia = 0

    def iniciar_zoom(self):
        self.progresso_zoom = 0.0
        return "ZOOM_PLACA"

    def abrir_guia_pausa(self):
        self.indice_guia = 0
        return "GUIA_PAUSA"

    #eventos
    def eventos_tela_inicial(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.botao_jogar.collidepoint(evento.pos):
                return self.iniciar_zoom()

        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.iniciar_zoom()

        return "TELA_INICIAL"

    def eventos_placa_cin(self, evento):
        #ESC volta pra tela inicial
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.progresso_zoom = 0.0
            return "TELA_INICIAL"

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.botao_voltar.collidepoint(evento.pos):
                self.progresso_zoom = 0.0
                return "TELA_INICIAL"
            elif self.botao_batalha.collidepoint(evento.pos):
                return "ABRIR_BATALHA"

        return "PLACA_CIN"

    def eventos_guia_pausa(self, evento):
        ultima_pagina = len(PAGINAS_AJUDA) - 1

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.indice_guia > 0 and self.btn_voltar_pag.collidepoint(evento.pos):
                self.indice_guia -= 1
            elif self.indice_guia < ultima_pagina and self.btn_avancar_pag.collidepoint(evento.pos):
                self.indice_guia += 1

        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_LEFT, pygame.K_a) and self.indice_guia > 0:
                self.indice_guia -= 1
            elif evento.key in (pygame.K_RIGHT, pygame.K_d) and self.indice_guia < ultima_pagina:
                self.indice_guia += 1
            elif evento.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                return "MAPA" #ou "PAUSA" quando o menu de pausa completo estiver pronto

        return "GUIA_PAUSA"

    #desenho
    def desenhar_tela_inicial(self, tela, pos_mouse):
        tela.blit(self.fundo_titulo, (0, 0))

        mouse_em_cima = self.botao_jogar.collidepoint(pos_mouse)
        cor_fundo = (225, 65, 50) if mouse_em_cima else (180, 35, 35)
        cor_borda = (255, 220, 120) if mouse_em_cima else (255, 255, 255)

        pygame.draw.rect(tela, cor_fundo, self.botao_jogar, border_radius=10)
        pygame.draw.rect(tela, cor_borda, self.botao_jogar, width=3, border_radius=10)

        texto_jogar = self.fonte_botao.render("JOGAR", True, (255, 255, 255))
        tela.blit(texto_jogar, texto_jogar.get_rect(center=self.botao_jogar.center))
        tela.blit(self.texto_creditos, self.rect_creditos)

    def desenhar_zoom_placa(self, tela):
        self.progresso_zoom = min(1.0, self.progresso_zoom + 0.025)
        t = self.progresso_zoom * self.progresso_zoom * (3 - 2 * self.progresso_zoom)

        escala = 1.0 + 2.6 * t
        fundo_ampliado = pygame.transform.scale(
            self.fundo_titulo, (int(LARGURA * escala), int(ALTURA * escala))
        )
        pos_x = int(t * (LARGURA // 2 - 140 * escala))
        pos_y = int(t * (ALTURA // 2 - 396 * escala))
        tela.blit(fundo_ampliado, (pos_x, pos_y))

        if self.progresso_zoom > 0.45:
            alpha = int(((self.progresso_zoom - 0.45) / 0.55) * 255)
            self.fundo_placa.set_alpha(alpha)
            tela.blit(self.fundo_placa, (0, 0))

        if self.progresso_zoom >= 1.0:
            self.fundo_placa.set_alpha(255)
            return "PLACA_CIN"

        return "ZOOM_PLACA"

    def desenhar_placa_cin(self, tela, pos_mouse):
        tela.blit(self.fundo_placa, (0, 0))

        #botao voltar
        mouse_em_cima = self.botao_voltar.collidepoint(pos_mouse)
        cor_fundo = (225, 65, 50) if mouse_em_cima else (20, 20, 25)
        cor_borda = (255, 220, 120) if mouse_em_cima else (255, 255, 255)

        pygame.draw.rect(tela, cor_fundo, self.botao_voltar, border_radius=6)
        pygame.draw.rect(tela, cor_borda, self.botao_voltar, width=2, border_radius=6)
        texto_esc = self.fonte_esc.render("ESC - Voltar", True, (255, 255, 255))
        tela.blit(texto_esc, texto_esc.get_rect(center=self.botao_voltar.center))

        #botao batalha(temporario do Mateus)
        mouse_batalha = self.botao_batalha.collidepoint(pos_mouse)
        cor_f_bat = (225, 65, 50) if mouse_batalha else (180, 35, 35)
        cor_b_bat = (255, 220, 120) if mouse_batalha else (255, 255, 255)

        pygame.draw.rect(tela, cor_f_bat, self.botao_batalha, border_radius=8)
        pygame.draw.rect(tela, cor_b_bat, self.botao_batalha, width=2, border_radius=8)
        texto_batalha = self.fonte_botao.render("BATALHA", True, (255, 255, 255))
        tela.blit(texto_batalha, texto_batalha.get_rect(center=self.botao_batalha.center))

    def desenhar_guia_pausa(self, tela, pos_mouse):
        pagina_atual = PAGINAS_AJUDA[self.indice_guia]
        ultima_pagina = len(PAGINAS_AJUDA) - 1

        pygame.draw.rect(tela, COR_FUNDO_CAIXA, self.caixa_dialogo, border_radius=10)
        pygame.draw.rect(tela, COR_BORDA_CAIXA, self.caixa_dialogo, width=2, border_radius=10)

        titulo_render = self.fonte_titulo_caixa.render(pagina_atual["titulo"], True, COR_TITULO)
        tela.blit(titulo_render, (self.caixa_dialogo.left + 16, self.caixa_dialogo.top + 14))

        pygame.draw.line(
            tela,
            (90, 95, 115),
            (self.caixa_dialogo.left + 16, self.caixa_dialogo.top + 44),
            (self.caixa_dialogo.right - 16, self.caixa_dialogo.top + 44),
            1,
        )

        area_texto = pygame.Rect(
            self.caixa_dialogo.left + 16,
            self.caixa_dialogo.top + 54,
            self.caixa_dialogo.width - 32,
            110,
        )
        if self.indice_guia == 1:
            desenhar_pagina_controles(tela, area_texto, self.fonte_texto_caixa, self.fonte_tecla)
        else:
            desenhar_texto_quebrado(tela, pagina_atual["texto"], self.fonte_texto_caixa, COR_TEXTO, area_texto)

        if self.indice_guia > 0:
            hover_v = self.btn_voltar_pag.collidepoint(pos_mouse)
            cor_v = (70, 75, 100) if hover_v else (40, 44, 62)
            pygame.draw.rect(tela, cor_v, self.btn_voltar_pag, border_radius=6)
            pygame.draw.rect(tela, (220, 220, 230), self.btn_voltar_pag, width=1, border_radius=6)
            txt_v = self.fonte_nav.render("<<", True, (255, 255, 255))
            tela.blit(txt_v, txt_v.get_rect(center=self.btn_voltar_pag.center))

        if self.indice_guia < ultima_pagina:
            hover_a = self.btn_avancar_pag.collidepoint(pos_mouse)
            cor_a = (70, 75, 100) if hover_a else (40, 44, 62)
            pygame.draw.rect(tela, cor_a, self.btn_avancar_pag, border_radius=6)
            pygame.draw.rect(tela, (220, 220, 230), self.btn_avancar_pag, width=1, border_radius=6)
            txt_a = self.fonte_nav.render(">>", True, (255, 255, 255))
            tela.blit(txt_a, txt_a.get_rect(center=self.btn_avancar_pag.center))
        else:
            txt_enter = self.fonte_texto_caixa.render("ENTER: Voltar", True, COR_VERDE_ACAO)
            tela.blit(txt_enter, txt_enter.get_rect(midright=(self.caixa_dialogo.right - 16, self.btn_avancar_pag.centery)))