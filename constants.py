LARGURA = 960
ALTURA = 640
FPS = 60

COR_FUNDO_CAIXA = (20, 22, 32)
COR_BORDA_CAIXA = (245, 245, 245)
COR_TITULO = (255, 220, 110)
COR_TEXTO = (245, 245, 245)
COR_VERDE_ACAO = (130, 235, 150)

#paginas sequenciais do guia (usadas no menu de pausa / ajuda)
PAGINAS_AJUDA = [
    {
        "titulo": "OBJETIVO",
        "texto": (
            "Recupere a maleta do Prof. Byte na Parada de Ônibus, capture CInMons pelo mapa, "
            "vença Raissa no Bloco E e derrote Lyoda no Grad 5!"
        ),
    },
    {
        "titulo": "CONTROLES",
        "texto": "", #desenhado dinamicamente pela funcao desenhar_pagina_controles
    },
    {
        "titulo": "COLA DE VANTAGENS",
        "texto": (
            "Lógica > Hardware > Rede\n"
            "Rede > Lógica\n"
            "Use a vantagem para dano extra!"
        ),
    },
]

#mapa epersonagem
PONTO_INICIAL = (560, 690)
ALTURA_SPRITE = 64
VELOCIDADE_ANIMACAO = 0.15

#cards da selecao de personagem
TAM_CARD = 100
TAM_IMG = 112