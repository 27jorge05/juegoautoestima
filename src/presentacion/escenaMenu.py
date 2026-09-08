"""Control y presentación de selección de niveles."""
import pygame
from src.aplicacion.menu import MenuPrincipal
from .dibujadorMenu import DibujadorMenu


class EscenaMenu:
    def __init__(self, pantalla, seleccionarNivel):
        self.menu = MenuPrincipal()
        self.dibujador = DibujadorMenu(pantalla)
        self.seleccionarNivel = seleccionarNivel

    def procesarEvento(self, evento):
        if evento.type != pygame.KEYDOWN:
            return
        movimientos = {
            pygame.K_LEFT: (-1, 0), pygame.K_a: (-1, 0),
            pygame.K_RIGHT: (1, 0), pygame.K_d: (1, 0),
            pygame.K_UP: (0, -1), pygame.K_w: (0, -1),
            pygame.K_DOWN: (0, 1), pygame.K_s: (0, 1),
        }
        if evento.key in movimientos:
            self.menu.moverSeleccion(*movimientos[evento.key])
        elif evento.key == pygame.K_SPACE and self.menu.seleccionarNivel():
            self.seleccionarNivel(self.menu.opcionSeleccionada.numero)

    def actualizar(self, deltaTiempo):
        pass

    def dibujar(self):
        self.dibujador.dibujar(self.menu)

    def cerrar(self):
        pass
