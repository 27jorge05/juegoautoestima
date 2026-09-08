"""Construcción declarativa de la Cueva del Velo."""

from src.dominio.dominio import RectanguloLogico, Vector2D
from src.dominio.enemigoHostil import EnemigoHostil
from .elementosNivel import ConfiguracionNiebla, ConfiguracionRocaImpulso, FarolNiebla, NieblaNivel, NUBES_NIEBLA_DENSA, PilarAliento, RocaImpulso, TipoNiebla
from src.dominio.enemigosNivel import TipoEnemigo
from .escenarioNivel import EscenarioNivel, TramoNivel
from src.dominio.plataformaNivel import DecoracionNivel, PlataformaNivel, TipoDecoracion, TipoTerreno
from src.dominio.dificultadEnemigos import NIVEL_TRES


class CreadorCuevaVelo:
    def __init__(self, recursos):
        self.niebla = NieblaNivel(
            ConfiguracionNiebla(
                RectanguloLogico(0, 0, 6000, 720),
                opacidadBase=238,
                variantesVisuales=(TipoNiebla.AZUL, TipoNiebla.VIOLETA, TipoNiebla.OSCURA),
                configuracionNubes=NUBES_NIEBLA_DENSA,
            )
        )
        self.niebla.activar()
        self.escenario = EscenarioNivel(recursos, [], [self.niebla], ancho=6000)
        for indice, nombre in enumerate(("Entrada", "Galería de cristales", "Pasaje estrecho", "Cámara luminosa", "Salida")):
            inicio = indice * 1200
            fin = inicio + 1200
            self.escenario.tramos.append(TramoNivel(nombre, inicio, fin))
            self.escenario.plataformas.append(
                PlataformaNivel(RectanguloLogico(inicio, 580, 1200, 160), TipoTerreno.CRISTAL)
            )
            for desplazamiento in (330, 720, 980):
                self.escenario.plataformas.append(
                    PlataformaNivel(RectanguloLogico(inicio + desplazamiento, 470, 155, 24), TipoTerreno.RUINAS)
                )
            for desplazamiento in (520, 900):
                self.escenario.elementos.append(
                    RocaImpulso(
                        ConfiguracionRocaImpulso(
                            RectanguloLogico(inicio + desplazamiento, 470, 100, 60),
                            brillo=True,
                        )
                    )
                )
            for desplazamiento in range(90, 1150, 180):
                self.escenario.decoraciones.append(DecoracionNivel(TipoDecoracion.CRISTAL, inicio + desplazamiento, 580))
            for numero, desplazamiento in enumerate((250, 680, 1080)):
                if indice == 0 and numero == 0:
                    continue
                tipo = TipoEnemigo.SUSURRO if numero != 1 else TipoEnemigo.ESPEJILLA
                x = inicio + desplazamiento
                y = 534 if tipo == TipoEnemigo.SUSURRO else 440
                self.escenario.enemigos.append(
                    EnemigoHostil(
                        tipo,
                        Vector2D(x, y),
                        x - 130,
                        x + 150,
                        "",
                        emiteFrase=False,
                        vulnerableALuz=False,
                        oscuro=True,
                        mostrarIndicadorEstado=False,
                        perfilDificultad=NIVEL_TRES,
                    )
                )
        for x, mensaje in ((700, "animo"), (1810, "brillo"), (3275, "camino"), (4705, "compania")):
            self.escenario.pilares.append(
                PilarAliento(RectanguloLogico(x, 460, 48, 120), mensaje)
            )
        for x in (480, 1640, 2860, 4100, 5380):
            self.escenario.elementos.append(FarolNiebla(RectanguloLogico(x, 500, 42, 80)))
        self.metaX = self.escenario.ancho - 90
