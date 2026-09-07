"""Ciclo de aplicación: inicia, selecciona, actualiza y dibuja escenas."""
import pygame
from .configuracion import ANCHO_VENTANA, ALTO_VENTANA, FOTOGRAMAS_POR_SEGUNDO
from .escenas import Escena
from .escenaMenu import EscenaMenu
from .fabricaNiveles import FabricaNiveles


class Juego:
    def __init__(self, fabrica=None):
        pygame.init()
        pygame.display.set_caption("Rumi: El Barranco del Velo")
        self.pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        self.reloj = pygame.time.Clock()
        self.fabrica = fabrica or FabricaNiveles()
        self.ejecutando = True
        self.escena: Escena = EscenaMenu(self.pantalla, self.iniciarNivel)

    def cambiarEscena(self, escena):
        self.escena.cerrar()
        self.escena = escena

    def iniciarNivel(self, numero):
        self.cambiarEscena(self.fabrica.crear(numero, self.pantalla, self.mostrarMenu))

    def mostrarMenu(self):
        self.cambiarEscena(EscenaMenu(self.pantalla, self.iniciarNivel))

    def ejecutar(self):
        try:
            while self.ejecutando:
                deltaTiempo = min(self.reloj.tick(FOTOGRAMAS_POR_SEGUNDO) / 1000.0, 0.033)
                escenaInicial = self.escena
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        self.ejecutando = False
                    elif self.escena is escenaInicial:
                        self.escena.procesarEvento(evento)
                if not self.ejecutando:
                    break
                self.escena.actualizar(deltaTiempo)
                self.escena.dibujar()
                pygame.display.flip()
        finally:
            self.escena.cerrar()
            pygame.quit()
