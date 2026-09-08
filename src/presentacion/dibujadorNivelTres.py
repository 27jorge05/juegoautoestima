"""Presentación de la cueva: roca, cristales y una niebla aclarada por Rumi."""

import pygame

from .dibujadorNivelDos import DibujadorNivelDos
from src.dominio.estadoJuegoNivel import EstadoJuegoNivel
from .dibujadorNiebla import DibujadorNiebla


class DibujadorNivelTres(DibujadorNivelDos):
    def __init__(self, pantalla, recursos):
        super().__init__(pantalla, recursos)
        self.tituloCueva = pygame.font.SysFont("sans", 32, bold=True)
        self.dibujadorNiebla = DibujadorNiebla(pantalla)

    def dibujarAmbienteEspecial(self, nivel, camara):
        ancho, alto = self.pantalla.get_size()
        techo = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        techo.fill((12, 15, 37, 165))
        for x in range(-70, ancho + 100, 140):
            pygame.draw.polygon(techo, (24, 29, 59, 235), [(x, 0), (x + 70, 0), (x + 36, 120)])
            pygame.draw.polygon(techo, (76, 190, 235, 165), [(x + 42, 85), (x + 56, 150), (x + 70, 85)])
        self.pantalla.blit(techo, (0, 0))
        for pilar in nivel.escenario.pilares:
            x = round(pilar.rectangulo.x - camara)
            if -80 < x < ancho + 80:
                pygame.draw.rect(self.pantalla, (52, 79, 108), (x, 460, 48, 120), border_radius=6)
                pygame.draw.polygon(self.pantalla, (131, 235, 249), [(x + 24, 435), (x + 39, 470), (x + 24, 495), (x + 9, 470)])
        self.dibujadorNiebla.dibujar(nivel.niebla, nivel.fuentesLuzNiebla, camara)
        self.escenario.dibujarBrillosEnemigos(nivel.escenario.enemigos, camara)

    def dibujarInterfaz(self, nivel):
        w, h = self.pantalla.get_size()
        self.pantalla.blit(self.tituloCueva.render("Cueva del Velo", True, (184, 236, 255)), (28, 20))
        self.corazones.dibujar(self.pantalla, nivel.vitalidad.puntos, 3, w - 180, 27, self.destelloDanio.activo)
        tramo = next((t.nombre for t in nivel.escenario.tramos if t.inicio <= nivel.rumi.posicion.x < t.fin), "Salida")
        self.pantalla.blit(self.fuente.render(tramo, True, (166, 209, 221)), (28, 62))
        if nivel.dialogoAlpha:
            panel = pygame.Surface((w - 48, 116), pygame.SRCALPHA)
            panel.fill((12, 15, 31, int(225 * nivel.dialogoAlpha / 255)))
            self.pantalla.blit(panel, (24, h - 136))
            from .dibujadorNivelUno import ajustarTexto
            for indice, linea in enumerate(ajustarTexto(nivel.dialogo, self.fuente, w - 96)):
                texto = self.fuente.render(linea, True, (233, 235, 249))
                texto.set_alpha(nivel.dialogoAlpha)
                self.pantalla.blit(texto, (44, h - 126 + indice * 26))
        luz = f"{nivel.luzRestante:.1f}s" if nivel.luzRestante > 0 else "apagada"
        ayuda = f"Espacio: saltar | E: farol/pilar | Luz: {luz} | R: reiniciar | Escape: menú"
        self.pantalla.blit(self.fuente.render(ayuda, True, (158, 217, 213)), (44, h - 49))

    def dibujarEfectoLuzRumi(self, nivel, pies):
        """Anillos finos que se atenúan con la distancia a una fuente de luz."""
        intensidad = nivel.intensidadHaloLuz
        if not nivel.mostrarHaloLuz or intensidad <= 0:
            return
        capa = pygame.Surface((230, 230), pygame.SRCALPHA)
        centro = (115, 115)
        escala = .42 + intensidad * .58
        suavidad = intensidad * intensidad
        for radio, alpha in ((106, 24), (74, 38), (46, 62)):
            pygame.draw.circle(
                capa,
                (255, 176, 85, round(alpha * suavidad)),
                centro,
                round(radio * escala),
                1,
            )
        self.pantalla.blit(capa, (pies[0] - 115, pies[1] - 138))

    def dibujarInterfazFija(self, nivel):
        """La niebla y el mundo se mueven; el texto narrativo permanece legible."""
        w, h = self.pantalla.get_size()
        pygame.draw.rect(self.pantalla, (9, 10, 20), (0, h - 152, w, 152))
        self.dibujarInterfaz(nivel)

    def dibujarFinal(self, nivel):
        if nivel.estado == EstadoJuegoNivel.COMPLETADO:
            ancho, alto = self.pantalla.get_size()
            capa = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            capa.fill((8, 15, 35, 180))
            self.pantalla.blit(capa, (0, 0))
            for indice, texto in enumerate(("Salida de la Cueva", "Rumi encontró la salida y siguió adelante con su propia luz.", "R: repetir | Escape: menú")):
                fuente = self.titulo if indice == 0 else self.fuente
                imagen = fuente.render(texto, True, (223, 244, 255))
                self.pantalla.blit(imagen, ((ancho - imagen.get_width()) // 2, alto // 2 - 55 + indice * 45))
            return
        ancho, alto = self.pantalla.get_size()
        capa = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        capa.fill((32, 8, 20, 175))
        self.pantalla.blit(capa, (0, 0))
        textos = (
            "Rumi ha caído",
            "Velo: «¿Ves? Te dije que fallarías».",
            "R: volver a jugar | Escape: menú",
        )
        for indice, texto in enumerate(textos):
            fuente = self.titulo if indice == 0 else self.fuente
            imagen = fuente.render(texto, True, (255, 224, 235))
            self.pantalla.blit(imagen, ((ancho - imagen.get_width()) // 2, alto // 2 - 58 + indice * 46))
