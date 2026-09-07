"""Presentación independiente del selector de niveles."""
import pygame
from .configuracion import ANCHO_VENTANA


class DibujadorMenu:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.fuente = pygame.font.SysFont("sans", 23)
        self.fuenteTitulo = pygame.font.SysFont("sans", 34, bold=True)

    def dibujar(self, menu) -> None:
        self.pantalla.fill((16, 24, 38))
        titulo = self.fuenteTitulo.render("Selecciona un nivel", True, (255, 220, 134))
        subtitulo = self.fuente.render("Rumi: Camino del Alba", True, (205, 220, 231))
        self.pantalla.blit(titulo, ((ANCHO_VENTANA - titulo.get_width()) // 2, 62))
        self.pantalla.blit(subtitulo, ((ANCHO_VENTANA - subtitulo.get_width()) // 2, 110))
        for indice, opcion in enumerate(menu.opciones):
            fila, columna = divmod(indice, 3)
            x, y = 414 + columna * 166, 185 + fila * 145
            seleccionado = indice == menu.indiceSeleccionado
            color = (61, 164, 177) if opcion.desbloqueado else (54, 64, 82)
            borde = (255, 216, 106) if seleccionado else (29, 38, 55)
            pygame.draw.rect(self.pantalla, borde, (x - 5, y - 5, 130, 130), border_radius=20)
            pygame.draw.rect(self.pantalla, color, (x, y, 120, 120), border_radius=16)
            if opcion.desbloqueado:
                pygame.draw.circle(self.pantalla, (255, 221, 98), (x + 60, y + 42), 15)
                numero = self.fuenteTitulo.render(str(opcion.numero), True, (246, 250, 247))
                self.pantalla.blit(numero, ((x + 60) - numero.get_width() // 2, y + 25))
                etiqueta = self.fuente.render("Abierto", True, (226, 255, 236))
            else:
                pygame.draw.rect(self.pantalla, (24, 31, 45), (x + 42, y + 41, 36, 32), border_radius=6)
                pygame.draw.arc(self.pantalla, (155, 170, 183), (x + 47, y + 26, 26, 28), 3.14, 6.28, 4)
                etiqueta = self.fuente.render("Bloqueado", True, (174, 184, 196))
            self.pantalla.blit(etiqueta, ((x + 60) - etiqueta.get_width() // 2, y + 87))
        ayuda = self.fuente.render("Flechas/A-D-W-S: elegir   |   Espacio: entrar", True, (255, 207, 99))
        self.pantalla.blit(ayuda, ((ANCHO_VENTANA - ayuda.get_width()) // 2, 650))

