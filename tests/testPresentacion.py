import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import pygame
from src.presentacion.camara import calcularCamara
from src.presentacion.animaciones import HojaSprites, ReproductorAnimacion, DefinicionAnimacion, crearAnimacionRumi
from src.aplicacion.entradaNivel import ControlNivel
from src.aplicacion.fabricaNiveles import FabricaNiveles
from src.presentacion.escenaMenu import EscenaMenu
from src.presentacion.dibujadorMenu import DibujadorMenu
from src.aplicacion.menu import MenuPrincipal
from src.presentacion.dibujadorNivelTres import DibujadorNivelTres
from src.presentacion.dibujadorEscenario import DibujadorEscenario
from src.niveles.nivelTres import NivelTres
from src.presentacion.dibujadorNiebla import DibujadorNiebla
from src.presentacion.dibujadorDialogoCriatura import dibujarBurbujaDialogoCriatura
from src.mundo.elementosNivel import (
    ConfiguracionNiebla,
    FuenteLuzNiebla,
    NieblaNivel,
    NUBES_NIEBLA_DENSA,
)
from src.dominio.dominio import RectanguloLogico, Vector2D


class PruebasPresentacion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.pantalla = pygame.display.set_mode((1280, 720))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def testDialogoSeAjustaAlPanel(self):
        from src.presentacion.dibujadorNivelUno import ajustarTexto
        fuente = pygame.font.SysFont("sans", 23)
        texto = "¡El suelo tiembla! Mr. Fox te impulsa al otro lado: Te encontraré más adelante."
        lineas = ajustarTexto(texto, fuente, 400)
        self.assertEqual(" ".join(lineas), texto)
        self.assertTrue(all(fuente.size(linea)[0] <= 400 for linea in lineas))

    def testRecorteSueloUsaFranjaCentral(self):
        from src.presentacion.cargadorRecursos import CargadorRecursosNivel
        from src.mundo.recursosNivel import crearRecursosBarrancoVelo
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

    def testFabricaIncluyeNivelTres(self):
        fabrica = FabricaNiveles()
        self.assertIn(3, fabrica.creadores)

    def testMenuSoloAbreDesbloqueados(self):
        seleccionados = []
        escena = EscenaMenu(self.pantalla, seleccionados.append)
        escena.menu.indiceSeleccionado = 3
        espacio = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
        escena.procesarEvento(espacio)
        self.assertEqual(seleccionados, [])
        escena.menu.indiceSeleccionado = 0
        escena.procesarEvento(espacio)
        self.assertEqual(seleccionados, [1])

    def testMenuDibujaMedallonesDeZorroConNumero(self):
        menu = MenuPrincipal()
        DibujadorMenu(self.pantalla).dibujar(menu)
        # El centro lleva el número y el borde mantiene la paleta del zorro.
        self.assertEqual(self.pantalla.get_at((472, 235))[:3], (52, 43, 51))
        self.assertEqual(
            self.pantalla.get_at((472, 192))[:3], DibujadorMenu.COLOR_ZORRO
        )

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

    def testCuevaDibujaNieblaYFarolesSinMrFox(self):
        nivel = NivelTres()
        dibujador = DibujadorNivelTres(self.pantalla, nivel.recursos)
        dibujador.dibujar(nivel, 0)
        self.assertIsNone(nivel.padre)
        self.assertGreater(nivel.niebla.configuracion.opacidadBase, 220)

    def testGrupoDeNubesSeSolapaSinHuecosHorizontales(self):
        grupo = NUBES_NIEBLA_DENSA.grupos[0].nubes
        for actual, siguiente in zip(grupo, grupo[1:]):
            distancia = ((siguiente[0] - actual[0]) ** 2 + (siguiente[1] - actual[1]) ** 2) ** .5
            self.assertLess(distancia, actual[2] + siguiente[2])
        primera, ultima = grupo[0], grupo[-1]
        self.assertLessEqual(ultima[0] - primera[0], NUBES_NIEBLA_DENSA.pasoHorizontal)

    def testNieblaReutilizaCapasGrandesConPatronesDistintos(self):
        nivel = NivelTres()
        dibujador = DibujadorNiebla(self.pantalla)
        dibujador.dibujar(nivel.niebla, [], 0)
        capasIniciales = dibujador._capasNubes
        self.assertEqual(len(capasIniciales), len(NUBES_NIEBLA_DENSA.grupos))
        self.assertTrue(all(capa.get_width() > self.pantalla.get_width() for capa, _ in capasIniciales))
        self.assertEqual(len({grupo.nubes for grupo in NUBES_NIEBLA_DENSA.grupos}), 3)
        dibujador.dibujar(nivel.niebla, [], 40)
        self.assertIs(capasIniciales, dibujador._capasNubes)

    def testDialogoDeCriaturaUsaBurbujaOvalada(self):
        self.pantalla.fill((0, 0, 0))
        fuente = pygame.font.SysFont("sans", 18)
        ovalo = dibujarBurbujaDialogoCriatura(
            self.pantalla, fuente, "Susurro: El Velo no tiene salida.", 300, 300
        )
        self.assertGreater(ovalo.width, ovalo.height)
        self.assertEqual(self.pantalla.get_at(ovalo.topleft), (0, 0, 0, 255))
        self.assertNotEqual(self.pantalla.get_at(ovalo.center), (0, 0, 0, 255))

    def testFuenteDeLuzVuelveMasTransparenteLaNiebla(self):
        niebla = NieblaNivel(ConfiguracionNiebla(RectanguloLogico(0, 0, 1280, 720), opacidadBase=238))
        niebla.activar()
        dibujador = DibujadorNiebla(self.pantalla)
        self.pantalla.fill((240, 240, 240))
        dibujador.dibujar(niebla, [], 0)
        sinLuz = self.pantalla.get_at((640, 360)).r
        self.pantalla.fill((240, 240, 240))
        dibujador.dibujar(niebla, [FuenteLuzNiebla(Vector2D(640, 360), 310)], 0)
        colorConLuz = self.pantalla.get_at((640, 360))
        self.assertGreater(colorConLuz.r, sinLuz + 100)
        self.assertGreater(colorConLuz.r, colorConLuz.g)
        self.assertGreater(colorConLuz.g, colorConLuz.b)

    def testOscurecerEnemigoConservaTransparenciaDelSprite(self):
        sprite = pygame.Surface((16, 16), pygame.SRCALPHA)
        sprite.fill((20, 30, 40, 0))
        sprite.set_at((8, 8), (180, 150, 210, 255))
        oscuro = DibujadorEscenario._oscurecerSprite(sprite)
        self.assertEqual(oscuro.get_at((0, 0)).a, 0)
        self.assertEqual(oscuro.get_at((8, 8)).a, 255)
        self.assertLess(oscuro.get_at((8, 8)).r, sprite.get_at((8, 8)).r)

    def testEnemigoAlumbradoRecibeUnResplandorSuave(self):
        self.pantalla.fill((0, 0, 0))
        dibujador = SimpleNamespace(pantalla=self.pantalla)
        DibujadorEscenario._dibujarResplandorEnemigo(dibujador, 300, 300, 1.0)
        color = self.pantalla.get_at((316, 321))
        self.assertGreater(color.r, color.b)
        self.assertGreater(color.g, 0)

    def testMusicaDeCuevaSoloSeSeleccionaParaLaCueva(self):
        from src.presentacion.escenaNivel import EscenaNivel

        class SonidosFalsos:
            instancias = []

            def __init__(self):
                self.inicial = 0
                self.cueva = 0
                self.__class__.instancias.append(self)

            def reproducirAmbienteInicial(self):
                self.inicial += 1

            def reproducirMusicaCueva(self):
                self.cueva += 1

        def escenaPara(identificador):
            nivel = SimpleNamespace(recursos=SimpleNamespace(identificadorMapa=identificador))
            return EscenaNivel(self.pantalla, lambda: None, lambda: nivel, lambda *_: object())

        with patch("src.presentacion.escenaNivel.SonidosJuego", SonidosFalsos):
            escenaPara("cueva_del_velo")
            escenaPara("espejos_de_niebla")
        cueva, bosque = SonidosFalsos.instancias[-2:]
        self.assertEqual((cueva.cueva, cueva.inicial), (1, 0))
        self.assertEqual((bosque.cueva, bosque.inicial), (0, 1))

    def testSacudidaRedibujaElPanelNarrativoEnPosicionFija(self):
        from src.presentacion.escenaNivel import EscenaNivel

        class DibujadorFalso:
            def __init__(self):
                self.panelFijo = 0

            def dibujar(self, *_):
                pass

            def dibujarInterfazFija(self, _):
                self.panelFijo += 1

        nivel = SimpleNamespace(
            rumi=SimpleNamespace(posicion=SimpleNamespace(x=0)),
            escenario=SimpleNamespace(ancho=1280),
            temblor=1.0,
            recursos=SimpleNamespace(identificadorMapa="barranco_del_velo"),
        )
        dibujador = DibujadorFalso()
        with patch("src.presentacion.escenaNivel.SonidosJuego"):
            escena = EscenaNivel(self.pantalla, lambda: None, lambda: nivel, lambda *_: dibujador)
        escena.sacudidaVisual = 7
        escena.dibujar()
        self.assertEqual(dibujador.panelFijo, 1)
