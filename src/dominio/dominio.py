"""Reglas de dominio independientes de Pygame."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from .luzNiebla import EfectoLuzTemporal


class EstadoNivel(Enum):
    SEGUIR_PADRE = auto()
    NIEBLA = auto()
    TERREMOTO = auto()
    MADRIGUERA = auto()
    PAJARITO = auto()
    SALIDA = auto()
    COMPLETADO = auto()


@dataclass
class Vector2D:
    x: float
    y: float

    def sumar(self, otro: Vector2D) -> Vector2D:
        return Vector2D(self.x + otro.x, self.y + otro.y)

    def multiplicar(self, escalar: float) -> Vector2D:
        return Vector2D(self.x * escalar, self.y * escalar)


@dataclass
class RectanguloLogico:
    x: float
    y: float
    ancho: float
    alto: float

    @property
    def derecha(self) -> float:
        return self.x + self.ancho

    @property
    def abajo(self) -> float:
        return self.y + self.alto

    def intersecta(self, otro: RectanguloLogico) -> bool:
        return not (
            self.derecha <= otro.x
            or self.x >= otro.derecha
            or self.abajo <= otro.y
            or self.y >= otro.abajo
        )


@dataclass
class EntradaJugador:
    izquierda: bool = False
    derecha: bool = False
    saltar: bool = False
    interactuar: bool = False
    usarGarras: bool = False
    reiniciar: bool = False


class Personaje:
    """Lo común a todo personaje físico: posición, tamaño, dirección y hitbox."""

    def __init__(self, posicion: Vector2D, ancho: float, alto: float) -> None:
        self.posicion = posicion
        self.velocidad = Vector2D(0.0, 0.0)
        self.ancho = ancho
        self.alto = alto
        self.miraDerecha = True

    @property
    def rectangulo(self) -> RectanguloLogico:
        return RectanguloLogico(self.posicion.x, self.posicion.y, self.ancho, self.alto)

    def reubicar(self, posicion: Vector2D) -> None:
        self.posicion = posicion
        self.velocidad = Vector2D(0.0, 0.0)


class Rumi(Personaje):
    """Personaje jugable: hereda cuerpo e hitbox y añade sus propias habilidades."""

    def __init__(self, posicion: Vector2D) -> None:
        super().__init__(posicion, ancho=42.0, alto=46.0)
        self.estaEnSuelo = False
        self.estaSaltando = False
        self.segundoSaltoUsado = False
        self.miraDerecha = True
        self.luz = 0.28
        self.estaEscondido = False
        self.tiempoGarras = 0.0
        self.efectoLuz = EfectoLuzTemporal()

    def reiniciar(self, posicion: Vector2D) -> None:
        self.reubicar(posicion)
        self.estaEnSuelo = False
        self.estaSaltando = False
        self.segundoSaltoUsado = False
        self.luz = 0.28
        self.estaEscondido = False
        self.tiempoGarras = 0.0
        self.efectoLuz.apagar()

    @property
    def garrasActivas(self) -> bool:
        return self.tiempoGarras > 0.0

    def actualizarMovimiento(
        self,
        entrada: EntradaJugador,
        deltaTiempo: float,
        gravedad: float,
        velocidadMaxima: float,
        fuerzaSalto: float,
    ) -> None:
        self.tiempoGarras = max(0.0, self.tiempoGarras - deltaTiempo)
        if entrada.usarGarras:
            self.tiempoGarras = 0.32
        direccion = int(entrada.derecha) - int(entrada.izquierda)
        self.velocidad.x = direccion * velocidadMaxima
        if direccion != 0:
            self.miraDerecha = direccion > 0
        if entrada.saltar and self.estaEnSuelo:
            self.velocidad.y = -fuerzaSalto
            self.estaEnSuelo = False
            self.estaSaltando = True
            self.segundoSaltoUsado = False
        self.velocidad.y += gravedad * deltaTiempo
        self.posicion = self.posicion.sumar(self.velocidad.multiplicar(deltaTiempo))

    def usarSegundoSalto(self, fuerzaSalto: float) -> bool:
        """Solo una roca cercana puede solicitar esta acción durante un salto iniciado."""
        if not self.estaSaltando or self.segundoSaltoUsado:
            return False
        self.velocidad.y = -fuerzaSalto
        self.segundoSaltoUsado = True
        return True

    def resolverSuelo(self, plataformas: list[RectanguloLogico], posicionAnteriorY: float) -> None:
        self.estaEnSuelo = False
        for plataforma in plataformas:
            estabaSobrePlataforma = posicionAnteriorY + self.alto <= plataforma.y
            caeSobrePlataforma = self.rectangulo.abajo >= plataforma.y
            tocaHorizontalmente = (
                self.rectangulo.derecha > plataforma.x and self.rectangulo.x < plataforma.derecha
            )
            if self.velocidad.y >= 0 and estabaSobrePlataforma and caeSobrePlataforma and tocaHorizontalmente:
                self.posicion.y = plataforma.y - self.alto
                self.velocidad.y = 0.0
                self.estaEnSuelo = True
                self.estaSaltando = False
                self.segundoSaltoUsado = False
                return


class Padre(Personaje):
    """Guía del prólogo: comparte cuerpo e hitbox, pero no habilidades de Rumi."""

    def __init__(self, posicion: Vector2D) -> None:
        super().__init__(posicion, ancho=54.0, alto=54.0)


class SecuenciaNivelUno:
    """Transiciones narrativas del prólogo, sin detalles de interfaz."""

    def __init__(self) -> None:
        self.estado = EstadoNivel.SEGUIR_PADRE

    def activarNiebla(self) -> None:
        if self.estado == EstadoNivel.SEGUIR_PADRE:
            self.estado = EstadoNivel.NIEBLA

    def activarTerremoto(self) -> None:
        if self.estado == EstadoNivel.NIEBLA:
            self.estado = EstadoNivel.TERREMOTO

    def llegarMadriguera(self) -> None:
        if self.estado == EstadoNivel.TERREMOTO:
            self.estado = EstadoNivel.MADRIGUERA

    def hablarConPajarito(self) -> None:
        if self.estado == EstadoNivel.MADRIGUERA:
            self.estado = EstadoNivel.PAJARITO

    def salirMadriguera(self) -> None:
        if self.estado == EstadoNivel.PAJARITO:
            self.estado = EstadoNivel.SALIDA

    def completar(self) -> None:
        if self.estado == EstadoNivel.SALIDA:
            self.estado = EstadoNivel.COMPLETADO

    def encontrarPadre(self) -> None:
        """El cierre del Barranco ocurre al reunirse con su padre."""
        if self.estado != EstadoNivel.COMPLETADO:
            self.estado = EstadoNivel.COMPLETADO
