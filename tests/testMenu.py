"""Pruebas del menú sin requerir Pygame."""

import unittest

from src.menu import MenuPrincipal


class PruebasMenu(unittest.TestCase):
    def testNivelUnoEstaDesbloqueado(self) -> None:
        self.assertTrue(MenuPrincipal().seleccionarNivel(1))

    def testNivelDosEstaDisponible(self) -> None:
        self.assertTrue(MenuPrincipal().seleccionarNivel(2))

    def testNivelTresSigueBloqueado(self):
        self.assertFalse(MenuPrincipal().seleccionarNivel(3))


if __name__ == "__main__":
    unittest.main()
