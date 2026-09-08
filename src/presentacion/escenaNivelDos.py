"""Composición de dependencias para Espejos de Niebla."""
from .escenaNivel import EscenaNivel
from src.niveles.nivelDos import NivelDos
from .dibujadorNivelDos import DibujadorNivelDos


class EscenaNivelDos(EscenaNivel):
    def __init__(self, pantalla, volverMenu):
        super().__init__(pantalla, volverMenu, NivelDos, DibujadorNivelDos)
