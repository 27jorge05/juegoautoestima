"""Evaluación de las transiciones y componentes del Nivel 01."""

import unittest

from src.dominio import EstadoNivel, Vector2D
from src.nivelUno import NivelUno


class PruebasNivelUno(unittest.TestCase):
    def setUp(self) -> None:
        self.nivel = NivelUno()

    def moverRumiA(self, x: float, y: float = 534.0) -> None:
        self.nivel.rumi.posicion = Vector2D(x, y)

    def testIniciaSiguiendoAlPadre(self) -> None:
        self.assertEqual(self.nivel.secuencia.estado, EstadoNivel.SEGUIR_PADRE)

    def testEntrarEnNieblaCambiaEstado(self) -> None:
        self.moverRumiA(450)
        self.nivel.actualizarNarrativa()
        self.assertEqual(self.nivel.secuencia.estado, EstadoNivel.NIEBLA)

    def testTerremotoRequiereNieblaPrevia(self) -> None:
        self.moverRumiA(850)
        self.nivel.actualizarNarrativa()
        self.assertEqual(self.nivel.secuencia.estado, EstadoNivel.NIEBLA)

    def testTerremotoMueveAlPadreAlBorde(self) -> None:
        self.moverRumiA(450)
        self.nivel.actualizarNarrativa()
        self.moverRumiA(850)
        self.nivel.actualizarNarrativa()
        self.assertEqual(self.nivel.padrePosicion.x, 770.0)

    def testMadrigueraRequiereTerremoto(self) -> None:
        self.moverRumiA(1200)
        self.nivel.actualizarNarrativa()
        self.assertNotEqual(self.nivel.secuencia.estado, EstadoNivel.MADRIGUERA)

    def testMadrigueraActivaEscondite(self) -> None:
        self.moverRumiA(450)
        self.nivel.actualizarNarrativa()
        self.moverRumiA(850)
        self.nivel.actualizarNarrativa()
        self.moverRumiA(1200)
        self.nivel.actualizarNarrativa()
        self.assertTrue(self.nivel.rumi.estaEscondido)

    def testPajaritoLejosNoCambiaEstado(self) -> None:
        self._llegarMadriguera()
        self.nivel.interactuar()
        self.assertEqual(self.nivel.secuencia.estado, EstadoNivel.MADRIGUERA)

    def testPajaritoCercaAnimaARumi(self) -> None:
        self._llegarMadriguera()
        self.moverRumiA(1420)
        self.nivel.interactuar()
        self.assertEqual(self.nivel.secuencia.estado, EstadoNivel.PAJARITO)

    def testSalirAumentaLuz(self) -> None:
        self._hablarConPajarito()
        self.moverRumiA(1680)
        self.nivel.actualizarNarrativa()
        self.assertEqual(self.nivel.rumi.luz, 0.65)

    def testSalirQuitaEscondite(self) -> None:
        self._hablarConPajarito()
        self.moverRumiA(1680)
        self.nivel.actualizarNarrativa()
        self.assertFalse(self.nivel.rumi.estaEscondido)

    def testCompletaDespuesDeSalir(self) -> None:
        self._hablarConPajarito()
        self.moverRumiA(1680)
        self.nivel.actualizarNarrativa()
        self.moverRumiA(self.nivel.metaX + 10)
        self.nivel.actualizarNarrativa()
        self.assertEqual(self.nivel.secuencia.estado, EstadoNivel.COMPLETADO)

    def testReiniciarRestauraEstadoInicial(self) -> None:
        self._hablarConPajarito()
        self.nivel.reiniciar()
        self.assertEqual(self.nivel.secuencia.estado, EstadoNivel.SEGUIR_PADRE)

    def testReiniciarRestauraLuzInicial(self) -> None:
        self._hablarConPajarito()
        self.nivel.reiniciar()
        self.assertEqual(self.nivel.rumi.luz, 0.28)

    def testDialogoInicialExplicaControles(self) -> None:
        self.assertIn("A/D", self.nivel.dialogo)

    def testDialogoPajaritoDaSiguientePaso(self) -> None:
        self._hablarConPajarito()
        self.assertIn("próxima luz", self.nivel.dialogo)

    def _llegarMadriguera(self) -> None:
        self.moverRumiA(450)
        self.nivel.actualizarNarrativa()
        self.moverRumiA(850)
        self.nivel.actualizarNarrativa()
        self.moverRumiA(1200)
        self.nivel.actualizarNarrativa()

    def _hablarConPajarito(self) -> None:
        self._llegarMadriguera()
        self.moverRumiA(1420)
        self.nivel.interactuar()


if __name__ == "__main__":
    unittest.main()
