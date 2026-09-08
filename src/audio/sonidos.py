"""Efectos de sonido locales, sin descargas ni datos del jugador."""

from __future__ import annotations

from array import array
from math import sin, pi
from pathlib import Path
from typing import Any


class RitmoPasos:
    """Regla pura: un paso por intervalo mientras Rumi corre sobre suelo."""

    def __init__(self, intervalo: float = 1.50) -> None:
        self.intervalo = intervalo
        self.tiempoRestante = 0.0

    def actualizar(self, seMueve: bool, estaEnSuelo: bool, deltaTiempo: float) -> bool:
        self.tiempoRestante = max(0.0, self.tiempoRestante - deltaTiempo)
        if seMueve and estaEnSuelo and self.tiempoRestante == 0.0:
            self.tiempoRestante = self.intervalo
            return True
        return False


class SonidosJuego:
    """Carga los sonidos elegidos para el nivel; si falla el audio, el juego continúa."""

    def __init__(self) -> None:
        self.paso: Any | None = None
        self.salto: Any | None = None
        self.aterrizaje: Any | None = None
        self.derrumbe: Any | None = None
        self.ambiente: Any | None = None
        self.musicaCueva: Any | None = None
        self.canalDerrumbe: Any | None = None
        self.canalAmbiente: Any | None = None
        self.canalMusicaCueva: Any | None = None
        self.tiempoDerrumbe = 0.0
        self.tiempoAmbiente = 0.0
        self.ambienteAtenuando = False
        try:
            import pygame

            if pygame.mixer.get_init() is None:
                pygame.mixer.init()
            raiz = Path(__file__).resolve().parents[2]
            self.paso = pygame.mixer.Sound(str(raiz / "assets/sounds/procesados/caminata.wav"))
            self.salto = pygame.mixer.Sound(str(raiz / "assets/sounds/procesados/salto.wav"))
            self.aterrizaje = pygame.mixer.Sound(str(raiz / "assets/sounds/procesados/aterrizaje.wav"))
            self.derrumbe = pygame.mixer.Sound(str(raiz / "assets/sounds/originales/explosion.ogg"))
            self.ambiente = pygame.mixer.Sound(str(raiz / "sounds/soundreality-jungle-night-pad-381096.mp3"))
            self.musicaCueva = pygame.mixer.Sound(
                str(raiz / "assets/sounds/musica/dungeon_ambient_1.ogg")
            )
            self.paso.set_volume(0.20)
            self.salto.set_volume(0.35)
            self.aterrizaje.set_volume(0.30)
            self.derrumbe.set_volume(0.32)
            self.ambiente.set_volume(0.22)
            self.musicaCueva.set_volume(0.16)
        except Exception:
            self.paso = self.salto = self.aterrizaje = self.derrumbe = self.ambiente = None
            self.musicaCueva = None

    def crearPaso(self) -> Any:
        import pygame

        frecuenciaMuestreo = 22050
        duracion = 0.075
        cantidad = int(frecuenciaMuestreo * duracion)
        muestras = array("h")
        for indice in range(cantidad):
            progreso = indice / cantidad
            envolvente = (1.0 - progreso) ** 2
            tono = sin(2 * pi * (165 - 80 * progreso) * indice / frecuenciaMuestreo)
            muestras.append(int(tono * envolvente * 4800))
        return pygame.mixer.Sound(buffer=muestras.tobytes())

    def reproducirPaso(self) -> None:
        if self.paso is not None:
            self.paso.play()

    def reproducirSalto(self) -> None:
        if self.salto is not None:
            self.salto.play()

    def reproducirAterrizaje(self) -> None:
        if self.aterrizaje is not None:
            self.aterrizaje.play()

    def reproducirDerrumbe(self, duracion: float = 5.0) -> None:
        if self.derrumbe is not None:
            self.canalDerrumbe = self.derrumbe.play()
            self.tiempoDerrumbe = duracion

    def reproducirAmbienteInicial(self) -> None:
        if self.ambiente is not None:
            self.canalAmbiente = self.ambiente.play()
            self.tiempoAmbiente = 3.0
            self.ambienteAtenuando = False

    def reproducirMusicaCueva(self) -> None:
        """Mantiene una ambientación discreta durante el recorrido de la cueva."""
        if self.musicaCueva is not None and self.canalMusicaCueva is None:
            self.canalMusicaCueva = self.musicaCueva.play(loops=-1)

    def actualizar(self, deltaTiempo: float) -> None:
        self.tiempoDerrumbe = max(0.0, self.tiempoDerrumbe - deltaTiempo)
        if self.tiempoDerrumbe == 0.0 and self.canalDerrumbe is not None:
            self.canalDerrumbe.stop()
            self.canalDerrumbe = None
        self.tiempoAmbiente = max(0.0, self.tiempoAmbiente - deltaTiempo)
        if self.tiempoAmbiente <= 1.0 and not self.ambienteAtenuando and self.canalAmbiente is not None:
            self.canalAmbiente.fadeout(1000)
            self.ambienteAtenuando = True
