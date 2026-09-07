# Rumi: El Barranco del Velo

Prototipo jugable de exploración y plataformas en español. El primer nivel contiene cinco tramos (6.360 píxeles), el prólogo de Rumi y su padre, y encuentros con Susurros y Espejillas.

## Ejecutar

Objetivo del proyecto: Python 3.11+ y Pygame CE. Con las dependencias ya instaladas:

```bash
.venv/bin/python main.py
```

El entorno disponible durante este refactor tiene Python 3.10.12 y Pygame CE 2.5.8; las pruebas se ejecutaron ahí. No se instaló ni cambió ninguna dependencia. Falta comprobar la ejecución en Python 3.11+.

## Controles

- Flechas o A/D: moverse; W/S o flechas verticales: navegar el menú.
- Espacio: entrar al nivel o saltar; en el aire, junto a una roca, dar un impulso adicional.
- E: escuchar al pajarito.
- F: activar garras luminosas y liberar criaturas cercanas.
- R: reiniciar el nivel completo.
- Escape: volver al menú. Al volver a entrar empieza una partida nueva.

## Arquitectura

`main.py` inicia `Juego`. El juego coordina escenas con un contrato común; la fábrica crea el nivel seleccionado. `EscenaNivelUno` coordina reglas, entrada, cámara, presentación y sonidos. `NivelUno` conserva las reglas sin importar Pygame.

`CreadorBarrancoVelo` construye el mundo; `EscenarioNivel` contiene plataformas tipadas, decoración, elementos, enemigos y tramos. `DibujadorEscenario` interpreta esos datos. Los frames viven en `animaciones.py`; dibujar no avanza su tiempo.

## Verificación

```bash
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python3 -m unittest discover -s tests -p 'test*.py'
```

El modo dummy comprueba integración sin abrir una ventana; no sustituye una partida manual ni la escucha del audio.

## Documentación

- [Fundamento y límites del juego](docs/01_tres_raices_autoestima.md)
- [Personaje Rumi](docs/02_personaje_rumi.md)
- [Criaturas del Velo](docs/03_enemigos_del_velo.md)
- [Niveles y capítulos](docs/04_niveles_y_capitulos.md)
- [Plan técnico inicial](docs/05_plan_tecnico_nivel_01.md)
- [Tareas atómicas, criterios y revisiones del refactor](docs/07_refactor_iteraciones.md)

El juego no presenta sus mecánicas como terapia, diagnóstico ni medición clínica. No usa cuentas, telemetría ni almacenamiento de respuestas personales.
