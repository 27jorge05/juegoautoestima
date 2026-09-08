"""Estado y opciones del menú principal."""

from dataclasses import dataclass


@dataclass(frozen=True)
class OpcionNivel:
    numero: int
    titulo: str
    desbloqueado: bool


class MenuPrincipal:
    def __init__(self) -> None:
        self.opciones = (
            OpcionNivel(1, "El Barranco del Velo", True),
            OpcionNivel(2, "Espejos de Niebla", True),
            OpcionNivel(3, "Cueva del Velo", True),
            OpcionNivel(4, "Jardines de Lluvia", False),
            OpcionNivel(5, "Próximamente", False),
            OpcionNivel(6, "Próximamente", False),
            OpcionNivel(7, "Próximamente", False),
            OpcionNivel(8, "Próximamente", False),
            OpcionNivel(9, "Próximamente", False),
        )
        self.indiceSeleccionado = 0

    @property
    def opcionSeleccionada(self) -> OpcionNivel:
        return self.opciones[self.indiceSeleccionado]

    def moverSeleccion(self, desplazamientoX: int, desplazamientoY: int) -> None:
        fila, columna = divmod(self.indiceSeleccionado, 3)
        nuevaFila = max(0, min(2, fila + desplazamientoY))
        nuevaColumna = max(0, min(2, columna + desplazamientoX))
        self.indiceSeleccionado = nuevaFila * 3 + nuevaColumna

    def seleccionarNivel(self, numero: int | None = None) -> bool:
        if numero is None:
            numero = self.opcionSeleccionada.numero
        return any(opcion.numero == numero and opcion.desbloqueado for opcion in self.opciones)
