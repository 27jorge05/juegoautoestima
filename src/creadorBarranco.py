"""Construcción del Barranco; concentra mapa y posiciones de sus entidades."""
from dataclasses import dataclass
from .dominio import RectanguloLogico, Vector2D, Padre
from .elementosNivel import ConfiguracionNiebla, ConfiguracionRocaImpulso, NieblaNivel, RocaImpulso
from .escenarioNivel import EscenarioNivel, TramoNivel
from .enemigosNivel import EnemigoNivel, TipoEnemigo
from .plataformaNivel import PlataformaNivel, TipoTerreno, DecoracionNivel, TipoDecoracion


@dataclass
class ZonaNivel:
    nombre: str
    rectangulo: RectanguloLogico


class CreadorBarrancoVelo:
    def __init__(self, recursos):
        self.recursos = recursos
        plataformas = [
            RectanguloLogico(-100.0, 580.0, 1020.0, 160.0),
            RectanguloLogico(1120.0, 580.0, 760.0, 160.0),
            RectanguloLogico(940.0, 490.0, 110.0, 24.0),
            RectanguloLogico(1320.0, 480.0, 140.0, 24.0),
        ]
        plataformas = [PlataformaNivel(rectangulo, TipoTerreno.BOSQUE) for rectangulo in plataformas]
        rocasImpulso = [
            RocaImpulso(
                ConfiguracionRocaImpulso(RectanguloLogico(590.0, 520.0, 130.0, 60.0))
            ),
            RocaImpulso(
                ConfiguracionRocaImpulso(RectanguloLogico(950.0, 515.0, 130.0, 65.0))
            ),
        ]
        self.niebla = NieblaNivel(
            ConfiguracionNiebla(RectanguloLogico(430.0, 0.0, 470.0, 720.0))
        )
        self.escenario = EscenarioNivel(self.recursos, plataformas, [*rocasImpulso, self.niebla])
        self.zonaTerremoto = ZonaNivel(
            "terremoto", RectanguloLogico(820.0, 0.0, 100.0, 720.0)
        )
        self.zonaMadriguera = ZonaNivel(
            "madriguera", RectanguloLogico(1170.0, 480.0, 140.0, 100.0)
        )
        self.zonaPajarito = ZonaNivel(
            "pajarito", RectanguloLogico(1370.0, 400.0, 130.0, 180.0)
        )
        self.zonaSalida = ZonaNivel(
            "salida", RectanguloLogico(1660.0, 450.0, 120.0, 130.0)
        )
        self.padre = Padre(Vector2D(350.0, 526.0))
        self.pajaritoPosicion = Vector2D(1420.0, 410.0)
        self.escenario.decoraciones = [
            DecoracionNivel(TipoDecoracion.HUELLA, x, 572 if i % 2 == 0 else 576)
            for i, x in enumerate(range(180, 820, 64))
        ]
        self.escenario.tramos = [TramoNivel("Camino del Alba", 0, 1880)]
        for nombre, inicio, fin, material in (
            ("Raíces del bosque", 1880, 3000, TipoTerreno.BOSQUE),
            ("Claro de susurros", 3000, 4120, TipoTerreno.ROCA_NIEBLA),
            ("Sendero de cristal", 4120, 5240, TipoTerreno.CRISTAL),
            ("Umbral luminoso", 5240, 6360, TipoTerreno.RUINAS),
        ):
            self.agregarTramo(nombre, inicio, fin, material)
        self.escenario.ancho = self.escenario.tramos[-1].fin
        self.metaX = self.escenario.ancho - 100
        self.escenario.enemigos = [
            EnemigoNivel(TipoEnemigo.SUSURRO, Vector2D(3220, 534)),
            EnemigoNivel(TipoEnemigo.SUSURRO, Vector2D(3340, 534)),
            EnemigoNivel(TipoEnemigo.ESPEJILLA, Vector2D(4520, 510)),
            EnemigoNivel(TipoEnemigo.ESPEJILLA, Vector2D(4830, 510)),
        ]

    def agregarTramo(self, nombre, inicio, fin, material):
        """Módulo reutilizable de suelo continuo y plataformas opcionales."""
        self.escenario.tramos.append(TramoNivel(nombre, inicio, fin))
        self.escenario.plataformas.append(PlataformaNivel(RectanguloLogico(inicio, 580, fin - inicio, 160), material))
        self.escenario.plataformas.append(PlataformaNivel(RectanguloLogico(inicio + 420, 490, 160, 24), material))
        for i, x in enumerate(range(int(inicio + 100), int(fin - 80), 150)):
            tipo = TipoDecoracion.CRISTAL if material == TipoTerreno.CRISTAL else TipoDecoracion.ARBUSTO
            self.escenario.decoraciones.append(DecoracionNivel(tipo, x, 580))
            self.escenario.decoraciones.append(DecoracionNivel(TipoDecoracion.HUELLA, x + 60, 570))
