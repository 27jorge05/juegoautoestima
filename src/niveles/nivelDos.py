"""Espejos de Niebla: exploración, combate y derrota sin interfaz gráfica."""
from dataclasses import replace
from src.dominio.dominio import Padre, Rumi, Vector2D
from src.dominio.estadoJuegoNivel import EstadoJuegoNivel
from src.mundo.creadorEspejos import CreadorEspejosNiebla
from src.mundo.recursosNivel import crearRecursosEspejosNiebla
from src.dominio.eventosNivel import ResultadoActualizacionNivel
from src.dominio.vitalidad import Vitalidad
from src.dominio.mensajes import Mensaje, PresentadorMensajes
from .narrativaNiveles import (
    NIVEL_DOS_CAIDA,
    NIVEL_DOS_FINAL,
    NIVEL_DOS_INICIO,
    NIVEL_DOS_LUZ,
    NIVEL_DOS_SIN_VIDAS,
    derrotaNivelDos,
)


class NivelDos:
    def __init__(self, recursos=None):
        self.recursos = recursos or crearRecursosEspejosNiebla()
        mundo = CreadorEspejosNiebla(self.recursos)
        self.escenario = mundo.escenario
        self.metaX = mundo.metaX
        self.padre: Padre = mundo.padre
        self.rumi = Rumi(Vector2D(110,534))
        self.vitalidad = Vitalidad()
        self.estado = EstadoJuegoNivel.JUGANDO
        self.recargaLuz = 0.0
        self.fHabilitada = True
        self.mensajes = PresentadorMensajes(NIVEL_DOS_INICIO)
        self.temblor = 0.0
        self.ayudas = NIVEL_DOS_LUZ
        self.indiceAyuda = 0

    @property
    def dialogoAlpha(self) -> int:
        return self.mensajes.alfa

    @property
    def dialogo(self) -> str:
        return self.mensajes.texto

    def reiniciar(self):
        self.__init__(self.recursos)

    def mostrarMensaje(self, mensaje: Mensaje):
        self.mensajes.mostrar(mensaje)

    def derrotar(self, motivo):
        self.vitalidad.puntos = 0
        self.estado = EstadoJuegoNivel.DERROTADO
        self.rumi.velocidad = Vector2D(0,0)
        self.mostrarMensaje(derrotaNivelDos(motivo))

    def actualizar(self, entrada, deltaTiempo, gravedad, velocidadNormal, fuerzaSalto, limiteCaida):
        if deltaTiempo < 0:
            raise ValueError('El tiempo no puede retroceder')
        if entrada.reiniciar:
            self.reiniciar()
            return ResultadoActualizacionNivel()
        if self.estado != EstadoJuegoNivel.JUGANDO:
            return ResultadoActualizacionNivel()
        self.mensajes.actualizar(deltaTiempo)
        self.temblor = max(0.0, self.temblor - deltaTiempo)
        self.vitalidad.actualizar(deltaTiempo)
        self.recargaLuz = max(0.0, self.recargaLuz - deltaTiempo)
        activarLuz = entrada.usarGarras and self.recargaLuz == 0
        if activarLuz:
            self.recargaLuz = 0.65
            self.indiceAyuda = (self.indiceAyuda + 1) % len(self.ayudas)
            self.mostrarMensaje(self.ayudas[self.indiceAyuda])
        entrada = replace(entrada, usarGarras=activarLuz)
        anteriorY = self.rumi.posicion.y
        estabaEnSuelo = self.rumi.estaEnSuelo
        veniaCayendo = self.rumi.velocidad.y > 80
        self.rumi.actualizarMovimiento(entrada,deltaTiempo,gravedad,velocidadNormal,fuerzaSalto)
        solicitaSegundoSalto = entrada.saltar and not estabaEnSuelo
        impulsoRoca = self.escenario.actualizar(self, solicitaSegundoSalto, deltaTiempo)
        if not impulsoRoca:
            self.rumi.resolverSuelo(self.escenario.geometriaSuelo,anteriorY)
        self.rumi.posicion.x = max(0.0,min(self.rumi.posicion.x,self.escenario.ancho-self.rumi.ancho))
        salto = entrada.saltar and estabaEnSuelo
        aterrizaje = not estabaEnSuelo and self.rumi.estaEnSuelo and veniaCayendo
        if self.rumi.posicion.y > limiteCaida:
            self.derrotar(NIVEL_DOS_CAIDA)
            return ResultadoActualizacionNivel(derrotaIniciada=True)
        golpe = False
        for enemigo in self.escenario.enemigos:
            if enemigo.actualizar(self.rumi,deltaTiempo):
                golpe = self.vitalidad.recibirGolpe() or golpe
        if self.vitalidad.agotada:
            self.derrotar(NIVEL_DOS_SIN_VIDAS)
        elif self.rumi.posicion.x >= self.metaX - self.rumi.ancho:
            self.rumi.velocidad = Vector2D(0,0)
            self.estado = EstadoJuegoNivel.COMPLETADO
            self.mostrarMensaje(NIVEL_DOS_FINAL)
        return ResultadoActualizacionNivel(
            saltoIniciado=salto, impulsoRoca=impulsoRoca, aterrizaje=aterrizaje, golpeRecibido=golpe,
            derrotaIniciada=self.estado == EstadoJuegoNivel.DERROTADO,
            nivelCompletado=self.estado == EstadoJuegoNivel.COMPLETADO,
        )
