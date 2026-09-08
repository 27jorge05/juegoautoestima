"""Burbujas de diálogo de criaturas, independientes de sus reglas."""

import pygame


def _ajustarTexto(texto, fuente, ancho):
    lineas, linea = [], ""
    for palabra in texto.split():
        candidata = f"{linea} {palabra}".strip()
        if linea and fuente.size(candidata)[0] > ancho:
            lineas.append(linea)
            linea = palabra
        else:
            linea = candidata
    return [*lineas, linea] if linea else lineas


def dibujarBurbujaDialogoCriatura(pantalla, fuente, texto, centroX, baseY):
    """Pinta una burbuja ovalada centrada sobre una criatura."""
    lineas = _ajustarTexto(texto, fuente, 250)
    anchoTexto = max(fuente.size(linea)[0] for linea in lineas)
    ancho, alto = anchoTexto + 34, len(lineas) * 24 + 30
    x = max(10, min(round(centroX - ancho / 2), pantalla.get_width() - ancho - 10))
    y = round(baseY - alto - 28)
    ovalo = pygame.Rect(x, y, ancho, alto)
    pygame.draw.ellipse(pantalla, (38, 26, 48), ovalo)
    pygame.draw.ellipse(pantalla, (246, 184, 117), ovalo, 2)
    pygame.draw.polygon(pantalla, (38, 26, 48), [(round(centroX) - 7, y + alto - 3), (round(centroX) + 8, y + alto - 3), (round(centroX), baseY - 7)])
    for indice, linea in enumerate(lineas):
        imagen = fuente.render(linea, True, (255, 220, 210))
        pantalla.blit(imagen, (x + (ancho - imagen.get_width()) // 2, y + 13 + indice * 24))
    return ovalo
