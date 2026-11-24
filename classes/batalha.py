import pygame
import random
from pathlib import Path

pygame.init()

LARGURA = 970
ALTURA = 550
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("CINMON")
relogio = pygame.time.Clock()

# --- 1. FUNÇÃO PARA SIMPLIFICAR CARREGAMENTO DE IMAGENS ---
def carregar_img(caminho, tamanho=None):
    img = pygame.image.load(caminho)
    if tamanho:
        img = pygame.transform.scale(img, tamanho)
    return img

# Carregando as imagens com a nova função
base_pasta = Path(__file__).resolve().parent.parent
assets = base_pasta / "assets" / "imagens"

fundo = carregar_img(assets / "background" / "background_batalha.png", (LARGURA, ALTURA))
barra_status_adv = carregar_img(assets / "background" / "barras_status_adv.png", (500, 200))
barra_status_jgd = carregar_img(assets / "background" / "barras_status_jgd.png", (550, 200))
interface_batalha = carregar_img(assets / "background" / "interface_batalha.png", (LARGURA, 450))
caixa_ataques = carregar_img(assets / "background" / "caixa_ataques.png", (990, 380))

tamanho_cinmon = (600, 600)
charcabras_frente = carregar_img(assets / "cinmons" / "charcabras_frente.png", tamanho_cinmon)
charcabras_tras = carregar_img(assets / "cinmons" / "charcabras_tras.png", tamanho_cinmon)
charcara_tras = carregar_img(assets / "cinmons" / "charcara_tras.png", tamanho_cinmon)
charcara_frente = carregar_img(assets / "cinmons" / "charcara_frente.png", tamanho_cinmon)

vampteuth_frente = carregar_img(assets / "cinmons" / "vampteuth_frente.png", (300, 300))
vampteuth_tras = carregar_img(assets / "cinmons" / "vampteuth_tras.png", (300, 300))

# --- 2. DADOS DO JOGO ---
fonte = pygame.font.Font(None, 40)
duracao_branco = 500
duracao_desaparecimento = 1000
duracao_impacto = 450

especies_cinmon = {
    "Charcabrás": {
        "tipo": "Fogo", "hp_base": 15,
        "sprite_jogador": charcabras_tras, "sprite_adversario": charcabras_frente,
        "ataques_aprendidos": {
            1: {"nome": "Brasa", "QR_max": 25, "dano": 15},
            5: {"nome": "Penas de Lava", "QR_max": 20, "dano": 20},
            10: {"nome": "Lança-chamas", "QR_max": 10, "dano": 30},
        }
    },
    "Charcará": {
        "tipo": "Fogo", "hp_base": 15,
        "sprite_jogador": charcara_tras, "sprite_adversario": charcara_frente,
        "ataques_aprendidos": {
            1: {"nome": "Brasa", "QR_max": 25, "dano": 15},
            5: {"nome": "Penas de Lava", "QR_max": 20, "dano": 20},
            10: {"nome": "Lança-chamas", "QR_max": 10, "dano": 30},
            25: {"nome": "Chute em Chamas", "QR_max": 5, "dano": 50}
        }
    },
    "Vampteuth": {
        "tipo": "Água", "hp_base": 17,
        "sprite_jogador": vampteuth_tras, "sprite_adversario": vampteuth_frente,
        "ataques_aprendidos": {
            1: {"nome": "Nuvem Paralisante", "QR_max": 25, "dano": 15},
            5: {"nome": "Bolhas de Energia", "QR_max": 20, "dano": 20},
            10: {"nome": "Jato d'Agua", "QR_max": 10, "dano": 30},
            25: {"nome": "Último Abraço", "QR_max": 5, "dano": 55}
        }
    }
}

# --- 3. FUNÇÕES AUXILIARES ---
def cor_hp(hp, hp_max):
    porcentagem = hp / hp_max
    if porcentagem > 0.5: return (40, 190, 60)   # Verde
    if porcentagem > 0.2: return (230, 190, 30)  # Amarelo
    return (210, 40, 40)                         # Vermelho

def efeito_derrota(sprite, tempo):
    sprite = sprite.copy()
    sprite.fill((214, 222, 226), special_flags=pygame.BLEND_RGB_MAX)
    if tempo > duracao_branco:
        progresso = (tempo - duracao_branco) / duracao_desaparecimento
        alpha = max(0, int(255 * (1 - progresso)))
        sprite.set_alpha(alpha)
    return sprite

