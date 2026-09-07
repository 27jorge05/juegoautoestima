"""Objetos reutilizables que un nivel puede componer, actualizar o quitar."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .dominio import Padre, RectanguloLogico, Rumi


class NivelConRumi(Protocol):
    rumi: Rumi
    padre: Padre


class ElementoNivel(Protocol):
    def actualizar(self, nivel: NivelConRumi, solicitaSegundoSalto: bool, deltaTiempo: float) -> bool:
        ...


@dataclass(frozen=True)
class ConfiguracionNiebla:
    rectangulo: RectanguloLogico
    multiplicadorVelocidad: float = 0.62
    radioProteccionPadre: float = 190.0
    opacidadBase: int = 218


@dataclass
class NieblaNivel:
    """Dominio de la niebla: área, efecto de velocidad y tiempo de animación."""

    configuracion: ConfiguracionNiebla
    activa: bool = False
    tiempoAnimacion: float = 0.0

    capaVisual: str = "frente"

    @property
    def rectangulo(self) -> RectanguloLogico:
        return self.configuracion.rectangulo

    def activar(self) -> None:
        self.activa = True

    def contiene(self, rumi: Rumi) -> bool:
        return self.activa and rumi.rectangulo.intersecta(self.rectangulo)

    def velocidadPermitida(self, rumi: Rumi, padre: Padre, velocidadNormal: float) -> float:
        if not self.contiene(rumi):
            return velocidadNormal
        if abs(rumi.posicion.x - padre.posicion.x) < self.configuracion.radioProteccionPadre:
            return velocidadNormal
        return velocidadNormal * self.configuracion.multiplicadorVelocidad

    def actualizar(self, nivel: NivelConRumi, solicitaSegundoSalto: bool, deltaTiempo: float) -> bool:
        if self.activa:
            self.tiempoAnimacion += deltaTiempo
        return False


@dataclass(frozen=True)
class ConfiguracionRocaImpulso:
    rectangulo: RectanguloLogico
    margenHorizontal: float = 80.0
    margenSuperior: float = 110.0
    impulsoVertical: float = 830.0
    anchoVisual: int = 172
    altoVisual: int = 132


@dataclass
class RocaImpulso:
    """Punto de impulso reutilizable: no es plataforma ni se consume."""

    configuracion: ConfiguracionRocaImpulso

    capaVisual: str = "mundo"

    @property
    def rectangulo(self) -> RectanguloLogico:
        return self.configuracion.rectangulo

    def actualizar(self, nivel: NivelConRumi, solicitaSegundoSalto: bool, deltaTiempo: float) -> bool:
        if not solicitaSegundoSalto:
            return False
        rectangulo = self.rectangulo
        zonaImpulso = RectanguloLogico(
            rectangulo.x - self.configuracion.margenHorizontal,
            rectangulo.y - self.configuracion.margenSuperior,
            rectangulo.ancho + self.configuracion.margenHorizontal * 2,
            rectangulo.alto + self.configuracion.margenSuperior + 25.0,
        )
        if nivel.rumi.rectangulo.intersecta(zonaImpulso):
            return nivel.rumi.usarSegundoSalto(self.configuracion.impulsoVertical)
        return False
