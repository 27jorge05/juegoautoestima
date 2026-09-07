"""Construcción del Barranco; concentra mapa y posiciones de sus entidades."""
from dataclasses import dataclass
from .dominio import RectanguloLogico, Vector2D, Padre
from .elementosNivel import ConfiguracionRocaImpulso, RocaImpulso
from .escenarioNivel import EscenarioNivel, TramoNivel
from .enemigosNivel import TipoEnemigo
from .enemigoHostil import EnemigoHostil
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
        # El Barranco no usa niebla: la dificultad es seguir a papá y encontrarlo al final.
        self.escenario = EscenarioNivel(self.recursos, plataformas, rocasImpulso)
        self.escenario.decoraciones = [
            DecoracionNivel(TipoDecoracion.HUELLA, x, 572 if i % 2 == 0 else 576)
            for i, x in enumerate(range(180, 820, 64))
        ]
        self.escenario.tramos = [TramoNivel("Camino del Alba", 0, 1880)]
        for nombre, inicio, fin, material in (
            ("Raíces del bosque", 1880, 3000, TipoTerreno.BOSQUE),
            ("Claro de susurros", 3000, 4120, TipoTerreno.BOSQUE),
            ("Sendero de cristal", 4120, 5240, TipoTerreno.CRISTAL),
            ("Umbral luminoso", 5240, 6360, TipoTerreno.RUINAS),
        ):
            self.agregarTramo(nombre, inicio, fin, material)
        self.escenario.ancho = self.escenario.tramos[-1].fin
        self.metaX = self.escenario.ancho - 100
        self.padre = Padre(Vector2D(self.metaX, 526.0))
        self.escenario.enemigos = [
            self.crearEnemigo(TipoEnemigo.SUSURRO, 3220, 534, "No llegarás con tu papá."),
            self.crearEnemigo(TipoEnemigo.SUSURRO, 3540, 534, "No puedes seguir."),
            self.crearEnemigo(TipoEnemigo.ESPEJILLA, 4520, 455, "Te vas a perder."),
            self.crearEnemigo(TipoEnemigo.ESPEJILLA, 5140, 455, "Vuelve atrás."),
        ]

    @staticmethod
    def crearEnemigo(tipo, x, y, frase):
        return EnemigoHostil(
            tipo,
            Vector2D(x, y),
            x - 150,
            x + 180,
            frase,
        )

    def agregarTramo(self, nombre, inicio, fin, material):
        """Módulo reutilizable de suelo continuo y plataformas opcionales."""
        self.escenario.tramos.append(TramoNivel(nombre, inicio, fin))
        self.escenario.plataformas.append(PlataformaNivel(RectanguloLogico(inicio, 580, fin - inicio, 160), material))
        self.escenario.plataformas.append(PlataformaNivel(RectanguloLogico(inicio + 420, 490, 160, 24), material))
        for i, x in enumerate(range(int(inicio + 100), int(fin - 80), 150)):
            tipo = TipoDecoracion.CRISTAL if material == TipoTerreno.CRISTAL else TipoDecoracion.ARBUSTO
            self.escenario.decoraciones.append(DecoracionNivel(tipo, x, 580))
            self.escenario.decoraciones.append(DecoracionNivel(TipoDecoracion.HUELLA, x + 60, 570))
