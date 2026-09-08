"""Cueva del Velo: Rumi avanza con luz propia entre niebla y criaturas silenciosas."""

from dataclasses import replace

from src.dominio.dominio import Rumi, Vector2D
from src.dominio.estadoJuegoNivel import EstadoJuegoNivel
from src.mundo.creadorCueva import CreadorCuevaVelo
from src.dominio.eventosNivel import ResultadoActualizacionNivel
from src.mundo.recursosNivel import crearRecursosCuevaVelo
from src.dominio.vitalidad import Vitalidad
from src.mundo.elementosNivel import FarolNiebla, FuenteLuzNiebla
from src.dominio.mensajes import Mensaje, PresentadorMensajes
from .narrativaNiveles import (
    NIVEL_TRES_CAIDA,
    NIVEL_TRES_DERROTA,
    NIVEL_TRES_INICIO,
    NIVEL_TRES_LUZ,
    NIVEL_TRES_LUZ_AGOTADA,
    NIVEL_TRES_SALIDA,
    NIVEL_TRES_SIN_VIDAS,
)


class NivelTres:
    def __init__(self, recursos=None):
        self.recursos = recursos or crearRecursosCuevaVelo()
        mundo = CreadorCuevaVelo(self.recursos)
        self.escenario = mundo.escenario
        self.metaX = mundo.metaX
        self.padre = None
        self.rumi = Rumi(Vector2D(110, 534))
        self.vitalidad = Vitalidad()
        self.estado = EstadoJuegoNivel.JUGANDO
        self.recargaLuz = 0.0
        self.niebla = mundo.niebla
        self.nieblaActiva = self.niebla.activa
        self.temblor = 0.0
        self.mostrarHaloLuz = True
        self.mensajes = PresentadorMensajes(NIVEL_TRES_INICIO)
        self.actualizarIluminacionEnemigos()

    @property
    def dialogoAlpha(self) -> int:
        return self.mensajes.alfa

    @property
    def dialogo(self) -> str:
        return self.mensajes.texto

    def reiniciar(self):
        self.__init__(self.recursos)

    def mostrarMensaje(self, mensaje: Mensaje) -> None:
        self.mensajes.mostrar(mensaje)

    def derrotar(self, motivo):
        self.vitalidad.puntos = 0
        self.estado = EstadoJuegoNivel.DERROTADO
        self.rumi.velocidad = Vector2D(0, 0)
        self.mostrarMensaje(NIVEL_TRES_DERROTA)

    def interactuarConPilar(self) -> bool:
        for elemento in self.escenario.elementos:
            if isinstance(elemento, FarolNiebla) and elemento.puedeEntregarLuz(self.rumi):
                self.rumi.efectoLuz.activar()
                self.mostrarMensaje(NIVEL_TRES_LUZ)
                return True
        for pilar in self.escenario.pilares:
            mensaje = pilar.mensajeSiEstaCerca(self.rumi)
            if mensaje:
                self.mostrarMensaje(mensaje)
                return True
        return False

    def actualizar(self, entrada, deltaTiempo, gravedad, velocidadNormal, fuerzaSalto, limiteCaida):
        if deltaTiempo < 0:
            raise ValueError("El tiempo no puede retroceder")
        if entrada.reiniciar:
            self.reiniciar()
            return ResultadoActualizacionNivel()
        if self.estado != EstadoJuegoNivel.JUGANDO:
            return ResultadoActualizacionNivel()
        self.mensajes.actualizar(deltaTiempo)
        self.vitalidad.actualizar(deltaTiempo)
        if entrada.interactuar:
            self.interactuarConPilar()
        teniaLuz = self.rumi.efectoLuz.activo
        self.rumi.efectoLuz.actualizar(deltaTiempo)
        if teniaLuz and not self.rumi.efectoLuz.activo:
            self.mostrarMensaje(NIVEL_TRES_LUZ_AGOTADA)
        entrada = replace(entrada, usarGarras=self.rumi.efectoLuz.activo)
        anteriorY = self.rumi.posicion.y
        estabaEnSuelo = self.rumi.estaEnSuelo
        veniaCayendo = self.rumi.velocidad.y > 80
        self.rumi.actualizarMovimiento(entrada, deltaTiempo, gravedad, velocidadNormal, fuerzaSalto)
        solicitaSegundoSalto = entrada.saltar and not estabaEnSuelo
        impulsoRoca = self.escenario.actualizar(self, solicitaSegundoSalto, deltaTiempo)
        if not impulsoRoca:
            self.rumi.resolverSuelo(self.escenario.geometriaSuelo, anteriorY)
        self.rumi.posicion.x = max(0.0, min(self.rumi.posicion.x, self.escenario.ancho - self.rumi.ancho))
        salto = entrada.saltar and estabaEnSuelo
        aterrizaje = not estabaEnSuelo and self.rumi.estaEnSuelo and veniaCayendo
        if self.rumi.posicion.y > limiteCaida:
            self.derrotar(NIVEL_TRES_CAIDA)
            return ResultadoActualizacionNivel(derrotaIniciada=True)
        golpe = False
        for enemigo in self.escenario.enemigos:
            if enemigo.actualizar(self.rumi, deltaTiempo):
                golpe = self.vitalidad.recibirGolpe() or golpe
        self.actualizarIluminacionEnemigos()
        if self.vitalidad.agotada:
            self.derrotar(NIVEL_TRES_SIN_VIDAS)
        elif self.rumi.posicion.x >= self.metaX - self.rumi.ancho:
            self.estado = EstadoJuegoNivel.COMPLETADO
            self.rumi.velocidad = Vector2D(0, 0)
            self.mostrarMensaje(NIVEL_TRES_SALIDA)
        return ResultadoActualizacionNivel(
            saltoIniciado=salto,
            impulsoRoca=impulsoRoca,
            aterrizaje=aterrizaje,
            golpeRecibido=golpe,
            derrotaIniciada=self.estado == EstadoJuegoNivel.DERROTADO,
            nivelCompletado=self.estado == EstadoJuegoNivel.COMPLETADO,
        )

    @property
    def fuentesLuzNiebla(self) -> list[FuenteLuzNiebla]:
        fuentes = [
            elemento.fuenteLuz
            for elemento in self.escenario.elementos
            if isinstance(elemento, FarolNiebla) and elemento.emiteLuz
        ]
        if self.rumi.efectoLuz.activo:
            fuentes.append(
                FuenteLuzNiebla(
                    Vector2D(self.rumi.posicion.x + 21, self.rumi.posicion.y + 23),
                    self.rumi.efectoLuz.radioActual,
                    self.rumi.efectoLuz.color,
                    self.rumi.efectoLuz.fuerzaClaro,
                )
            )
        return fuentes

    def actualizarIluminacionEnemigos(self) -> None:
        """Entrega las fuentes disponibles; cada criatura resuelve su atributo."""
        fuentes = self.fuentesLuzNiebla
        for enemigo in self.escenario.enemigos:
            enemigo.actualizarIluminacion(fuentes)

    @property
    def intensidadHaloLuz(self) -> float:
        """La luz de Rumi o de un farol cercano suaviza el halo visual."""
        centroRumi = Vector2D(self.rumi.posicion.x + 21, self.rumi.posicion.y + 23)
        return max(
            (fuente.intensidadEn(centroRumi) for fuente in self.fuentesLuzNiebla),
            default=0.0,
        )

    @property
    def luzRestante(self) -> float:
        """Compatibilidad de interfaz: la fuente real vive en Rumi."""
        return self.rumi.efectoLuz.tiempoRestante
