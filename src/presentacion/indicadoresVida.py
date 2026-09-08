"""Elementos visuales reutilizables para comunicar vida y daño."""

import pygame


class CorazonesVida:
    """Dibuja los puntos de vida; un golpe reciente tiñe el valor actual."""

    def __init__(self, fuente) -> None:
        self.fuente = fuente

    def dibujar(self, pantalla, puntos, maximos, x, y, danioReciente) -> None:
        for indice in range(maximos):
            lleno = indice < puntos
            color = (247, 91, 95) if lleno else (81, 54, 67)
            if danioReciente and indice == puntos:
                color = (255, 78, 66)
            self._dibujarCorazon(pantalla, x + indice * 31, y, color, lleno)
        etiqueta = self.fuente.render(f"{puntos}/{maximos}", True, (255, 90, 82) if danioReciente else (255, 214, 194))
        pantalla.blit(etiqueta, (x + maximos * 31 + 4, y - 3))

    @staticmethod
    def _dibujarCorazon(pantalla, x, y, color, lleno) -> None:
        puntos = [(x + 11, y + 24), (x, y + 12), (x + 1, y + 5), (x + 6, y + 1), (x + 11, y + 6), (x + 16, y + 1), (x + 21, y + 5), (x + 22, y + 12)]
        pygame.draw.polygon(pantalla, color, puntos, 0 if lleno else 2)


class DestelloDanio:
    """Overlay breve de pantalla; no contiene reglas de daño."""

    def __init__(self, duracion=0.24) -> None:
        self.duracion = duracion
        self.tiempoRestante = 0.0

    @property
    def activo(self) -> bool:
        return self.tiempoRestante > 0.0

    def activar(self) -> None:
        self.tiempoRestante = self.duracion

    def actualizar(self, deltaTiempo) -> None:
        self.tiempoRestante = max(0.0, self.tiempoRestante - deltaTiempo)

    def dibujar(self, pantalla) -> None:
        if not self.activo:
            return
        progreso = self.tiempoRestante / self.duracion
        alpha = max(18, round(120 * progreso))
        capa = pygame.Surface(pantalla.get_size(), pygame.SRCALPHA)
        capa.fill((200, 32, 42, alpha))
        pantalla.blit(capa, (0, 0))
