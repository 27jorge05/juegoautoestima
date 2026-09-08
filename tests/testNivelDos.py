import unittest
from src.mundo.creadorEspejos import CreadorEspejosNiebla
from src.mundo.recursosNivel import crearRecursosEspejosNiebla
from src.niveles.nivelUno import NivelUno


class PruebasMapaDos(unittest.TestCase):
    def testTramosYEnemigos(self):
        mapa = CreadorEspejosNiebla(crearRecursosEspejosNiebla()).escenario
        self.assertEqual(mapa.ancho, 7200)
        self.assertEqual(len(mapa.tramos),5)
        self.assertEqual(len(mapa.enemigos),30)
        self.assertGreater(len(mapa.enemigos),len(NivelUno().escenario.enemigos))
        self.assertEqual(len(mapa.elementos), 10)
        self.assertGreaterEqual(len(mapa.plataformas), 25)
        for a,b in zip(mapa.tramos,mapa.tramos[1:]):
            self.assertEqual(a.fin,b.inicio)
        for enemigo in mapa.enemigos:
            self.assertGreaterEqual(enemigo.limiteIzquierdo,0)
            self.assertLessEqual(enemigo.limiteDerecho+42,mapa.ancho)
        self.assertTrue(mapa.decoraciones)

    def testRocasElevadasNoCompartenPlataformaCercana(self):
        mapa = CreadorEspejosNiebla(crearRecursosEspejosNiebla()).escenario
        for roca in mapa.elementos:
            self.assertLess(roca.rectangulo.y, 500)
            for plataforma in mapa.plataformas:
                if plataforma.rectangulo.y >= 580:
                    continue
                horizontal = min(abs(roca.rectangulo.x - plataforma.rectangulo.derecha), abs(plataforma.rectangulo.x - roca.rectangulo.derecha))
                self.assertGreaterEqual(horizontal, 120)

    def testCadaTramoUsaUnPatronDeTerrenoDistinto(self):
        mapa = CreadorEspejosNiebla(crearRecursosEspejosNiebla()).escenario
        patrones = []
        for tramo in mapa.tramos:
            plataformas = [
                (plataforma.rectangulo.x - tramo.inicio, plataforma.rectangulo.ancho)
                for plataforma in mapa.plataformas
                if plataforma.rectangulo.y == 580
                and tramo.inicio <= plataforma.rectangulo.x < tramo.fin
            ]
            patrones.append(tuple(plataformas))
        self.assertEqual(len(patrones), len(set(patrones)))

    def testFabricaIndependiente(self):
        a,b = (CreadorEspejosNiebla(crearRecursosEspejosNiebla()) for _ in range(2))
        a.escenario.enemigos[0].posicion.x = -1
        self.assertGreater(b.escenario.enemigos[0].posicion.x,0)
        self.assertNotEqual(a.escenario.recursos.identificadorMapa,NivelUno().recursos.identificadorMapa)

from src.dominio.enemigoHostil import EnemigoHostil, EstadoEnemigo
from src.dominio.enemigosNivel import TipoEnemigo
from src.dominio.dominio import Rumi, Vector2D
from src.dominio.vitalidad import Vitalidad
from src.dominio.dificultadEnemigos import NIVEL_DOS, NIVEL_TRES, NIVEL_UNO
from src.niveles.nivelTres import NivelTres


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
        self.assertFalse(enemigo.actualizar(rumi,enemigo.duracionAviso - .01))
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
        enemigo.actualizar(rumi,enemigo.duracionAviso + .01)
        rumi.posicion = Vector2D(1000,300)
        self.assertFalse(enemigo.actualizar(rumi,.1))
        enemigo.actualizar(rumi,.8)
        self.assertEqual(enemigo.estado,EstadoEnemigo.RECUPERACION)

    def testEspejillaEmbisteEnVertical(self):
        enemigo = self.crearEnemigo(TipoEnemigo.ESPEJILLA)
        enemigo.posicion.y = 420
        rumi = Rumi(Vector2D(600,534))
        enemigo.actualizar(rumi,.01)
        enemigo.actualizar(rumi,enemigo.duracionAviso + .01)
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

    def testPerfilesSubenVelocidadYAgresividadPorNivel(self):
        nivelUno = NivelUno().escenario.enemigos[0].perfilDificultad
        nivelDos = NivelDos().escenario.enemigos[0].perfilDificultad
        nivelTres = NivelTres().escenario.enemigos[0].perfilDificultad
        self.assertEqual((nivelUno, nivelDos, nivelTres), (NIVEL_UNO, NIVEL_DOS, NIVEL_TRES))
        self.assertLess(nivelUno.velocidadAtaque, nivelDos.velocidadAtaque)
        self.assertLess(nivelDos.velocidadAtaque, nivelTres.velocidadAtaque)
        self.assertLess(nivelTres.duracionAviso, nivelDos.duracionAviso)

