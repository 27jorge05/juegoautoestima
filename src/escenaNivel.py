"""Coordinación reutilizable de entrada, dominio, dibujo y audio."""
import pygame
from .entradaNivel import ControlNivel
from .sonidos import SonidosJuego, RitmoPasos
from .configuracion import GRAVEDAD, VELOCIDAD_RUMI, FUERZA_SALTO, ALTO_VENTANA
from .camara import calcularCamara


class EscenaNivel:
    def __init__(self, pantalla, volverMenu, crearNivel, crearDibujador):
        self.pantalla = pantalla
        self.volverMenu = volverMenu
        self.nivel = crearNivel()
        self.dibujador = crearDibujador(pantalla, self.nivel.recursos)
        self.control = ControlNivel()
        self.sonidos = SonidosJuego()
        self.ritmoPasos = RitmoPasos()
        self.desplazamientoCamara = 0.0
        self.sonidos.reproducirAmbienteInicial()

    def procesarEvento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.volverMenu()
        else:
            self.control.procesarEvento(evento)

    def actualizar(self, deltaTiempo):
        entrada = self.control.leer()
        self.actualizarNivel(entrada, deltaTiempo)
        self.desplazamientoCamara = calcularCamara(self.nivel.rumi.posicion.x, self.nivel.escenario.ancho, self.pantalla.get_width())
        self.dibujador.actualizar(self.nivel, deltaTiempo)

    def dibujar(self):
        self.dibujador.dibujar(self.nivel, self.desplazamientoCamara)

    def cerrar(self):
        self.control.pendientes.clear()
        if pygame.mixer.get_init():
            pygame.mixer.stop()

    def actualizarNivel(self, entrada, deltaTiempo: float) -> None:
        """Coordina efectos externos; las reglas físicas viven en el dominio del nivel."""
        resultado = self.nivel.actualizar(
            entrada,
            deltaTiempo,
            GRAVEDAD,
            VELOCIDAD_RUMI,
            FUERZA_SALTO,
            ALTO_VENTANA + 120,
        )
        if getattr(self.nivel, 'terremotoIniciado', False):
            self.sonidos.reproducirDerrumbe()
            self.nivel.terremotoIniciado = False
        if resultado.golpeRecibido:
            self.dibujador.registrarGolpe()
        if entrada.reiniciar or resultado.reiniciadoPorCaida:
            self.dibujador.reiniciar()
            self.ritmoPasos = RitmoPasos()
            return
        rumi = self.nivel.rumi
        if resultado.saltoIniciado:
            self.dibujador.registrarSalto(rumi.posicion.x + 21, rumi.posicion.y + rumi.alto)
            self.sonidos.reproducirSalto()
        if resultado.impulsoRoca:
            self.dibujador.registrarSalto(rumi.posicion.x + 21, rumi.posicion.y + rumi.alto)
            self.sonidos.reproducirSalto()
        if resultado.aterrizaje or resultado.golpeRecibido:
            self.sonidos.reproducirAterrizaje()
        if self.ritmoPasos.actualizar(abs(rumi.velocidad.x) > 1.0, rumi.estaEnSuelo, deltaTiempo):
            self.sonidos.reproducirPaso()
        if resultado.terremotoIniciado or resultado.nivelCompletado:
            self.sonidos.reproducirDerrumbe()
        self.sonidos.actualizar(deltaTiempo)
