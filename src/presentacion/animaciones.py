"""Animaciones visuales de Pygame; no contiene reglas del nivel."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pygame


@dataclass(frozen=True)
class DefinicionAnimacion:
    """Indica qué casillas de una hoja de sprites componen una animación."""

    casillas: tuple[int, ...]
    duracionFotograma: float
    esperaInicial: float = 0.0

    def __post_init__(self):
        if not self.casillas or self.duracionFotograma <= 0 or self.esperaInicial < 0:
            raise ValueError("La animación requiere casillas, duración positiva y espera no negativa")


class HojaSprites:
    """Carga una hoja regular y extrae sus casillas como superficies independientes."""

    def __init__(self, ruta: Path, columnas: int = 4, filas: int = 3) -> None:
        if columnas <= 0 or filas <= 0:
            raise ValueError("La cuadrícula debe tener filas y columnas positivas")
        imagen = pygame.image.load(str(ruta)).convert_alpha()
        anchoCasilla = imagen.get_width() // columnas
        altoCasilla = imagen.get_height() // filas
        if anchoCasilla == 0 or altoCasilla == 0:
            raise ValueError("La cuadrícula supera el tamaño de la imagen")
        self.fotogramas: list[pygame.Surface] = []
        for fila in range(filas):
            for columna in range(columnas):
                area = pygame.Rect(columna * anchoCasilla, fila * altoCasilla, anchoCasilla, altoCasilla)
                fotograma = imagen.subsurface(area).copy()
                self.eliminarHaloInferior(fotograma)
                # Recortar transparencia una sola vez, sin alterar el archivo fuente.
                limites = fotograma.get_bounding_rect(min_alpha=160)
                self.fotogramas.append(fotograma.subsurface(limites).copy() if limites.width and limites.height else fotograma)

    def eliminarHaloInferior(self, fotograma: pygame.Surface) -> None:
        """Quita la neblina/reflejo tenue que vino pegado a las hojas generadas."""
        ancho, alto = fotograma.get_size()
        for y in range(alto):
            for x in range(ancho):
                rojo, verde, azul, alfa = fotograma.get_at((x, y))
                if alfa < 72:
                    fotograma.set_at((x, y), (rojo, verde, azul, 0))

    def obtenerFotograma(self, indice: int, tamano: tuple[int, int], miraDerecha: bool) -> pygame.Surface:
        original = self.fotogramas[indice]
        factor = min(tamano[0] / original.get_width(), tamano[1] / original.get_height())
        dimensiones = (max(1, round(original.get_width() * factor)), max(1, round(original.get_height() * factor)))
        fotograma = pygame.transform.scale(original, dimensiones)
        return fotograma if miraDerecha else pygame.transform.flip(fotograma, True, False)


class ReproductorAnimacion:
    """Selecciona y avanza fotogramas sin conocer el personaje ni el nivel."""

    def __init__(self, hoja: HojaSprites, definiciones: dict[str, DefinicionAnimacion]) -> None:
        self.hoja = hoja
        self.definiciones = definiciones
        self.reiniciar()

    def reiniciar(self):
        self.nombreActual = "reposo"
        self.indiceActual = 0
        self.tiempoAcumulado = 0.0
        self.tiempoEnPose = 0.0

    def actualizar(self, nombre: str, deltaTiempo: float) -> None:
        if nombre != self.nombreActual:
            self.nombreActual = nombre
            self.indiceActual = 0
            self.tiempoAcumulado = 0.0
            self.tiempoEnPose = 0.0
        definicion = self.definiciones[nombre]
        if deltaTiempo < 0:
            raise ValueError("El tiempo no puede retroceder")
        tiempoAnterior = self.tiempoEnPose
        self.tiempoEnPose += deltaTiempo
        self.tiempoAcumulado += max(0.0, self.tiempoEnPose - definicion.esperaInicial) - max(0.0, tiempoAnterior - definicion.esperaInicial)
        while self.tiempoAcumulado >= definicion.duracionFotograma:
            self.tiempoAcumulado -= definicion.duracionFotograma
            self.indiceActual = (self.indiceActual + 1) % len(definicion.casillas)

    def dibujar(
        self,
        pantalla: pygame.Surface,
        posicion: tuple[int, int],
        tamano: tuple[int, int],
        miraDerecha: bool,
    ) -> None:
        definicion = self.definiciones[self.nombreActual]
        indiceHoja = definicion.casillas[self.indiceActual]
        fotograma = self.hoja.obtenerFotograma(indiceHoja, tamano, miraDerecha)
        pantalla.blit(fotograma, posicion)

    def dibujarAnclado(self, pantalla, pies, tamano, miraDerecha):
        definicion = self.definiciones[self.nombreActual]
        fotograma = self.hoja.obtenerFotograma(definicion.casillas[self.indiceActual], tamano, miraDerecha)
        destino = fotograma.get_rect(midbottom=pies)
        pantalla.blit(fotograma, destino)
        return destino


def crearAnimacionRumi(ruta: Path) -> ReproductorAnimacion:
    hoja = HojaSprites(ruta)
    definiciones = {
        "reposo": DefinicionAnimacion((0, 1, 2, 3), 0.22, esperaInicial=5.0),
        "correr": DefinicionAnimacion((4, 5, 6, 7), 0.09),
        "saltar": DefinicionAnimacion((8, 9), 0.16),
        "garras": DefinicionAnimacion((10,), 0.12),
        "cansado": DefinicionAnimacion((11,), 0.25),
    }
    return ReproductorAnimacion(hoja, definiciones)


def crearAnimacionPadre(ruta: Path) -> ReproductorAnimacion:
    hoja = HojaSprites(ruta)
    definiciones = {
        "reposo": DefinicionAnimacion((0, 1, 2), 0.35),
        "guiar": DefinicionAnimacion((3,), 0.18),
        "caminar": DefinicionAnimacion((4, 5, 6), 0.15),
        "correr": DefinicionAnimacion((7,), 0.12),
        "saltar": DefinicionAnimacion((8, 9), 0.14),
        "proteger": DefinicionAnimacion((10,), 0.15),
        "reencuentro": DefinicionAnimacion((11,), 0.3),
    }
    return ReproductorAnimacion(hoja, definiciones)
