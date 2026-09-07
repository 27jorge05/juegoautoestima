"""Presentación del Barranco y sus entidades."""

from __future__ import annotations

import pygame
from pathlib import Path
from dataclasses import dataclass

from .configuracion import ALTO_VENTANA, ANCHO_VENTANA
from .animaciones import crearAnimacionPadre, crearAnimacionRumi
from .dibujadorEscenario import DibujadorEscenario
from .dominio import EstadoNivel
from .estadoVisual import obtenerAnimacionRumi
from .nivelUno import NivelUno


@dataclass
class EfectoSalto:
    x: float
    y: float
    tiempoRestante: float = 0.26


class DibujadorNivelUno:
    """Render de Nivel 1: el estado lógico decide la pose, esta clase la pinta."""

    def __init__(self, pantalla: pygame.Surface, recursosNivel) -> None:
        self.pantalla = pantalla
        self.fuente = pygame.font.SysFont("sans", 23)
        self.fuenteTitulo = pygame.font.SysFont("sans", 34, bold=True)
        self.dibujadorEscenario = DibujadorEscenario(pantalla, recursosNivel)
        carpetaPersonajes = Path(__file__).resolve().parents[1] / "assets" / "characters" / "rumi"
        self.animacionRumi = crearAnimacionRumi(carpetaPersonajes / "rumi_sprite_sheet_v3.png")
        self.animacionPadre = crearAnimacionPadre(carpetaPersonajes / "padre_sprite_sheet_v1.png")
        self.efectosSalto: list[EfectoSalto] = []

    def reiniciar(self):
        self.efectosSalto.clear()
        self.animacionRumi.reiniciar()
        self.animacionPadre.reiniciar()

    def actualizar(self, nivel, deltaTiempo):
        for efecto in self.efectosSalto:
            efecto.tiempoRestante -= deltaTiempo
        self.efectosSalto = [e for e in self.efectosSalto if e.tiempoRestante > 0]
        rumi = nivel.rumi
        self.animacionRumi.actualizar(obtenerAnimacionRumi(rumi.velocidad.x, rumi.velocidad.y, rumi.estaEnSuelo, rumi.garrasActivas), deltaTiempo)
        self.animacionPadre.actualizar("reposo" if nivel.secuencia.estado == EstadoNivel.SEGUIR_PADRE else "guiar", deltaTiempo)

    def registrarSalto(self, x: float, y: float) -> None:
        self.efectosSalto.append(EfectoSalto(x, y))

    def dibujar(self, nivel: NivelUno, desplazamientoCamara: float) -> None:
        self.dibujadorEscenario.dibujarMundo(nivel.escenario, nivel.padre, desplazamientoCamara)
        self.dibujarEfectosSalto(desplazamientoCamara)
        self.dibujarPadre(nivel, desplazamientoCamara)
        self.dibujarPajarito(nivel, desplazamientoCamara)
        self.dibujarRumi(nivel, desplazamientoCamara)
        self.dibujadorEscenario.dibujarFrente(nivel.escenario, nivel.padre, desplazamientoCamara)
        self.dibujarInterfaz(nivel)

    def dibujarEfectosSalto(self, desplazamientoCamara: float) -> None:
        for efecto in self.efectosSalto:
            progreso = 1.0 - efecto.tiempoRestante / 0.26
            radio = int(10 + progreso * 24)
            alpha = int(150 * (1.0 - progreso))
            x = int(efecto.x - desplazamientoCamara)
            y = int(efecto.y)
            capa = pygame.Surface((radio * 4, radio * 2), pygame.SRCALPHA)
            pygame.draw.ellipse(capa, (177, 231, 255, alpha), (radio, 0, radio * 2, max(2, radio // 2)), 2)
            self.pantalla.blit(capa, (x - radio * 2, y - radio // 2))

    def dibujarRumi(self, nivel: NivelUno, desplazamientoCamara: float) -> None:
        rumi = nivel.rumi
        x = int(rumi.posicion.x - desplazamientoCamara)
        y = int(rumi.posicion.y)
        self.animacionRumi.dibujarAnclado(self.pantalla, (int(x + rumi.ancho / 2), int(y + rumi.alto)), (132, 118), rumi.miraDerecha)

    def dibujarPadre(self, nivel: NivelUno, desplazamientoCamara: float) -> None:
        x = int(nivel.padre.posicion.x - desplazamientoCamara)
        y = int(nivel.padre.posicion.y)
        if -90 < x < ANCHO_VENTANA + 90:
            self.animacionPadre.dibujarAnclado(self.pantalla, (int(x + nivel.padre.ancho / 2), int(y + nivel.padre.alto)), (176, 157), True)

    def dibujarPajarito(self, nivel: NivelUno, desplazamientoCamara: float) -> None:
        x = int(nivel.pajaritoPosicion.x - desplazamientoCamara)
        y = int(nivel.pajaritoPosicion.y)
        if -40 < x < ANCHO_VENTANA + 40:
            pygame.draw.circle(self.pantalla, (255, 220, 82), (x, y), 13)
            pygame.draw.polygon(self.pantalla, (247, 184, 56), [(x + 11, y), (x + 27, y + 5), (x + 11, y + 9)])
            pygame.draw.circle(self.pantalla, (31, 35, 46), (x - 4, y - 2), 2)

    def dibujarInterfaz(self, nivel: NivelUno) -> None:
        titulo = self.fuenteTitulo.render("Rumi: El Barranco del Velo", True, (255, 232, 177))
        self.pantalla.blit(titulo, (28, 22))
        fondo = pygame.Surface((ANCHO_VENTANA - 56, 112), pygame.SRCALPHA)
        fondo.fill((11, 17, 25, 210))
        self.pantalla.blit(fondo, (28, ALTO_VENTANA - 138))
        for indice, linea in enumerate(ajustarTexto(nivel.dialogo, self.fuente, ANCHO_VENTANA - 96)):
            texto = self.fuente.render(linea, True, (242, 245, 248))
            self.pantalla.blit(texto, (48, ALTO_VENTANA - 116 + indice * 27))
        estado = self.fuente.render(
            "Espacio: salto  |  En el aire, junto a roca: impulso  |  F: garras",
            True,
            (181, 211, 222),
        )
        self.pantalla.blit(estado, (48, ALTO_VENTANA - 49))




def ajustarTexto(texto, fuente, ancho):
    lineas = []
    linea = ""
    for palabra in texto.split():
        candidata = f"{linea} {palabra}".strip()
        if linea and fuente.size(candidata)[0] > ancho:
            lineas.append(linea)
            linea = palabra
        else:
            linea = candidata
    if linea:
        lineas.append(linea)
    return lineas
