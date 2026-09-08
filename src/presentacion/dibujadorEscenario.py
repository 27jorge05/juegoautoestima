"""Render del escenario: fondo, terreno y objetos ambientales."""

from __future__ import annotations

from pathlib import Path

import pygame

from .cargadorRecursos import CargadorRecursosNivel
from src.aplicacion.configuracion import ALTO_VENTANA, ANCHO_VENTANA
from src.mundo.elementosNivel import FarolNiebla, NieblaNivel, RocaImpulso
from src.mundo.escenarioNivel import EscenarioNivel
from src.mundo.recursosNivel import COLORES_TERRENO, TINTES_TERRENO
from src.dominio.plataformaNivel import TipoDecoracion
from .parallax import posicionesMosaicos
from src.dominio.enemigosNivel import TipoEnemigo


class DibujadorEscenario:
    """Responsable visual exclusivo del escenario, nunca de Rumi o la narrativa."""

    def __init__(self, pantalla: pygame.Surface, recursos) -> None:
        self.pantalla = pantalla
        imagenes = CargadorRecursosNivel(Path(__file__).resolve().parents[2]).cargar(
            recursos
        )
        self.fondo = imagenes.fondo
        self.fondoEspejo = pygame.transform.flip(self.fondo, True, False) if self.fondo else None
        self.texturas = {}
        self.spritesEnemigos = {}
        self.spritesEnemigosOscuros = {}
        if imagenes.enemigos:
            for tipo, area in {
                TipoEnemigo.SUSURRO: (70, 20, 300, 240),
                TipoEnemigo.ESPEJILLA: (70, 265, 300, 220),
            }.items():
                recorte = imagenes.enemigos.subsurface(area).copy()
                self.spritesEnemigos[tipo] = pygame.transform.scale(recorte, (72, 58))
                self.spritesEnemigosOscuros[tipo] = self._oscurecerSprite(
                    self.spritesEnemigos[tipo]
                )
        self.suelo = imagenes.suelo
        self.rocas = imagenes.rocas
        self.enemigos = imagenes.enemigos
        self.renderizadores = {
            NieblaNivel: self.dibujarNiebla,
            RocaImpulso: self.dibujarRoca,
            FarolNiebla: self.dibujarFarol,
        }

    def dibujarMundo(
        self, escenario: EscenarioNivel, padre, desplazamientoCamara: float
    ) -> None:
        if self.fondo is None:
            self.pantalla.fill((18, 27, 40))
        else:
            for indice, x in posicionesMosaicos(desplazamientoCamara, 0.2, self.fondo.get_width(), self.pantalla.get_width()):
                self.pantalla.blit(self.fondo if indice % 2 == 0 else self.fondoEspejo, (x, 0))
        self.dibujarPlataformas(escenario.plataformas, desplazamientoCamara)
        self.dibujarElementos(escenario.elementos, "mundo", padre, desplazamientoCamara)
        self.dibujarDecoracion(escenario.decoraciones, desplazamientoCamara)
        self.dibujarEnemigos(escenario.enemigos, desplazamientoCamara)

    def dibujarFrente(
        self, escenario: EscenarioNivel, padre, desplazamientoCamara: float
    ) -> None:
        self.dibujarElementos(
            escenario.elementos, "frente", padre, desplazamientoCamara
        )

    def dibujarPlataformas(self, plataformas, desplazamientoCamara: float) -> None:
        for plataformaNivel in plataformas:
            plataforma = plataformaNivel.rectangulo
            rectangulo = pygame.Rect(
                int(plataforma.x - desplazamientoCamara),
                int(plataforma.y),
                int(plataforma.ancho),
                int(plataforma.alto),
            )
            if not rectangulo.colliderect(self.pantalla.get_rect()):
                continue
            color = COLORES_TERRENO[plataformaNivel.tipo]
            pygame.draw.rect(self.pantalla, color, rectangulo)
            if self.suelo is not None:
                alturaTextura = max(160, rectangulo.height)
                clave = (plataformaNivel.tipo, alturaTextura)
                if clave not in self.texturas:
                    ancho = max(1, round(self.suelo.get_width() * alturaTextura / self.suelo.get_height()))
                    textura = pygame.transform.scale(self.suelo, (ancho, alturaTextura))
                    textura.fill((*TINTES_TERRENO[plataformaNivel.tipo], 255), special_flags=pygame.BLEND_RGBA_MULT)
                    self.texturas[clave] = textura
                textura = self.texturas[clave]
                clipAnterior = self.pantalla.get_clip()
                self.pantalla.set_clip(rectangulo.clip(clipAnterior))
                primerTile = max(0, (-rectangulo.x) // textura.get_width())
                for x in range(rectangulo.x + primerTile * textura.get_width(), min(rectangulo.right, self.pantalla.get_width()), textura.get_width()):
                    self.pantalla.blit(textura, (x, rectangulo.y))
                self.pantalla.set_clip(clipAnterior)
            pygame.draw.line(self.pantalla, color, rectangulo.topleft, (rectangulo.right - 1, rectangulo.top), 3)

    def dibujarEnemigos(self, enemigos, camara):
        for enemigo in enemigos:
            x, y = int(enemigo.posicion.x - camara), int(enemigo.posicion.y)
            if not -100 < x < self.pantalla.get_width() + 100:
                continue
            if enemigo.liberado:
                pygame.draw.circle(self.pantalla, (158, 235, 217), (x + 16, y + 20), 9)
                pygame.draw.circle(self.pantalla, (255, 244, 155), (x + 16, y + 20), 4)
            elif enemigo.tipo in self.spritesEnemigos:
                sprite = (
                    self.spritesEnemigosOscuros[enemigo.tipo]
                    if enemigo.oscuro
                    else self.spritesEnemigos[enemigo.tipo]
                )
                self.pantalla.blit(sprite, (x - 20, y - 12))
            else:
                pygame.draw.circle(self.pantalla, (61, 44, 79), (x + 16, y + 20), 20)
            if enemigo.tipo == TipoEnemigo.ESPEJILLA and enemigo.mostrarIndicadorEstado:
                # La ilusión es presentación: nunca entra en geometriaSuelo.
                color = (112, 220, 197) if enemigo.liberado else (131, 104, 174)
                pygame.draw.line(self.pantalla, color, (x - 25, y - 30), (x + 65, y - 30), 2)

    def dibujarBrillosEnemigos(self, enemigos, camara: float) -> None:
        """Capa posterior a la niebla para revelar solo criaturas iluminadas."""
        for enemigo in enemigos:
            if not enemigo.alumbrado:
                continue
            x, y = int(enemigo.posicion.x - camara), int(enemigo.posicion.y)
            if -100 < x < self.pantalla.get_width() + 100:
                self._dibujarResplandorEnemigo(x, y, enemigo.intensidadLuz)

    def _dibujarResplandorEnemigo(self, x: int, y: int, intensidad: float) -> None:
        resplandor = pygame.Surface((92, 82), pygame.SRCALPHA)
        centro = (46, 42)
        for radio, alpha in ((36, 12), (26, 23), (16, 42)):
            pygame.draw.circle(
                resplandor,
                (255, 208, 128, min(96, round(alpha * intensidad))),
                centro,
                radio,
            )
        self.pantalla.blit(resplandor, (x - 30, y - 21))

    @staticmethod
    def _oscurecerSprite(sprite: pygame.Surface) -> pygame.Surface:
        """Oscurece solo los píxeles visibles y conserva el alfa del recorte."""
        oscuro = sprite.copy()
        oscuro.fill((52, 62, 94), special_flags=pygame.BLEND_RGB_MULT)
        return oscuro

    def dibujarElementos(
        self, elementos, capa: str, padre, desplazamientoCamara: float
    ) -> None:
        for indice, elemento in enumerate(elementos):
            if getattr(elemento, "capaVisual", "mundo") == capa:
                renderizador = self.renderizadores.get(type(elemento))
                if renderizador:
                    renderizador(elemento, indice, padre, desplazamientoCamara)

    def dibujarRoca(
        self, roca: RocaImpulso, indice: int, padre, desplazamientoCamara: float
    ) -> None:
        x, y = int(roca.rectangulo.x - desplazamientoCamara), int(roca.rectangulo.y)
        if self.rocas:
            configuracion = roca.configuracion
            imagen = pygame.transform.scale(
                self.rocas[indice % len(self.rocas)],
                (configuracion.anchoVisual, configuracion.altoVisual),
            )
            self.pantalla.blit(imagen, (x - 21, y - 76))
            if configuracion.brillo:
                brillo = pygame.Surface((configuracion.anchoVisual, configuracion.altoVisual), pygame.SRCALPHA)
                pygame.draw.ellipse(brillo, (94, 233, 255, 115), (16, 22, configuracion.anchoVisual - 32, configuracion.altoVisual - 42), 4)
                self.pantalla.blit(brillo, (x - 21, y - 76))

    def dibujarFarol(self, farol: FarolNiebla, indice: int, padre, desplazamientoCamara: float) -> None:
        x, y = int(farol.rectangulo.x - desplazamientoCamara), int(farol.rectangulo.y)
        if farol.emiteLuz:
            resplandor = pygame.Surface((150, 150), pygame.SRCALPHA)
            for radio, alpha in ((66, 18), (48, 28), (30, 48)):
                pygame.draw.circle(resplandor, (255, 181, 83, alpha), (75, 75), radio)
            self.pantalla.blit(resplandor, (x - 54, y - 54))
        pygame.draw.rect(self.pantalla, (68, 79, 95), (x + 16, y + 28, 10, 52), border_radius=3)
        pygame.draw.circle(self.pantalla, (255, 186, 91), (x + 21, y + 21), 17)
        pygame.draw.circle(self.pantalla, (255, 245, 192), (x + 21, y + 21), 8)

    def dibujarNiebla(
        self, niebla: NieblaNivel, indice: int, padre, desplazamientoCamara: float
    ) -> None:
        if not niebla.activa:
            return
        capa = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)
        inicio = int(niebla.rectangulo.x - desplazamientoCamara)
        pygame.draw.rect(
            capa,
            (8, 13, 27, niebla.configuracion.opacidadBase),
            (inicio, 0, int(niebla.rectangulo.ancho), ALTO_VENTANA),
        )
        capa.set_clip(pygame.Rect(inicio, 0, int(niebla.rectangulo.ancho), ALTO_VENTANA))
        for profundidad, alpha in ((0.22, 40), (0.46, 56), (0.75, 74)):
            avance = int(niebla.tiempoAnimacion * (18 + profundidad * 25))
            for numero in range(13):
                x = inicio + (numero * 155 - avance) % (ANCHO_VENTANA + 220) - 110
                y, radio = int(115 + (numero % 5) * 118 + profundidad * 28), int(
                    78 + profundidad * 62
                )
                pygame.draw.circle(capa, (82, 73, 111, alpha), (x, y), radio)
        padreX, padreY = int(padre.posicion.x - desplazamientoCamara), int(
            padre.posicion.y + 25
        )
        claro = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)
        pygame.draw.circle(claro, (0, 0, 0, 145), (padreX, padreY), 175)
        capa.blit(claro, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self.pantalla.blit(capa, (0, 0))

    def dibujarDecoracion(self, decoraciones, desplazamientoCamara: float) -> None:
        for decoracion in decoraciones:
            x, y = int(decoracion.x - desplazamientoCamara), int(decoracion.y)
            if x < -100 or x > ANCHO_VENTANA + 100:
                continue
            if decoracion.tipo == TipoDecoracion.HUELLA:
                capa = pygame.Surface((28, 26), pygame.SRCALPHA)
                color = (183, 220, 198, 125)
                pygame.draw.ellipse(capa, color, (9, 11, 11, 10))
                for dedo in ((5, 8), (11, 4), (17, 4), (22, 8)):
                    pygame.draw.circle(capa, color, dedo, 3)
                self.pantalla.blit(capa, (x - 14, y - 13))
            elif decoracion.tipo == TipoDecoracion.CRISTAL:
                pygame.draw.polygon(self.pantalla, (102, 198, 213), [(x, y - 34), (x + 12, y - 12), (x, y), (x - 10, y - 12)])
            elif decoracion.tipo == TipoDecoracion.ARBUSTO:
                for dx in (-15, 0, 15):
                    pygame.draw.circle(self.pantalla, (32, 83, 86), (x + dx, y - 10), 17)
            elif decoracion.tipo == TipoDecoracion.ARBOL:
                pygame.draw.rect(self.pantalla, (32, 39, 58), (x - 12, y - 180, 24, 180))
                pygame.draw.circle(self.pantalla, (22, 52, 66), (x, y - 175), 62)
