"""Ejecuta los controles finales; las capturas requieren revisión humana."""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'
import sys
from pathlib import Path
raiz = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(raiz), str(raiz/'tests')]
import unittest
import pygame
from src.juego import Juego
from src.dominio import EstadoNivel

revisiones = [
 (41, 'Dependencias', ['testIntegridad.PruebasIntegridad.testDominioNoImportaPresentacion']),
 (42, 'Geometría', ['testEscenario.PruebasEscenario.testMaterialNoCambiaColision','testEscenario.PruebasEscenario.testDecoracionNoEsSuelo']),
 (43, 'Reinicio', ['testEscenario.PruebasEscenario.testFabricaNoComparteElementos','testRecorrido.PruebasRecorrido.testReinicioRestauraCriaturas','testIntegridad.PruebasIntegridad.testReinicioLimpiaPresentacionYDibujoNoAvanza']),
 (44, 'Narrativa', ['testNivelUno']),
 (45, 'Física', ['testDominio','testIntegridad.PruebasIntegridad.testCaidaYLimites','testIntegridad.PruebasIntegridad.testImpulsoSoloUnaVezYCerca']),
 (46, 'Animaciones', ['testPresentacion.PruebasPresentacion.testFrameYAnclajeReal','testPresentacion.PruebasPresentacion.testEsperaSoloCuentaExcedente','testPresentacion.PruebasPresentacion.testDefinicionRechazaAnimacionInvalida']),
 (47, 'Mapa', ['testRecorrido']),
 (48, 'Aplicación', ['testMenu','testPresentacion.PruebasPresentacion.testEntradaConsumePulsacion','testPresentacion.PruebasPresentacion.testMenuSoloAbreDesbloqueados','testPresentacion.PruebasPresentacion.testFabricaInyectable','testIntegridad.PruebasIntegridad.testCerrarAplicacion']),
]
for numero, nombre, casos in revisiones:
    print(f'ITERACIÓN {numero}: {nombre}',flush=True)
    resultado=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromNames(casos))
    if not resultado.wasSuccessful():
        raise SystemExit(1)
print('ITERACIÓN 49: capturas reales',flush=True)
juego=Juego()
juego.escena.dibujar()
pygame.image.save(juego.pantalla,'/tmp/rumi-menu-final.png')
juego.iniciarNivel(1)
escena=juego.escena
escena.actualizar(.016);escena.dibujar()
pygame.image.save(juego.pantalla,'/tmp/rumi-inicio-final.png')
escena.nivel.rumi.posicion.x=4400
escena.nivel.secuencia.estado=EstadoNivel.SALIDA
escena.nivel.dialogo='Sigue las huellas. F: ilumina a las criaturas del Velo.'
escena.actualizar(.016);escena.dibujar()
pygame.image.save(juego.pantalla,'/tmp/rumi-cristal-final.png')
escena.cerrar();pygame.quit()
print('Capturas generadas para inspección; la revisión 49 requiere inspección visual.',flush=True)

print('ITERACIÓN 50: regresión completa', flush=True)
resultado = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.discover(str(raiz/'tests'), pattern='test*.py'))
if not resultado.wasSuccessful():
    raise SystemExit(1)
import compileall
if not compileall.compile_dir(str(raiz/'src'), quiet=1):
    raise SystemExit(1)
print('Regresión y compilación correctas.', flush=True)
