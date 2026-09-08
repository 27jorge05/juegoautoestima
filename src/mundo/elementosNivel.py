"""Objetos reutilizables que un nivel puede componer, actualizar o quitar."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Protocol

from src.dominio.dominio import Padre, RectanguloLogico, Rumi, Vector2D
from src.dominio.mensajesPilares import obtenerMensajePilar
from src.dominio.mensajes import Dialogo


class NivelConRumi(Protocol):
    rumi: Rumi
    padre: Padre


class ElementoNivel(Protocol):
    def actualizar(self, nivel: NivelConRumi, solicitaSegundoSalto: bool, deltaTiempo: float) -> bool:
        ...


class TipoNiebla(Enum):
    """Variantes visuales reutilizables que un nivel puede combinar."""

    AZUL = auto()
    VIOLETA = auto()
    OSCURA = auto()


@dataclass(frozen=True)
class GrupoNubesNiebla:
    """Una silueta y su desplazamiento dentro de una niebla reutilizable."""

    variante: TipoNiebla
    nubes: tuple[tuple[int, int, int], ...]
    desfaseX: int = 0
    desfaseY: int = 0
    velocidad: int = 12


@dataclass(frozen=True)
class ConfiguracionNubesNiebla:
    """Forma, densidad y movimiento que pertenecen al objeto niebla."""

    pasoHorizontal: int
    pasoVertical: int
    grupos: tuple[GrupoNubesNiebla, ...]


NUBES_NIEBLA_LIGERA = ConfiguracionNubesNiebla(
    128,
    142,
    (
        GrupoNubesNiebla(
            TipoNiebla.AZUL,
            ((-35, 5, 58), (15, -14, 54), (58, 10, 61), (99, -8, 49)),
        ),
    ),
)

NUBES_NIEBLA_DENSA = ConfiguracionNubesNiebla(
    170,
    128,
    (
        GrupoNubesNiebla(
            TipoNiebla.AZUL,
            ((-54, 8, 92), (8, -25, 88), (74, 12, 98), (112, -17, 82)),
            velocidad=11,
        ),
        GrupoNubesNiebla(
            TipoNiebla.VIOLETA,
            ((-60, -12, 80), (2, 18, 110), (83, -20, 91), (155, 10, 86)),
            desfaseX=41,
            desfaseY=31,
            velocidad=17,
        ),
        GrupoNubesNiebla(
            TipoNiebla.OSCURA,
            ((-48, 14, 104), (35, -22, 76), (95, 13, 112), (168, -9, 72)),
            desfaseX=79,
            desfaseY=52,
            velocidad=23,
        ),
    ),
)


@dataclass(frozen=True)
class ConfiguracionNiebla:
    rectangulo: RectanguloLogico
    multiplicadorVelocidad: float = 0.62
    radioProteccionPadre: float = 190.0
    opacidadBase: int = 218
    variantesVisuales: tuple[TipoNiebla, ...] = (TipoNiebla.AZUL,)
    configuracionNubes: ConfiguracionNubesNiebla = NUBES_NIEBLA_LIGERA


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
class FuenteLuzNiebla:
    """Claro de visión expresado en coordenadas lógicas, sin depender de Pygame."""

    posicion: Vector2D
    radio: float
    color: tuple[int, int, int] = (255, 190, 96)
    fuerzaClaro: float = 1.0

    def intensidadEn(self, posicion: Vector2D) -> float:
        """Atenúa de forma suave la luz al alejarse de su fuente."""
        dx = posicion.x - self.posicion.x
        dy = posicion.y - self.posicion.y
        distancia = (dx * dx + dy * dy) ** 0.5
        return max(0.0, 1.0 - distancia / self.radio) if self.radio else 0.0


@dataclass(frozen=True)
class FarolNiebla:
    """Fuente permanente: interactuar cerca de ella presta luz temporal a Rumi."""

    rectangulo: RectanguloLogico
    radioLuz: float = 285.0
    alcanceInteraccion: float = 95.0
    emiteLuz: bool = True
    colorLuz: tuple[int, int, int] = (255, 196, 102)
    fuerzaClaro: float = 1.60

    capaVisual: str = "mundo"

    @property
    def fuenteLuz(self) -> FuenteLuzNiebla:
        return FuenteLuzNiebla(
            Vector2D(self.rectangulo.x + self.rectangulo.ancho / 2, self.rectangulo.y + 24),
            self.radioLuz,
            self.colorLuz,
            self.fuerzaClaro,
        )

    def puedeEntregarLuz(self, rumi: Rumi) -> bool:
        zona = RectanguloLogico(
            self.rectangulo.x - self.alcanceInteraccion,
            self.rectangulo.y - self.alcanceInteraccion,
            self.rectangulo.ancho + self.alcanceInteraccion * 2,
            self.rectangulo.alto + self.alcanceInteraccion * 2,
        )
        return rumi.rectangulo.intersecta(zona)

    def actualizar(self, nivel: NivelConRumi, solicitaSegundoSalto: bool, deltaTiempo: float) -> bool:
        return False


@dataclass(frozen=True)
class ConfiguracionRocaImpulso:
    rectangulo: RectanguloLogico
    margenHorizontal: float = 80.0
    margenSuperior: float = 110.0
    impulsoVertical: float = 830.0
    anchoVisual: int = 172
    altoVisual: int = 132
    brillo: bool = False


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


@dataclass(frozen=True)
class PilarAliento:
    """Objeto interactivo: conserva su alcance y el mensaje que ofrece."""

    rectangulo: RectanguloLogico
    identificadorMensaje: str
    alcance: float = 90.0

    def mensajeSiEstaCerca(self, rumi: Rumi) -> Dialogo | None:
        zona = RectanguloLogico(
            self.rectangulo.x - self.alcance,
            self.rectangulo.y - self.alcance,
            self.rectangulo.ancho + self.alcance * 2,
            self.rectangulo.alto + self.alcance * 2,
        )
        if not rumi.rectangulo.intersecta(zona):
            return None
        return obtenerMensajePilar(self.identificadorMensaje).dialogo
