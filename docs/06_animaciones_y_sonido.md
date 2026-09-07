# Animaciones y sonido del prólogo

## Decisión

Rumi y su padre se renderizan desde hojas de sprites pixel art. La física y la secuencia narrativa permanecen en `src/dominio.py` y `src/nivelUno.py`; elegir una pose es una adaptación visual en `src/estadoVisual.py`.

## Rumi

- `assets/characters/rumi/rumi_sprite_sheet_v3.png` contiene 12 casillas: reposo, carrera, salto, garras luminosas y cansancio.
- `A`/`D` o flechas activan la carrera; al detenerse vuelve a reposo.
- Al saltar usa la pose de salto.
- `F` muestra durante 0.32 segundos las garras luminosas. Es una respuesta visual y todavía no derrota enemigos ni mide ninguna emoción.

## Padre de Rumi

- `assets/characters/rumi/padre_sprite_sheet_v1.png` añade diseño propio: bufanda azul profundo, broche de brújula y garras luminosas dominadas.
- Mientras Rumi lo sigue, el padre camina; con la niebla adopta la pose de guía y alumbra el camino.

## Pasos

`src/sonidos.py` sintetiza al iniciar el juego un toque corto y suave para las pisadas. No descarga audios, no guarda datos y falla silenciosamente si el equipo no tiene audio disponible. `RitmoPasos` limita el efecto a un paso cada 0.19 segundos y solo se activa al correr sobre una plataforma.

## Verificación

Las reglas de prioridad de pose y de intervalo de pasos están cubiertas en `tests/testEstadoVisual.py`. La prueba visual requiere ejecutar Pygame en un equipo con su dependencia instalada.
