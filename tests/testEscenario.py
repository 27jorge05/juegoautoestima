import unittest
from src.niveles.nivelUno import NivelUno
from src.dominio.plataformaNivel import PlataformaNivel, TipoTerreno
from src.dominio.dominio import Rumi, Vector2D, RectanguloLogico
from src.mundo.escenarioNivel import EscenarioNivel
from src.mundo.recursosNivel import crearRecursosBarrancoVelo, COLORES_TERRENO


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
        a.escenario.enemigos[0].posicion.x = -1
        self.assertGreater(b.escenario.enemigos[0].posicion.x, 0)
        a.reiniciar()
        self.assertGreater(a.escenario.enemigos[0].posicion.x, 0)
        self.assertFalse(any(elemento.__class__.__name__ == "NieblaNivel" for elemento in a.escenario.elementos))

    def testDecoracionNoEsSuelo(self):
        nivel = NivelUno()
        self.assertTrue(nivel.escenario.decoraciones)
        self.assertEqual(len(nivel.escenario.geometriaSuelo), len(nivel.escenario.plataformas))
