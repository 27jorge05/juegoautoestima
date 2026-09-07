import unittest

from src.estadoVisual import obtenerAnimacionRumi
from src.sonidos import RitmoPasos


class PruebasEstadoVisual(unittest.TestCase):
    def testGarrasTienenPrioridadSobreElMovimiento(self) -> None:
        animacion = obtenerAnimacionRumi(300.0, 0.0, True, True)
        self.assertEqual("garras", animacion)

    def testCarreraYSaltoTienenPosesDiferentes(self) -> None:
        self.assertEqual("correr", obtenerAnimacionRumi(300.0, 0.0, True, False))
        self.assertEqual("saltar", obtenerAnimacionRumi(0.0, -120.0, False, False))

    def testPasosNoSeRepitenAntesDelIntervalo(self) -> None:
        ritmo = RitmoPasos(intervalo=0.20)
        self.assertTrue(ritmo.actualizar(True, True, 0.01))
        self.assertFalse(ritmo.actualizar(True, True, 0.10))
        self.assertTrue(ritmo.actualizar(True, True, 0.10))

    def testNoHayPasosEnElAireNiQuieto(self) -> None:
        ritmo = RitmoPasos()
        self.assertFalse(ritmo.actualizar(True, False, 1.0))
        self.assertFalse(ritmo.actualizar(False, True, 1.0))
