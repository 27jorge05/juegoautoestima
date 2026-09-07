import ast
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
from pathlib import Path
import unittest
import pygame
from src.dominio import EntradaJugador, Vector2D
from src.nivelUno import NivelUno
from src.configuracion import GRAVEDAD, VELOCIDAD_RUMI, FUERZA_SALTO
from src.juego import Juego


class PruebasIntegridad(unittest.TestCase):
    def testDominioNoImportaPresentacion(self):
        raiz = Path(__file__).resolve().parents[1]
        for nombre in ('dominio','nivelUno','escenarioNivel','plataformaNivel','enemigosNivel','creadorBarranco'):
            arbol = ast.parse((raiz / 'src' / (nombre+'.py')).read_text())
            for nodo in ast.walk(arbol):
                if isinstance(nodo, ast.Import):
                    self.assertTrue(all(not a.name.startswith('pygame') for a in nodo.names))
                if isinstance(nodo, ast.ImportFrom):
                    self.assertNotIn(nodo.module, ('pygame','dibujadorNivelUno','dibujadorEscenario'))
        main = (raiz / 'main.py').read_text()
        self.assertNotIn('pygame', main)
        juego = (raiz / 'src/juego.py').read_text()
        for detalle in ('rumi','blit(', 'image.load', 'GRAVEDAD', 'SonidosJuego'):
            self.assertNotIn(detalle, juego)

    def testImpulsoSoloUnaVezYCerca(self):
        nivel = NivelUno()
        rumi = nivel.rumi
        rumi.posicion = Vector2D(600,460)
        rumi.estaSaltando = True
        self.assertTrue(nivel.actualizarElementos(True, .01))
        self.assertEqual(rumi.velocidad.y,-830)
        self.assertFalse(nivel.actualizarElementos(True,.01))
        rumi.segundoSaltoUsado = False
        rumi.posicion.x = 2500
        self.assertFalse(nivel.actualizarElementos(True,.01))

    def testCaidaYLimites(self):
        nivel = NivelUno()
        nivel.rumi.posicion = Vector2D(100,900)
        resultado = nivel.actualizar(EntradaJugador(), .01, GRAVEDAD, VELOCIDAD_RUMI,FUERZA_SALTO,840)
        self.assertTrue(resultado.reiniciadoPorCaida)
        self.assertEqual(nivel.rumi.posicion.x,110)
        for x, esperado in ((-100,0),(10000,nivel.escenario.ancho-nivel.rumi.ancho)):
            nivel.rumi.posicion.x = x
            nivel.actualizar(EntradaJugador(),0,GRAVEDAD,VELOCIDAD_RUMI,FUERZA_SALTO,840)
            self.assertEqual(nivel.rumi.posicion.x,esperado)

    def testReinicioLimpiaPresentacionYDibujoNoAvanza(self):
        juego = Juego()
        try:
            juego.iniciarNivel(1)
            escena = juego.escena
            escena.dibujador.registrarSalto(100,580)
            escena.actualizarNivel(EntradaJugador(reiniciar=True),.01)
            self.assertEqual(escena.dibujador.efectosSalto,[])
            escena.dibujador.registrarSalto(100,580)
            escena.dibujar()
            escena.dibujar()
            self.assertEqual(escena.dibujador.efectosSalto[0].tiempoRestante,.26)
            self.assertEqual(escena.dibujador.animacionRumi.tiempoEnPose,0)
            escena.procesarEvento(pygame.event.Event(pygame.KEYDOWN,key=pygame.K_ESCAPE))
            self.assertNotEqual(juego.escena,escena)
        finally:
            juego.escena.cerrar()
            pygame.quit()

    def testCerrarAplicacion(self):
        juego = Juego()
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        juego.ejecutar()
        self.assertFalse(pygame.get_init())
