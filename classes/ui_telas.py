import os
import pygame
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
        #imagens de fundo
        self.fundo_titulo = pygame.image.load("assets/imagens/cenarios/tela_inicial.png").convert()
        self.fundo_titulo = pygame.transform.scale(self.fundo_titulo, (LARGURA, ALTURA))

        self.fundo_placa = pygame.image.load("assets/imagens/cenarios/Placa_cin.png").convert()
        self.fundo_placa = pygame.transform.scale(self.fundo_placa, (LARGURA, ALTURA))

        #fontes
        self.fonte_botao = pygame.font.Font(None, 48)
        self.fonte_creditos = pygame.font.Font(None, 36)
        self.fonte_esc = pygame.font.Font(None, 26)
        self.fonte_titulo_caixa = pygame.font.Font(None, 34)
        self.fonte_texto_caixa = pygame.font.Font(None, 27)
        self.fonte_pequena = pygame.font.Font(None, 20)
        self.fonte_tecla = pygame.font.Font(None, 18)
        self.fonte_nav = pygame.font.Font(None, 30)

        #botoes principais
        self.botao_jogar = pygame.Rect(0, 0, 220, 60)
        self.botao_jogar.center = (LARGURA // 2, 336)

        self.botao_voltar = pygame.Rect(LARGURA - 145, ALTURA - 42, 130, 28)

        self.texto_creditos = self.fonte_creditos.render("@EC2026.2", True, (0, 0, 0))
        self.rect_creditos = self.texto_creditos.get_rect(center=(LARGURA // 2, 596))

        #caixa principal que fica dentro da placa
        self.caixa_dialogo = pygame.Rect(278, 332, 404, 220)

        #lista com os 3 personagens
        self.personagens = [
            {
                "id": "feminino",
                "sprite": self.carregar_imagem_personagem("assets/imagens/personagens/personagem_fem.png"),
                "cor_placeholder": (215, 95, 130),
            },
            {
                "id": "masculino",
                "sprite": self.carregar_imagem_personagem("assets/imagens/personagens/personagem_masc.png"),
                "cor_placeholder": (75, 145, 220),
            },
            {
                "id": "neutro",
                "sprite": self.carregar_imagem_personagem("assets/imagens/personagens/personagem_neutro.png"),
                "cor_placeholder": (145, 110, 215),
            },
        ]

        self.indice_personagem = 0
        self.personagem_escolhido = None

        #criando os 3 quadrados lado a lado
        self.cards_personagem = []
        larg_card = 88
        alt_card = 88
        espaco = 26
        inicio_x = self.caixa_dialogo.left + (self.caixa_dialogo.width - (3 * larg_card + 2 * espaco)) // 2
        y_cards = self.caixa_dialogo.top + 48

        for i in range(3):
            x = inicio_x + i * (larg_card + espaco)
            quadrado = pygame.Rect(x, y_cards, larg_card, alt_card)
            self.cards_personagem.append(quadrado)

        #campo de digitar o nome e botao confirmar
        self.nome_jogador = ""
        self.input_nome_ativo = True
        self.rect_input_nome = pygame.Rect(self.caixa_dialogo.left + 20, self.caixa_dialogo.bottom - 66, 220, 32)
        self.btn_confirmar_pers = pygame.Rect(self.caixa_dialogo.right - 144, self.caixa_dialogo.bottom - 66, 124, 32)

        #botoes das setas do guia da pausa
        self.btn_voltar_pag = pygame.Rect(self.caixa_dialogo.left + 16, self.caixa_dialogo.bottom - 44, 68, 30)
        self.btn_avancar_pag = pygame.Rect(self.caixa_dialogo.right - 84, self.caixa_dialogo.bottom - 44, 68, 30)

        self.progresso_zoom = 0.0
        self.indice_guia = 0

    def carregar_imagem_personagem(self, caminho):
        #verifica se o arquivo existe antes de tentar abrir
        if not os.path.exists(caminho):
            return None
        img = pygame.image.load(caminho).convert_alpha()
        larg, alt = img.get_size()
        #se for spritesheet pega so o primeiro quadradinho
        if larg >= 64 and alt >= 64:
            frame = img.subsurface((0, 0, larg // 4, alt // 4))
        else:
            frame = img
        return pygame.transform.scale(frame, (80, 80))

    def iniciar_zoom(self):
        self.progresso_zoom = 0.0
        return "ZOOM_PLACA"

    def abrir_guia_pausa(self):
        self.indice_guia = 0
        return "GUIA_PAUSA"

    def confirmar_selecao(self):
        nome_limpo = self.nome_jogador.strip()
        if nome_limpo == "":
            return "PLACA_CIN" #nao deixa avancar sem nome
        self.personagem_escolhido = self.personagens[self.indice_personagem]["id"]
        self.nome_jogador = nome_limpo
        return "HISTORIA_INICIAL"

    def eventos_tela_inicial(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.botao_jogar.collidepoint(evento.pos):
                return self.iniciar_zoom()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
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

            for i in range(len(self.cards_personagem)):
                if self.cards_personagem[i].collidepoint(evento.pos):
                    self.indice_personagem = i

            if self.rect_input_nome.collidepoint(evento.pos):
                self.input_nome_ativo = True
            else:
                self.input_nome_ativo = False

            if self.btn_confirmar_pers.collidepoint(evento.pos):
                return self.confirmar_selecao()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                self.indice_personagem = (self.indice_personagem - 1) % len(self.personagens)
            elif evento.key == pygame.K_RIGHT:
                self.indice_personagem = (self.indice_personagem + 1) % len(self.personagens)
            elif evento.key == pygame.K_RETURN:
                return self.confirmar_selecao()
            elif self.input_nome_ativo:
                if evento.key == pygame.K_BACKSPACE:
                    self.nome_jogador = self.nome_jogador[:-1]
                elif len(self.nome_jogador) < 12 and evento.unicode.isprintable() and evento.unicode != "":
                    self.nome_jogador += evento.unicode

        return "PLACA_CIN"

    def eventos_guia_pausa(self, evento):
        ultima_pagina = len(PAGINAS_AJUDA) - 1

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.indice_guia > 0 and self.btn_voltar_pag.collidepoint(evento.pos):
                self.indice_guia -= 1
            elif self.indice_guia < ultima_pagina and self.btn_avancar_pag.collidepoint(evento.pos):
                self.indice_guia += 1

        if evento.type == pygame.KEYDOWN:
            if (evento.key == pygame.K_LEFT or evento.key == pygame.K_a) and self.indice_guia > 0:
                self.indice_guia -= 1
            elif (evento.key == pygame.K_RIGHT or evento.key == pygame.K_d) and self.indice_guia < ultima_pagina:
                self.indice_guia += 1
            elif evento.key == pygame.K_RETURN or evento.key == pygame.K_ESCAPE:
                return "MAPA"

        return "GUIA_PAUSA"

    def desenhar_tela_inicial(self, tela, pos_mouse):
        tela.blit(self.fundo_titulo, (0, 0))

        mouse_em_cima = self.botao_jogar.collidepoint(pos_mouse)
        if mouse_em_cima:
            cor_fundo = (225, 65, 50)
            cor_borda = (255, 220, 120)
        else:
            cor_fundo = (180, 35, 35)
            cor_borda = (255, 255, 255)

        pygame.draw.rect(tela, cor_fundo, self.botao_jogar, border_radius=10)
        pygame.draw.rect(tela, cor_borda, self.botao_jogar, width=3, border_radius=10)

        texto_jogar = self.fonte_botao.render("JOGAR", True, (255, 255, 255))
        tela.blit(texto_jogar, texto_jogar.get_rect(center=self.botao_jogar.center))
        tela.blit(self.texto_creditos, self.rect_creditos)

    def desenhar_zoom_placa(self, tela):
        self.progresso_zoom += 0.025
        if self.progresso_zoom > 1.0:
            self.progresso_zoom = 1.0

        t = self.progresso_zoom * self.progresso_zoom * (3 - 2 * self.progresso_zoom)

        escala = 1.0 + 2.6 * t
        fundo_ampliado = pygame.transform.scale(self.fundo_titulo, (int(LARGURA * escala), int(ALTURA * escala)))
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

        pygame.draw.rect(tela, COR_FUNDO_CAIXA, self.caixa_dialogo, border_radius=10)
        pygame.draw.rect(tela, COR_BORDA_CAIXA, self.caixa_dialogo, width=2, border_radius=10)

        titulo = self.fonte_titulo_caixa.render("ESCOLHA SEU PERSONAGEM", True, COR_TITULO)
        tela.blit(titulo, titulo.get_rect(centerx=self.caixa_dialogo.centerx, top=self.caixa_dialogo.top + 12))

        for i in range(len(self.personagens)):
            pers = self.personagens[i]
            card = self.cards_personagem[i]
            selecionado = (i == self.indice_personagem)
            hover = card.collidepoint(pos_mouse)

            #muda cor de fundo e borda ao passar o mouse ou selecionar
            if selecionado:
                cor_card = (52, 60, 88)
                cor_borda = COR_TITULO
                espessura = 3
            elif hover:
                cor_card = (42, 48, 70)
                cor_borda = (220, 225, 240)
                espessura = 2
            else:
                cor_card = (26, 30, 44)
                cor_borda = (85, 92, 115)
                espessura = 1

            pygame.draw.rect(tela, cor_card, card, border_radius=8)
            pygame.draw.rect(tela, cor_borda, card, width=espessura, border_radius=8)

            #espaco onde vai ficar a imagem da Lara
            if pers["sprite"] != None:
                tela.blit(pers["sprite"], pers["sprite"].get_rect(center=card.center))
            else:
                txt_img = self.fonte_pequena.render("IMG", True, pers["cor_placeholder"])
                tela.blit(txt_img, txt_img.get_rect(center=card.center))

        #campo de digitar o nome
        if self.input_nome_ativo:
            cor_borda_input = COR_TITULO
        else:
            cor_borda_input = (110, 115, 135)

        pygame.draw.rect(tela, (14, 16, 24), self.rect_input_nome, border_radius=6)
        pygame.draw.rect(tela, cor_borda_input, self.rect_input_nome, width=2, border_radius=6)

        #cursor piscando
        if self.input_nome_ativo and (pygame.time.get_ticks() // 500) % 2 == 0:
            cursor = "|"
        else:
            cursor = ""

        if self.nome_jogador != "":
            txt_input = self.fonte_texto_caixa.render(self.nome_jogador + cursor, True, (255, 255, 255))
        else:
            txt_input = self.fonte_pequena.render("Digite seu nome..." + cursor, True, (130, 135, 155))
        tela.blit(txt_input, txt_input.get_rect(midleft=(self.rect_input_nome.left + 8, self.rect_input_nome.centery)))

        #botao confirmar (fica verde quando tem nome digitado)
        pode_confirmar = len(self.nome_jogador.strip()) > 0
        hover_conf = self.btn_confirmar_pers.collidepoint(pos_mouse)
        if pode_confirmar:
            if hover_conf:
                cor_f_conf = (55, 165, 85)
            else:
                cor_f_conf = (40, 130, 65)
            cor_b_conf = COR_VERDE_ACAO
            cor_txt_conf = (255, 255, 255)
        else:
            cor_f_conf = (55, 60, 75)
            cor_b_conf = (100, 105, 120)
            cor_txt_conf = (160, 165, 180)

        pygame.draw.rect(tela, cor_f_conf, self.btn_confirmar_pers, border_radius=6)
        pygame.draw.rect(tela, cor_b_conf, self.btn_confirmar_pers, width=2, border_radius=6)
        txt_conf = self.fonte_pequena.render("CONFIRMAR", True, cor_txt_conf)
        tela.blit(txt_conf, txt_conf.get_rect(center=self.btn_confirmar_pers.center))

        #dica no rodape da caixa
        dica = self.fonte_tecla.render("Setas/Clique: escolher | Digite o nome + ENTER", True, (165, 170, 190))
        tela.blit(dica, dica.get_rect(centerx=self.caixa_dialogo.centerx, bottom=self.caixa_dialogo.bottom - 10))

        #botao voltar
        mouse_em_cima = self.botao_voltar.collidepoint(pos_mouse)
        if mouse_em_cima:
            cor_fundo = (225, 65, 50)
            cor_borda = (255, 220, 120)
        else:
            cor_fundo = (20, 20, 25)
            cor_borda = (255, 255, 255)

        pygame.draw.rect(tela, cor_fundo, self.botao_voltar, border_radius=6)
        pygame.draw.rect(tela, cor_borda, self.botao_voltar, width=2, border_radius=6)
        texto_esc = self.fonte_esc.render("ESC - Voltar", True, (255, 255, 255))
        tela.blit(texto_esc, texto_esc.get_rect(center=self.botao_voltar.center))

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
            if self.btn_voltar_pag.collidepoint(pos_mouse):
                cor_v = (70, 75, 100)
            else:
                cor_v = (40, 44, 62)
            pygame.draw.rect(tela, cor_v, self.btn_voltar_pag, border_radius=6)
            pygame.draw.rect(tela, (220, 220, 230), self.btn_voltar_pag, width=1, border_radius=6)
            txt_v = self.fonte_nav.render("<<", True, (255, 255, 255))
            tela.blit(txt_v, txt_v.get_rect(center=self.btn_voltar_pag.center))

        if self.indice_guia < ultima_pagina:
            if self.btn_avancar_pag.collidepoint(pos_mouse):
                cor_a = (70, 75, 100)
            else:
                cor_a = (40, 44, 62)
            pygame.draw.rect(tela, cor_a, self.btn_avancar_pag, border_radius=6)
            pygame.draw.rect(tela, (220, 220, 230), self.btn_avancar_pag, width=1, border_radius=6)
            txt_a = self.fonte_nav.render(">>", True, (255, 255, 255))
            tela.blit(txt_a, txt_a.get_rect(center=self.btn_avancar_pag.center))
        else:
            txt_enter = self.fonte_texto_caixa.render("ENTER: Voltar", True, COR_VERDE_ACAO)
            tela.blit(txt_enter, txt_enter.get_rect(midright=(self.caixa_dialogo.right - 16, self.btn_avancar_pag.centery)))