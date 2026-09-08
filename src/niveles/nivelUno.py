"""Datos y reglas específicas del nivel El Barranco del Velo."""

from __future__ import annotations

from src.dominio.eventosNivel import EventoNivel, ResultadoActualizacionNivel

from dataclasses import replace

from src.dominio.dominio import EntradaJugador, EstadoNivel, Rumi, SecuenciaNivelUno, Vector2D
from src.mundo.creadorBarranco import CreadorBarrancoVelo
from src.mundo.recursosNivel import SeleccionRecursosNivel, crearRecursosBarrancoVelo
from src.dominio.vitalidad import Vitalidad
from src.dominio.mensajes import Mensaje, PresentadorMensajes
from .narrativaNiveles import (
    NIVEL_UNO_CAIDA,
    NIVEL_UNO_INICIO,
    NIVEL_UNO_MR_FOX,
    NIVEL_UNO_SIN_VIDAS,
    EVENTO_TERREMOTO_NIVEL_UNO,
    NIVEL_UNO_TERREMOTO_FINAL,
)


class NivelUno:
    def __init__(self, recursos: SeleccionRecursosNivel | None = None) -> None:
        self.recursos = recursos or crearRecursosBarrancoVelo()
        self.secuencia = SecuenciaNivelUno()
        self.posicionInicial = Vector2D(110.0, 534.0)
        self.rumi = Rumi(self.posicionInicial)
        mundo = CreadorBarrancoVelo(self.recursos)
        self.escenario = mundo.escenario
        self.metaX = mundo.metaX
        self.padre = mundo.padre
        self.vitalidad = Vitalidad()
        self.recargaLuz = 0.0
        self.mensajes = PresentadorMensajes(NIVEL_UNO_INICIO)
        self.temblor = 0.0
        self.reencuentroIniciado = False
        self.esperaAvisoTerremoto = False
        self.eventoActivo: EventoNivel | None = None
        self.tiempoEvento = 0.0
        self.fHabilitada = False

    def reiniciar(self) -> None:
        self.__init__(self.recursos)

    @property
    def dialogoAlpha(self) -> int:
        return self.mensajes.alfa

    @property
    def dialogo(self) -> str:
        return self.mensajes.texto

    def mostrarMensaje(self, mensaje: Mensaje) -> None:
        self.mensajes.mostrar(mensaje)

    @property
    def terremotoIniciado(self) -> bool:
        return self.eventoActivo is not None

    @property
    def padrePosicion(self) -> Vector2D:
        """Compatibilidad temporal: el resto del juego debe preferir `padre.posicion`."""
        return self.padre.posicion

    @padrePosicion.setter
    def padrePosicion(self, posicion: Vector2D) -> None:
        self.padre.reubicar(posicion)

    def actualizarElementos(
        self, solicitaSegundoSalto: bool, deltaTiempo: float
    ) -> bool:
        """Recorre objetos interactivos; el nivel puede crecer sin ifs específicos."""
        return self.escenario.actualizar(self, solicitaSegundoSalto, deltaTiempo)

    def actualizar(
        self,
        entrada: EntradaJugador,
        deltaTiempo: float,
        gravedad: float,
        velocidadNormal: float,
        fuerzaSalto: float,
        limiteCaida: float,
    ) -> ResultadoActualizacionNivel:
        if entrada.reiniciar:
            self.reiniciar()
            return ResultadoActualizacionNivel()

        self.mensajes.actualizar(deltaTiempo)
        self.temblor = max(0.0, self.temblor - deltaTiempo)

        if self.esperaAvisoTerremoto:
            if self.mensajes.terminado:
                self.esperaAvisoTerremoto = False
                evento = EVENTO_TERREMOTO_NIVEL_UNO
                self.eventoActivo = evento
                self.tiempoEvento = evento.duracion
                self.temblor = evento.duracion
                self.mostrarMensaje(evento.mensaje)
                return ResultadoActualizacionNivel(
                    eventoIniciado=evento,
                )
            return ResultadoActualizacionNivel()

        if self.eventoActivo is not None:
            self.tiempoEvento = max(0.0, self.tiempoEvento - deltaTiempo)
            if self.tiempoEvento <= 1e-6:
                self.tiempoEvento = 0.0
                self.eventoActivo = None
                self.secuencia.encontrarPadre()
                self.rumi.velocidad = Vector2D(0.0, 0.0)
                self.mostrarMensaje(NIVEL_UNO_TERREMOTO_FINAL)
                return ResultadoActualizacionNivel(nivelCompletado=True)
            return ResultadoActualizacionNivel()

        rumi = self.rumi
        self.vitalidad.actualizar(deltaTiempo)
        self.recargaLuz = max(0.0, self.recargaLuz - deltaTiempo)
        activarLuz = False
        entrada = replace(entrada, usarGarras=False)
        posicionAnteriorY = rumi.posicion.y
        estabaEnSuelo = rumi.estaEnSuelo
        veniaCayendo = rumi.velocidad.y > 80.0
        rumi.actualizarMovimiento(
            entrada,
            deltaTiempo,
            gravedad,
            velocidadNormal,
            fuerzaSalto,
        )

        saltoIniciado = entrada.saltar and estabaEnSuelo
        solicitaSegundoSalto = False
        impulsoRoca = self.actualizarElementos(solicitaSegundoSalto, deltaTiempo)
        if not impulsoRoca:
            rumi.resolverSuelo(self.escenario.geometriaSuelo, posicionAnteriorY)

        aterrizaje = not estabaEnSuelo and rumi.estaEnSuelo and veniaCayendo
        if rumi.posicion.y > limiteCaida:
            self.reiniciar()
            self.mostrarMensaje(NIVEL_UNO_CAIDA)
            return ResultadoActualizacionNivel(
                saltoIniciado=saltoIniciado,
                impulsoRoca=impulsoRoca,
                aterrizaje=aterrizaje,
                reiniciadoPorCaida=True,
            )

        rumi.posicion.x = max(0.0, min(rumi.posicion.x, self.escenario.ancho - rumi.ancho))

        golpe = False
        for enemigo in self.escenario.enemigos:
            if enemigo.actualizar(rumi, deltaTiempo):
                golpe = self.vitalidad.recibirGolpe() or golpe
        if self.vitalidad.agotada:
            self.reiniciar()
            self.mostrarMensaje(NIVEL_UNO_SIN_VIDAS)
            return ResultadoActualizacionNivel(golpeRecibido=golpe, reiniciadoPorCaida=True)

        self.actualizarNarrativa()
        return ResultadoActualizacionNivel(
            saltoIniciado=saltoIniciado,
            impulsoRoca=impulsoRoca,
            aterrizaje=aterrizaje,
            golpeRecibido=golpe,
            nivelCompletado=self.secuencia.estado == EstadoNivel.COMPLETADO,
        )

    def actualizarNarrativa(self) -> bool:
        if self.rumi.rectangulo.intersecta(self.padre.rectangulo) and not self.reencuentroIniciado:
            self.rumi.velocidad = Vector2D(0.0, 0.0)
            self.reencuentroIniciado = True
            self.esperaAvisoTerremoto = True
            self.mostrarMensaje(NIVEL_UNO_MR_FOX)
            return False
        return False
