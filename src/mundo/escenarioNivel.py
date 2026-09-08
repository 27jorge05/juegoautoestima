"""Composición de suelo, fondo y elementos que pertenecen a un escenario."""

from __future__ import annotations

from dataclasses import dataclass, field

from src.dominio.dominio import RectanguloLogico
from src.dominio.enemigosNivel import CriaturaNivel
from src.dominio.plataformaNivel import PlataformaNivel, DecoracionNivel
from .elementosNivel import ElementoNivel, NivelConRumi, PilarAliento
from .recursosNivel import SeleccionRecursosNivel


@dataclass(frozen=True)
class TramoNivel:
    nombre: str
    inicio: float
    fin: float


@dataclass
class EscenarioNivel:
    """Una fuente de verdad para terreno, recursos y objetos de un nivel."""

    recursos: SeleccionRecursosNivel
    plataformas: list[PlataformaNivel]
    elementos: list[ElementoNivel]

    decoraciones: list[DecoracionNivel] = field(default_factory=list)
    ancho: float = 1880.0
    tramos: list[TramoNivel] = field(default_factory=list)
    enemigos: list[CriaturaNivel] = field(default_factory=list)
    pilares: list[PilarAliento] = field(default_factory=list)

    @property
    def geometriaSuelo(self) -> list[RectanguloLogico]:
        return [plataforma.rectangulo for plataforma in self.plataformas]

    def contieneElemento(self, elemento: ElementoNivel) -> bool:
        return elemento in self.elementos

    def actualizar(self, nivel: NivelConRumi, solicitaSegundoSalto: bool, deltaTiempo: float) -> bool:
        accionActivada = False
        for elemento in self.elementos:
            accionActivada = elemento.actualizar(nivel, solicitaSegundoSalto, deltaTiempo) or accionActivada
        return accionActivada
