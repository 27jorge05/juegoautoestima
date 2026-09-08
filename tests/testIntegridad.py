import ast
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
from pathlib import Path
import unittest
import pygame
from src.dominio.dominio import EntradaJugador, Vector2D
from src.niveles.nivelUno import NivelUno
from src.aplicacion.configuracion import GRAVEDAD, VELOCIDAD_RUMI, FUERZA_SALTO
from src.aplicacion.juego import Juego


class PruebasIntegridad(unittest.TestCase):
    def testDominioNoImportaPresentacion(self):
        raiz = Path(__file__).resolve().parents[1]
        modulosDominio = (
            'dominio/dominio.py',
            'dominio/plataformaNivel.py',
            'dominio/enemigosNivel.py',
            'mundo/escenarioNivel.py',
            'mundo/creadorBarranco.py',
            'niveles/nivelUno.py',
        )
        for ruta in modulosDominio:
            arbol = ast.parse((raiz / 'src' / ruta).read_text())
            for nodo in ast.walk(arbol):
                if isinstance(nodo, ast.Import):
                    self.assertTrue(all(not a.name.startswith('pygame') for a in nodo.names))
                if isinstance(nodo, ast.ImportFrom):
                    self.assertNotIn(nodo.module, ('pygame','dibujadorNivelUno','dibujadorEscenario'))
        main = (raiz / 'main.py').read_text()
        self.assertNotIn('pygame', main)
        juego = (raiz / 'src/aplicacion/juego.py').read_text()
        for detalle in ('rumi','blit(', 'image.load', 'GRAVEDAD', 'SonidosJuego'):
            self.assertNotIn(detalle, juego)

    def testNivelesYMundoNoSeAcoplanEntreSi(self):
        """Cada nivel elige su mundo; los datos comunes viven en dominio."""
        raiz = Path(__file__).resolve().parents[1] / 'src'
        constructores = {
            'niveles/nivelUno.py': 'src.mundo.creadorBarranco',
            'niveles/nivelDos.py': 'src.mundo.creadorEspejos',
            'niveles/nivelTres.py': 'src.mundo.creadorCueva',
        }
        for ruta, importacionEsperada in constructores.items():
            codigo = (raiz / ruta).read_text()
            self.assertIn(importacionEsperada, codigo)
            self.assertNotIn('from .nivel', codigo)
            self.assertNotIn('from src.niveles.nivel', codigo)

        for ruta in (
            'mundo/creadorBarranco.py',
            'mundo/creadorEspejos.py',
            'mundo/elementosNivel.py',
        ):
            self.assertNotIn('src.niveles', (raiz / ruta).read_text())

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
