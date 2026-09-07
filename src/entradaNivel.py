"""Traducción del teclado a intenciones del jugador."""
import pygame
from .dominio import EntradaJugador


class ControlNivel:
    def __init__(self):
        self.pendientes = set()

    def procesarEvento(self, evento):
        if evento.type == pygame.KEYDOWN:
            self.pendientes.add(evento.key)

    def leer(self):
        teclas = pygame.key.get_pressed()
        entrada = EntradaJugador(
            izquierda=bool(teclas[pygame.K_a] or teclas[pygame.K_LEFT]),
            derecha=bool(teclas[pygame.K_d] or teclas[pygame.K_RIGHT]),
            saltar=bool(self.pendientes & {pygame.K_SPACE, pygame.K_w, pygame.K_UP}),
            interactuar=pygame.K_e in self.pendientes,
            usarGarras=pygame.K_f in self.pendientes,
            reiniciar=pygame.K_r in self.pendientes,
        )
        self.pendientes.clear()
        return entrada
