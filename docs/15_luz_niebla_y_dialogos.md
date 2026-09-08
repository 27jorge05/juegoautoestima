# Luz, niebla y diálogos de criaturas

Las voces del Velo siguen siendo ficción atribuida a criaturas. Los pilares
hablan como personajes y no diagnostican ni miden la autoestima del jugador.

## Iteración 1 — diálogos de criaturas

| Tarea | Subtarea atómica | Criterio de aceptación |
|---|---|---|
| Duración | Declarar 1.5 s mínimos para el aviso hablado | Un enemigo hablante permanece en aviso al menos 1.5 s |
| Forma | Dibujar una burbuja ovalada, no un rectángulo de depuración | La voz usa una burbuja legible y redondeada |

## Iteración 2 — efecto Luz de Rumi

| Tarea | Subtarea atómica | Criterio de aceptación |
|---|---|---|
| Dominio | Crear efecto temporal de luz con fase plena y fundido | Dura 1.5 s pleno y 1.5 s de descenso |
| Activación | Obtenerlo al interactuar con E junto a un farol | El farol entrega el efecto y su diálogo |
| Radio | Declarar un radio amplio para la fuente de Rumi | El claro temporal es mayor que el de antes |

## Iteración 3 — capas de niebla y enemigos

| Tarea | Subtarea atómica | Criterio de aceptación |
|---|---|---|
| Nubes | Combinar tipos de nube superpuestos | Las capas suman opacidad en zonas compartidas |
| Claros | Restar opacidad con fuentes permanentes y temporales | Faroles y Rumi aclaran la niebla cercana |
| Ocultación | Desactivar indicadores visuales de criaturas de cueva | La hitbox sigue lógica y no se dibuja sobre la niebla |

## Iteración 4 — pilares

| Tarea | Subtarea atómica | Criterio de aceptación |
|---|---|---|
| Voz | Mantener mensajes de pilar como `Dialogo` con hablante | El panel muestra `Pilar:` y no un relato anónimo |

## Iteración 5 — integración

| Tarea | Subtarea atómica | Criterio de aceptación |
|---|---|---|
| Pruebas | Cubrir reglas temporales, render y voces | Cada regla nueva tiene prueba |
| Revisión | Ejecutar validaciones de cierre | Suite, compilación y espacios correctos |

## Diez validaciones finales

| ID | Criterio | Estado |
|---|---|---|
| V01 | Diálogo hostil dura 1.5 s | verificado por perfiles y diálogo declarativo |
| V02 | Burbuja hostil es ovalada | verificado por render de burbuja |
| V03 | E junto a farol activa la luz | verificado por interacción de Nivel 3 |
| V04 | Luz plena dura 1.5 s | verificado por efecto temporal |
| V05 | Luz se funde otros 1.5 s | verificado: intensidad baja de 1 a 0 |
| V06 | Luz temporal crea fuente amplia | verificado: radio máximo de 310 |
| V07 | Faroles conservan fuente permanente | verificado: 5 fuentes permanentes |
| V08 | Nubes combinan tres tipos | verificado: azul, violeta y oscura |
| V09 | Indicadores de cueva no se dibujan | verificado: bandera visual desactivada |
| V10 | Pilar sigue siendo diálogo y suite íntegra | verificado: `Pilar:` y 98 pruebas |

La revisión final ejecutó los diez criterios anteriores, la suite completa con
`SDL_VIDEODRIVER=dummy` y `SDL_AUDIODRIVER=dummy`, `compileall` y
`git diff --check`.
