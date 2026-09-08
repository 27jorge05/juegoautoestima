"""Colocación de mosaicos de fondo sin depender de Pygame."""
import math


def posicionesMosaicos(camara, factor, anchoTile, anchoPantalla):
    if anchoTile <= 0:
        raise ValueError("El ancho del mosaico debe ser positivo")
    desplazamiento = camara * factor
    primero = math.floor(desplazamiento / anchoTile)
    cantidad = math.ceil(anchoPantalla / anchoTile) + 1
    return [(indice, round(indice * anchoTile - desplazamiento)) for indice in range(primero, primero + cantidad)]
