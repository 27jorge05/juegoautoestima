"""Reglas del Barranco: sin niebla, criaturas hostiles y encuentro con Mr. Fox."""

import unittest

from src.aplicacion.configuracion import FUERZA_SALTO, GRAVEDAD, VELOCIDAD_RUMI
from src.dominio.dominio import EntradaJugador, EstadoNivel, Vector2D
from src.dominio.enemigoHostil import EstadoEnemigo
from src.dominio.eventosNivel import TipoEventoNivel
from src.niveles.nivelUno import NivelUno


class PruebasNivelUno(unittest.TestCase):
    def actualizar(self, nivel, entrada=EntradaJugador(), dt=1 / 60):
        return nivel.actualizar(
            entrada, dt, GRAVEDAD, VELOCIDAD_RUMI, FUERZA_SALTO, 840
        )

    def testIniciaBuscandoAMrFoxSinNiebla(self):
        nivel = NivelUno()
        self.assertEqual(nivel.secuencia.estado, EstadoNivel.SEGUIR_PADRE)
        self.assertFalse(any(elemento.__class__.__name__ == "NieblaNivel" for elemento in nivel.escenario.elementos))
        self.assertIn("Mr. Fox", nivel.dialogo)

    def testPadreEsperaEnElUltimoTramo(self):
        nivel = NivelUno()
        self.assertGreater(nivel.padre.posicion.x, 6000)
        self.assertEqual(nivel.padre.posicion.x, nivel.metaX)

    def testEncuentroMuestraPrimeroAMrFoxYLuegoIniciaTerremoto(self):
        nivel = NivelUno()
        nivel.rumi.posicion = Vector2D(nivel.padre.posicion.x, nivel.padre.posicion.y)
        evento = self.actualizar(nivel)
        self.assertFalse(evento.terremotoIniciado)
        self.assertTrue(nivel.esperaAvisoTerremoto)
        self.assertFalse(nivel.terremotoIniciado)
        self.assertIn("por fin llegas", nivel.dialogo)
        posiciones = [enemigo.posicion.x for enemigo in nivel.escenario.enemigos]
        duracionMensaje = (
            nivel.mensajes.mensaje.duracionVisible
            + nivel.mensajes.mensaje.duracionFundido
        )
        evento = self.actualizar(nivel, EntradaJugador(derecha=True), dt=duracionMensaje)
        self.assertIsNotNone(evento.eventoIniciado)
        self.assertEqual(evento.eventoIniciado.tipo, TipoEventoNivel.TERREMOTO)
        self.assertEqual(evento.eventoIniciado.mensaje.texto, "¡Un terremoto! Hay que apresurarnos.")
        self.assertEqual(evento.eventoIniciado.duracion, 5.0)
        self.assertTrue(nivel.terremotoIniciado)
        self.assertIn("Un terremoto", nivel.dialogo)
        self.assertEqual(posiciones, [enemigo.posicion.x for enemigo in nivel.escenario.enemigos])
        self.actualizar(nivel, EntradaJugador(derecha=True), dt=4.9)
        self.assertNotEqual(nivel.secuencia.estado, EstadoNivel.COMPLETADO)
        self.actualizar(nivel, dt=.1)
        self.assertEqual(nivel.secuencia.estado, EstadoNivel.COMPLETADO)

    def testBichosTienenFrasesPropiasDelBanco(self):
        nivel = NivelUno()
        frases = [enemigo.dialogoAviso for enemigo in nivel.escenario.enemigos]
        self.assertTrue(all(enemigo.emiteFrase for enemigo in nivel.escenario.enemigos))
        self.assertTrue(all(frase.texto and frase.hablante for frase in frases))
        self.assertEqual(len(frases), len({frase.texto for frase in frases}))
        self.assertTrue(all(frase.duracionVisible >= 1.5 for frase in frases))
        self.assertTrue(all(enemigo.duracionAviso >= 1.5 for enemigo in nivel.escenario.enemigos))

    def testRecorridoDificilIncluyeOchoEncuentros(self):
        nivel = NivelUno()
        self.assertEqual(len(nivel.escenario.enemigos), 8)

    def testSoloConservaLaRocaLejanaDeLasPlataformasElevadas(self):
        nivel = NivelUno()
        rocas = [elemento for elemento in nivel.escenario.elementos if elemento.__class__.__name__ == "RocaImpulso"]
        self.assertEqual(len(rocas), 1)
        plataformasElevadas = [plataforma for plataforma in nivel.escenario.plataformas if plataforma.rectangulo.y < 580]
        for plataforma in plataformasElevadas:
            self.assertGreaterEqual(abs(rocas[0].rectangulo.x - plataforma.rectangulo.x), 200)

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

    def testFNoLiberaBichoNiActivaSegundoSalto(self):
        nivel = NivelUno()
        enemigo = nivel.escenario.enemigos[0]
        nivel.rumi.posicion = Vector2D(enemigo.posicion.x, enemigo.posicion.y)
        self.actualizar(nivel, EntradaJugador(usarGarras=True))
        self.assertFalse(enemigo.liberado)
        self.assertFalse(nivel.rumi.garrasActivas)
        nivel.rumi.estaSaltando = True
        self.assertFalse(nivel.actualizarElementos(True, 0.01))

    def testReinicioRestauraVidaYEnemigos(self):
        nivel = NivelUno()
        nivel.vitalidad.puntos = 1
        nivel.escenario.enemigos[0].cambiarEstado(EstadoEnemigo.LIBERADO)
        nivel.reiniciar()
        self.assertEqual(nivel.vitalidad.puntos, 3)
        self.assertFalse(nivel.escenario.enemigos[0].liberado)
