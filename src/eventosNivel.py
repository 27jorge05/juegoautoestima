"""Eventos de dominio compartidos por los niveles."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ResultadoActualizacionNivel:
    """Hechos del nivel para que interfaz y sonido reaccionen sin dirigir sus reglas."""

    saltoIniciado: bool = False
    impulsoRoca: bool = False
    aterrizaje: bool = False
    terremotoIniciado: bool = False
    reiniciadoPorCaida: bool = False
    golpeRecibido: bool = False
    derrotaIniciada: bool = False


