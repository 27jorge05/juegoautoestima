"""Geometría y material declarativo; no contiene recursos de Pygame."""
from dataclasses import dataclass
from enum import Enum, auto
from .dominio import RectanguloLogico


class TipoTerreno(Enum):
    ROCA_NIEBLA = auto()
    BOSQUE = auto()
    CRISTAL = auto()
    RUINAS = auto()


@dataclass(frozen=True)
class PlataformaNivel:
    rectangulo: RectanguloLogico
    tipo: TipoTerreno = TipoTerreno.ROCA_NIEBLA


class TipoDecoracion(Enum):
    HUELLA = auto()
    ARBUSTO = auto()
    CRISTAL = auto()
    ARBOL = auto()


@dataclass(frozen=True)
class DecoracionNivel:
    tipo: TipoDecoracion
    x: float
    y: float
