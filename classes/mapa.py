import pygame
from pathlib import Path
from constants import LARGURA, ALTURA

class Mapa:
    def __init__(self):
        base_pasta = Path(__file__).resolve().parent.parent
        caminho_mapa = base_pasta / "assets" / "imagens" / "cenarios" / "mapa_cin.jpeg"
        caminho_folha = base_pasta / "assets" / "imagens" / "personagens" / "spritesheet_personagem_1.png"

        self.imagem = pygame.image.load(caminho_mapa).convert()
        self.largura = self.imagem.get_width()
        self.altura = self.imagem.get_height()

        self.ponto_inicial = (560, 690)#onde o jogador
        self.area_andavel = pygame.Rect(40, 40, self.largura - 80, 670)#por onde ele pode andar

        self.linhas = {"down": 0, "right": 1, "up": 2, "left": 3}#cada direcao na folha de sprites

        self.altura_sprite = 64
        self.frames_fem = self.carregar_folha(caminho_folha)
        self.frame_atual = 0.0

    def carregar_folha(self, caminho): #a folha tem 4 linhas e 4 colunas
        if not caminho.exists():
            print("folha de sprites nao encontrada:", caminho)
            return None

        folha = pygame.image.load(caminho).convert_alpha()
        larg_cel = folha.get_width() // 4
        alt_cel = folha.get_height() // 4
        larg_sprite = int(self.altura_sprite * larg_cel / alt_cel)

        frames = []
        
        for linha in range(4):
            frames.append([])
            for coluna in range(4):
                area = pygame.Rect(coluna * larg_cel, linha * alt_cel, larg_cel, alt_cel)
                frame = folha.subsurface(area).copy()
                frame = pygame.transform.scale(frame, (larg_sprite, self.altura_sprite))
                frames[linha].append(frame)
        return frames

    def atualizar(self, jogador):#ficar na area andavel
        if jogador.player_x < self.area_andavel.left:
            jogador.player_x = self.area_andavel.left

        if jogador.player_x > self.area_andavel.right:
            jogador.player_x = self.area_andavel.right

        if jogador.player_y < self.area_andavel.top:
            jogador.player_y = self.area_andavel.top

        if jogador.player_y > self.area_andavel.bottom:
            jogador.player_y = self.area_andavel.bottom
        
        if jogador.x_direction != 0 or jogador.y_direction != 0:#anima so quando anda
            self.frame_atual += 0.15
            if self.frame_atual >= 4:
                self.frame_atual = 0.0
        else:
            self.frame_atual = 0.0

    def camera(self, jogador):
        cam_x = int(jogador.player_x) - LARGURA // 2
        cam_y = int(jogador.player_y) - ALTURA // 2

        cam_x = max(0, min(cam_x, self.largura - LARGURA))
        cam_y = max(0, min(cam_y, self.altura - ALTURA))
        return cam_x, cam_y

    def desenhar(self, tela, jogador):
        cam_x, cam_y = self.camera(jogador)
        tela.blit(self.imagem, (-cam_x, -cam_y))

        pos_x = int(jogador.player_x) - cam_x

        pos_y = int(jogador.player_y) - cam_y

        direcao = "down"#direcao so depois da primeira tecla, enquant isso a personagem fica de frente
        if hasattr(jogador, "direction"):
            direcao = jogador.direction

        if jogador.genero == "feminino" and self.frames_fem != None:
            imagem = self.frames_fem[self.linhas[direcao]][int(self.frame_atual)]
            tela.blit(imagem, imagem.get_rect(midbottom=(pos_x, pos_y)))
        else:
            #quadrado provisorio p o personagem masculino
            quadrado = pygame.Rect(0, 0, 40, self.altura_sprite)
            quadrado.midbottom = (pos_x, pos_y)
            pygame.draw.rect(tela, (75, 145, 220), quadrado, border_radius=6)