"""Reglas del Barranco: sin niebla, criaturas hostiles y encuentro con papá."""

import unittest

from src.configuracion import FUERZA_SALTO, GRAVEDAD, VELOCIDAD_RUMI
from src.dominio import EntradaJugador, EstadoNivel, Vector2D
from src.enemigoHostil import EstadoEnemigo
from src.nivelUno import NivelUno


class PruebasNivelUno(unittest.TestCase):
    def actualizar(self, nivel, entrada=EntradaJugador(), dt=1 / 60):
        return nivel.actualizar(
            entrada, dt, GRAVEDAD, VELOCIDAD_RUMI, FUERZA_SALTO, 840
        )

    def testIniciaBuscandoAlPadreSinNiebla(self):
        nivel = NivelUno()
        self.assertEqual(nivel.secuencia.estado, EstadoNivel.SEGUIR_PADRE)
        self.assertFalse(any(elemento.__class__.__name__ == "NieblaNivel" for elemento in nivel.escenario.elementos))
        self.assertIn("papá", nivel.dialogo)

    def testPadreEsperaEnElUltimoTramo(self):
        nivel = NivelUno()
        self.assertGreater(nivel.padre.posicion.x, 6000)
        self.assertEqual(nivel.padre.posicion.x, nivel.metaX)

    def testEncontrarPadreCompletaNivel(self):
        nivel = NivelUno()
        nivel.rumi.posicion = Vector2D(nivel.padre.posicion.x, nivel.padre.posicion.y)
        nivel.actualizarNarrativa()
        self.assertEqual(nivel.secuencia.estado, EstadoNivel.COMPLETADO)
        self.assertIn("Encontraste", nivel.dialogo)

    def testBichosUsanEstadosHostiles(self):
        nivel = NivelUno()
        enemigo = nivel.escenario.enemigos[0]
        nivel.rumi.posicion = Vector2D(enemigo.posicion.x, enemigo.posicion.y)
        self.actualizar(nivel)
        self.assertEqual(enemigo.estado, EstadoEnemigo.AVISO)
        self.actualizar(nivel, dt=enemigo.duracionAviso)
        self.assertEqual(enemigo.estado, EstadoEnemigo.ATAQUE)

    def testGolpeRestaUnaVidaConInvulnerabilidad(self):
        nivel = NivelUno()
        enemigo = nivel.escenario.enemigos[0]
        enemigo.posicion = Vector2D(110, 534)
        enemigo.limiteIzquierdo = 0
        enemigo.estado = EstadoEnemigo.ATAQUE
        enemigo.objetivo = Vector2D(110, 534)
        evento = self.actualizar(nivel)
        self.assertTrue(evento.golpeRecibido)
        self.assertEqual(nivel.vitalidad.puntos, 2)
        enemigo.estado = EstadoEnemigo.ATAQUE
        self.actualizar(nivel)
        self.assertEqual(nivel.vitalidad.puntos, 2)

    def testLuzLiberaBichoCercanoConRecarga(self):
        nivel = NivelUno()
        enemigo = nivel.escenario.enemigos[0]
        nivel.rumi.posicion = Vector2D(enemigo.posicion.x, enemigo.posicion.y)
        self.actualizar(nivel, EntradaJugador(usarGarras=True))
        self.assertTrue(enemigo.liberado)
        self.assertGreater(nivel.recargaLuz, 0)

    def testReinicioRestauraVidaYEnemigos(self):
        nivel = NivelUno()
        nivel.vitalidad.puntos = 1
        nivel.escenario.enemigos[0].cambiarEstado(EstadoEnemigo.LIBERADO)
        nivel.reiniciar()
        self.assertEqual(nivel.vitalidad.puntos, 3)
        self.assertFalse(nivel.escenario.enemigos[0].liberado)
