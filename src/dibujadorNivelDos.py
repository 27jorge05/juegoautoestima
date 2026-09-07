"""Presentación de Espejos de Niebla: avisos legibles y derrota jugable."""
from pathlib import Path
import pygame
from .animaciones import crearAnimacionRumi
from .dibujadorEscenario import DibujadorEscenario
from .dibujadorNivelUno import ajustarTexto
from .estadoVisual import obtenerAnimacionRumi
from .enemigoHostil import EstadoEnemigo
from .nivelDos import EstadoNivelDos
from .indicadoresVida import CorazonesVida, DestelloDanio


class DibujadorNivelDos:
    def __init__(self,pantalla,recursos):
        self.pantalla = pantalla
        self.escenario = DibujadorEscenario(pantalla,recursos)
        # Variante nocturna de los recursos compartidos, solo en esta instancia.
        if self.escenario.fondo:
            self.escenario.fondo.fill((150,165,215,255),special_flags=pygame.BLEND_RGBA_MULT)
            self.escenario.fondoEspejo = pygame.transform.flip(self.escenario.fondo,True,False)
        self.animacion = crearAnimacionRumi(Path(__file__).resolve().parents[1]/'assets/characters/rumi/rumi_sprite_sheet_v3.png')
        self.fuente = pygame.font.SysFont('sans',22)
        self.titulo = pygame.font.SysFont('sans',32,bold=True)
        self.tiempoEfectoSalto = 0.0
        self.destelloDanio = DestelloDanio()
        self.corazones = CorazonesVida(self.fuente)

    def reiniciar(self):
        self.animacion.reiniciar()
        self.tiempoEfectoSalto = 0.0

    def registrarSalto(self,x,y):
        self.tiempoEfectoSalto = .2

    def registrarGolpe(self):
        self.destelloDanio.activar()

    def actualizar(self,nivel,deltaTiempo):
        self.tiempoEfectoSalto = max(0.0,self.tiempoEfectoSalto-deltaTiempo)
        self.destelloDanio.actualizar(deltaTiempo)
        rumi=nivel.rumi
        nombre = 'cansado' if nivel.estado == EstadoNivelDos.DERROTADO else obtenerAnimacionRumi(rumi.velocidad.x,rumi.velocidad.y,rumi.estaEnSuelo,rumi.garrasActivas)
        if nivel.estado != EstadoNivelDos.JUGANDO:
            self.animacion.actualizar(nombre,0)
        else:
            self.animacion.actualizar(nombre,deltaTiempo)

    def dibujar(self,nivel,camara):
        if nivel.temblor > 0:
            w,h=self.pantalla.get_size()
            flash=pygame.Surface((w,h),pygame.SRCALPHA)
            flash.fill((255,110,90,min(130,int(180*(nivel.temblor/2.4)))))
            self.pantalla.blit(flash,(0,0))
        self.escenario.dibujarMundo(nivel.escenario,None,camara)
        rumi=nivel.rumi
        pies=(round(rumi.posicion.x+rumi.ancho/2-camara),round(rumi.rectangulo.abajo))
        self.animacion.dibujarAnclado(self.pantalla,pies,(132,118),rumi.miraDerecha)
        if nivel.vitalidad.invulnerabilidad > 0 and nivel.estado == EstadoNivelDos.JUGANDO:
            pygame.draw.ellipse(self.pantalla,(150,223,240),(pies[0]-60,pies[1]-125,120,130),2)
        if rumi.garrasActivas and nivel.estado == EstadoNivelDos.JUGANDO:
            pygame.draw.circle(self.pantalla,(174,245,219),(pies[0],pies[1]-23),110,2)
        if self.tiempoEfectoSalto > 0:
            pygame.draw.ellipse(self.pantalla,(177,231,255),(pies[0]-25,pies[1]-4,50,8),2)
        if nivel.estado == EstadoNivelDos.JUGANDO:
            self.dibujarAvisos(nivel,camara)
        meta=round(nivel.metaX-camara)
        pygame.draw.rect(self.pantalla,(152,175,187),(meta,460,12,120))
        pygame.draw.circle(self.pantalla,(255,228,135),(meta+6,450),24)
        self.dibujarInterfaz(nivel)
        if nivel.estado != EstadoNivelDos.JUGANDO:
            self.dibujarFinal(nivel)
        self.destelloDanio.dibujar(self.pantalla)

    def dibujarAvisos(self,nivel,camara):
        for enemigo in nivel.escenario.enemigos:
            if enemigo.estado not in (EstadoEnemigo.AVISO,EstadoEnemigo.ATAQUE):
                continue
            x,y=round(enemigo.posicion.x-camara),round(enemigo.posicion.y)
            if not -60 < x < self.pantalla.get_width()+60:
                continue
            color=(246,184,117) if enemigo.estado == EstadoEnemigo.AVISO else (240,124,146)
            pygame.draw.circle(self.pantalla,color,(x+20,y+22),38,3)
            if enemigo.estado == EstadoEnemigo.AVISO:
                texto=self.fuente.render(f'Velo: «{enemigo.frase}»',True,(255,220,210))
                tx=max(8,min(x-texto.get_width()/2,self.pantalla.get_width()-texto.get_width()-8))
                fondo=pygame.Rect(round(tx)-6,y-85,texto.get_width()+12,34)
                pygame.draw.rect(self.pantalla,(38,26,48),fondo,border_radius=6)
                self.pantalla.blit(texto,(round(tx),y-82))
                signo=self.titulo.render('!',True,color)
                self.pantalla.blit(signo,(x+14,y-40))

    def dibujarInterfaz(self,nivel):
        w,h=self.pantalla.get_size()
        self.pantalla.blit(self.titulo.render('Espejos de Niebla',True,(230,222,255)),(28,20))
        self.corazones.dibujar(self.pantalla,nivel.vitalidad.puntos,3,w-180,27,self.destelloDanio.activo)
        tramo=next((t.nombre for t in nivel.escenario.tramos if t.inicio <= nivel.rumi.posicion.x < t.fin),'Farol del Nombre')
        self.pantalla.blit(self.fuente.render(tramo,True,(166,209,221)),(28,62))
        panel=pygame.Surface((w-48,116),pygame.SRCALPHA);panel.fill((12,15,31,225))
        self.pantalla.blit(panel,(24,h-136))
        for i,linea in enumerate(ajustarTexto(nivel.dialogo,self.fuente,w-96)):
            self.pantalla.blit(self.fuente.render(linea,True,(233,235,249)),(44,h-126+i*26))
        luz='lista' if nivel.recargaLuz == 0 else f'{nivel.recargaLuz:.1f}s'
        ayuda=f'Espacio: saltar | F: luz ({luz}) | R: reiniciar | Escape: menú'
        self.pantalla.blit(self.fuente.render(ayuda,True,(158,217,213)),(44,h-49))

    def dibujarFinal(self,nivel):
        w,h=self.pantalla.get_size()
        capa=pygame.Surface((w,h),pygame.SRCALPHA);capa.fill((10,12,26,165))
        self.pantalla.blit(capa,(0,0))
        if nivel.estado == EstadoNivelDos.COMPLETADO:
            textos=(
                'Farol recuperado',
                'Ya no encuentras a tu padre. Busca el farol para seguir el camino.',
                'Siguiente nivel: bloqueado (nivel 3 en construcción)  |  R: volver a jugar  |  Escape: menú',
            )
        else:
            textos=(
                'Rumi ha caído',
                'Un intento no decide lo que puedes aprender.',
                'R: volver a jugar    |    Escape: menú',
            )
        for i,texto in enumerate(textos):
            fuente=self.titulo if i==0 else self.fuente
            imagen=fuente.render(texto,True,(240,230,255))
            self.pantalla.blit(imagen,((w-imagen.get_width())//2,h//2-60+i*48))
