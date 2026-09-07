# Nivel 2 — Espejos de Niebla

## Decisiones de alcance

Se amplía el prototipo autorizado con un segundo mapa jugable, accesible desde el menú sin guardar progreso. Cinco tramos, 7.200 píxeles y veinte enemigos (frente a cuatro del Barranco). Se reutilizan recursos con una variante nocturna; no se crea una imagen gigante nueva.

Rumi tiene tres puntos de vida, separados de su luz y de cualquier concepto de autoestima. Tres golpes válidos causan muerte jugable/derrota, con pantalla de reintento mediante R. Una caída también derrota. La derrota congela el mundo; nunca elimina datos del usuario. Los enemigos anuncian su ataque antes de embestir y existe invulnerabilidad breve tras recibir daño.

Susurros terrestres y Espejillas voladoras emplean patrulla, aviso, ataque y recuperación. La luz F libera criaturas cercanas con recarga, de modo que esquivar y escoger el momento importa. Las frases «No puedes» y «Vas a fallar» pertenecen a enemigos identificados como voces del Velo. Su aviso visual crea tensión; sin gore, flashes ni sobresaltos realistas. El reintento responde: «Un intento no decide lo que puedes aprender». No se hacen afirmaciones clínicas.

## Tareas atómicas y aceptación

Una fila es una iteración con un único resultado. Se evalúa al cerrar cada tarea/categoría y en 05, 10, 15 y 20. Después se realizan diez evaluaciones finales diferentes. Los fallos se corrigen antes del cierre correspondiente.

| Iteración | Categoría / tarea | Subtarea atómica | Criterio de aceptación | Estado |
|---|---|---|---|---|
| 01 | A / mapa | Declarar recursos del nivel 2 | Identificador distinto; reutilización explícita | verificada |
| 02 | A / mapa | Construir cinco tramos | 7.200 px conectados y salida alcanzable | verificada |
| 03 | A / mapa | Distribuir encuentros | 20 enemigos con territorios dentro del suelo | verificada |
| 04 | A / mapa | Declarar decoración | Cristales y ruta visible como datos | verificada |
| 05 | A / mapa | Verificar fábrica | Instancias indeverificadas; más enemigos que nivel 1 | verificada |
| 06 | B / combate | Modelar vida | Tres golpes válidos derrotan; vida no es luz | verificada |
| 07 | B / combate | Añadir invulnerabilidad | Grupo simultáneo no consume todas las vidas | verificada |
| 08 | B / enemigos | Implementar patrulla | No sale del territorio asignado | verificada |
| 09 | B / enemigos | Implementar aviso y embestida | No daña antes del aviso; recuperación entre ataques | verificada |
| 10 | B / enemigos | Implementar liberación | F cerca neutraliza ataques; fuera de alcance no | verificada |
| 11 | C / reglas | Implementar actualización de nivel | Física, daño y meta sin Pygame | pendiente |
| 12 | C / reglas | Implementar derrota y reinicio | Mundo congelado; R restaura partida completa | pendiente |
| 13 | C / reglas | Implementar recarga de luz | Pulsaciones durante recarga no reactivan habilidad | pendiente |
| 14 | C / presentación | Mostrar vida y estados terminales | HUD legible y controles de reintento | pendiente |
| 15 | C / presentación | Mostrar avisos del Velo | Frase atribuida; señal de ataque visible y temporal | pendiente |
| 16 | D / integración | Compartir coordinación de escena | Mismo controlador con dominio/dibujador inyectables | pendiente |
| 17 | D / integración | Registrar nivel 2 | Fábrica crea escena propia | pendiente |
| 18 | D / integración | Habilitar selección | Nivel 2 abre; futuros niveles siguen bloqueados | pendiente |
| 19 | D / integración | Verificar recorrido | Simulación llega al final usando luz y movimiento | pendiente |
| 20 | D / integración | Registrar documentación | Controles, alcance y limitaciones actualizados | pendiente |
| 21 | E / auditoría | Revisar independencia del dominio | Sin importaciones gráficas | pendiente |
| 22 | E / auditoría | Revisar fábrica y mapa | Tramos y territorios válidos | pendiente |
| 23 | E / auditoría | Revisar daño | Invulnerabilidad y muerte comprobadas | pendiente |
| 24 | E / auditoría | Revisar ataques | Aviso, alcance y recuperación comprobados | pendiente |
| 25 | E / auditoría | Revisar defensa | Recarga y liberación comprobadas | pendiente |
| 26 | E / auditoría | Revisar reinicio y terminales | Sin movimiento/daño tras muerte o victoria | pendiente |
| 27 | E / auditoría | Revisar jugabilidad | Recorrido físico completo sin teletransporte | pendiente |
| 28 | E / auditoría | Revisar navegación | Menú, nivel 2, vuelta y nivel 1 funcionan | pendiente |
| 29 | E / auditoría | Revisar presentación | Capturas de juego, aviso y derrota inspeccionadas | pendiente |
| 30 | E / auditoría | Revisar regresión completa | Suite y compilación pasan; límites registrados | pendiente |

## Evidencias

Pendientes de ejecución. La validación gráfica utiliza SDL dummy; no equivale a una partida manual con audio.

- Cierre A/mapa, control 05: dos pruebas verifican cinco tramos, 20 enemigos, límites, recursos e independencia de instancias.
- Cierre B/combate y B/enemigos, control 10: ocho pruebas pasan; daño con protección, patrulla acotada, aviso antes de golpe, recuperación, esquiva, vuelo y liberación.
