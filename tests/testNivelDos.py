import unittest
from src.creadorEspejos import CreadorEspejosNiebla
from src.recursosNivel import crearRecursosEspejosNiebla
from src.nivelUno import NivelUno


class PruebasMapaDos(unittest.TestCase):
    def testTramosYEnemigos(self):
        mapa = CreadorEspejosNiebla(crearRecursosEspejosNiebla()).escenario
        self.assertEqual(mapa.ancho, 7200)
        self.assertEqual(len(mapa.tramos),5)
        self.assertEqual(len(mapa.enemigos),20)
        self.assertGreater(len(mapa.enemigos),len(NivelUno().escenario.enemigos))
        for a,b in zip(mapa.tramos,mapa.tramos[1:]):
            self.assertEqual(a.fin,b.inicio)
        for enemigo in mapa.enemigos:
            self.assertGreaterEqual(enemigo.limiteIzquierdo,0)
            self.assertLessEqual(enemigo.limiteDerecho+42,mapa.ancho)
        self.assertTrue(mapa.decoraciones)

    def testFabricaIndependiente(self):
        a,b = (CreadorEspejosNiebla(crearRecursosEspejosNiebla()) for _ in range(2))
        a.escenario.enemigos[0].posicion.x = -1
        self.assertGreater(b.escenario.enemigos[0].posicion.x,0)
        self.assertNotEqual(a.escenario.recursos.identificadorMapa,NivelUno().recursos.identificadorMapa)

from src.enemigoHostil import EnemigoHostil, EstadoEnemigo
from src.enemigosNivel import TipoEnemigo
from src.dominio import Rumi, Vector2D
from src.vitalidad import Vitalidad


class PruebasCombateDos(unittest.TestCase):
    def crearEnemigo(self, tipo=TipoEnemigo.SUSURRO):
        return EnemigoHostil(tipo, Vector2D(500,534), 300,750,'No puedes.')

    def testTresGolpesDerrotanConProteccion(self):
        vida = Vitalidad()
        for puntos in (2,1,0):
            self.assertTrue(vida.recibirGolpe())
            self.assertEqual(vida.puntos,puntos)
            self.assertFalse(vida.recibirGolpe())
            vida.actualizar(1.2)
        self.assertTrue(vida.agotada)
        self.assertFalse(vida.recibirGolpe())

    def testPatrullaAcotada(self):
        enemigo = self.crearEnemigo()
        rumi = Rumi(Vector2D(5000,534))
        enemigo.actualizar(rumi,20)
        self.assertEqual(enemigo.posicion.x,750)
        self.assertEqual(enemigo.direccion,-1)
        enemigo.actualizar(rumi,20)
        self.assertEqual(enemigo.posicion.x,300)
        self.assertEqual(enemigo.direccion,1)

    def testAvisoAntesDeGolpeYRecuperacion(self):
        enemigo = self.crearEnemigo()
        rumi = Rumi(Vector2D(500,534))
        self.assertFalse(enemigo.actualizar(rumi,.01))
        self.assertEqual(enemigo.estado,EstadoEnemigo.AVISO)
        self.assertFalse(enemigo.actualizar(rumi,.64))
        self.assertEqual(enemigo.estado,EstadoEnemigo.AVISO)
        self.assertFalse(enemigo.actualizar(rumi,.02))
        self.assertEqual(enemigo.estado,EstadoEnemigo.ATAQUE)
        self.assertTrue(enemigo.actualizar(rumi,.01))
        self.assertEqual(enemigo.estado,EstadoEnemigo.RECUPERACION)
        self.assertFalse(enemigo.actualizar(rumi,.5))

    def testAtaqueFallaSiJugadorEsquiva(self):
        enemigo = self.crearEnemigo()
        rumi = Rumi(Vector2D(600,534))
        enemigo.actualizar(rumi,.01)
        enemigo.actualizar(rumi,.65)
        rumi.posicion = Vector2D(1000,300)
        self.assertFalse(enemigo.actualizar(rumi,.1))
        enemigo.actualizar(rumi,.8)
        self.assertEqual(enemigo.estado,EstadoEnemigo.RECUPERACION)

    def testEspejillaEmbisteEnVertical(self):
        enemigo = self.crearEnemigo(TipoEnemigo.ESPEJILLA)
        enemigo.posicion.y = 420
        rumi = Rumi(Vector2D(600,534))
        enemigo.actualizar(rumi,.01)
        enemigo.actualizar(rumi,.65)
        enemigo.actualizar(rumi,.1)
        self.assertGreater(enemigo.posicion.y,420)
        self.assertLessEqual(enemigo.posicion.y,534)

    def testLuzAnulaAtaqueSoloCerca(self):
        for tipo in TipoEnemigo:
            enemigo = self.crearEnemigo(tipo)
            enemigo.estado = EstadoEnemigo.ATAQUE
            rumi = Rumi(Vector2D(900,534));rumi.tiempoGarras=.32
            enemigo.actualizar(rumi,0)
            self.assertFalse(enemigo.liberado)
            rumi.posicion = Vector2D(enemigo.posicion.x,enemigo.posicion.y)
            self.assertFalse(enemigo.actualizar(rumi,.01))
            self.assertTrue(enemigo.liberado)
            rumi.tiempoGarras=0
            self.assertFalse(enemigo.actualizar(rumi,5))

from src.nivelDos import NivelDos, EstadoNivelDos
from src.dominio import EntradaJugador
from src.configuracion import GRAVEDAD, VELOCIDAD_RUMI, FUERZA_SALTO


