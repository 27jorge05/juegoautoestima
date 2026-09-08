"""Pruebas del menú sin requerir Pygame."""

import unittest

from src.aplicacion.menu import MenuPrincipal


class PruebasMenu(unittest.TestCase):
    def testNivelUnoEstaDesbloqueado(self) -> None:
        self.assertTrue(MenuPrincipal().seleccionarNivel(1))

    def testNivelDosEstaDisponible(self) -> None:
        self.assertTrue(MenuPrincipal().seleccionarNivel(2))

    def testNivelTresEstaDisponible(self):
        self.assertTrue(MenuPrincipal().seleccionarNivel(3))


if __name__ == "__main__":
    unittest.main()
