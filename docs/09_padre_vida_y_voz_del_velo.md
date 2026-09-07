# Padre, vida y voces del Velo

## Alcance y decisiones

La niebla visual y su regla de lentitud se desactivan por completo en el Nivel 1. El Barranco pasa a ser una búsqueda: Rumi recorre el mapa, evita o libera criaturas y termina al alcanzar a su padre, que espera en el último tramo.

La vida es una regla de juego separada de `luz` y de los temas narrativos. Cada golpe válido resta un corazón; un intervalo de invulnerabilidad evita que un grupo de criaturas reste más de uno a la vez. El destello rojo y el corazón temporalmente rojo son reacciones visuales a `golpeRecibido`.

Los Susurros y Espejillas del Nivel 1 son `EnemigoHostil`: cada criatura posee su propia patrulla, aviso, embestida, recuperación y reacción a la luz. No hay lógica de ataques en el dibujador ni en la escena.

El Nivel 2 comienza recordando el terremoto y la separación del padre. Las frases de los enemigos están atribuidas al Velo; el texto de derrota anima a reintentar sin presentarse como terapia o evaluación de autoestima.

## Iteraciones atómicas

| Iteración | Tarea atómica | Criterio de aceptación | Estado |
|---|---|---|---|
| 01 | Desactivar niebla del Barranco | No existe en los elementos, ni modifica velocidad | verificada |
| 02 | Reubicar al padre como meta | Espera en el último tramo | verificada |
| 03 | Completar al encontrar al padre | La intersección padre/Rumi termina el nivel | verificada |
| 04 | Crear criaturas hostiles del Nivel 1 | Cada una es `EnemigoHostil` y tiene territorio | verificada |
| 05 | Aplicar vida y daño del Nivel 1 | Golpe resta un corazón con protección temporal | verificada |
| 06 | Registrar destello de daño | Escena solicita efecto solo ante un golpe válido | verificada |
| 07 | Dibujar corazones | Un corazón por vida; valor de golpe se pinta rojo | verificada |
| 08 | Dibujar parpadeo rojo | Overlay temporal, limitado a presentación | verificada |
| 09 | Actualizar prólogo del Nivel 2 | Explica terremoto, padre y voces | verificada |
| 10 | Ejecutar pruebas y revisión visual | Pruebas de reglas y capturas de ambos estados | en curso |

## Evidencia

La iteración 10 se completa con la suite completa, compilación y capturas SDL dummy. La inspección manual de audio queda fuera del entorno de pruebas.