class PruebasReglasDos(unittest.TestCase):
    def actualizar(self,nivel,entrada=None,dt=1/60):
        return nivel.actualizar(entrada or EntradaJugador(),dt,GRAVEDAD,VELOCIDAD_RUMI,FUERZA_SALTO,840)

    def testAtaquesSimultaneosSoloQuitanUnaVida(self):
        nivel=NivelDos()
        for enemigo in nivel.escenario.enemigos[:3]:
            enemigo.posicion=Vector2D(110,534)
            enemigo.limiteIzquierdo=0
            enemigo.estado=EstadoEnemigo.ATAQUE
            enemigo.objetivo=Vector2D(110,534)
        evento=self.actualizar(nivel)
        self.assertTrue(evento.golpeRecibido)
        self.assertEqual(nivel.vitalidad.puntos,2)
        self.assertEqual(nivel.rumi.luz,.28)

    def testMuerteCongelaYReinicioRestaura(self):
        nivel=NivelDos()
        nivel.vitalidad.puntos=1
        enemigo=nivel.escenario.enemigos[0]
        nivel.rumi.posicion=Vector2D(enemigo.posicion.x,534)
        enemigo.estado=EstadoEnemigo.ATAQUE
        enemigo.objetivo=Vector2D(enemigo.posicion.x,534)
        evento=self.actualizar(nivel)
        self.assertTrue(evento.derrotaIniciada)
        self.assertEqual(nivel.estado,EstadoNivelDos.DERROTADO)
        x=nivel.rumi.posicion.x
        tiempos=[e.tiempoEstado for e in nivel.escenario.enemigos]
        self.actualizar(nivel,EntradaJugador(derecha=True,usarGarras=True),1)
        self.assertEqual(nivel.rumi.posicion.x,x)
        self.assertEqual(tiempos,[e.tiempoEstado for e in nivel.escenario.enemigos])
        self.actualizar(nivel,EntradaJugador(reiniciar=True))
        self.assertEqual(nivel.estado,EstadoNivelDos.JUGANDO)
        self.assertEqual(nivel.vitalidad.puntos,3)
        self.assertEqual(nivel.rumi.posicion.x,110)
        self.assertTrue(all(e.estado==EstadoEnemigo.PATRULLA for e in nivel.escenario.enemigos))

    def testCaidaDerrota(self):
        nivel=NivelDos();nivel.rumi.posicion.y=900
        self.actualizar(nivel)
        self.assertEqual(nivel.estado,EstadoNivelDos.DERROTADO)
        self.assertEqual(nivel.vitalidad.puntos,0)

    def testRecargaImpideSpamDeLuz(self):
        nivel=NivelDos()
        self.actualizar(nivel,EntradaJugador(usarGarras=True))
        self.assertEqual(nivel.recargaLuz,.65)
        self.actualizar(nivel,EntradaJugador(usarGarras=True),.4)
        self.assertFalse(nivel.rumi.garrasActivas)
        self.actualizar(nivel,EntradaJugador(usarGarras=True),.25)
        self.assertTrue(nivel.rumi.garrasActivas)

    def testFinalCongelaYSePuedeRepetir(self):
        nivel=NivelDos();nivel.rumi.posicion.x=nivel.metaX
        self.actualizar(nivel)
        self.assertEqual(nivel.estado,EstadoNivelDos.COMPLETADO)
        x=nivel.rumi.posicion.x
        self.actualizar(nivel,EntradaJugador(izquierda=True),1)
        self.assertEqual(nivel.rumi.posicion.x,x)
        self.actualizar(nivel,EntradaJugador(reiniciar=True))
        self.assertEqual(nivel.estado,EstadoNivelDos.JUGANDO)

    def testLimitesHorizontales(self):
        nivel=NivelDos();nivel.rumi.posicion.x=-100
        self.actualizar(nivel,dt=0)
        self.assertEqual(nivel.rumi.posicion.x,0)
        nivel.rumi.posicion.x=9000
        self.actualizar(nivel,dt=0)
        self.assertEqual(nivel.rumi.posicion.x,7200-42)

    def testRecorridoCompletoConLuzYSaltos(self):
        nivel=NivelDos()
        for _ in range(3000):
            entrada=EntradaJugador(derecha=True,usarGarras=nivel.recargaLuz <= 1/60)
            self.actualizar(nivel,entrada)
            self.assertNotEqual(nivel.estado,EstadoNivelDos.DERROTADO)
            if nivel.estado==EstadoNivelDos.COMPLETADO:
                break
        self.assertEqual(nivel.estado,EstadoNivelDos.COMPLETADO)
        self.assertGreater(sum(e.liberado for e in nivel.escenario.enemigos),0)

    def testJugadorQuietoPuedeMorirPorEnemigoReal(self):
        nivel=NivelDos()
        nivel.rumi.posicion=Vector2D(500,534)
        for _ in range(1000):
            self.actualizar(nivel)
            if nivel.estado==EstadoNivelDos.DERROTADO:
                break
        self.assertEqual(nivel.estado,EstadoNivelDos.DERROTADO)
        self.assertEqual(nivel.vitalidad.puntos,0)

    def testTiemposNegativosRechazados(self):
        with self.assertRaises(ValueError):
            self.actualizar(NivelDos(),dt=-1)
        with self.assertRaises(ValueError):
            Vitalidad().actualizar(-1)
        enemigo=CreadorEspejosNiebla(crearRecursosEspejosNiebla()).escenario.enemigos[0]
        with self.assertRaises(ValueError):
            enemigo.actualizar(Rumi(Vector2D(0,0)),-1)
