"""Vida de juego e invulnerabilidad; no representan autoestima."""
from dataclasses import dataclass


@dataclass
class Vitalidad:
    puntos: int = 3
    invulnerabilidad: float = 0.0
    duracionProteccion: float = 1.2

    @property
    def agotada(self):
        return self.puntos == 0

    def actualizar(self, deltaTiempo):
        if deltaTiempo < 0:
            raise ValueError("El tiempo no puede retroceder")
        self.invulnerabilidad = max(0.0, self.invulnerabilidad - deltaTiempo)

    def recibirGolpe(self):
        if self.agotada or self.invulnerabilidad > 0:
            return False
        self.puntos -= 1
        self.invulnerabilidad = self.duracionProteccion
        return True