from src.niveles.nivelDos import NivelDos
from src.dominio.estadoJuegoNivel import EstadoJuegoNivel
from src.dominio.dominio import EntradaJugador
from src.aplicacion.configuracion import GRAVEDAD, VELOCIDAD_RUMI, FUERZA_SALTO


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
        self.assertEqual(nivel.estado,EstadoJuegoNivel.DERROTADO)
        x=nivel.rumi.posicion.x
        tiempos=[e.tiempoEstado for e in nivel.escenario.enemigos]
        self.actualizar(nivel,EntradaJugador(derecha=True,usarGarras=True),1)
        self.assertEqual(nivel.rumi.posicion.x,x)
        self.assertEqual(tiempos,[e.tiempoEstado for e in nivel.escenario.enemigos])
        self.actualizar(nivel,EntradaJugador(reiniciar=True))
        self.assertEqual(nivel.estado,EstadoJuegoNivel.JUGANDO)
        self.assertEqual(nivel.vitalidad.puntos,3)
        self.assertEqual(nivel.rumi.posicion.x,110)
        self.assertTrue(all(e.estado==EstadoEnemigo.PATRULLA for e in nivel.escenario.enemigos))

    def testCaidaDerrota(self):
        nivel=NivelDos();nivel.rumi.posicion.y=900
        self.actualizar(nivel)
        self.assertEqual(nivel.estado,EstadoJuegoNivel.DERROTADO)
        self.assertEqual(nivel.vitalidad.puntos,0)

    def testRecargaImpideSpamDeLuz(self):
        nivel=NivelDos()
        self.actualizar(nivel,EntradaJugador(usarGarras=True))
        self.assertEqual(nivel.recargaLuz,.65)
        self.actualizar(nivel,EntradaJugador(usarGarras=True),.4)
        self.assertFalse(nivel.rumi.garrasActivas)
        self.actualizar(nivel,EntradaJugador(usarGarras=True),.25)
        self.assertTrue(nivel.rumi.garrasActivas)

    def testFinalEnFarolSinTerremotoYSePuedeRepetir(self):
        nivel=NivelDos();nivel.rumi.posicion = Vector2D(nivel.metaX - nivel.rumi.ancho, nivel.rumi.posicion.y)
        evento = self.actualizar(nivel)
        self.assertEqual(nivel.estado,EstadoJuegoNivel.COMPLETADO)
        self.assertIsNone(evento.eventoIniciado)
        self.assertIn("me escondo", nivel.dialogo)
        x=nivel.rumi.posicion.x
        self.actualizar(nivel,EntradaJugador(izquierda=True),1)
        self.assertEqual(nivel.rumi.posicion.x,x)
        self.actualizar(nivel,EntradaJugador(reiniciar=True))
        self.assertEqual(nivel.estado,EstadoJuegoNivel.JUGANDO)

    def testFarolNoEmiteTerremoto(self):
        nivel = NivelDos()
        nivel.rumi.posicion = Vector2D(nivel.metaX - nivel.rumi.ancho, nivel.rumi.posicion.y)
        primerEvento = self.actualizar(nivel)
        self.assertIsNone(primerEvento.eventoIniciado)
        self.assertTrue(primerEvento.nivelCompletado)

    def testPrologoYPadreGuianElInicio(self):
        nivel = NivelDos()
        self.assertLess(nivel.padre.posicion.x, 400)
        self.assertIn("rocas", nivel.dialogo)
        self.assertIn("segundo salto", nivel.dialogo)

    def testRocaHabilitaSegundoSalto(self):
        nivel = NivelDos()
        roca = nivel.escenario.elementos[0]
        nivel.rumi.posicion = Vector2D(roca.rectangulo.x + 20, roca.rectangulo.y - 20)
        nivel.rumi.estaEnSuelo = False
        nivel.rumi.estaSaltando = True
        evento = self.actualizar(nivel, EntradaJugador(saltar=True), dt=0)
        self.assertTrue(evento.impulsoRoca)
        self.assertTrue(nivel.rumi.segundoSaltoUsado)

    def testLimitesHorizontales(self):
        nivel=NivelDos();nivel.rumi.posicion.x=-100
        self.actualizar(nivel,dt=0)
        self.assertEqual(nivel.rumi.posicion.x,0)
        nivel.rumi.posicion.x=9000
        self.actualizar(nivel,dt=0)
        self.assertEqual(nivel.rumi.posicion.x,7200-42)

    def testRecorridoCompletoConLuzYSaltos(self):
        nivel=NivelDos()
        for enemigo in nivel.escenario.enemigos:
            enemigo.cambiarEstado(EstadoEnemigo.LIBERADO)
        for _ in range(6000):
            tramo = nivel.rumi.posicion.x % 1440
            saltar = (
                (nivel.rumi.estaEnSuelo and (450 <= tramo <= 590 or 850 <= tramo <= 1000))
                or (not nivel.rumi.estaEnSuelo and not nivel.rumi.segundoSaltoUsado)
            )
            entrada=EntradaJugador(derecha=True,saltar=saltar,usarGarras=nivel.recargaLuz <= 1/60)
            self.actualizar(nivel,entrada)
            self.assertNotEqual(nivel.estado,EstadoJuegoNivel.DERROTADO, nivel.rumi.posicion)
            if nivel.estado==EstadoJuegoNivel.COMPLETADO:
                break
        self.assertEqual(nivel.estado,EstadoJuegoNivel.COMPLETADO)
        self.assertGreater(sum(e.liberado for e in nivel.escenario.enemigos),0)

    def testJugadorQuietoPuedeMorirPorEnemigoReal(self):
        nivel=NivelDos()
        nivel.rumi.posicion=Vector2D(500,534)
        for _ in range(1000):
            self.actualizar(nivel)
            if nivel.estado==EstadoJuegoNivel.DERROTADO:
                break
        self.assertEqual(nivel.estado,EstadoJuegoNivel.DERROTADO)
        self.assertEqual(nivel.vitalidad.puntos,0)

    def testTiemposNegativosRechazados(self):
        with self.assertRaises(ValueError):
            self.actualizar(NivelDos(),dt=-1)
        with self.assertRaises(ValueError):
            Vitalidad().actualizar(-1)
        enemigo=CreadorEspejosNiebla(crearRecursosEspejosNiebla()).escenario.enemigos[0]
        with self.assertRaises(ValueError):
            enemigo.actualizar(Rumi(Vector2D(0,0)),-1)
