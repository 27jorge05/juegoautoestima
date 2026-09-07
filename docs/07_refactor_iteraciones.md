# Refactor del Barranco: tareas, criterios e iteraciones

## Método de trabajo

Cada fila es una subtarea atómica: un único resultado verificable. Una iteración corresponde a una fila, incluyendo su comprobación. Las tareas agrupan filas y las categorías agrupan tareas. Al cerrar cada tarea se contrastan todos sus criterios; al cerrar cada categoría se comprueba su integración. Cada cinco iteraciones se registra un control acumulado. Los fallos abren correcciones antes de aprobar el cierre. Las diez evaluaciones finales son revisiones distintas, no diez ejecuciones idénticas.

Estados: pendiente, en curso, verificada. No se considera verificada una revisión visual por pasar pruebas de lógica.

## A. Diagnóstico y contrato

Tarea A1: establecer evidencia y decisiones.

| Iteración | Subtarea atómica | Criterio de aceptación | Estado |
|---|---|---|---|
| 01 | Leer las convenciones y fundamento narrativo | Restricciones incorporadas a este plan | verificada |
| 02 | Inventariar responsabilidades actuales | Identificados dibujo, entrada, cámara y sonido dentro de main | verificada |
| 03 | Ejecutar pruebas iniciales | Resultado real registrado, incluidos fallos previos | verificada |
| 04 | Definir límites de módulos | Reglas sin Pygame; presentación por escena; fábrica crea mundo | verificada |
| 05 | Definir controles y criterios de cierre | Cada fila tiene resultado comprobable y diez auditorías finales | verificada |

Cierre A1/A, control 05: 27 pruebas iniciales, 9 fallos. La niebla existe pero no pertenece a escenario.elementos, impidiendo avanzar la narrativa. Main contiene dibujo de entidades, menú, entrada, cámara y efectos de audio.

## B. Composición del mundo

Tarea B1: geometría y apariencia.

| Iteración | Subtarea atómica | Criterio de aceptación | Estado |
|---|---|---|---|
| 06 | Declarar TipoTerreno | Enum sin rutas de imágenes | verificada |
| 07 | Declarar PlataformaNivel | Rectángulo y tipo indeverificadas del comportamiento | verificada |
| 08 | Adaptar colisiones a geometría | Aterrizaje idéntico con tipos visuales distintos | verificada |
| 09 | Resolver apariencia por tipo | Dibujador consulta recursos; no elige textura el nivel | verificada |
| 10 | Declarar decoraciones | Huellas son datos del escenario; no colisionan | verificada |

Tarea B2: fábrica del Barranco.

| Iteración | Subtarea atómica | Criterio de aceptación | Estado |
|---|---|---|---|
| 11 | Extraer construcción del mapa | NivelUno delega en fábrica | verificada |
| 12 | Integrar niebla en escenario | Transiciones narrativas iniciales vuelven a pasar | verificada |
| 13 | Separar posiciones y zonas | Fábrica concentra coordenadas del mundo | verificada |
| 14 | Garantizar instancias nuevas | Reiniciar no comparte elementos mutables | verificada |
| 15 | Renderizar decoración declarada | Dibujador no inventa posiciones de huellas | verificada |

## C. Aplicación y escenas

Tarea C1: presentación del nivel.

| Iteración | Subtarea atómica | Criterio de aceptación | Estado |
|---|---|---|---|
| 16 | Extraer DibujadorNivelUno | Main no dibuja personajes ni carga sprites | verificada |
| 17 | Extraer presentación del menú | Menú no depende de las fuentes del nivel | verificada |
| 18 | Encapsular entrada del nivel | Teclas traducidas a EntradaJugador fuera de Juego | verificada |
| 19 | Encapsular efectos del nivel | Escena coordina eventos, audio y efectos | verificada |
| 20 | Encapsular cámara | Desplazamiento limitado al ancho del mapa y probado | verificada |

Tarea C2: coordinación extensible.

| Iteración | Subtarea atómica | Criterio de aceptación | Estado |
|---|---|---|---|
| 21 | Definir contrato de escena | Eventos, actualización y dibujo uniformes | verificada |
| 22 | Registrar fábrica de niveles | Crear por número sin condicionales de NivelUno en Juego | verificada |
| 23 | Delegar selección en escena de menú | Niveles bloqueados no se abren | verificada |
| 24 | Reducir main a entrada | Solo inicia la aplicación | verificada |
| 25 | Verificar ciclo entre escenas | Menú, entrar, volver y cerrar sin eventos residuales | verificada |

## D. Frames y alineación

Tarea D1: cadena de sprites.

