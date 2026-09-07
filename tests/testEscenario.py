import unittest
from src.nivelUno import NivelUno
from src.plataformaNivel import PlataformaNivel, TipoTerreno
from src.dominio import Rumi, Vector2D, RectanguloLogico
from src.escenarioNivel import EscenarioNivel
from src.recursosNivel import crearRecursosBarrancoVelo, COLORES_TERRENO


class PruebasEscenario(unittest.TestCase):
    def testMaterialNoCambiaColision(self):
        for tipo in TipoTerreno:
            escenario = EscenarioNivel(crearRecursosBarrancoVelo(), [PlataformaNivel(RectanguloLogico(0, 580, 100, 100), tipo)], [])
            rumi = Rumi(Vector2D(10, 540))
            rumi.velocidad.y = 100
            rumi.resolverSuelo(escenario.geometriaSuelo, 530)
            self.assertTrue(rumi.estaEnSuelo)
            self.assertEqual(rumi.rectangulo.abajo, 580)
            self.assertIn(tipo, COLORES_TERRENO)

    def testFabricaNoComparteElementos(self):
        a, b = NivelUno(), NivelUno()
        a.niebla.activar()
        self.assertFalse(b.niebla.activa)
        a.reiniciar()
        self.assertFalse(a.niebla.activa)
        self.assertIn(a.niebla, a.escenario.elementos)

    def testDecoracionNoEsSuelo(self):
        nivel = NivelUno()
        self.assertTrue(nivel.escenario.decoraciones)
        self.assertEqual(len(nivel.escenario.geometriaSuelo), len(nivel.escenario.plataformas))
