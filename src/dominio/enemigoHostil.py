"""Criatura territorial del nivel 2; reglas independientes del render."""
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Iterable, Protocol
from .dominio import RectanguloLogico, Vector2D
from .enemigosNivel import TipoEnemigo
from .mensajes import Dialogo
from .dificultadEnemigos import PerfilDificultadEnemigo


class EstadoEnemigo(Enum):
    PATRULLA = auto()
    AVISO = auto()
    ATAQUE = auto()
    RECUPERACION = auto()
    LIBERADO = auto()


class FuenteDeIluminacion(Protocol):
    def intensidadEn(self, posicion: Vector2D) -> float:
        ...


@dataclass
class EnemigoHostil:
    tipo: TipoEnemigo
    posicion: Vector2D
    limiteIzquierdo: float
    limiteDerecho: float
    dialogoAviso: Dialogo | str
    emiteFrase: bool = True
    vulnerableALuz: bool = True
    oscuro: bool = False
    mostrarIndicadorEstado: bool = True
    alumbrado: bool = False
    intensidadLuz: float = 0.0
    estado: EstadoEnemigo = EstadoEnemigo.PATRULLA
    tiempoEstado: float = 0.0
    direccion: int = 1
    objetivo: Vector2D = field(default_factory=lambda: Vector2D(0, 0))
    radioDeteccion: float = 250.0
    radioLuz: float = 180.0
    duracionAviso: float = 1.5
    duracionAtaque: float = 0.8
    duracionRecuperacion: float = 1.1
    velocidadPatrulla: float = 45.0
    velocidadAtaque: float = 330.0
    velocidadAviso: float = 0.0
    perfilDificultad: PerfilDificultadEnemigo | None = None

    def __post_init__(self) -> None:
        if isinstance(self.dialogoAviso, str):
            hablante = "Susurro" if self.tipo == TipoEnemigo.SUSURRO else "Espejilla"
            self.dialogoAviso = Dialogo(
                self.dialogoAviso,
                hablante=hablante,
                duracionVisible=1.5,
                duracionFundido=0.0,
            )
        if self.perfilDificultad is not None:
            self.velocidadPatrulla = self.perfilDificultad.velocidadPatrulla
            self.velocidadAtaque = self.perfilDificultad.velocidadAtaque
            self.radioDeteccion = self.perfilDificultad.radioDeteccion
            self.duracionAviso = self.perfilDificultad.duracionAviso
            self.duracionAtaque = self.perfilDificultad.duracionAtaque
            self.velocidadAviso = self.perfilDificultad.velocidadAviso
        if self.emiteFrase:
            self.duracionAviso = max(self.duracionAviso, self.dialogoAviso.duracionVisible)

    @property
    def frase(self) -> str:
        """Compatibilidad de lectura; la voz efectiva vive en `dialogoAviso`."""
        return self.dialogoAviso.texto

    @property
    def liberado(self):
        return self.estado == EstadoEnemigo.LIBERADO

    @property
    def rectangulo(self):
        return RectanguloLogico(self.posicion.x, self.posicion.y, 42, 46)

    def cambiarEstado(self, estado):
        self.estado = estado
        self.tiempoEstado = 0.0

    def actualizarIluminacion(self, fuentes: Iterable[FuenteDeIluminacion]) -> None:
        """Regla propia: la criatura sabe si una fuente de luz la alcanza."""
        centro = Vector2D(self.posicion.x + 21, self.posicion.y + 23)
        self.intensidadLuz = max(
            (fuente.intensidadEn(centro) for fuente in fuentes), default=0.0
        )
        self.alumbrado = self.intensidadLuz >= 0.12

    def actualizar(self, rumi, deltaTiempo):
        """Devuelve contacto peligroso solo durante la embestida."""
        if deltaTiempo < 0:
            raise ValueError("El tiempo no puede retroceder")
        if self.liberado:
            return False
        dx, dy = rumi.posicion.x - self.posicion.x, rumi.posicion.y - self.posicion.y
        distancia = (dx * dx + dy * dy) ** 0.5
        if self.vulnerableALuz and rumi.garrasActivas and distancia <= self.radioLuz:
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
            # Las criaturas avanzadas pueden acercarse mientras avisan. El
            # texto es una señal visual, no una pausa de su comportamiento.
            if self.velocidadAviso:
                self._moverHaciaObjetivo(self.velocidadAviso, deltaTiempo)
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
        self._moverHaciaObjetivo(self.velocidadAtaque, deltaTiempo)
        contacto = self.rectangulo.intersecta(rumi.rectangulo)
        if contacto:
            self.cambiarEstado(EstadoEnemigo.RECUPERACION)
        return contacto

    def _moverHaciaObjetivo(self, velocidad: float, deltaTiempo: float) -> None:
        """Acerca la criatura al último punto detectado sin salir de su zona."""
        dx = self.objetivo.x - self.posicion.x
        dy = self.objetivo.y - self.posicion.y if self.tipo == TipoEnemigo.ESPEJILLA else 0
        distanciaObjetivo = (dx * dx + dy * dy) ** 0.5
        if distanciaObjetivo:
            factor = min(1.0, velocidad * deltaTiempo / distanciaObjetivo)
            self.posicion.x = max(self.limiteIzquierdo, min(self.posicion.x + dx * factor, self.limiteDerecho))
            self.posicion.y += dy * factor
