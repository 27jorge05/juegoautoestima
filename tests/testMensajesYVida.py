import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import unittest

import pygame

from src.presentacion.indicadoresVida import CorazonesVida, DestelloDanio
from src.presentacion.mensajesTemporales import MensajeTemporal
from src.audio.sonidos import SonidosJuego
from src.niveles.narrativaNiveles import NIVEL_DOS_INICIO, NIVEL_UNO_MR_FOX
from src.dominio.frasesVelo import FRASES_DESALENTADORAS
from src.dominio.mensajes import Dialogo, PresentadorMensajes, Relato


class PruebasMensajesYVida(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.pantalla = pygame.display.set_mode((160, 80))
        cls.fuente = pygame.font.SysFont("sans", 16)

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def testMensajeVisibleSieteSegundosYLuegoFundido(self):
        mensaje = MensajeTemporal()
        mensaje.actualizar("hola", 0)
        mensaje.actualizar("hola", 7)
        self.assertEqual(mensaje.alfa, 255)
        mensaje.actualizar("hola", .5)
        self.assertLess(mensaje.alfa, 255)
        self.assertGreater(mensaje.alfa, 0)
        mensaje.actualizar("hola", 1)
        self.assertEqual(mensaje.alfa, 0)

    def testDialogoConservaHablanteYControlaSuPropioTiempo(self):
        mensaje = Dialogo("Sigue adelante.", duracionVisible=2.0, duracionFundido=.5, hablante="Mr. Fox")
        presentador = PresentadorMensajes(mensaje)
        self.assertEqual(presentador.texto, "Mr. Fox: Sigue adelante.")
        presentador.actualizar(2.25)
        self.assertGreater(presentador.alfa, 0)
        self.assertLess(presentador.alfa, 255)
        presentador.mostrar(Relato("El camino se abre."))
        self.assertEqual(presentador.alfa, 255)

    def testDestelloRojoEsTemporal(self):
        destello = DestelloDanio()
        destello.activar()
        self.assertTrue(destello.activo)
        self.pantalla.fill((0, 0, 0))
        destello.dibujar(self.pantalla)
        rojo, verde, azul, _ = self.pantalla.get_at((30, 30))
        self.assertGreater(rojo, verde)
        self.assertGreater(rojo, azul)
        destello.actualizar(destello.duracion)
        self.assertFalse(destello.activo)

    def testCorazonesYNumeroDeVidaSeDibujan(self):
        self.pantalla.fill((0, 0, 0))
        CorazonesVida(self.fuente).dibujar(self.pantalla, 2, 3, 8, 8, True)
        self.assertNotEqual(self.pantalla.get_at((19, 19)), (0, 0, 0, 255))

    def testNuevoTextoReiniciaLosSieteSegundos(self):
        mensaje = MensajeTemporal()
        mensaje.actualizar("primero", 0)
        mensaje.actualizar("primero", 7.5)
        self.assertLess(mensaje.alfa, 255)
        mensaje.actualizar("segundo", 0)
        self.assertEqual(mensaje.alfa, 255)

    def testDerrumbeSeCortaExactamenteACincoSegundos(self):
        class CanalFalso:
            detenido = False

            def stop(self):
                self.detenido = True

        class SonidoFalso:
            def __init__(self, canal):
                self.canal = canal

            def play(self):
                return self.canal

        sonidos = SonidosJuego.__new__(SonidosJuego)
        canal = CanalFalso()
        sonidos.derrumbe = SonidoFalso(canal)
        sonidos.canalDerrumbe = None
        sonidos.tiempoDerrumbe = 0.0
        sonidos.tiempoAmbiente = 0.0
        sonidos.ambienteAtenuando = False
        sonidos.canalAmbiente = None
        sonidos.reproducirDerrumbe()
        self.assertEqual(sonidos.tiempoDerrumbe, 5.0)
        sonidos.actualizar(4.99)
        self.assertFalse(canal.detenido)
        sonidos.actualizar(.01)
        self.assertTrue(canal.detenido)
        self.assertEqual(sonidos.tiempoDerrumbe, 0.0)

    def testMusicaCuevaSeRepiteSinDuplicarCanal(self):
        class SonidoFalso:
            def __init__(self):
                self.repeticiones = []

            def play(self, *, loops):
                self.repeticiones.append(loops)
                return object()

        sonidos = SonidosJuego.__new__(SonidosJuego)
        sonidos.musicaCueva = SonidoFalso()
        sonidos.canalMusicaCueva = None
        sonidos.reproducirMusicaCueva()
        sonidos.reproducirMusicaCueva()
        self.assertEqual(sonidos.musicaCueva.repeticiones, [-1])

    def testDialogosDeMrFoxNoLoLlamanPapaYNieganLasEtiquetasDelVelo(self):
        for dialogo in (NIVEL_UNO_MR_FOX, NIVEL_DOS_INICIO):
            self.assertEqual(dialogo.hablante, "Mr. Fox")
            self.assertNotIn("papá", dialogo.texto.lower())
        self.assertIn("no deciden quién eres", NIVEL_UNO_MR_FOX.texto)

    def testFrasesHostilesSiguenAtribuidasYSinEtiquetasSobreRumi(self):
        for frases in FRASES_DESALENTADORAS.values():
            self.assertTrue(frases)
            for frase in frases:
                self.assertNotIn("eres inútil", frase.lower())
                self.assertNotIn("te abandonaron", frase.lower())
