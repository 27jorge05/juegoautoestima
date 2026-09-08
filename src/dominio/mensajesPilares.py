"""Datos narrativos de los pilares de aliento de la Cueva del Velo."""

from dataclasses import dataclass
from src.dominio.mensajes import Dialogo


@dataclass(frozen=True)
class MensajeAliento:
    identificador: str
    dialogo: Dialogo


MENSAJES_PILARES: dict[str, MensajeAliento] = {
    "animo": MensajeAliento("animo", Dialogo("Ánimo, tú puedes dar el siguiente paso.", hablante="Pilar")),
    "brillo": MensajeAliento("brillo", Dialogo("Brillas más en la oscuridad cuando sigues avanzando.", hablante="Pilar")),
    "camino": MensajeAliento("camino", Dialogo("No necesitas verlo todo; busca la próxima luz.", hablante="Pilar")),
    "compania": MensajeAliento("compania", Dialogo("Tu miedo puede acompañarte, pero no tiene que guiarte.", hablante="Pilar")),
}


def obtenerMensajePilar(identificador: str) -> MensajeAliento:
    return MENSAJES_PILARES[identificador]
