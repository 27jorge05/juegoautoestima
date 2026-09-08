"""Coordinación reutilizable de entrada, dominio, dibujo y audio."""
import pygame
from math import sin
from src.aplicacion.entradaNivel import ControlNivel
from src.audio.sonidos import SonidosJuego, RitmoPasos
from src.dominio.eventosNivel import TipoEventoNivel
from src.aplicacion.configuracion import GRAVEDAD, VELOCIDAD_RUMI, FUERZA_SALTO, ALTO_VENTANA
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
        self.tiempoEscena = 0.0
        self.sacudidaVisual = 0
        if self.nivel.recursos.identificadorMapa == "cueva_del_velo":
            self.sonidos.reproducirMusicaCueva()
        else:
            self.sonidos.reproducirAmbienteInicial()

    def procesarEvento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.volverMenu()
        else:
            self.control.procesarEvento(evento)

    def actualizar(self, deltaTiempo):
        self.tiempoEscena += deltaTiempo
        entrada = self.control.leer()
        self.actualizarNivel(entrada, deltaTiempo)
        camaraBase = calcularCamara(self.nivel.rumi.posicion.x, self.nivel.escenario.ancho, self.pantalla.get_width())
        intensidad = getattr(self.nivel, "temblor", 0.0)
        self.sacudidaVisual = round(sin(self.tiempoEscena * 52.0) * min(14.0, intensidad * 3.0)) if intensidad > 0 else 0
        limite = max(0.0, self.nivel.escenario.ancho - self.pantalla.get_width())
        self.desplazamientoCamara = max(0.0, min(limite, camaraBase))
        self.dibujador.actualizar(self.nivel, deltaTiempo)

    def dibujar(self):
        self.dibujador.dibujar(self.nivel, self.desplazamientoCamara)
        if self.sacudidaVisual:
            fotograma = self.pantalla.copy()
            self.pantalla.fill((9, 10, 20))
            self.pantalla.blit(fotograma, (self.sacudidaVisual, -self.sacudidaVisual // 2))
            dibujarInterfazFija = getattr(self.dibujador, "dibujarInterfazFija", None)
            if dibujarInterfazFija is not None:
                dibujarInterfazFija(self.nivel)

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
        if resultado.eventoIniciado is not None:
            if resultado.eventoIniciado.tipo == TipoEventoNivel.TERREMOTO:
                self.sonidos.reproducirDerrumbe(resultado.eventoIniciado.duracion)
        self.sonidos.actualizar(deltaTiempo)
