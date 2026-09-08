"""Criaturas del Velo: reglas de acercamiento y liberación por luz."""
from dataclasses import dataclass
from enum import Enum, auto
from typing import Protocol
from .dominio import Vector2D


class TipoEnemigo(Enum):
    SUSURRO = auto()
    ESPEJILLA = auto()


class CriaturaNivel(Protocol):
    tipo: TipoEnemigo
    posicion: Vector2D

    @property
    def liberado(self) -> bool: ...

    def actualizar(self, rumi, deltaTiempo): ...


@dataclass
class EnemigoNivel:
    tipo: TipoEnemigo
    posicion: Vector2D
    liberado: bool = False
    radioLuz: float = 110.0

    def actualizar(self, rumi, deltaTiempo):
        if self.liberado:
            return
        dx = rumi.posicion.x - self.posicion.x
        dy = rumi.posicion.y - self.posicion.y
        distancia = (dx * dx + dy * dy) ** 0.5
        if rumi.garrasActivas and distancia <= self.radioLuz:
            self.liberado = True
            return
        if self.tipo == TipoEnemigo.SUSURRO:
            if 30 < distancia < 230:
                paso = min(abs(dx), 32 * deltaTiempo)
                self.posicion.x += paso if dx > 0 else -paso
            if distancia < 55:
                rumi.luz = max(0.15, rumi.luz - 0.08 * deltaTiempo)
