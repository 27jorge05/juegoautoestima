import unittest
from src.nivelUno import NivelUno
from src.enemigosNivel import TipoEnemigo
from src.enemigoHostil import EnemigoHostil, EstadoEnemigo
from src.dominio import EntradaJugador, EstadoNivel, Vector2D, Rumi
from src.parallax import posicionesMosaicos
from src.configuracion import GRAVEDAD, VELOCIDAD_RUMI, FUERZA_SALTO


class PruebasRecorrido(unittest.TestCase):
    def testCincoTramosContiguos(self):
        nivel = NivelUno()
        self.assertEqual(len(nivel.escenario.tramos), 5)
        for a, b in zip(nivel.escenario.tramos, nivel.escenario.tramos[1:]):
            self.assertEqual(a.fin, b.inicio)
        self.assertGreater(nivel.metaX, 6000)
        nivel.rumi.posicion.x = 1800
        nivel.actualizarNarrativa()
        self.assertEqual(nivel.secuencia.estado, EstadoNivel.SEGUIR_PADRE)

    def testParallaxCubrePantalla(self):
        for camara in (0, 1279, 1280, 9000, -10):
            mosaicos = posicionesMosaicos(camara, .2, 1280, 1280)
            self.assertLessEqual(mosaicos[0][1], 0)
            self.assertGreaterEqual(mosaicos[-1][1] + 1280, 1280)
            self.assertEqual(mosaicos[1][1] - mosaicos[0][1], 1280)
        with self.assertRaises(ValueError):
            posicionesMosaicos(0, .2, 0, 1280)

    def testSusurroPatrullaYNoSaleDeSuTerritorio(self):
        rumi = Rumi(Vector2D(2000, 534))
        enemigo = EnemigoHostil(TipoEnemigo.SUSURRO, Vector2D(0, 534), 0, 100, "No puedes.")
        enemigo.actualizar(rumi, 10)
        self.assertEqual(enemigo.posicion.x, 100)
        self.assertEqual(enemigo.direccion, -1)

    def testLuzLiberaAmbosTiposSoloCerca(self):
        for tipo in TipoEnemigo:
            rumi = Rumi(Vector2D(0,534))
            rumi.actualizarMovimiento(EntradaJugador(usarGarras=True), 0, 0, 300,680)
            enemigo = EnemigoHostil(tipo, Vector2D(400,534), 0, 500, "No puedes.")
            enemigo.actualizar(rumi,.01)
            self.assertFalse(enemigo.liberado)
            enemigo.posicion.x = 40
            enemigo.actualizar(rumi,.01)
            self.assertTrue(enemigo.liberado)
            luz = rumi.luz
            enemigo.actualizar(rumi,10)
            self.assertEqual(rumi.luz,luz)

    def testReinicioRestauraCriaturas(self):
        nivel = NivelUno()
        nivel.escenario.enemigos[0].cambiarEstado(EstadoEnemigo.LIBERADO)
        nivel.reiniciar()
        self.assertFalse(nivel.escenario.enemigos[0].liberado)

    def testRecorridoConFisicaHastaFinal(self):
        nivel = NivelUno()
        saltoBarranco = False
        for _ in range(6000):
            rumi = nivel.rumi
            saltar = not saltoBarranco and rumi.posicion.x >= 870 and rumi.estaEnSuelo
            if saltar:
                saltoBarranco = True
            cerca = any(abs(enemigo.posicion.x - rumi.posicion.x) < 105 for enemigo in nivel.escenario.enemigos)
            entrada = EntradaJugador(derecha=True, saltar=saltar, usarGarras=cerca and nivel.recargaLuz == 0)
            resultado = nivel.actualizar(entrada, 1/60, GRAVEDAD, VELOCIDAD_RUMI, FUERZA_SALTO, 840)
            self.assertFalse(resultado.reiniciadoPorCaida, f'Cayó al cruzar el barranco en {rumi.posicion}')
            if nivel.secuencia.estado == EstadoNivel.COMPLETADO:
                break
        self.assertEqual(nivel.secuencia.estado, EstadoNivel.COMPLETADO)