| Iteración | Subtarea atómica | Criterio de aceptación | Estado |
|---|---|---|---|
| 26 | Inspeccionar hojas reales | Cuadrícula contrastada con imágenes existentes | verificada |
| 27 | Validar extracción de frame | Un personaje por frame, sin hoja completa | verificada |
| 28 | Definir anclaje de pies | Cuerpo alineado al suelo sin offsets arbitrarios | verificada |
| 29 | Verificar avance de animación | Actualización separada de dibujado, tiempos probados | verificada |
| 30 | Revisar sprites renderizados | Captura real inspeccionada de Rumi y padre | verificada |

## E. Recorrido ampliado

Tarea E1: cinco tramos reutilizables.

| Iteración | Subtarea atómica | Criterio de aceptación | Estado |
|---|---|---|---|
| 31 | Declarar tramos del escenario | Cinco secciones con límites explícitos | verificada |
| 32 | Extender plataformas | Camino mayor que el original, saltos alcanzables | verificada |
| 33 | Distribuir decoración reutilizable | Bosque, cristales y huellas definidos como datos | verificada |
| 34 | Añadir desplazamiento de fondo | Parallax con continuidad al mover cámara | verificada |
| 35 | Situar final del nivel | No completa antes del último tramo | verificada |

Tarea E2: criaturas y recorrido.

| Iteración | Subtarea atómica | Criterio de aceptación | Estado |
|---|---|---|---|
| 36 | Declarar criaturas del prólogo ampliado | Susurros y Espejillas separados de plataformas y decoración | verificada |
| 37 | Implementar interacción luminosa | Liberación reversible al reiniciar; sin matar criaturas | verificada |
| 38 | Dibujar formas de criaturas | Oscura y liberada distinguibles | verificada |
| 39 | Comprobar recorrido físico | Simulación llega a salida sin teletransportar al jugador | verificada |
| 40 | Registrar decisiones de alcance | Ampliación y mecánicas documentadas, sin datos personales | verificada |

## F. Diez evaluaciones finales de integridad

Cada evaluación deja evidencia y resultado; cualquier fallo se corrige y se repite la comprobación afectada.

| Iteración | Evaluación | Criterio de aceptación | Estado |
|---|---|---|---|
| 41 | Dependencias y SOLID | Dominio sin Pygame; Juego no conoce entidades | verificada |
| 42 | Geometría y tipos | Física indeverificada de apariencia | verificada |
| 43 | Fábricas y reinicio | Sin estado mutable compartido ni efectos residuales | verificada |
| 44 | Secuencia narrativa | Todos los estados alcanzables en orden | verificada |
| 45 | Movimiento y colisiones | Suelo, salto, impulso y caída pasan pruebas | verificada |
| 46 | Sprites y animaciones | Recorte, anclaje, orientación y tiempos correctos | verificada |
| 47 | Escenario extenso | Tramos conectados, cámara acotada y final alcanzable | verificada |
| 48 | Menú y ciclo de aplicación | Selección, regreso y cierre funcionales | verificada |
| 49 | Presentación real | Capturas inspeccionadas; recursos existentes cargan | verificada |
| 50 | Regresión y documentación | Suite completa pasa y limitaciones quedan explícitas | verificada |

## Decisiones de diseño

- NivelUno mantiene reglas y narrativa; EscenaNivelUno integra presentación y sonido. No se introduce Pygame en el dominio.
- Los frames pertenecen a animaciones, no son elementos del escenario.
- El Barranco conserva su secuencia inicial y se extiende después de la madriguera a cinco tramos. Solo se incorporan las criaturas pertinentes al nivel; no todos los jefes de los capítulos futuros.
- La referencia adjunta guía paleta, profundidad y reutilización. No se tratará la lámina con etiquetas como una textura lista para usar.
- Se utilizan los recursos disponibles; no se instala ni migra Pygame CE.
- Cada regla o cálculo nuevo requiere prueba. No hay telemetría, cuentas ni respuestas personales persistidas.

## Registro de cierres

- A1 y A: verificadas mediante lectura e inventario; control 05 documentado arriba.

- B1/control 10: materiales separados y colisión comprobada para los cuatro tipos en testEscenario.
- B2/control 15 y categoría B: fábrica integrada, decoración declarativa, reinicio independiente y niebla restaurada; 30 pruebas pasan.

- C1/control 20: cámara probada en inicio, centro, final y mapas menores que la ventana. Presentación, entrada y efectos extraídos.
- C2/control 25 y categoría C: fábrica inyectable, menú bloqueado probado, ciclo real menú/nivel/menú ejecutado con SDL dummy.
- D1/control 30 y categoría D: 36 pruebas pasan. Captura /tmp/rumi-inicio.png inspeccionada: un sprite por entidad, sin hoja repetida. Se detecta transparencia superior del suelo: pendiente corregir durante extensión del terreno para alinear superficie visible y colisión.

