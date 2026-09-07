"""Registro extensible de constructores de escenas jugables."""
from .escenaNivelUno import EscenaNivelUno
from .escenaNivelDos import EscenaNivelDos


class FabricaNiveles:
    def __init__(self, creadores=None):
        self.creadores = dict({1: EscenaNivelUno, 2: EscenaNivelDos} if creadores is None else creadores)

    def crear(self, numero, pantalla, volverMenu):
        if numero not in self.creadores:
            raise ValueError(f"Nivel no disponible: {numero}")
        return self.creadores[numero](pantalla, volverMenu)
