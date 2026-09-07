"""Mapa largo y encuentros declarativos de Espejos de Niebla."""
from .dominio import RectanguloLogico, Vector2D
from .escenarioNivel import EscenarioNivel, TramoNivel
from .plataformaNivel import PlataformaNivel, TipoTerreno, DecoracionNivel, TipoDecoracion
from .enemigosNivel import TipoEnemigo
from .enemigoHostil import EnemigoHostil


class CreadorEspejosNiebla:
    def __init__(self, recursos):
        self.escenario = EscenarioNivel(recursos, [], [], ancho=7200)
        nombres = ("Faroles apagados", "Arboleda de ecos", "Lago de reflejos", "Cristales del Velo", "Farol del Nombre")
        for indice, nombre in enumerate(nombres):
            inicio = indice * 1440
            fin = inicio + 1440
            material = TipoTerreno.BOSQUE if indice < 2 else TipoTerreno.CRISTAL
            self.escenario.tramos.append(TramoNivel(nombre, inicio, fin))
            self.escenario.plataformas.append(PlataformaNivel(RectanguloLogico(inicio, 580, 1440, 160), material))
            for offset in (680, 1120):
                self.escenario.plataformas.append(PlataformaNivel(RectanguloLogico(inicio + offset, 470, 180, 24), material))
            for offset in range(100, 1440, 160):
                tipo = TipoDecoracion.ARBUSTO if indice < 2 else TipoDecoracion.CRISTAL
                self.escenario.decoraciones.append(DecoracionNivel(tipo, inicio + offset, 580))
            for numero, offset in enumerate((480, 740, 1000, 1260)):
                tipo = TipoEnemigo.SUSURRO if numero % 2 == 0 else TipoEnemigo.ESPEJILLA
                x = inicio + offset
                y = 534 if tipo == TipoEnemigo.SUSURRO else 455
                frase = "No puedes." if tipo == TipoEnemigo.SUSURRO else "Vas a fallar."
                self.escenario.enemigos.append(EnemigoHostil(tipo, Vector2D(x,y), x - 110, min(fin - 50, x + 160), frase))
        self.metaX = self.escenario.ancho - 90
