"""Espejos de Niebla: exploración, combate y derrota sin interfaz gráfica."""
from dataclasses import replace
from enum import Enum, auto
from .dominio import Rumi, Vector2D
from .creadorEspejos import CreadorEspejosNiebla
from .recursosNivel import crearRecursosEspejosNiebla
from .eventosNivel import ResultadoActualizacionNivel
from .vitalidad import Vitalidad


class EstadoNivelDos(Enum):
    JUGANDO = auto()
    DERROTADO = auto()
    COMPLETADO = auto()


class NivelDos:
    def __init__(self, recursos=None):
        self.recursos = recursos or crearRecursosEspejosNiebla()
        mundo = CreadorEspejosNiebla(self.recursos)
        self.escenario = mundo.escenario
        self.metaX = mundo.metaX
        self.rumi = Rumi(Vector2D(110,534))
        self.vitalidad = Vitalidad()
        self.estado = EstadoNivelDos.JUGANDO
        self.recargaLuz = 0.0
        self.dialogo = 'Alcanza el Farol del Nombre. F libera criaturas; salta para esquivar sus embestidas.'

    def reiniciar(self):
        self.__init__(self.recursos)

    def derrotar(self, motivo):
        self.vitalidad.puntos = 0
        self.estado = EstadoNivelDos.DERROTADO
        self.rumi.velocidad = Vector2D(0,0)
        self.dialogo = f'{motivo} Un intento no decide lo que puedes aprender. R: volver a intentarlo.'

    def actualizar(self, entrada, deltaTiempo, gravedad, velocidadNormal, fuerzaSalto, limiteCaida):
        if deltaTiempo < 0:
            raise ValueError('El tiempo no puede retroceder')
        if entrada.reiniciar:
            self.reiniciar()
            return ResultadoActualizacionNivel()
        if self.estado != EstadoNivelDos.JUGANDO:
            return ResultadoActualizacionNivel()
        self.vitalidad.actualizar(deltaTiempo)
        self.recargaLuz = max(0.0, self.recargaLuz - deltaTiempo)
        activarLuz = entrada.usarGarras and self.recargaLuz == 0
        if activarLuz:
            self.recargaLuz = 0.9
        entrada = replace(entrada, usarGarras=activarLuz)
        anteriorY = self.rumi.posicion.y
        estabaEnSuelo = self.rumi.estaEnSuelo
        veniaCayendo = self.rumi.velocidad.y > 80
        self.rumi.actualizarMovimiento(entrada,deltaTiempo,gravedad,velocidadNormal,fuerzaSalto)
        self.rumi.resolverSuelo(self.escenario.geometriaSuelo,anteriorY)
        self.rumi.posicion.x = max(0.0,min(self.rumi.posicion.x,self.escenario.ancho-self.rumi.ancho))
        salto = entrada.saltar and estabaEnSuelo
        aterrizaje = not estabaEnSuelo and self.rumi.estaEnSuelo and veniaCayendo
        if self.rumi.posicion.y > limiteCaida:
            self.derrotar('Rumi cayó en la niebla.')
            return ResultadoActualizacionNivel(derrotaIniciada=True)
        golpe = False
        for enemigo in self.escenario.enemigos:
            if enemigo.actualizar(self.rumi,deltaTiempo):
                golpe = self.vitalidad.recibirGolpe() or golpe
        if self.vitalidad.agotada:
            self.derrotar('Rumi perdió sus tres vidas.')
        elif self.rumi.posicion.x >= self.metaX:
            self.estado = EstadoNivelDos.COMPLETADO
            self.rumi.velocidad = Vector2D(0,0)
            self.dialogo = 'Farol recuperado. Las voces del Velo no decidieron tu camino. Escape: menú; R: repetir.'
        return ResultadoActualizacionNivel(
            saltoIniciado=salto, aterrizaje=aterrizaje, golpeRecibido=golpe,
            derrotaIniciada=self.estado == EstadoNivelDos.DERROTADO,
        )
