"""Selección declarativa de los recursos visuales de cada nivel."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SeleccionRecursosNivel:
    identificadorMapa: str
    rutaFondo: str
    rutaSuelo: str
    rutaRocas: str
    rutaEnemigos: str
    recorteSuperiorSuelo: int = 320
    recorteInferiorSuelo: int = 100


def crearRecursosBarrancoVelo() -> SeleccionRecursosNivel:
    return SeleccionRecursosNivel(
        identificadorMapa="barranco_del_velo",
        rutaFondo="assets/backgrounds/barranco_del_velo_v1.png",
        rutaSuelo="assets/backgrounds/tierra_bosque_pixel_v1.png",
        rutaRocas="assets/enemies/rocas_impulso_v1.png",
        rutaEnemigos="assets/enemies/enemigos_nivel_01_v1.png",
    )


# Apariencia de cada material: el nivel solo declara el enum.
from src.dominio.plataformaNivel import TipoTerreno

COLORES_TERRENO = {
    TipoTerreno.ROCA_NIEBLA: (82, 91, 115),
    TipoTerreno.BOSQUE: (67, 114, 92),
    TipoTerreno.CRISTAL: (112, 153, 195),
    TipoTerreno.RUINAS: (99, 103, 128),
}

TINTES_TERRENO = {
    TipoTerreno.ROCA_NIEBLA: (200, 205, 235),
    TipoTerreno.BOSQUE: (255, 255, 255),
    TipoTerreno.CRISTAL: (185, 235, 255),
    TipoTerreno.RUINAS: (210, 200, 225),
}


def crearRecursosEspejosNiebla() -> SeleccionRecursosNivel:
    from dataclasses import replace
    return replace(crearRecursosBarrancoVelo(), identificadorMapa="espejos_de_niebla")


def crearRecursosCuevaVelo() -> SeleccionRecursosNivel:
    from dataclasses import replace
    return replace(crearRecursosBarrancoVelo(), identificadorMapa="cueva_del_velo")
