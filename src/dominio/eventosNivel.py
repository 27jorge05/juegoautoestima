"""Eventos de dominio compartidos por los niveles."""
from dataclasses import dataclass
from enum import Enum, auto

from .mensajes import Mensaje


class TipoEventoNivel(Enum):
    TERREMOTO = auto()


@dataclass(frozen=True)
class EventoNivel:
    """Hecho narrativo de alto nivel con su mensaje y duración propias."""

    tipo: TipoEventoNivel
    mensaje: Mensaje
    duracion: float


@dataclass(frozen=True)
class ResultadoActualizacionNivel:
    """Hechos del nivel para que interfaz y sonido reaccionen sin dirigir sus reglas."""

    saltoIniciado: bool = False
    impulsoRoca: bool = False
    aterrizaje: bool = False
    eventoIniciado: EventoNivel | None = None
    reiniciadoPorCaida: bool = False
    golpeRecibido: bool = False
    derrotaIniciada: bool = False
    nivelCompletado: bool = False

    @property
    def terremotoIniciado(self) -> bool:
        """Compatibilidad de lectura para presentaciones anteriores."""
        return (
            self.eventoIniciado is not None
            and self.eventoIniciado.tipo == TipoEventoNivel.TERREMOTO
        )

    @property
    def duracionTerremoto(self) -> float:
        if self.terremotoIniciado:
            return self.eventoIniciado.duracion
        return 0.0
