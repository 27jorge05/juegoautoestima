"""Criatura territorial del nivel 2; reglas independientes del render."""
from dataclasses import dataclass, field
from enum import Enum, auto
from .dominio import RectanguloLogico, Vector2D
from .enemigosNivel import TipoEnemigo


class EstadoEnemigo(Enum):
    PATRULLA = auto()
    AVISO = auto()
    ATAQUE = auto()
    RECUPERACION = auto()
    LIBERADO = auto()


@dataclass
class EnemigoHostil:
    tipo: TipoEnemigo
    posicion: Vector2D
    limiteIzquierdo: float
    limiteDerecho: float
    frase: str
    estado: EstadoEnemigo = EstadoEnemigo.PATRULLA
    tiempoEstado: float = 0.0
    direccion: int = 1
    objetivo: Vector2D = field(default_factory=lambda: Vector2D(0, 0))
    radioDeteccion: float = 250.0
    radioLuz: float = 110.0
    duracionAviso: float = 0.65
    duracionAtaque: float = 0.8
    duracionRecuperacion: float = 1.1
    velocidadPatrulla: float = 45.0
    velocidadAtaque: float = 330.0

    @property
    def liberado(self):
        return self.estado == EstadoEnemigo.LIBERADO

    @property
    def rectangulo(self):
        return RectanguloLogico(self.posicion.x, self.posicion.y, 42, 46)

    def cambiarEstado(self, estado):
        self.estado = estado
        self.tiempoEstado = 0.0

    def actualizar(self, rumi, deltaTiempo):
        """Devuelve contacto peligroso solo durante la embestida."""
        if deltaTiempo < 0:
            raise ValueError("El tiempo no puede retroceder")
        if self.liberado:
            return False
        dx, dy = rumi.posicion.x - self.posicion.x, rumi.posicion.y - self.posicion.y
        distancia = (dx * dx + dy * dy) ** 0.5
        if rumi.garrasActivas and distancia <= self.radioLuz:
            self.cambiarEstado(EstadoEnemigo.LIBERADO)
            return False
        self.tiempoEstado += deltaTiempo
        if self.estado == EstadoEnemigo.PATRULLA:
            if distancia <= self.radioDeteccion:
                self.objetivo = Vector2D(rumi.posicion.x, rumi.posicion.y)
                self.cambiarEstado(EstadoEnemigo.AVISO)
            else:
                x = self.posicion.x + self.direccion * self.velocidadPatrulla * deltaTiempo
                self.posicion.x = max(self.limiteIzquierdo, min(x, self.limiteDerecho))
                if x <= self.limiteIzquierdo or x >= self.limiteDerecho:
                    self.direccion *= -1
            return False
        if self.estado == EstadoEnemigo.AVISO:
            if self.tiempoEstado >= self.duracionAviso:
                self.cambiarEstado(EstadoEnemigo.ATAQUE)
            return False
        if self.estado == EstadoEnemigo.RECUPERACION:
            if self.tiempoEstado >= self.duracionRecuperacion:
                self.cambiarEstado(EstadoEnemigo.PATRULLA)
            return False
        if self.tiempoEstado >= self.duracionAtaque:
            self.cambiarEstado(EstadoEnemigo.RECUPERACION)
            return False
        dx = self.objetivo.x - self.posicion.x
        dy = self.objetivo.y - self.posicion.y if self.tipo == TipoEnemigo.ESPEJILLA else 0
        distanciaObjetivo = (dx * dx + dy * dy) ** 0.5
        if distanciaObjetivo:
            factor = min(1.0, self.velocidadAtaque * deltaTiempo / distanciaObjetivo)
            self.posicion.x = max(self.limiteIzquierdo, min(self.posicion.x + dx * factor, self.limiteDerecho))
            self.posicion.y += dy * factor
        contacto = self.rectangulo.intersecta(rumi.rectangulo)
        if contacto:
            self.cambiarEstado(EstadoEnemigo.RECUPERACION)
        return contacto
