"""Datos y reglas específicas del nivel El Barranco del Velo."""

from __future__ import annotations

from .eventosNivel import ResultadoActualizacionNivel

from .dominio import (
    EntradaJugador,
    EstadoNivel,
    Rumi,
    SecuenciaNivelUno,
    Vector2D,
)
from .creadorBarranco import CreadorBarrancoVelo
from .recursosNivel import SeleccionRecursosNivel, crearRecursosBarrancoVelo


class NivelUno:
    def __init__(self, recursos: SeleccionRecursosNivel | None = None) -> None:
        self.recursos = recursos or crearRecursosBarrancoVelo()
        self.secuencia = SecuenciaNivelUno()
        self.posicionInicial = Vector2D(110.0, 534.0)
        self.rumi = Rumi(self.posicionInicial)
        mundo = CreadorBarrancoVelo(self.recursos)
        self.escenario = mundo.escenario
        self.metaX = mundo.metaX
        self.niebla = mundo.niebla
        self.zonaTerremoto = mundo.zonaTerremoto
        self.zonaMadriguera = mundo.zonaMadriguera
        self.zonaPajarito = mundo.zonaPajarito
        self.zonaSalida = mundo.zonaSalida
        self.padre = mundo.padre
        self.pajaritoPosicion = mundo.pajaritoPosicion
        self.dialogo = "Sigue a tu padre con A/D o flechas. Salta con Espacio."

    def reiniciar(self) -> None:
        self.__init__(self.recursos)

    @property
    def padrePosicion(self) -> Vector2D:
        """Compatibilidad temporal: el resto del juego debe preferir `padre.posicion`."""
        return self.padre.posicion

    @padrePosicion.setter
    def padrePosicion(self, posicion: Vector2D) -> None:
        self.padre.reubicar(posicion)

    def estaEnNiebla(self) -> bool:
        return self.escenario.contieneElemento(self.niebla) and self.niebla.contiene(self.rumi)

    def velocidadEnNiebla(self, velocidadNormal: float) -> float:
        """La niebla vuelve prudente el avance; la luz del padre protege el inicio."""
        if not self.escenario.contieneElemento(self.niebla):
            return velocidadNormal
        return self.niebla.velocidadPermitida(self.rumi, self.padre, velocidadNormal)

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
        """Actualiza las reglas de este escenario y devuelve sus eventos observables.

        No dibuja ni reproduce audio. Así el nivel conserva sus reglas aunque se
        cambie Pygame por otra interfaz en el futuro.
        """
        if entrada.reiniciar:
            self.reiniciar()
            return ResultadoActualizacionNivel()

        rumi = self.rumi
        posicionAnteriorY = rumi.posicion.y
        estabaEnSuelo = rumi.estaEnSuelo
        veniaCayendo = rumi.velocidad.y > 80.0
        rumi.actualizarMovimiento(
            entrada,
            deltaTiempo,
            gravedad,
            self.velocidadEnNiebla(velocidadNormal),
            fuerzaSalto,
        )

        saltoIniciado = entrada.saltar and estabaEnSuelo
        solicitaSegundoSalto = entrada.saltar and not estabaEnSuelo
        impulsoRoca = self.actualizarElementos(solicitaSegundoSalto, deltaTiempo)
        if not impulsoRoca:
            rumi.resolverSuelo(self.escenario.geometriaSuelo, posicionAnteriorY)

        aterrizaje = not estabaEnSuelo and rumi.estaEnSuelo and veniaCayendo
        if rumi.posicion.y > limiteCaida:
            self.reiniciar()
            self.dialogo = "Rumi cayó en la niebla. Respira y vuelve a intentarlo."
            return ResultadoActualizacionNivel(
                saltoIniciado=saltoIniciado,
                impulsoRoca=impulsoRoca,
                aterrizaje=aterrizaje,
                reiniciadoPorCaida=True,
            )

        rumi.posicion.x = max(0.0, min(rumi.posicion.x, self.escenario.ancho - rumi.ancho))

        if entrada.interactuar:
            self.interactuar()
        estadoAnterior = self.secuencia.estado
        self.actualizarNarrativa()
        terremotoIniciado = (
            estadoAnterior != EstadoNivel.TERREMOTO
            and self.secuencia.estado == EstadoNivel.TERREMOTO
        )
        return ResultadoActualizacionNivel(
            saltoIniciado=saltoIniciado,
            impulsoRoca=impulsoRoca,
            aterrizaje=aterrizaje,
            terremotoIniciado=terremotoIniciado,
        )

    def actualizarNarrativa(self) -> None:
        posicion = self.rumi.rectangulo
        if self.escenario.contieneElemento(self.niebla) and self.secuencia.estado == EstadoNivel.SEGUIR_PADRE and posicion.intersecta(
            self.niebla.rectangulo
        ):
            self.secuencia.activarNiebla()
            self.niebla.activar()
            self.dialogo = (
                "La niebla cubre el sendero. Las garras de papá iluminan el camino."
            )
            return
        if self.secuencia.estado == EstadoNivel.NIEBLA and posicion.intersecta(
            self.zonaTerremoto.rectangulo
        ):
            self.secuencia.activarTerremoto()
            self.dialogo = "¡El suelo tiembla! Papá te impulsa al otro lado: ‘Te encontraré más adelante’."
            self.padre.reubicar(Vector2D(770.0, 526.0))
            return
        if self.secuencia.estado == EstadoNivel.TERREMOTO and posicion.intersecta(
            self.zonaMadriguera.rectangulo
        ):
            self.secuencia.llegarMadriguera()
            self.rumi.estaEscondido = True
            self.dialogo = "Rumi se esconde en la madriguera. Presiona E junto al pajarito para escucharle."
            return
        if self.secuencia.estado == EstadoNivel.PAJARITO and posicion.intersecta(
            self.zonaSalida.rectangulo
        ):
            self.secuencia.salirMadriguera()
            self.rumi.estaEscondido = False
            self.rumi.luz = 0.65
            self.dialogo = (
                "Rumi sale. Sigue las huellas. F: ilumina a las criaturas del Velo."
            )
            return
        if self.secuencia.estado == EstadoNivel.SALIDA and posicion.x >= self.metaX:
            self.secuencia.completar()
            self.dialogo = "Nivel completado: la aventura de Rumi comienza ahora."

    def interactuar(self) -> None:
        cercaPajarito = abs(self.rumi.posicion.x - self.pajaritoPosicion.x) < 100.0
        if self.secuencia.estado == EstadoNivel.MADRIGUERA and cercaPajarito:
            self.secuencia.hablarConPajarito()
            self.dialogo = "Pajarito: ‘No necesitas ver todo el camino. Solo busca la próxima luz’."
