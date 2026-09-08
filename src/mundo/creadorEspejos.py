"""Mapa largo y encuentros declarativos de Espejos de Niebla."""
from src.dominio.dominio import Padre, RectanguloLogico, Vector2D
from .escenarioNivel import EscenarioNivel, TramoNivel
from src.dominio.plataformaNivel import PlataformaNivel, TipoTerreno, DecoracionNivel, TipoDecoracion
from src.dominio.enemigosNivel import TipoEnemigo
from src.dominio.enemigoHostil import EnemigoHostil
from .elementosNivel import ConfiguracionRocaImpulso, RocaImpulso
from src.dominio.frasesVelo import dialogoParaCriatura
from src.dominio.dificultadEnemigos import NIVEL_DOS


class CreadorEspejosNiebla:
    def __init__(self, recursos):
        self.escenario = EscenarioNivel(recursos, [], [], ancho=7200)
        nombres = ("Faroles apagados", "Arboleda de ecos", "Lago de reflejos", "Cristales del Velo", "Farol del Nombre")
        terrenoPorTramo = (
            ((0, 560), (820, 160), (1240, 200)),
            ((0, 540), (800, 190), (1220, 220)),
            ((0, 575), (835, 145), (1215, 225)),
            ((0, 520), (790, 205), (1200, 240)),
            ((0, 555), (825, 170), (1235, 205)),
        )
        rocasPorTramo = (
            ((640, 430), (1060, 370)),
            ((620, 445), (1040, 360)),
            ((650, 410), (1055, 385)),
            ((600, 450), (1035, 350)),
            ((635, 420), (1070, 375)),
        )
        encuentrosPorTramo = (
            (270, 510, 690, 910, 1090, 1310),
            (240, 470, 650, 875, 1110, 1340),
            (290, 530, 720, 945, 1080, 1290),
            (230, 495, 675, 900, 1135, 1360),
            (280, 455, 705, 930, 1100, 1325),
        )
        for indice, nombre in enumerate(nombres):
            inicio = indice * 1440
            fin = inicio + 1440
            material = TipoTerreno.BOSQUE if indice < 2 else TipoTerreno.CRISTAL
            self.escenario.tramos.append(TramoNivel(nombre, inicio, fin))
            # Dos precipicios por tramo: las rocas elevadas dan la ruta segura.
            for offset, ancho in terrenoPorTramo[indice]:
                self.escenario.plataformas.append(PlataformaNivel(RectanguloLogico(inicio + offset, 580, ancho, 160), material))
            for offset, altura in ((100, 470), (1350, 430)):
                self.escenario.plataformas.append(PlataformaNivel(RectanguloLogico(inicio + offset, altura, 80, 24), material))
            for offset, altura in rocasPorTramo[indice]:
                self.escenario.elementos.append(
                    RocaImpulso(
                        ConfiguracionRocaImpulso(
                            RectanguloLogico(inicio + offset, altura, 100, 60),
                            margenSuperior=150,
                        )
                    )
                )
            for offset in range(100, 1440, 160):
                tipo = TipoDecoracion.ARBUSTO if indice < 2 else TipoDecoracion.CRISTAL
                self.escenario.decoraciones.append(DecoracionNivel(tipo, inicio + offset, 580))
            for numero, offset in enumerate(encuentrosPorTramo[indice]):
                tipo = TipoEnemigo.SUSURRO if numero % 2 == 0 else TipoEnemigo.ESPEJILLA
                x = inicio + offset
                y = 534 if tipo == TipoEnemigo.SUSURRO else 335
                dialogo = dialogoParaCriatura(tipo, indice * 6 + numero)
                self.escenario.enemigos.append(EnemigoHostil(tipo, Vector2D(x,y), x - 110, min(fin - 50, x + 160), dialogo, perfilDificultad=NIVEL_DOS))
        self.metaX = self.escenario.ancho - 90
        self.padre = Padre(Vector2D(250, 526))
