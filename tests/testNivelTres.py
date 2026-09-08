import unittest

from src.aplicacion.configuracion import FUERZA_SALTO, GRAVEDAD, VELOCIDAD_RUMI
from src.dominio.dominio import EntradaJugador, Vector2D
from src.dominio.enemigoHostil import EstadoEnemigo
from src.mundo.elementosNivel import NUBES_NIEBLA_DENSA, TipoNiebla
from src.dominio.estadoJuegoNivel import EstadoJuegoNivel
from src.niveles.nivelTres import NivelTres


class PruebasNivelTres(unittest.TestCase):
    def actualizar(self, nivel, entrada=EntradaJugador(), dt=1 / 60):
        return nivel.actualizar(entrada, dt, GRAVEDAD, VELOCIDAD_RUMI, FUERZA_SALTO, 840)

    def testCincoTramosYEnemigosSilenciosos(self):
        nivel = NivelTres()
        self.assertEqual(len(nivel.escenario.tramos), 5)
        self.assertEqual(len(nivel.escenario.enemigos), 14)
        self.assertGreaterEqual(min(enemigo.posicion.x for enemigo in nivel.escenario.enemigos), 680)
        self.assertTrue(nivel.nieblaActiva)
        self.assertTrue(all(not enemigo.emiteFrase for enemigo in nivel.escenario.enemigos))
        self.assertTrue(all(not enemigo.mostrarIndicadorEstado for enemigo in nivel.escenario.enemigos))
        for primero, segundo in zip(nivel.escenario.tramos, nivel.escenario.tramos[1:]):
            self.assertEqual(primero.fin, segundo.inicio)

    def testFarolEntregaLuzPlenaYLuegoLaDesvanece(self):
        nivel = NivelTres()
        farol = next(elemento for elemento in nivel.escenario.elementos if elemento.__class__.__name__ == "FarolNiebla")
        nivel.rumi.posicion = Vector2D(farol.rectangulo.x, 534)
        self.actualizar(nivel, EntradaJugador(interactuar=True), dt=0)
        self.assertTrue(nivel.rumi.garrasActivas)
        self.assertEqual(nivel.luzRestante, 3.0)
        self.assertIn("Farol:", nivel.dialogo)
        self.actualizar(nivel, dt=1.5)
        self.assertEqual(nivel.rumi.efectoLuz.intensidad, 1.0)
        self.assertGreater(nivel.fuentesLuzNiebla[-1].radio, 285)
        self.assertGreater(nivel.fuentesLuzNiebla[-1].fuerzaClaro, 1.0)
        self.actualizar(nivel, dt=.75)
        self.assertAlmostEqual(nivel.rumi.efectoLuz.intensidad, .5)
        self.assertEqual(len(nivel.fuentesLuzNiebla), 6)
        self.assertLess(nivel.fuentesLuzNiebla[-1].radio, 285)
        self.actualizar(nivel, dt=.75)
        self.assertEqual(nivel.luzRestante, 0.0)
        self.assertIn("Tengo miedo", nivel.dialogo)
        self.assertEqual(nivel.recargaLuz, 0.0)

    def testPilarCercanoEntregaAlientoYLejanoNo(self):
        nivel = NivelTres()
        pilar = nivel.escenario.pilares[0]
        nivel.rumi.posicion = Vector2D(pilar.rectangulo.x, 534)
        self.actualizar(nivel, EntradaJugador(interactuar=True), dt=0)
        self.assertIn("Pilar: Ánimo", nivel.dialogo)
        nivel.rumi.posicion = Vector2D(0, 534)
        dialogo = nivel.dialogo
        self.actualizar(nivel, EntradaJugador(interactuar=True), dt=0)
        self.assertEqual(nivel.dialogo, dialogo)

    def testCriaturaNoMuestraFraseAunqueAvise(self):
        nivel = NivelTres()
        enemigo = nivel.escenario.enemigos[0]
        nivel.rumi.posicion = Vector2D(enemigo.posicion.x, enemigo.posicion.y)
        self.actualizar(nivel)
        self.assertEqual(enemigo.estado, EstadoEnemigo.AVISO)
        self.assertEqual(enemigo.frase, "")

    def testCriaturaAvanzaMientrasEstaEnAviso(self):
        nivel = NivelTres()
        enemigo = nivel.escenario.enemigos[0]
        nivel.rumi.posicion = Vector2D(enemigo.posicion.x + 120, enemigo.posicion.y)
        self.actualizar(nivel, dt=0)
        posicionInicial = enemigo.posicion.x
        self.actualizar(nivel, dt=0.1)
        self.assertEqual(enemigo.estado, EstadoEnemigo.AVISO)
        self.assertGreater(enemigo.posicion.x, posicionInicial)

    def testDerrotaIncluyeEcoSoloAlPerder(self):
        nivel = NivelTres()
        self.assertNotIn("fallarías", nivel.dialogo)
        nivel.vitalidad.puntos = 1
        enemigo = nivel.escenario.enemigos[0]
        enemigo.posicion = Vector2D(110, 534)
        enemigo.estado = EstadoEnemigo.ATAQUE
        enemigo.objetivo = Vector2D(110, 534)
        self.actualizar(nivel)
        self.assertEqual(nivel.estado, EstadoJuegoNivel.DERROTADO)
        self.assertIn("fallarías", nivel.dialogo)

    def testSalidaCompletaLaCueva(self):
        nivel = NivelTres()
        nivel.rumi.posicion = Vector2D(nivel.metaX - nivel.rumi.ancho, nivel.rumi.posicion.y)
        self.actualizar(nivel, dt=0)
        self.assertEqual(nivel.estado, EstadoJuegoNivel.COMPLETADO)

    def testCriaturasEstanOscuras(self):
        nivel = NivelTres()
        self.assertTrue(all(enemigo.oscuro for enemigo in nivel.escenario.enemigos))

    def testCuevaNoContieneAMrFox(self):
        nivel = NivelTres()
        self.assertIsNone(nivel.padre)

    def testFarolesSonClarosPermanentesEnLaNiebla(self):
        nivel = NivelTres()
        fuentes = nivel.fuentesLuzNiebla
        self.assertEqual(len(fuentes), 5)
        self.assertTrue(all(fuente.radio >= 285 for fuente in fuentes))
        self.assertTrue(all(fuente.fuerzaClaro >= 1.60 for fuente in fuentes))

    def testEnemigoActualizaElAtributoAlumbradoSegunLaFuente(self):
        nivel = NivelTres()
        enemigo = nivel.escenario.enemigos[0]
        self.assertTrue(enemigo.alumbrado)
        enemigo.posicion = Vector2D(1200, enemigo.posicion.y)
        nivel.actualizarIluminacionEnemigos()
        self.assertFalse(enemigo.alumbrado)
        self.assertEqual(enemigo.intensidadLuz, 0.0)

    def testHaloSeAtenuaAlAlejarseDeUnFarol(self):
        nivel = NivelTres()
        farol = next(
            elemento
            for elemento in nivel.escenario.elementos
            if elemento.__class__.__name__ == "FarolNiebla"
        )
        nivel.rumi.posicion = Vector2D(farol.rectangulo.x, 534)
        intensidadCerca = nivel.intensidadHaloLuz
        nivel.rumi.posicion = Vector2D(farol.rectangulo.x + farol.radioLuz, 534)
        self.assertGreater(intensidadCerca, nivel.intensidadHaloLuz)
        self.assertEqual(nivel.intensidadHaloLuz, 0.0)

    def testNieblaCombinaTresVariantesYLaLuzDeRumiLaAclara(self):
        nivel = NivelTres()
        self.assertEqual(
            nivel.niebla.configuracion.variantesVisuales,
            (TipoNiebla.AZUL, TipoNiebla.VIOLETA, TipoNiebla.OSCURA),
        )
        self.assertIs(nivel.niebla.configuracion.configuracionNubes, NUBES_NIEBLA_DENSA)
        farol = next(elemento for elemento in nivel.escenario.elementos if elemento.__class__.__name__ == "FarolNiebla")
        nivel.rumi.posicion = Vector2D(farol.rectangulo.x, 534)
        self.actualizar(nivel, EntradaJugador(interactuar=True), dt=0)
        self.assertEqual(len(nivel.fuentesLuzNiebla), 6)
        self.assertTrue(nivel.mostrarHaloLuz)

    def testPilaresTienenSeparacionIrregular(self):
        nivel = NivelTres()
        posiciones = [pilar.rectangulo.x for pilar in nivel.escenario.pilares]
        separaciones = [segundo - primero for primero, segundo in zip(posiciones, posiciones[1:])]
        self.assertGreater(len(set(separaciones)), 1)

    def testRocasDeCuevaBrillanYDanSegundoSalto(self):
        nivel = NivelTres()
        rocas = [elemento for elemento in nivel.escenario.elementos if elemento.__class__.__name__ == "RocaImpulso"]
        self.assertEqual(len(rocas), 10)
        self.assertTrue(all(roca.configuracion.brillo for roca in rocas))
        roca = rocas[0]
        nivel.rumi.posicion = Vector2D(roca.rectangulo.x + 20, roca.rectangulo.y - 20)
        nivel.rumi.estaEnSuelo = False
        nivel.rumi.estaSaltando = True
        evento = self.actualizar(nivel, EntradaJugador(saltar=True), dt=0)
        self.assertTrue(evento.impulsoRoca)

    def testLaNieblaNoReduceLaVelocidadDeRumi(self):
        nivel = NivelTres()
        self.actualizar(nivel, EntradaJugador(derecha=True), 1)
        self.assertEqual(nivel.rumi.velocidad.x, VELOCIDAD_RUMI)
