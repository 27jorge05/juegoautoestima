"""Carga de imágenes Pygame separada del diseño y la lógica de un nivel."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pygame

from .configuracion import ALTO_VENTANA, ANCHO_VENTANA
from .recursosNivel import SeleccionRecursosNivel


@dataclass
class ImagenesNivel:
    fondo: pygame.Surface | None
    suelo: pygame.Surface | None
    rocas: list[pygame.Surface]
    enemigos: pygame.Surface | None


class CargadorRecursosNivel:
    def __init__(self, raizProyecto: Path) -> None:
        self.raizProyecto = raizProyecto

    def cargarImagen(self, rutaRelativa: str) -> pygame.Surface | None:
        ruta = self.raizProyecto / rutaRelativa
        return pygame.image.load(str(ruta)).convert_alpha() if ruta.exists() else None

    def cargarSuelo(self, seleccion: SeleccionRecursosNivel) -> pygame.Surface | None:
        imagen = self.cargarImagen(seleccion.rutaSuelo)
        if imagen is None:
            return None
        imagen.set_colorkey((255, 255, 255))
        altoUtil = imagen.get_height() - seleccion.recorteSuperiorSuelo - seleccion.recorteInferiorSuelo
        if altoUtil <= 0:
            return imagen
        # El recurso contiene bordes redondeados transparentes; usar la franja central
        # para que los mosaicos de suelo no parezcan barrancos adicionales.
        margen = imagen.get_width() // 12
        areaUtil = pygame.Rect(margen, seleccion.recorteSuperiorSuelo, imagen.get_width() - 2 * margen, altoUtil)
        return imagen.subsurface(areaUtil).copy()

    def dividirEnCuadricula(self, imagen: pygame.Surface | None, columnas: int, filas: int) -> list[pygame.Surface]:
        if imagen is None:
            return []
        ancho, alto = imagen.get_width() // columnas, imagen.get_height() // filas
        return [
            imagen.subsurface(pygame.Rect(columna * ancho, fila * alto, ancho, alto)).copy()
            for fila in range(filas)
            for columna in range(columnas)
        ]

    def cargar(self, seleccion: SeleccionRecursosNivel) -> ImagenesNivel:
        fondoOriginal = self.cargarImagen(seleccion.rutaFondo)
        fondo = pygame.transform.smoothscale(fondoOriginal, (ANCHO_VENTANA, ALTO_VENTANA)) if fondoOriginal else None
        return ImagenesNivel(
            fondo=fondo,
            suelo=self.cargarSuelo(seleccion),
            rocas=self.dividirEnCuadricula(self.cargarImagen(seleccion.rutaRocas), 2, 2),
            enemigos=self.cargarImagen(seleccion.rutaEnemigos),
        )
