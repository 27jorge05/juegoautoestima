"""Prepara segmentos WAV elegidos por diseño para Rumi."""

from __future__ import annotations

from pathlib import Path
import wave


def recortarWav(origen: Path, destino: Path, inicio: float, final: float | None) -> None:
    with wave.open(str(origen), "rb") as lector:
        frecuencia = lector.getframerate()
        inicioFotograma = int(inicio * frecuencia)
        finalFotograma = lector.getnframes() if final is None else int(final * frecuencia)
        lector.setpos(inicioFotograma)
        datos = lector.readframes(max(0, finalFotograma - inicioFotograma))
        parametros = lector.getparams()
    destino.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(destino), "wb") as escritor:
        escritor.setparams(parametros)
        escritor.writeframes(datos)


if __name__ == "__main__":
    raiz = Path(__file__).resolve().parents[1]
    origen = raiz / "sounds" / "main character"
    destino = raiz / "assets" / "sounds" / "procesados"
    recortarWav(origen / "jumping.wav", destino / "salto.wav", 0.0, 0.37)
    recortarWav(origen / "jumping.wav", destino / "aterrizaje.wav", 0.37, None)
    recortarWav(origen / "runing.wav", destino / "caminata.wav", 1.0, 2.5)
