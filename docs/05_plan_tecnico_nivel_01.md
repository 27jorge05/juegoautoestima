# Plan técnico: Nivel 01 — El Barranco del Velo

## Alcance del prototipo

Se construirá un nivel jugable de Pygame, en español, con gráficos temporales dibujados por código hasta incorporar sprites PNG. El objetivo es comprobar que Rumi se mueve bien, que la secuencia narrativa se entiende y que el nivel puede ampliarse.

## Secuencia del nivel

1. Rumi sigue a su padre por el Camino del Alba.
2. El padre espera y sus garras luminosas iluminan la ruta cuando entra la niebla.
3. Un terremoto abre un barranco y los separa; el padre promete encontrarlo más adelante.
4. Rumi llega asustado a una madriguera y puede esconderse.
5. Un pajarito luminoso le habla y lo anima a salir.
6. Rumi sale de la madriguera; empieza la aventura real.

## Iteraciones 01–05: planificación

| Iteración | Decisión | Criterio de aceptación |
|---|---|---|
| 01 | Arquitectura por capas: presentación, dominio y nivel. | Lógica del nivel no depende directamente de cómo se dibuja. |
| 02 | Modelo de estados para la secuencia narrativa. | El nivel pasa entre seguir, niebla, terremoto, madriguera y salida. |
| 03 | Física simple y determinista: posición, velocidad, suelo, salto y colisión. | Rumi no atraviesa el suelo ni salta indefinidamente. |
| 04 | Entradas configurables: A/D o flechas, espacio para saltar y E para interactuar. | El jugador completa las acciones con teclado. |
| 05 | Render temporal reemplazable por sprites. | Se puede cambiar a PNG sin reescribir reglas del juego. |

## Principios aplicados

- **Responsabilidad única:** cada clase controla física, diálogo, nivel o dibujo, pero no varias a la vez.
- **Abierto/cerrado:** nuevas fases y enemigos se añaden sin reescribir a Rumi.
- **Inversión de dependencias:** la lógica recibe entradas y produce estado; el dibujo consume ese estado.
- **Nombres en español y camelCase:** por ejemplo, `estadoNivel`, `actualizarFisica`, `mostrarDialogo`.

## Iteraciones 06–30: construcción

| Rango | Entregable |
|---|---|
| 06–10 | Ventana, bucle, configuración, movimiento y colisiones. |
| 11–15 | Padre, luz de garras, cámara y ruta inicial. |
| 16–20 | Niebla, terremoto, barranco y separación. |
| 21–25 | Madriguera, escondite, pajarito y diálogos. |
| 26–30 | Susurro, Espejilla, pulido de UI, guardado de progreso y documentación. |

### Registro de construcción 06–30

| Iteración | Resultado |
|---|---|
| 06 | Se creó `requirements.txt` con Pygame CE. |
| 07 | Se creó configuración central de pantalla, física y controles. |
| 08 | Se creó el modelo `Vector2D` y rectángulos de colisión. |
| 09 | Se creó `Rumi` con posición, gravedad, salto y luz. |
| 10 | Se agregó resolución de suelo y reinicio. |
| 11 | Se creó la secuencia de estados del prólogo. |
| 12 | Se agregaron plataformas y zonas del nivel. |
| 13 | Se agregó padre con posición y luz temporal. |
| 14 | Se agregó cámara lateral. |
| 15 | Se agregaron controles A/D, flechas, espacio, E y R. |
| 16 | Se agregó niebla visual temporal. |
| 17 | Se agregó disparador narrativo de niebla. |
| 18 | Se agregó terremoto, barranco y separación. |
| 19 | Se corrigió la transición para impedir dos escenas en un fotograma. |
| 20 | Se agregó reinicio al caer en la niebla. |
| 21 | Se agregó zona de madriguera. |
| 22 | Se agregó estado de escondite. |
| 23 | Se agregó pajarito luminoso. |
| 24 | Se agregó interacción contextual con E. |
| 25 | Se agregó salida y aumento de luz de Rumi. |
| 26 | Se preparó arquitectura para Susurro y Espejilla; no se activan aún en el prólogo. |
| 27 | Se agregó interfaz con diálogo y etapa actual. |
| 28 | Se agregaron sprites temporales dibujados por código. |
| 29 | Se documentó contrato de sprites PNG y rutas. |
| 30 | Se añadieron pruebas automatizadas y comprobación sintáctica. |

## Iteraciones 31–50: evaluación

Después de cada verificación se corrige el hallazgo antes de continuar. Las 20 evaluaciones incluyen pruebas de reglas, ejecución sin ventana, controles, transición de estados, reinicio, colisiones y revisión manual.

| Iteración | Verificación | Resultado actual |
|---|---|---|
| 31 | Rectángulos: intersección real. | Aprobada por prueba automática. |
| 32 | Rectángulos: borde sin colisión falsa. | Aprobada por prueba automática. |
| 33 | Colisión: Rumi aterriza sobre una plataforma. | Aprobada por prueba automática. |
| 34 | Secuencia: no permite saltar estados. | Aprobada por prueba automática. |
| 35 | Secuencia: recorrido completo permitido. | Aprobada por prueba automática. |
| 36 | Nivel: inicia siguiendo al padre. | Aprobada por prueba automática. |
| 37 | Nivel: entrada a niebla. | Aprobada por prueba automática. |
| 38 | Nivel: terremoto requiere niebla previa. | Aprobada por prueba automática. |
| 39 | Nivel: el padre queda al borde del barranco. | Aprobada por prueba automática. |
| 40 | Nivel: madriguera requiere terremoto. | Aprobada por prueba automática. |
| 41 | Nivel: madriguera activa escondite. | Aprobada por prueba automática. |
| 42 | Nivel: pajarito lejano no avanza la historia. | Aprobada por prueba automática. |
| 43 | Nivel: pajarito cercano permite avanzar. | Aprobada por prueba automática. |
| 44 | Nivel: la salida aumenta la luz. | Aprobada por prueba automática. |
| 45 | Nivel: la salida desactiva escondite. | Aprobada por prueba automática. |
| 46 | Nivel: final solo después de salir. | Aprobada por prueba automática. |
| 47 | Nivel: reinicio restaura estado. | Aprobada por prueba automática. |
| 48 | Nivel: reinicio restaura luz. | Aprobada por prueba automática. |
| 49 | Texto: controles iniciales presentes. | Aprobada por prueba automática. |
| 50 | Texto: pajarito entrega siguiente paso. | Aprobada por prueba automática. |

### Límite de la evaluación actual

La evaluación automática está completa para la lógica: 20 pruebas en total. La prueba visual/manual de la ventana está pendiente porque Pygame no está instalado y este equipo requiere contraseña de administrador para habilitar `venv`. No se declara como probada hasta ejecutar `main.py` con Pygame disponible.
