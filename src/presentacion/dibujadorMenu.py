"""Presentación independiente del selector de niveles."""

import pygame

from src.aplicacion.configuracion import ALTO_VENTANA, ANCHO_VENTANA


class DibujadorMenu:
    """Dibuja un mapa alegre sin decidir qué niveles están disponibles."""

    COLOR_ZORRO = (225, 102, 52)
    COLOR_ZORRO_SOMBRA = (126, 52, 42)
    COLOR_CREMA = (255, 225, 166)
    COLOR_DORADO = (255, 206, 92)

    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.fuente = pygame.font.SysFont("sans", 20)
        self.fuentePequena = pygame.font.SysFont("sans", 16, bold=True)
        self.fuenteTitulo = pygame.font.SysFont("sans", 35, bold=True)
        self.fuenteNumero = pygame.font.SysFont("sans", 31, bold=True)

    def dibujar(self, menu) -> None:
        self._dibujarFondo()
        self._dibujarEncabezado()
        for indice, opcion in enumerate(menu.opciones):
            fila, columna = divmod(indice, 3)
            centro = (472 + columna * 168, 235 + fila * 166)
            self._dibujarOpcion(
                opcion,
                centro,
                seleccionado=indice == menu.indiceSeleccionado,
            )
        ayuda = self.fuente.render(
            "Flechas/A-D-W-S: elegir   |   Espacio: entrar", True, self.COLOR_CREMA
        )
        self.pantalla.blit(
            ayuda, ((ANCHO_VENTANA - ayuda.get_width()) // 2, ALTO_VENTANA - 38)
        )

    def _dibujarFondo(self) -> None:
        """Bosque nocturno con sendero, luciérnagas y siluetas de montaña."""
        ancho, alto = self.pantalla.get_size()
        for y in range(alto):
            progreso = y / max(1, alto - 1)
            color = (
                int(20 + 13 * progreso),
                int(37 + 18 * progreso),
                int(69 + 25 * progreso),
            )
            pygame.draw.line(self.pantalla, color, (0, y), (ancho, y))

        pygame.draw.circle(self.pantalla, (154, 183, 238), (1045, 105), 47)
        pygame.draw.circle(self.pantalla, (207, 224, 250), (1031, 94), 39)
        pygame.draw.polygon(
            self.pantalla, (30, 53, 87),
            ((0, 305), (130, 170), (275, 306), (420, 185), (575, 308), (750, 155), (930, 305), (1100, 180), (1280, 316)),
        )
        pygame.draw.polygon(
            self.pantalla, (22, 43, 65),
            ((0, 382), (175, 245), (350, 390), (510, 265), (690, 390), (875, 240), (1080, 390), (1280, 255), (1280, 470), (0, 470)),
        )

        for x in range(-20, ancho + 80, 118):
            altura = 125 + (x // 118 % 3) * 32
            color = (13, 48, 57) if (x // 118) % 2 else (15, 61, 66)
            pygame.draw.rect(self.pantalla, (44, 43, 54), (x + 38, alto - altura - 35, 18, altura))
            pygame.draw.circle(self.pantalla, color, (x + 48, alto - altura - 36), 52)
            pygame.draw.circle(self.pantalla, color, (x + 12, alto - altura + 4), 36)
            pygame.draw.circle(self.pantalla, color, (x + 82, alto - altura + 10), 38)

        pygame.draw.ellipse(self.pantalla, (70, 80, 94), (330, alto - 122, 620, 190))
        pygame.draw.ellipse(self.pantalla, (106, 94, 84), (410, alto - 105, 460, 140))
        for x, y in ((126, 192), (284, 280), (366, 160), (913, 263), (1140, 222), (1198, 367), (98, 514)):
            pygame.draw.circle(self.pantalla, self.COLOR_DORADO, (x, y), 3)
            pygame.draw.circle(self.pantalla, (255, 239, 168), (x, y), 1)

    def _dibujarEncabezado(self) -> None:
        panel = pygame.Surface((590, 102), pygame.SRCALPHA)
        panel.fill((11, 26, 49, 192))
        pygame.draw.rect(panel, (116, 191, 184, 160), panel.get_rect(), 2, border_radius=20)
        self.pantalla.blit(panel, ((ANCHO_VENTANA - panel.get_width()) // 2, 28))
        titulo = self.fuenteTitulo.render("Elige tu aventura", True, self.COLOR_CREMA)
        subtitulo = self.fuente.render("Rumi: Camino del Alba", True, (163, 222, 213))
        self.pantalla.blit(titulo, ((ANCHO_VENTANA - titulo.get_width()) // 2, 43))
        self.pantalla.blit(subtitulo, ((ANCHO_VENTANA - subtitulo.get_width()) // 2, 87))

    def _dibujarOpcion(self, opcion, centro: tuple[int, int], seleccionado: bool) -> None:
        x, y = centro
        if opcion.desbloqueado:
            if seleccionado:
                pygame.draw.circle(self.pantalla, (255, 237, 151), centro, 66)
                pygame.draw.circle(self.pantalla, (255, 176, 74), centro, 62)
            else:
                pygame.draw.circle(self.pantalla, (53, 35, 47), (x + 4, y + 6), 61)
                pygame.draw.circle(self.pantalla, self.COLOR_ZORRO_SOMBRA, centro, 59)
            pygame.draw.circle(self.pantalla, self.COLOR_ZORRO, centro, 54)
            pygame.draw.circle(self.pantalla, self.COLOR_CREMA, (x, y + 13), 34)
            pygame.draw.polygon(self.pantalla, self.COLOR_ZORRO_SOMBRA, ((x - 39, y - 35), (x - 27, y - 67), (x - 4, y - 45)))
            pygame.draw.polygon(self.pantalla, self.COLOR_ZORRO_SOMBRA, ((x + 39, y - 35), (x + 27, y - 67), (x + 4, y - 45)))
            numero = self.fuenteNumero.render(str(opcion.numero), True, (52, 43, 51))
            self.pantalla.blit(numero, (x - numero.get_width() // 2, y - 7))
            etiqueta = self.fuentePequena.render(opcion.titulo, True, self.COLOR_CREMA)
        else:
            pygame.draw.circle(self.pantalla, (39, 49, 70), centro, 58)
            pygame.draw.circle(self.pantalla, (22, 30, 48), centro, 51)
            pygame.draw.rect(self.pantalla, (70, 87, 108), (x - 18, y - 4, 36, 29), border_radius=6)
            pygame.draw.arc(self.pantalla, (143, 160, 177), (x - 13, y - 20, 26, 30), 3.14, 6.28, 4)
            etiqueta = self.fuentePequena.render("Próximamente", True, (170, 190, 205))
        self.pantalla.blit(etiqueta, (x - etiqueta.get_width() // 2, y + 78))
