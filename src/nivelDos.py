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
        self.fHabilitada = True
        self.dialogoBase = 'Prólogo: ocurrió un terremoto que separó a Rumi de su padre. Ya no lo encuentra. Busca el farol para guiarte por el camino.'
        self.dialogo = self.dialogoBase
        self.dialogoTemporal = self.dialogoBase
        self.tiempoDialogo = 7.0
        self.fadeDialogo = 0.0
        self.temblor = 0.0
        self.ayudas = [
            'Ignora a esos insectos: solo te están molestando.',
            'Tú puedes. Yo puedo. Soy suficiente.',
            'No dejes que los insectos decidan quién eres.',
        ]
        self.indiceAyuda = 0
        self.terremotoIniciado = False
        self.tiempoTerremoto = 0.0

    @property
    def dialogoAlpha(self) -> int:
        if self.tiempoDialogo > 0.0:
            return 255
        if self.fadeDialogo > 0.0:
            return int(255 * max(0.0, min(1.0, self.fadeDialogo / 1.2)))
        return 0

    def reiniciar(self):
        self.__init__(self.recursos)

    def mostrarDialogo(self, texto, duracion=7.0):
        self.dialogo = texto
        self.dialogoTemporal = texto
        self.tiempoDialogo = duracion
        self.fadeDialogo = 0.0

    def actualizarDialogo(self, deltaTiempo):
        if self.tiempoDialogo > 0:
            self.tiempoDialogo = max(0.0, self.tiempoDialogo - deltaTiempo)
            if self.tiempoDialogo == 0.0:
                self.fadeDialogo = 1.2
        elif self.fadeDialogo > 0:
            self.fadeDialogo = max(0.0, self.fadeDialogo - deltaTiempo)
            if self.fadeDialogo == 0.0:
                self.dialogo = self.dialogoBase
                self.dialogoTemporal = self.dialogoBase

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
        self.actualizarDialogo(deltaTiempo)
        self.temblor = max(0.0, self.temblor - deltaTiempo)
        if self.terremotoIniciado:
            self.tiempoTerremoto = max(0.0, self.tiempoTerremoto - deltaTiempo)
            if self.tiempoTerremoto == 0.0:
                self.estado = EstadoNivelDos.COMPLETADO
                self.rumi.velocidad = Vector2D(0,0)
                self.dialogo = 'Farol recuperado. Las voces del Velo no decidieron tu camino. Escape: menú; R: repetir.'
                return ResultadoActualizacionNivel(
                    terremotoIniciado=True,
                    nivelCompletado=True,
                )
        self.vitalidad.actualizar(deltaTiempo)
        self.recargaLuz = max(0.0, self.recargaLuz - deltaTiempo)
        activarLuz = entrada.usarGarras and self.recargaLuz == 0
        if activarLuz:
            self.recargaLuz = 0.65
            self.indiceAyuda = (self.indiceAyuda + 1) % len(self.ayudas)
            self.mostrarDialogo(self.ayudas[self.indiceAyuda], 7.0)
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
        if self.dialogo == self.dialogoBase and not self.terremotoIniciado:
            self.terremotoIniciado = True
            self.tiempoTerremoto = 3.0
            self.temblor = 2.4
            self.dialogo = '¡Un terremoto! ¡Corre!'
            self.dialogoTemporal = self.dialogo
            self.tiempoDialogo = 7.0
        return ResultadoActualizacionNivel(
            saltoIniciado=salto, aterrizaje=aterrizaje, golpeRecibido=golpe,
            derrotaIniciada=self.estado == EstadoNivelDos.DERROTADO,
            nivelCompletado=self.estado == EstadoNivelDos.COMPLETADO,
            terremotoIniciado=self.terremotoIniciado and self.tiempoTerremoto > 0.0,
        )
