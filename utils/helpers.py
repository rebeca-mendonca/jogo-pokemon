import pygame
from constants import COR_TITULO, COR_TEXTO

def desenhar_texto_quebrado(superficie, texto, fonte, cor, rect_area, espaco_linha=6):
    y = rect_area.top
    for paragrafo in texto.split("\n"):
        palavras = paragrafo.split(" ")
        linha_atual = ""
        for palavra in palavras:
            teste = f"{linha_atual}{palavra} "
            if fonte.size(teste)[0] <= rect_area.width:
                linha_atual = teste
            else:
                render = fonte.render(linha_atual.strip(), True, cor)
                superficie.blit(render, (rect_area.left, y))
                y += fonte.get_height() + espaco_linha
                linha_atual = f"{palavra} "
        if linha_atual.strip():
            render = fonte.render(linha_atual.strip(), True, cor)
            superficie.blit(render, (rect_area.left, y))
            y += fonte.get_height() + espaco_linha


def desenhar_tecla(superficie, rect, fonte_tecla, texto="", seta=None, pressionada=False):
    desloc = 2 if pressionada else 0
    cor_borda_inf = (180, 140, 40) if pressionada else (110, 115, 135)
    cor_fundo = (255, 220, 110) if pressionada else (235, 238, 245)
    cor_texto = (20, 22, 32)

    #base 3D da tecla
    pygame.draw.rect(superficie, cor_borda_inf, (rect.x, rect.y + 2, rect.width, rect.height), border_radius=4)
    #topo da tecla
    topo = pygame.Rect(rect.x, rect.y + desloc, rect.width, rect.height)
    pygame.draw.rect(superficie, cor_fundo, topo, border_radius=4)
    pygame.draw.rect(superficie, (40, 44, 62), topo, width=1, border_radius=4)

    if texto:
        render = fonte_tecla.render(texto, True, cor_texto)
        superficie.blit(render, render.get_rect(center=topo.center))
    elif seta:
        cx, cy = topo.center
        if seta == "UP":
            pts = [(cx, cy - 3), (cx - 4, cy + 3), (cx + 4, cy + 3)]
        elif seta == "DOWN":
            pts = [(cx, cy + 3), (cx - 4, cy - 3), (cx + 4, cy - 3)]
        elif seta == "LEFT":
            pts = [(cx - 3, cy), (cx + 3, cy - 4), (cx + 3, cy + 4)]
        elif seta == "RIGHT":
            pts = [(cx + 3, cy), (cx - 3, cy - 4), (cx - 3, cy + 4)]
        pygame.draw.polygon(superficie, cor_texto, pts)


def desenhar_pagina_controles(superficie, area, fonte_texto, fonte_tecla):
    #teclas pressionadas no momento para animar as ilustracoes
    teclas = pygame.key.get_pressed()
    x0, y0 = area.left, area.top

    #WASD + SETAS (Mover pelo mapa)
    desenhar_tecla(superficie, pygame.Rect(x0 + 18, y0, 16, 15), fonte_tecla, "W", pressionada=teclas[pygame.K_w])
    desenhar_tecla(superficie, pygame.Rect(x0, y0 + 17, 16, 15), fonte_tecla, "A", pressionada=teclas[pygame.K_a])
    desenhar_tecla(superficie, pygame.Rect(x0 + 18, y0 + 17, 16, 15), fonte_tecla, "S", pressionada=teclas[pygame.K_s])
    desenhar_tecla(superficie, pygame.Rect(x0 + 36, y0 + 17, 16, 15), fonte_tecla, "D", pressionada=teclas[pygame.K_d])

    mais1 = fonte_texto.render("+", True, COR_TITULO)
    superficie.blit(mais1, (x0 + 60, y0 + 10))

    desenhar_tecla(superficie, pygame.Rect(x0 + 94, y0, 16, 15), fonte_tecla, seta="UP", pressionada=teclas[pygame.K_UP])
    desenhar_tecla(superficie, pygame.Rect(x0 + 76, y0 + 17, 16, 15), fonte_tecla, seta="LEFT", pressionada=teclas[pygame.K_LEFT])
    desenhar_tecla(superficie, pygame.Rect(x0 + 94, y0 + 17, 16, 15), fonte_tecla, seta="DOWN", pressionada=teclas[pygame.K_DOWN])
    desenhar_tecla(superficie, pygame.Rect(x0 + 112, y0 + 17, 16, 15), fonte_tecla, seta="RIGHT", pressionada=teclas[pygame.K_RIGHT])

    lbl_mover = fonte_texto.render("Mover pelo mapa", True, COR_TEXTO)
    superficie.blit(lbl_mover, (x0 + 150, y0 + 10))

    y2 = y0 + 44
    desenhar_tecla(superficie, pygame.Rect(x0, y2, 54, 22), fonte_tecla, "ENTER", pressionada=teclas[pygame.K_RETURN])
    superficie.blit(mais1, (x0 + 60, y2 + 3))
    desenhar_tecla(superficie, pygame.Rect(x0 + 76, y2, 64, 22), fonte_tecla, "ESPAÇO", pressionada=teclas[pygame.K_SPACE])

    lbl_conf = fonte_texto.render("Confirmar", True, COR_TEXTO)
    superficie.blit(lbl_conf, (x0 + 150, y2 + 3))

    y3 = y0 + 78
    desenhar_tecla(superficie, pygame.Rect(x0, y3, 46, 22), fonte_tecla, "ESC", pressionada=teclas[pygame.K_ESCAPE])

    lbl_esc = fonte_texto.render("Pausar ou voltar", True, COR_TEXTO)
    superficie.blit(lbl_esc, (x0 + 150, y3 + 3))