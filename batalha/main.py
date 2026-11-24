import pygame
from pathlib import Path

pygame.init()
print("CINMON INICIOU!")

base_pasta = Path(__file__).resolve().parent.parent
assets = base_pasta / "assets" / "imagens"

charcara = pygame.image.load(assets / "cinmons" / "charcara_tras.png")
vampteuth = pygame.image.load(assets / "cinmons" / "vampteuth_frente.png")
fundo = pygame.image.load(assets / "background" / "background_batalha.png")
barra_status_adv = pygame.image.load(assets / "background" / "barras_status_adv.png")
barra_status_jgd = pygame.image.load(assets / "background" / "barras_status_jgd.png")
interface_batalha = pygame.image.load(assets / "background" / "interface_batalha.png")

fundo = pygame.transform.scale(fundo, (970, 550))
barra_status_adv = pygame.transform.scale(barra_status_adv, (500, 200))
barra_status_jgd = pygame.transform.scale(barra_status_jgd, (550, 200))

charcara = pygame.transform.scale(charcara, (600, 600))
vampteuth = pygame.transform.scale(vampteuth, (300, 300))

interface_batalha = pygame.transform.scale(interface_batalha, (970, 450)) 

print("Tamanho do Charcará:", charcara.get_size())
print("Tamanho do Vampteuth:", vampteuth.get_size())

LARGURA = 970
ALTURA = 550

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("CINMON")

relogio = pygame.time.Clock()

rodando = True

#hp
vampteuth_hp = 100
vampteuth_hp_max = 100

charcara_hp = 97
charcara_hp_max = 97

#qr
brasa_qr = 25
brasa_qr_max = 25

def cor_hp(hp, hp_max):
    porcentagem = hp / hp_max

    if porcentagem > 0.5:
        return (40, 190, 60)  # Verde
    elif porcentagem > 0.2:
        return (230, 190, 30)  # Amarelo
    else:
        return (210, 40, 40)  # Vermelho

fonte = pygame.font.Font(None, 40)
texto = fonte.render("O que Charcará vai fazer?", True, (255, 255, 255))

opcoes = [
    "LUTAR",
    "MOCHILA",
    "CINMON",
    "FUGIR"
]

textos_opcoes = []

for opcao in opcoes:
    texto_opcao = fonte.render(opcao, True, (0, 0, 0))
    textos_opcoes.append(texto_opcao)

selecao = 0

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            #movimento:
            if evento.key == pygame.K_d:
                selecao = min(3, selecao + 1)

            if evento.key == pygame.K_a:
                selecao = max(0, selecao - 1)

            if evento.key == pygame.K_s:
                selecao = min(3, selecao + 2)

            if evento.key == pygame.K_w:
                selecao = max(0, selecao - 2)

            #ataques
            if evento.key == pygame.K_1 and brasa_qr > 0:
                vampteuth_hp = max(0, vampteuth_hp - 15)
                brasa_qr -= 1

    tela.blit(fundo, (0, 0))
    largura_hp = 140 * (vampteuth_hp / vampteuth_hp_max)
    cor = cor_hp(vampteuth_hp, vampteuth_hp_max)

    largura_hp_charcara = 140 * (charcara_hp / charcara_hp_max)
    cor_charcara = cor_hp(charcara_hp, charcara_hp_max)

    pygame.draw.rect(tela, cor_charcara, (792, 330, largura_hp_charcara, 23))

    pygame.draw.rect(tela, cor, (105, 100, largura_hp, 23))
    
    tela.blit(barra_status_adv, (-10, -10))
    tela.blit(barra_status_jgd, (420, 250))
    
    tela.blit(charcara, (-50, 60))
    tela.blit(vampteuth, (580, -10))

    pygame.draw.rect(tela, (60, 60, 60), (0, 395, 980, 200))
    tela.blit(interface_batalha, (0, 105))
    tela.blit(texto, (40, 425))
    tela.blit(textos_opcoes[0], (630, 430))
    tela.blit(textos_opcoes[1], (780, 430))

    tela.blit(textos_opcoes[2], (630, 480))
    tela.blit(textos_opcoes[3], (780, 480))

    posicoes_seta = [
        (610, 438),  # LUTAR
        (760, 438),  # MOCHILA
        (610, 488),  # CINMON
        (760, 488)   # FUGIR
        ]

    x, y = posicoes_seta[selecao]

    pygame.draw.polygon(tela, (0, 0, 0), [
        (x, y),
        (x + 12, y + 7),
        (x, y + 14)
    ])
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()