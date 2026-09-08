"""Pruebas de reglas puras; no requieren Pygame."""

import unittest

from src.dominio.dominio import EntradaJugador, EstadoNivel, RectanguloLogico, Rumi, SecuenciaNivelUno, Vector2D


class PruebasRectangulo(unittest.TestCase):
    def testIntersectaCuandoCompartenArea(self) -> None:
        primero = RectanguloLogico(0, 0, 10, 10)
        segundo = RectanguloLogico(5, 5, 10, 10)
        self.assertTrue(primero.intersecta(segundo))

    def testNoIntersectaCuandoSoloSeTocan(self) -> None:
        primero = RectanguloLogico(0, 0, 10, 10)
        segundo = RectanguloLogico(10, 0, 10, 10)
        self.assertFalse(primero.intersecta(segundo))


class PruebasSecuencia(unittest.TestCase):
    def testSecuenciaCompleta(self) -> None:
        secuencia = SecuenciaNivelUno()
        secuencia.activarNiebla()
        secuencia.activarTerremoto()
        secuencia.llegarMadriguera()
        secuencia.hablarConPajarito()
        secuencia.salirMadriguera()
        secuencia.completar()
        self.assertEqual(secuencia.estado, EstadoNivel.COMPLETADO)

    def testNoPermiteSaltarEstados(self) -> None:
        secuencia = SecuenciaNivelUno()
        secuencia.activarTerremoto()
        self.assertEqual(secuencia.estado, EstadoNivel.SEGUIR_PADRE)


class PruebasRumi(unittest.TestCase):
    def testAterrizaSobrePlataforma(self) -> None:
        rumi = Rumi(Vector2D(10, 40))
        rumi.velocidad.y = 120
        rumi.resolverSuelo([RectanguloLogico(0, 80, 100, 10)], 30)
        self.assertTrue(rumi.estaEnSuelo)
        self.assertEqual(rumi.posicion.y, 34)

    def testGarrasSeMantienenSoloDuranteSuVentanaVisual(self) -> None:
        rumi = Rumi(Vector2D(0, 0))
        rumi.actualizarMovimiento(EntradaJugador(usarGarras=True), 0.01, 0, 0, 0)
        self.assertTrue(rumi.garrasActivas)
        rumi.actualizarMovimiento(EntradaJugador(), 0.33, 0, 0, 0)
        self.assertFalse(rumi.garrasActivas)


if __name__ == "__main__":
    unittest.main()
