import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
import unittest
from pathlib import Path
import pygame
from src.camara import calcularCamara
from src.animaciones import HojaSprites, ReproductorAnimacion, DefinicionAnimacion, crearAnimacionRumi
from src.entradaNivel import ControlNivel
from src.fabricaNiveles import FabricaNiveles
from src.escenaMenu import EscenaMenu


class PruebasPresentacion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.pantalla = pygame.display.set_mode((1280, 720))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def testDialogoSeAjustaAlPanel(self):
        from src.dibujadorNivelUno import ajustarTexto
        fuente = pygame.font.SysFont("sans", 23)
        texto = "¡El suelo tiembla! Papá te impulsa al otro lado: Te encontraré más adelante."
        lineas = ajustarTexto(texto, fuente, 400)
        self.assertEqual(" ".join(lineas), texto)
        self.assertTrue(all(fuente.size(linea)[0] <= 400 for linea in lineas))

    def testRecorteSueloUsaFranjaCentral(self):
        from src.cargadorRecursos import CargadorRecursosNivel
        from src.recursosNivel import crearRecursosBarrancoVelo
        cargador = CargadorRecursosNivel(Path(__file__).resolve().parents[1])
        seleccion = crearRecursosBarrancoVelo()
        original = cargador.cargarImagen(seleccion.rutaSuelo)
        suelo = cargador.cargarSuelo(seleccion)
        self.assertEqual(suelo.get_width(), original.get_width() - 2 * (original.get_width() // 12))
        self.assertEqual(suelo.get_height(), original.get_height() - seleccion.recorteSuperiorSuelo - seleccion.recorteInferiorSuelo)

    def testCamaraLimitada(self):
        self.assertEqual(calcularCamara(-100, 5000, 1280), 0)
        self.assertEqual(calcularCamara(900, 5000, 1280), 540)
        self.assertEqual(calcularCamara(9000, 5000, 1280), 3720)
        self.assertEqual(calcularCamara(900, 600, 1280), 0)

    def testFabricaInyectable(self):
        fabrica = FabricaNiveles({2: lambda pantalla, volver: 'otra escena'})
        self.assertEqual(fabrica.crear(2, None, None), 'otra escena')
        with self.assertRaises(ValueError):
            fabrica.crear(3, None, None)

    def testMenuSoloAbreDesbloqueados(self):
        seleccionados = []
        escena = EscenaMenu(self.pantalla, seleccionados.append)
        escena.menu.indiceSeleccionado = 2
        espacio = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
        escena.procesarEvento(espacio)
        self.assertEqual(seleccionados, [])
        escena.menu.indiceSeleccionado = 0
        escena.procesarEvento(espacio)
        self.assertEqual(seleccionados, [1])

    def testEntradaConsumePulsacion(self):
        control = ControlNivel()
        control.procesarEvento(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
        self.assertTrue(control.leer().saltar)
        self.assertFalse(control.leer().saltar)

    def testDefinicionRechazaAnimacionInvalida(self):
        for casillas, duracion, espera in (((),.1,0), ((0,),0,0), ((0,),.1,-1)):
            with self.assertRaises(ValueError):
                DefinicionAnimacion(casillas,duracion,espera)

    def testEsperaSoloCuentaExcedente(self):
        animacion = ReproductorAnimacion(None, {'reposo': DefinicionAnimacion((0,1,2), 0.2, 1.0)})
        animacion.actualizar('reposo', 1.1)
        self.assertEqual(animacion.indiceActual, 0)
        animacion.actualizar('reposo', 0.11)
        self.assertEqual(animacion.indiceActual, 1)
        animacion.reiniciar()
        self.assertEqual(animacion.indiceActual, 0)
        with self.assertRaises(ValueError):
            animacion.actualizar('reposo', -1)

    def testFrameYAnclajeReal(self):
        ruta = Path(__file__).resolve().parents[1] / 'assets/characters/rumi/rumi_sprite_sheet_v3.png'
        animacion = crearAnimacionRumi(ruta)
        self.assertEqual(len(animacion.hoja.fotogramas), 12)
        frame = animacion.hoja.obtenerFotograma(0, (132,118), True)
        self.assertLessEqual(frame.get_width(), 132)
        self.assertLessEqual(frame.get_height(), 118)
        destino = animacion.dibujarAnclado(self.pantalla, (200,580), (132,118), True)
        self.assertEqual(destino.midbottom, (200,580))
        inverso = animacion.hoja.obtenerFotograma(0,(132,118),False)
        self.assertEqual(pygame.image.tobytes(inverso,'RGBA'), pygame.image.tobytes(pygame.transform.flip(frame,True,False),'RGBA'))
        with self.assertRaises(ValueError):
            HojaSprites(ruta, 0, 3)
