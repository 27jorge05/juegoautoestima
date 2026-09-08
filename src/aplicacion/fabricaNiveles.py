"""Registro extensible de constructores de escenas jugables."""
from src.presentacion.escenaNivelUno import EscenaNivelUno
from src.presentacion.escenaNivelDos import EscenaNivelDos
from src.presentacion.escenaNivelTres import EscenaNivelTres


class FabricaNiveles:
    def __init__(self, creadores=None):
        self.creadores = dict({1: EscenaNivelUno, 2: EscenaNivelDos, 3: EscenaNivelTres} if creadores is None else creadores)

    def crear(self, numero, pantalla, volverMenu):
        if numero not in self.creadores:
            raise ValueError(f"Nivel no disponible: {numero}")
        return self.creadores[numero](pantalla, volverMenu)