- E1/control 35: cinco tramos contiguos, ancho 6360 y meta 6260. Prueba confirma que x=1800 ya no completa el nivel. Parallax cubre ventana en cambios de mosaico.
- E2/control 40 y categoría E: 42 pruebas pasan, incluida simulación de movimiento continuo desde inicio hasta COMPLETADO sin teletransporte ni caídas. Susurros se acercan a 32 px/s y reducen luz a 0,08/s hasta mínimo 0,15; F libera criaturas a 110 px. Espejillas muestran una señal ilusoria sin colisión que cambia al liberarlas. Son reglas de juego, no mediciones psicológicas.
- Recursos: se conserva el bosque existente; repetición alternada en espejo para continuidad del fondo. La decoración suplementaria usa formas de código; no se han producido assets nuevos equivalentes a la lámina.

## Evidencia de las diez evaluaciones finales

Ejecutor reproducible: `python3 herramientas/evaluarIntegridad.py`. Usa SDL dummy, ejecuta grupos de pruebas, genera capturas en /tmp y termina con regresión completa y compilación. La inspección visual se realizó además del script.

| Revisión | Evidencia y resultado |
|---|---|
| 41 | Inspección AST de seis módulos: sin importaciones de Pygame/presentación en dominio y mapa; main tiene seis líneas y Juego no referencia Rumi, imágenes, gravedad ni sonidos. Pasa. |
| 42 | Colisión comprobada con los cuatro materiales; decoración excluida del suelo. Dos pruebas pasan. |
| 43 | Tres pruebas verifican independencia entre fábricas, restauración de criaturas y limpieza de efectos/animaciones. Dibujar dos veces no avanza el tiempo. Pasa. |
| 44 | Las quince pruebas del nivel pasan; se conserva el orden narrativo y el final depende de la meta nueva. |
| 45 | Ocho pruebas de dominio, caída, límites e impulso: caída reinicia, impulso requiere cercanía y no se repite durante el mismo salto. Pasa. Control acumulado 45 aprobado. |
| 46 | Frame real, orientación, anclaje y espera temporal comprobados. Se añadió rechazo de definiciones de animación vacías o con duración inválida. Pasa. |
| 47 | Seis pruebas cubren cinco tramos, parallax, criaturas y recorrido físico completo. El jugador llega desde el inicio hasta COMPLETADO sin teletransporte ni reinicio por caída. Pasa. |
| 48 | Seis pruebas de menú, entrada, fábrica y cierre. Selección bloqueada no entra; pulsaciones consumidas una vez; QUIT finaliza Pygame. Pasa. |
| 49 | Inspeccionadas las capturas finales de menú, inicio y tramo de cristal. Un personaje por entidad, pies sobre superficie, suelo continuo y textos legibles. Corregidos bordes transparentes que parecían huecos y compresión del suelo en plataformas delgadas. Añadidos saltos de línea de diálogo y prueba de ajuste. Pasa con límites artísticos descritos abajo. |
| 50 | Regresión completa: 50 pruebas correctas; compilación de src correcta. README actualizado y versiones reales documentadas. Control acumulado 50 y cierre de F aprobados para el entorno disponible. |

Cierre de tareas A1, B1, B2, C1, C2, D1, E1 y E2 contrastado con sus filas. La corrección visual de suelo detectada en D1 quedó resuelta en E y revalidada en 49. No quedan fallos conocidos de las pruebas ejecutadas.

### Límites de la evaluación

- Python instalado: 3.10.12; Pygame CE ya instalado: 2.5.8. El objetivo sigue siendo Python 3.11+, pero su ejecución no pudo verificarse en este entorno. No se instalaron dependencias.
- Se inspeccionaron capturas reales en SDL dummy; no se realizó una sesión manual de juego ni escucha de audio.
- El fondo reutiliza el asset existente con parallax 0,2 y repetición en espejo; decoración y terreno se desplazan con el mundo. No equivale a tres capas de arte independientes extraídas de la referencia. Cristales y arbustos adicionales conservan presentación provisional por código.
- Las Espejillas muestran una señal ilusoria sin colisión, que cambia al liberarlas. No se añadieron clones, jefes ni enemigos de capítulos futuros.
- Las capturas se guardan en /tmp/rumi-menu-final.png, /tmp/rumi-inicio-final.png y /tmp/rumi-cristal-final.png; el ejecutor permite regenerarlas.