def efeito_impacto(sprite, tempo):
    sprite = sprite.copy()
    if (tempo // 80) % 2 == 0:
        sprite.fill((180, 180, 180), special_flags=pygame.BLEND_RGB_ADD)
    return sprite

def ataques_disponiveis(especie, nivel):
    ataques = especies_cinmon[especie]["ataques_aprendidos"]
    return [dados for niv, dados in ataques.items() if nivel >= niv]

# config atual
especie_jogador = "Charcará"
nivel_jogador = 25
especie_adversario = "Vampteuth"
nivel_adversario = 25

# Setup Jogador
dados_ataques_jogador = ataques_disponiveis(especie_jogador, nivel_jogador)
ataques = [a["nome"] for a in dados_ataques_jogador]
qr_max = [a["QR_max"] for a in dados_ataques_jogador]
qr_ataques = qr_max.copy()
dano_ataques = [a["dano"] for a in dados_ataques_jogador]

cinmon_jogador = {
    "hp_max": round(especies_cinmon[especie_jogador]["hp_base"] + 3 * nivel_jogador),
    "hp": round(especies_cinmon[especie_jogador]["hp_base"] + 3 * nivel_jogador)
}
sprite_jogador = especies_cinmon[especie_jogador]["sprite_jogador"]

# Setup Adversário
dados_ataques_adversario = ataques_disponiveis(especie_adversario, nivel_adversario)
ataques_adversario = [a["nome"] for a in dados_ataques_adversario]
qr_adversario = [a["QR_max"] for a in dados_ataques_adversario]
dano_adversario = [a["dano"] for a in dados_ataques_adversario]

cinmon_adversario = {
    "hp_max": round(especies_cinmon[especie_adversario]["hp_base"] + 3 * nivel_adversario),
    "hp": round(especies_cinmon[especie_adversario]["hp_base"] + 3 * nivel_adversario)
}
sprite_adversario = especies_cinmon[especie_adversario]["sprite_adversario"]

# Textos pré-renderizados
textos_opcoes = [fonte.render(op, True, (0, 0, 0)) for op in ["LUTAR", "MOCHILA", "CINMON", "FUGIR"]]
textos_ataques = [fonte.render(atq, True, (0, 0, 0)) for atq in ataques]
texto_pergunta = fonte.render(f"O que {especie_jogador} vai fazer?", True, (255, 255, 255))

# Variáveis de Estado
selecao = 0
selecao_ataque = 0
tela_atual = "menu"
etapa_batalha = ""
mensagem_batalha = ""
tempo_mensagem = 0
cinmon_derrotado = None
inicio_derrota = 0
alvo_impacto = None
inicio_impacto = 0
rodando = True

areas_opcoes = [
    pygame.Rect(610, 415, 150, 45),
    pygame.Rect(760, 415, 150, 45),
    pygame.Rect(610, 465, 150, 45),
    pygame.Rect(760, 465, 150, 45),
]
areas_ataques = [
    pygame.Rect(30, 410, 280, 45),
    pygame.Rect(330, 410, 280, 45),
    pygame.Rect(30, 465, 280, 45),
    pygame.Rect(330, 465, 280, 45),
]

def ativar_opcao_menu():
    global tela_atual, selecao_ataque, mensagem_batalha, rodando

    if selecao == 0:
        tela_atual = "ataques"
        selecao_ataque = 0
    elif selecao == 1:
        mensagem_batalha = "Mochila *não implementado*"
        tela_atual = "mochila"
    elif selecao == 2:
        mensagem_batalha = "Cinmon *não implementado*"
        tela_atual = "cinmon"
    elif selecao == 3:
        rodando = False

def ativar_ataque():
    global mensagem_batalha, etapa_batalha, tela_atual, tempo_mensagem

    qr_ataques[selecao_ataque] -= 1
    mensagem_batalha = f"{especie_jogador} usou {ataques[selecao_ataque]}!"
    etapa_batalha = "ataque_jogador"
    tela_atual = "mensagem"
    tempo_mensagem = pygame.time.get_ticks()

def avancar_mensagem():
    global ataque_escolhido, mensagem_batalha, etapa_batalha, tempo_mensagem

    atqs_disponiveis = [i for i, qr in enumerate(qr_adversario) if qr > 0]
    if atqs_disponiveis:
        ataque_escolhido = random.choice(atqs_disponiveis)
        qr_adversario[ataque_escolhido] -= 1
        mensagem_batalha = f"{especie_adversario} usou {ataques_adversario[ataque_escolhido]}!"
        etapa_batalha = "ataque_adversario"
        tempo_mensagem = pygame.time.get_ticks()

# --- 5. LOOP PRINCIPAL ---
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            rodando = False

        elif evento.type == pygame.KEYDOWN:
            if tela_atual == "menu":
                if evento.key == pygame.K_d: selecao = min(3, selecao + 1)
                if evento.key == pygame.K_a: selecao = max(0, selecao - 1)
                if evento.key == pygame.K_s: selecao = min(3, selecao + 2)
                if evento.key == pygame.K_w: selecao = max(0, selecao - 2)

                if evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                    ativar_opcao_menu()

            elif tela_atual == "ataques":
                if evento.key == pygame.K_d and selecao_ataque % 2 == 0: selecao_ataque += 1
                if evento.key == pygame.K_a and selecao_ataque % 2 == 1: selecao_ataque -= 1
                if evento.key == pygame.K_s and selecao_ataque < 2: selecao_ataque += 2
                if evento.key == pygame.K_w and selecao_ataque >= 2: selecao_ataque -= 2
                
                if qr_ataques[selecao_ataque] > 0 and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                    ativar_ataque()

            elif tela_atual == "mensagem":
                if evento.key in (pygame.K_RETURN, pygame.K_SPACE) and etapa_batalha == "esperando_jogador":
                    avancar_mensagem()

            elif tela_atual == "mochila":
                if evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                    tela_atual = "menu"

            elif tela_atual == "cinmon":
                if evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                    tela_atual = "menu"

            elif tela_atual == "fim_batalha" and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                rodando = False

        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if tela_atual == "menu":
                for indice, area in enumerate(areas_opcoes):
                    if area.collidepoint(evento.pos):
                        selecao = indice
                        ativar_opcao_menu()
                        break
            elif tela_atual == "ataques":
                for indice, area in enumerate(areas_ataques):
                    if area.collidepoint(evento.pos):
                        selecao_ataque = indice
                        if qr_ataques[selecao_ataque] > 0:
                            ativar_ataque()
                        break
            elif tela_atual == "mensagem" and etapa_batalha == "esperando_jogador":
                avancar_mensagem()
            elif tela_atual in ("mochila", "cinmon"):
                tela_atual = "menu"
            elif tela_atual == "fim_batalha":
                rodando = False

    # Lógica de Tempo (Dano)
    if etapa_batalha == "ataque_jogador" and pygame.time.get_ticks() - tempo_mensagem >= 1000:
        cinmon_adversario["hp"] = max(0, cinmon_adversario["hp"] - dano_ataques[selecao_ataque])
        alvo_impacto = "adversario"
        inicio_impacto = pygame.time.get_ticks()
        if cinmon_adversario["hp"] == 0:
            mensagem_batalha = f"{especie_adversario} foi derrotado!"
            cinmon_derrotado, etapa_batalha = "adversario", "animacao_derrota"
            inicio_derrota = pygame.time.get_ticks()
            tela_atual = "fim_batalha"
        else:
            etapa_batalha = "esperando_jogador"

    elif etapa_batalha == "ataque_adversario" and pygame.time.get_ticks() - tempo_mensagem >= 1000:
        cinmon_jogador["hp"] = max(0, cinmon_jogador["hp"] - dano_adversario[ataque_escolhido])
        alvo_impacto = "jogador"
        inicio_impacto = pygame.time.get_ticks()
        if cinmon_jogador["hp"] == 0:
            mensagem_batalha = f"{especie_jogador} foi derrotado!"
            cinmon_derrotado, etapa_batalha = "jogador", "animacao_derrota"
            inicio_derrota = pygame.time.get_ticks()
            tela_atual = "fim_batalha"
        else:
            etapa_batalha = ""
            tela_atual = "menu"

    # --- RENDERIZAÇÃO ---
    tela.blit(fundo, (0, 0))

    # Barras de HP
    pygame.draw.rect(tela, cor_hp(cinmon_jogador["hp"], cinmon_jogador["hp_max"]), 
                     (792, 330, 140 * (cinmon_jogador["hp"] / cinmon_jogador["hp_max"]), 23))
    pygame.draw.rect(tela, cor_hp(cinmon_adversario["hp"], cinmon_adversario["hp_max"]), 
                     (105, 100, 140 * (cinmon_adversario["hp"] / cinmon_adversario["hp_max"]), 23))

    tela.blit(barra_status_adv, (-10, -10))
    tela.blit(barra_status_jgd, (420, 250))

    # Sprites
    tempo_derrota = pygame.time.get_ticks() - inicio_derrota
    tempo_impacto = pygame.time.get_ticks() - inicio_impacto
    impacto_ativo = alvo_impacto is not None and tempo_impacto < duracao_impacto
    
    if cinmon_derrotado == "jogador" and tempo_derrota < duracao_branco + duracao_desaparecimento:
        sprite_atual_jogador = efeito_derrota(sprite_jogador, tempo_derrota)
    else:
        sprite_atual_jogador = sprite_jogador
    pos_x_jogador = -50
    if impacto_ativo and alvo_impacto == "jogador":
        sprite_atual_jogador = efeito_impacto(sprite_atual_jogador, tempo_impacto)
        pos_x_jogador -= int(12 * (1 - tempo_impacto / duracao_impacto))
    if cinmon_derrotado != "jogador" or tempo_derrota < duracao_branco + duracao_desaparecimento:
        tela.blit(sprite_atual_jogador, (pos_x_jogador, 60))

    if cinmon_derrotado == "adversario" and tempo_derrota < duracao_branco + duracao_desaparecimento:
        sprite_atual_adversario = efeito_derrota(sprite_adversario, tempo_derrota)
    else:
        sprite_atual_adversario = sprite_adversario
    pos_x_adversario = 580
    if impacto_ativo and alvo_impacto == "adversario":
        sprite_atual_adversario = efeito_impacto(sprite_atual_adversario, tempo_impacto)
        pos_x_adversario += int(12 * (1 - tempo_impacto / duracao_impacto))
    if cinmon_derrotado != "adversario" or tempo_derrota < duracao_branco + duracao_desaparecimento:
        tela.blit(sprite_atual_adversario, (pos_x_adversario, -10))

    # --- INTERFACE INFERIOR ---
    if tela_atual in ["menu", "mensagem", "mochila", "cinmon", "fim_batalha"]:
        pygame.draw.rect(tela, (0, 0, 0), (0, 395, 990, 210))
        tela.blit(interface_batalha, (0, 105)) 
        
        if tela_atual == "menu":
            tela.blit(texto_pergunta, (40, 425))
            posicoes_txt = [(630, 430), (780, 430), (630, 480), (780, 480)]
            posicoes_seta = [(610, 438), (760, 438), (610, 488), (760, 488)]
            
            for i, txt in enumerate(textos_opcoes):
                tela.blit(txt, posicoes_txt[i])
            
            x, y = posicoes_seta[selecao]
            pygame.draw.polygon(tela, (0, 0, 0), [(x, y), (x + 12, y + 7), (x, y + 14)])

        else: # mensagem ou fim_batalha
            tela.blit(fonte.render(mensagem_batalha, True, (255, 255, 255)), (40, 425))

    elif tela_atual == "ataques":
        pygame.draw.rect(tela, (0, 0, 0), (0, 395, 990, 210))
        tela.blit(caixa_ataques, (-10, 210))
        posicoes_txt_atq = [(50, 425), (350, 425), (50, 480), (350, 480)]
        posicoes_seta_atq = [(30, 433), (330, 433), (30, 488), (330, 488)]
        
        for i, txt in enumerate(textos_ataques):
            tela.blit(txt, posicoes_txt_atq[i])
            
        x, y = posicoes_seta_atq[selecao_ataque]
        pygame.draw.polygon(tela, (0, 0, 0), [(x, y), (x + 12, y + 7), (x, y + 14)])

        tela.blit(fonte.render(f"QR: {qr_ataques[selecao_ataque]}/{qr_max[selecao_ataque]}", True, (0, 0, 0)), (730, 425))
        tela.blit(fonte.render(f"TIPO: {especies_cinmon[especie_jogador]['tipo'].upper()}", True, (0, 0, 0)), (730, 480))
    
    print("Rodando...")  # Debugging line to check if the loop is running
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
