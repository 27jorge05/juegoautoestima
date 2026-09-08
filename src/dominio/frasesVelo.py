"""Voces ficticias del Velo asociadas al comportamiento de cada criatura."""

from src.dominio.enemigosNivel import TipoEnemigo
from src.dominio.mensajes import Dialogo


FRASES_DESALENTADORAS: dict[TipoEnemigo, tuple[str, ...]] = {
    TipoEnemigo.SUSURRO: (
        "¿De verdad crees que llegarás hasta Mr. Fox?",
        "No podrás seguir mucho más.",
        "Te vas a quedar atrás.",
        "Mejor vuelve atrás.",
        "El camino parece demasiado largo.",
        "Vas a fallar antes de llegar.",
        "Tus pasos no alcanzarán.",
        "El Velo no tiene salida.",
    ),
    TipoEnemigo.ESPEJILLA: (
        "Te vas a perder en la niebla.",
        "No encontrarás el farol.",
        "El final está demasiado lejos.",
        "Nadie llegará a tiempo.",
        "La oscuridad te alcanzará.",
        "Mejor ni lo intentes.",
    ),
}


def dialogoParaCriatura(tipo: TipoEnemigo, indice: int) -> Dialogo:
    """Entrega una voz determinista que pertenece a la criatura creada."""
    frases = FRASES_DESALENTADORAS[tipo]
    hablante = "Susurro" if tipo == TipoEnemigo.SUSURRO else "Espejilla"
    return Dialogo(
        frases[indice % len(frases)],
        hablante=hablante,
        duracionVisible=1.5,
        duracionFundido=0.0,
    )
