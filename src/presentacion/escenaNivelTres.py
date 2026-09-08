"""Composición de dependencias para la Cueva del Velo."""

from .dibujadorNivelTres import DibujadorNivelTres
from .escenaNivel import EscenaNivel
from src.niveles.nivelTres import NivelTres


class EscenaNivelTres(EscenaNivel):
    def __init__(self, pantalla, volverMenu):
        super().__init__(pantalla, volverMenu, NivelTres, DibujadorNivelTres)
