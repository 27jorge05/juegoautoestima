"""Perfiles declarativos de comportamiento para las criaturas por nivel."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PerfilDificultadEnemigo:
    nivel: int
    velocidadPatrulla: float
    velocidadAtaque: float
    radioDeteccion: float
    duracionAviso: float
    duracionAtaque: float
    velocidadAviso: float = 0.0


NIVEL_UNO = PerfilDificultadEnemigo(1, 45.0, 290.0, 220.0, 1.50, 0.75)
NIVEL_DOS = PerfilDificultadEnemigo(2, 55.0, 360.0, 250.0, 1.50, 0.80)
NIVEL_TRES = PerfilDificultadEnemigo(3, 95.0, 520.0, 330.0, 0.35, 1.00, 145.0)
