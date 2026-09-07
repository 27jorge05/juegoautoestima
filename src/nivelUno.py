"""Datos y reglas específicas del nivel El Barranco del Velo."""

from __future__ import annotations

from .eventosNivel import ResultadoActualizacionNivel

from dataclasses import replace

from .dominio import EntradaJugador, EstadoNivel, Rumi, SecuenciaNivelUno, Vector2D
from .creadorBarranco import CreadorBarrancoVelo
from .recursosNivel import SeleccionRecursosNivel, crearRecursosBarrancoVelo
from .vitalidad import Vitalidad


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
        self.dialogoBase = "Encuentra a tu padre al final del camino."
        self.dialogo = self.dialogoBase
        self.dialogoTemporal = self.dialogoBase
        self.tiempoDialogo = 0.0
        self.fadeDialogo = 0.0
        self.temblor = 0.0
        self.fHabilitada = False

    def reiniciar(self) -> None:
        self.__init__(self.recursos)

    @property
    def dialogoAlpha(self) -> int:
        if self.tiempoDialogo > 0.0:
            return 255
        if self.fadeDialogo > 0.0:
            return int(255 * max(0.0, min(1.0, self.fadeDialogo / 1.2)))
        return 0

    def mostrarDialogo(self, texto: str, duracion: float = 7.0) -> None:
        self.dialogo = texto
        self.dialogoTemporal = texto
        self.tiempoDialogo = duracion
        self.fadeDialogo = 0.0

    def actualizarDialogo(self, deltaTiempo: float) -> None:
        if self.tiempoDialogo > 0.0:
            self.tiempoDialogo = max(0.0, self.tiempoDialogo - deltaTiempo)
            if self.tiempoDialogo == 0.0:
                self.fadeDialogo = 1.2
        elif self.fadeDialogo > 0.0:
            self.fadeDialogo = max(0.0, self.fadeDialogo - deltaTiempo)
            if self.fadeDialogo == 0.0:
                self.dialogo = self.dialogoBase
                self.dialogoTemporal = self.dialogoBase

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

        self.actualizarDialogo(deltaTiempo)
        self.temblor = max(0.0, self.temblor - deltaTiempo)

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
            self.dialogo = "Rumi cayó del camino. Respira y vuelve a intentarlo."
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
            self.dialogo = "El Velo agotó las vidas de Rumi. Respira y vuelve a intentarlo."
            return ResultadoActualizacionNivel(golpeRecibido=golpe, reiniciadoPorCaida=True)

        self.actualizarNarrativa()
        return ResultadoActualizacionNivel(
            saltoIniciado=saltoIniciado,
            impulsoRoca=impulsoRoca,
            aterrizaje=aterrizaje,
            golpeRecibido=golpe,
            nivelCompletado=self.secuencia.estado == EstadoNivel.COMPLETADO,
        )

    def actualizarNarrativa(self) -> None:
        if self.rumi.posicion.x >= self.metaX - 200 and self.secuencia.estado == EstadoNivel.SEGUIR_PADRE:
            self.dialogo = "Papá: ¡Corre! ¡El suelo se mueve!"
            self.dialogoTemporal = self.dialogo
            self.tiempoDialogo = 7.0
            self.fadeDialogo = 0.0
            self.temblor = 2.2
        if self.rumi.rectangulo.intersecta(self.padre.rectangulo):
            self.secuencia.encontrarPadre()
            self.mostrarDialogo(
                "Te encontré, Rumi. Ten cuidado con esos insectos: solo te están molestando. "
                "Ignóralos. Tú puedes, yo puedo, soy suficiente."
            )
            self.temblor = 1.8
