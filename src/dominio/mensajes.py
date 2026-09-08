"""Mensajes narrativos y diálogos con su propio tiempo de presentación."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Mensaje:
    texto: str
    duracionVisible: float = 7.0
    duracionFundido: float = 1.2

    @property
    def textoMostrado(self) -> str:
        return self.texto


@dataclass(frozen=True)
class Relato(Mensaje):
    """Voz narrativa sin personaje que habla."""


@dataclass(frozen=True)
class Dialogo(Mensaje):
    """Palabras dichas por un personaje o una criatura concreta."""

    hablante: str = ""

    @property
    def textoMostrado(self) -> str:
        return f"{self.hablante}: {self.texto}" if self.hablante else self.texto


class PresentadorMensajes:
    """Estado temporal reutilizable; los niveles no administran alfa ni fundido."""

    def __init__(self, mensaje: Mensaje) -> None:
        self.mensaje = mensaje
        self.tiempoTranscurrido = 0.0

    def mostrar(self, mensaje: Mensaje) -> None:
        self.mensaje = mensaje
        self.tiempoTranscurrido = 0.0

    def actualizar(self, deltaTiempo: float) -> None:
        self.tiempoTranscurrido += max(0.0, deltaTiempo)

    @property
    def alfa(self) -> int:
        visible = self.mensaje.duracionVisible
        fundido = self.mensaje.duracionFundido
        if self.tiempoTranscurrido <= visible:
            return 255
        if fundido <= 0.0:
            return 0
        progreso = (self.tiempoTranscurrido - visible) / fundido
        return max(0, round(255 * (1.0 - progreso)))

    @property
    def texto(self) -> str:
        return self.mensaje.textoMostrado

    @property
    def terminado(self) -> bool:
        """Indica que ya concluyeron el tiempo visible y el fundido del mensaje."""
        return self.tiempoTranscurrido >= (
            self.mensaje.duracionVisible + self.mensaje.duracionFundido
        )
