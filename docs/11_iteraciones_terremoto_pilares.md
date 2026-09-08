# Terremoto, voces y pilares de aliento

Este capítulo presenta voces hostiles como conductas ficticias de criaturas. No
describe al jugador ni mide su autoestima. Los pilares ofrecen apoyo narrativo;
no sustituyen ayuda profesional ni son una intervención clínica.

## Decisión de diálogo

`Relato` no tiene hablante; `Dialogo` siempre conserva a quién corresponde la
voz. Ambos declaran su propio tiempo visible y de fundido. Los niveles solo
eligen instancias del guion y no gestionan alfa, temporizadores ni cadenas de
presentación. Las criaturas tienen un `dialogoAviso` propio y se activa en el
Nivel 1 y el Nivel 2 cuando pasan al estado de aviso. Mr. Fox es el nombre
visible del guía de Rumi.

## Decisión de niebla y dificultad

La cueva usa `NieblaNivel` como elemento de dominio, `FarolNiebla` como fuente
de luz permanente y `DibujadorNiebla` como presentación de nubes densas. Rumi
solo recibe dos segundos de luz al interactuar con un farol cercano. Los
perfiles de criatura viven en `dificultadEnemigos.py`: Nivel 1 es suave, Nivel
2 acelera el mismo patrón y Nivel 3 reduce el aviso y acelera la embestida.

## Categoría A — cierre del Barranco y voces (iteraciones 01–05)

| Iteración | Tarea atómica | Criterio de aceptación | Estado |
|---|---|---|---|
| 01 | Crear banco de frases por tipo de criatura | Cada frase se obtiene desde datos, no desde el dibujador | verificada |
| 02 | Asignar frase propia a cada insecto del Nivel 1 | Todos emiten una frase desalentadora al avisar | verificada |
| 03 | Trasladar el inicio del terremoto al Nivel 1 | Solo el encuentro con padre inicia el evento | verificada |
| 04 | Congelar Nivel 1 durante tres segundos de terremoto | Física y enemigos no avanzan durante ese lapso | verificada |
| 05 | Mostrar mensaje final del padre y disparar sonido | El mensaje solicitado y un solo evento de sonido ocurren al final | verificada |

**Revisión 1:** pruebas de datos, cierre y duración de tres segundos.

## Categoría B — recorrido del Nivel 2 (iteraciones 06–10)

| Iteración | Tarea atómica | Criterio de aceptación | Estado |
|---|---|---|---|
| 06 | Ubicar padre al inicio del Nivel 2 | Su diálogo guía el comienzo sin bloquear la meta | verificada |
| 07 | Convertir el farol en meta del Nivel 2 | Llegar al farol completa el nivel sin terremoto | verificada |
| 08 | Añadir plataformas al mapa de Espejos | Cada tramo tiene plataformas adicionales declarativas | verificada |
| 09 | Añadir rocas de impulso al mapa de Espejos | El escenario contiene rocas reutilizables por tramo | verificada |
| 10 | Conectar segundo salto de roca a Nivel 2 | Un salto en aire sobre una roca produce `impulsoRoca` | verificada |

**Revisión 2:** pruebas de prólogo, meta, plataformas, rocas e impulso.

## Categoría C — Cueva, luz y pilares (iteraciones 11–15)

| Iteración | Tarea atómica | Criterio de aceptación | Estado |
|---|---|---|---|
| 11 | Definir datos de aliento de pilares | Mensajes identificados y reutilizables viven fuera del nivel | verificada |
| 12 | Crear objeto PilarAliento | El objeto detecta cercanía y entrega su mensaje con E | verificada |
| 13 | Colocar pilares en la Cueva | La cueva declara pilares dentro de sus tramos | verificada |
| 14 | Limitar luz de Rumi a dos segundos | F inicia brillo y, al expirar, aparece una duda narrativa | verificada |
| 15 | Oscurecer criaturas y niebla sin brillo | El dibujo reduce el claro y mantiene enemigos visibles solo cerca | verificada |

**Revisión 3:** pruebas de mensajes, interacción, tiempo de luz y estado visual.

## Categoría D — salida e integración (iteraciones 16–20)

| Iteración | Tarea atómica | Criterio de aceptación | Estado |
|---|---|---|---|
| 16 | Hacer que la salida, no el padre, complete la cueva | Cruzar la meta termina Nivel 3 | verificada |
| 17 | Mostrar objetivo de salida de cueva | El final describe que Rumi salió de la cueva | verificada |
| 18 | Conservar frases hostiles solo en sus criaturas | Nivel 1 y 2 avisan; Nivel 3 mantiene su regla silenciosa | verificada |
| 19 | Mantener corte de sonido del terremoto en tres segundos | `SonidosJuego` no reproduce más tiempo | verificada |
| 20 | Actualizar documentación de controles y flujo | README describe F, E, rocas y transiciones actuales | verificada |

**Revisión 4:** recorrido y pruebas de regresión de los tres niveles.

## Diez validaciones de integridad final

| Validación | Criterio | Estado |
|---|---|---|
| I01 | Banco de frases sin texto de UI embebido | verificada |
| I02 | Nivel 1 dispara terremoto una vez | verificada |
| I03 | Terremoto dura exactamente tres segundos | verificada |
| I04 | Nivel 2 no dispara terremoto | verificada |
| I05 | Roca habilita segundo salto solo en Nivel 2 | verificada |
| I06 | Cada mapa mantiene límites y tramos contiguos | verificada |
| I07 | Luz de cueva dura dos segundos | verificada |
| I08 | E activa pilar cercano y no uno lejano | verificada |
| I09 | Salida de cueva completa el Nivel 3 | verificada |
| I10 | Suite, compilación y revisión de espacios correctas | verificada |
