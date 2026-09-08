"""Pinta la configuración visual que entrega cada objeto `NieblaNivel`."""

import pygame

from src.mundo.elementosNivel import FuenteLuzNiebla, NieblaNivel, TipoNiebla


class DibujadorNiebla:
    """Renderizador genérico: las formas y la densidad las decide la niebla."""

    ESTILOS = {
        TipoNiebla.AZUL: ((84, 124, 173), 96),
        TipoNiebla.VIOLETA: ((80, 66, 132), 108),
        TipoNiebla.OSCURA: ((15, 21, 52), 138),
    }

    def __init__(self, pantalla: pygame.Surface) -> None:
        self.pantalla = pantalla
        self._claveNubes = None
        self._capasNubes: tuple[tuple[pygame.Surface, int], ...] = ()
        self._mascarasLuz: dict[tuple[int, float], pygame.Surface] = {}
        self._resplandoresLuz: dict[tuple[int, tuple[int, int, int], float], pygame.Surface] = {}

    def dibujar(self, niebla: NieblaNivel, fuentes: list[FuenteLuzNiebla], camara: float) -> None:
        if not niebla.activa:
            return
        ancho, alto = self.pantalla.get_size()
        capa = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        capa.fill((22, 29, 61, niebla.configuracion.opacidadBase))
        paso = niebla.configuracion.configuracionNubes.pasoHorizontal
        for indice, (nubes, velocidad) in enumerate(self._obtenerCapasNubes(niebla, ancho, alto)):
            avance = int(camara * (0.11 + indice * 0.04) + niebla.tiempoAnimacion * velocidad)
            capa.blit(nubes, (-paso - avance % paso, 0))
        self._abrirClaros(capa, fuentes, camara)
        self.pantalla.blit(capa, (0, 0))

    def _obtenerCapasNubes(
        self, niebla: NieblaNivel, ancho: int, alto: int
    ) -> tuple[tuple[pygame.Surface, int], ...]:
        configuracion = niebla.configuracion.configuracionNubes
        clave = (ancho, alto, niebla.configuracion.variantesVisuales, configuracion)
        if clave == self._claveNubes:
            return self._capasNubes
        capas = []
        paso = configuracion.pasoHorizontal
        for grupo in configuracion.grupos:
            if grupo.variante not in niebla.configuracion.variantesVisuales:
                continue
            color, alpha = self.ESTILOS[grupo.variante]
            superficie = pygame.Surface((ancho + paso * 2, alto), pygame.SRCALPHA)
            for fila, y in enumerate(
                range(-42 - grupo.desfaseY, alto + configuracion.pasoVertical, configuracion.pasoVertical)
            ):
                corrimientoFila = (fila % 2) * (paso // 2) + grupo.desfaseX
                for baseX in range(-paso, ancho + paso * 2, paso):
                    for dx, dy, radio in grupo.nubes:
                        pygame.draw.circle(
                            superficie,
                            (*color, alpha),
                            (baseX + paso + corrimientoFila + dx, y + dy),
                            radio,
                        )
            capas.append((superficie, grupo.velocidad))
        self._claveNubes = clave
        self._capasNubes = tuple(capas)
        return self._capasNubes

    def _abrirClaros(
        self, capa: pygame.Surface, fuentes: list[FuenteLuzNiebla], camara: float
    ) -> None:
        for fuente in fuentes:
            radio = max(1, round(fuente.radio))
            mascara = self._obtenerMascaraLuz(radio, fuente.fuerzaClaro)
            resplandor = self._obtenerResplandorLuz(
                radio, fuente.color, fuente.fuerzaClaro
            )
            x = round(fuente.posicion.x - camara)
            y = round(fuente.posicion.y)
            capa.blit(mascara, (x - radio - 1, y - radio - 1), special_flags=pygame.BLEND_RGBA_SUB)
            capa.blit(resplandor, (x - radio - 1, y - radio - 1))

    def _obtenerMascaraLuz(self, radio: int, fuerza: float) -> pygame.Surface:
        clave = (radio, fuerza)
        if clave in self._mascarasLuz:
            return self._mascarasLuz[clave]
        lado = radio * 2 + 2
        mascara = pygame.Surface((lado, lado), pygame.SRCALPHA)
        centro = (radio + 1, radio + 1)
        for escala, alpha in ((1.0, 38), (.82, 64), (.62, 102), (.42, 150), (.24, 210)):
            pygame.draw.circle(
                mascara,
                (0, 0, 0, min(255, round(alpha * fuerza))),
                centro,
                round(radio * escala),
            )
        self._mascarasLuz[clave] = mascara
        return mascara

    def _obtenerResplandorLuz(
        self, radio: int, color: tuple[int, int, int], fuerza: float
    ) -> pygame.Surface:
        clave = (radio, color, fuerza)
        if clave in self._resplandoresLuz:
            return self._resplandoresLuz[clave]
        lado = radio * 2 + 2
        resplandor = pygame.Surface((lado, lado), pygame.SRCALPHA)
        centro = (radio + 1, radio + 1)
        for escala, alpha in ((.76, 14), (.52, 28), (.30, 55), (.14, 100)):
            pygame.draw.circle(
                resplandor,
                (*color, min(180, round(alpha * fuerza))),
                centro,
                round(radio * escala),
            )
        self._resplandoresLuz[clave] = resplandor
        return resplandor
