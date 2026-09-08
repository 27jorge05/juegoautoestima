"""Composición de dependencias para el Barranco."""
from .escenaNivel import EscenaNivel
from src.niveles.nivelUno import NivelUno
from .dibujadorNivelUno import DibujadorNivelUno


class EscenaNivelUno(EscenaNivel):
    def __init__(self, pantalla, volverMenu):
        super().__init__(pantalla, volverMenu, NivelUno, DibujadorNivelUno)
