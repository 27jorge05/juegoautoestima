"""Traduce el estado de juego a una pose visual, sin depender de Pygame."""

from __future__ import annotations


def obtenerAnimacionRumi(
    velocidadX: float,
    velocidadY: float,
    estaEnSuelo: bool,
    garrasActivas: bool,
) -> str:
    if garrasActivas:
        return "garras"
    if not estaEnSuelo:
        return "saltar"
    if abs(velocidadX) > 1.0:
        return "correr"
    if velocidadY > 0:
        return "cansado"
    return "reposo"
