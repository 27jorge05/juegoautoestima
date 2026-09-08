"""Efecto temporal de luz reutilizable, sin depender de Pygame."""

from dataclasses import dataclass


@dataclass
class EfectoLuzTemporal:
    """Mantiene luz plena y después reduce suavemente su alcance."""

    duracionPlena: float = 1.5
    duracionFundido: float = 1.5
    radioMaximo: float = 400.0
    color: tuple[int, int, int] = (255, 174, 82)
    fuerzaClaro: float = 1.90
    tiempoRestante: float = 0.0

    @property
    def duracionTotal(self) -> float:
        return self.duracionPlena + self.duracionFundido

    @property
    def activo(self) -> bool:
        return self.tiempoRestante > 0.0

    @property
    def intensidad(self) -> float:
        if not self.activo:
            return 0.0
        if self.tiempoRestante >= self.duracionFundido:
            return 1.0
        return self.tiempoRestante / self.duracionFundido

    @property
    def radioActual(self) -> float:
        return self.radioMaximo * self.intensidad

    def activar(self) -> None:
        self.tiempoRestante = self.duracionTotal

    def actualizar(self, deltaTiempo: float) -> None:
        if deltaTiempo < 0:
            raise ValueError("El tiempo no puede retroceder")
        self.tiempoRestante = max(0.0, self.tiempoRestante - deltaTiempo)

    def apagar(self) -> None:
        self.tiempoRestante = 0.0
