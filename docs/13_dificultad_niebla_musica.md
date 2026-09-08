# Dificultad, niebla densa y música de cueva

Las voces hostiles siguen siendo ficción de criaturas, no evaluaciones del
jugador. La música se incorporará solo con licencia explícita compatible.

## Iteración 1 — diagnóstico y Nivel 1

| Tarea | Subtarea atómica | Criterio |
|---|---|---|
| Dificultad | Aumentar rutas y encuentros del Barranco | Nivel 1 exige más decisiones sin activar segundo salto |
| Perfil | Ajustar agresividad de Nivel 1 | Sigue siendo menor que Nivel 2, pero no trivial |
| Terremoto | Revisar duración, audio y sacudida | Cinco segundos coordinan estado, sonido y pantalla |

## Iteración 2 — variedad del Nivel 2

| Tarea | Subtarea atómica | Criterio |
|---|---|---|
| Mapa | Alternar patrones de precipicio por tramo | Ningún tramo repite la misma secuencia exacta |
| Rocas | Variar altura y posición de rutas | Cada precipicio mantiene una ruta alcanzable |
| Enemigos | Alternar posiciones y tipos | Encuentros altos y terrestres no se repiten por tramo |

## Iteración 3 — Nivel 3

| Tarea | Subtarea atómica | Criterio |
|---|---|---|
| Nubes | Aumentar densidad y solapamiento | La niebla no deja huecos amplios entre nubes |
| Luz | Cambiar duración temporal a tres segundos | E cerca de farol activa exactamente 3 s |
| Pilares | Alternar distancias entre pilares | Posiciones no siguen un intervalo constante |

## Iteración 4 — música

| Tarea | Subtarea atómica | Criterio |
|---|---|---|
| Licencia | Verificar fuente y licencia | Archivo CC0 con autor y URL documentados |
| Recurso | Descargar audio de cueva | Archivo queda bajo `assets/sounds/musica/` |
| Audio | Reproducir loop solo en Nivel 3 | No interrumpe efectos ni se reproduce fuera de cueva |

## Iteración 5 — integración

| Tarea | Subtarea atómica | Criterio |
|---|---|---|
| Pruebas | Añadir reglas para rutas, luz, niebla y música | Una prueba por regla nueva |
| Render | Verificar faroles, rocas y niebla | Render dummy no falla y mantiene claros |
| Documentación | Registrar decisiones y crédito | README y créditos describen el recurso |

## 20 validaciones finales

| ID | Criterio | Estado |
|---|---|---|
| V01 | Nivel 1 tiene ruta más exigente | verificado: 8 encuentros hostiles |
| V02 | Nivel 1 conserva F desactivada | verificado por regla de Nivel 1 |
| V03 | Perfil 1 es menor que Perfil 2 | verificado por perfiles declarativos |
| V04 | Terremoto inicia una vez | verificado por transición de encuentro |
| V05 | Terremoto, sonido y pantalla duran 5 s | verificado por pruebas de nivel y sonido |
| V06 | Nivel 2 mantiene cinco tramos | verificado: 5 tramos |
| V07 | Patrones de precipicio no son idénticos | verificado: 5 patrones distintos |
| V08 | Rutas de roca siguen alcanzables | verificado por recorrido completo |
| V09 | Encuentros Nivel 2 varían | verificado por posiciones declarativas |
| V10 | Farol final completa Nivel 2 | verificado por regla de final |
| V11 | Nivel 3 no contiene Mr. Fox | verificado: `padre is None` |
| V12 | Nubes densas se solapan | verificado por contrato del grupo de nubes |
| V13 | Faroles generan claros permanentes | verificado: 5 fuentes de luz |
| V14 | Luz temporal dura 3 s | verificado por prueba de farol |
| V15 | Pilar lejano no interactúa | verificado por prueba de alcance |
| V16 | Pilares tienen distancias distintas | verificado por prueba de separaciones |
| V17 | Rocas de cueva brillan | verificado: 10 rocas con brillo |
| V18 | Música es CC0 y está acreditada | verificado en `CREDITOS.md` |
| V19 | Música se limita a Nivel 3 | verificado por prueba de escena |
| V20 | Suite, compilación y espacios correctos | verificado: 94 pruebas, `compileall` y `diff --check` |

La revisión final se ejecutó con `SDL_VIDEODRIVER=dummy` y
`SDL_AUDIODRIVER=dummy`: comprueba integración y render sin abrir ventana. La
escucha musical y la sensación de dificultad requieren además una partida
manual antes de publicar.

## Ajuste posterior de lectura

- Se eliminó la roca de impulso junto a la plataforma elevada del Barranco.
  El Nivel 1 conserva una sola roca alejada de esas plataformas.
- Durante una sacudida, el mundo se desplaza, pero el panel narrativo se
  repinta anclado a la pantalla para conservar su lectura.
- La Cueva del Velo combina capas azul, violeta y oscura. Sus solapamientos
  vuelven algunas zonas más densas; los indicadores de estado de sus enemigos
  están desactivados. El halo de Rumi es opcional y visual: no abre un claro
  dinámico en la niebla; los faroles conservan esa función de forma permanente.

## Auditoría posterior — 10 iteraciones

| Iteración | Área revisada | Resultado |
|---|---|---|
| 1 | Reglas del Nivel 1 | 10 pruebas correctas |
| 2 | Mapa, combate y reglas del Nivel 2 | 23 pruebas correctas |
| 3 | Cueva, faroles, niebla y halo del Nivel 3 | 13 pruebas correctas |
| 4 | Mensajes, vida y audio | 7 pruebas correctas |
| 5 | Presentación, interfaz fija y render | 14 pruebas correctas |
| 6 | Recorrido físico del Barranco | 6 pruebas correctas |
| 7 | Integridad de capas y responsabilidades | 5 pruebas correctas |
| 8 | Menú y selección de niveles | 3 pruebas correctas |
| 9 | Integración completa | 94 pruebas correctas |
| 10 | Compilación y espacios de cambios | `compileall` y `git diff --check` correctos |

## Ajuste posterior — aviso móvil en la Cueva

Las criaturas del Nivel 3 avanzan hacia su último objetivo mientras están en
estado de aviso. La señal visual de alerta no detiene su patrón agresivo. El
valor `velocidadAviso` pertenece al perfil declarativo de dificultad, por lo
que los perfiles de Nivel 1 y 2 permanecen sin movimiento durante el aviso.
La regla tiene una prueba específica en `testNivelTres.py`.

## Ajuste posterior — nubes densas y claros ampliados

La Cueva del Velo invoca una configuración reutilizable de niebla con tres
familias de nubes grandes, cada una con una silueta distinta y solapamiento
deliberado. Esa forma, densidad y movimiento son datos de `NieblaNivel`; el
dibujador guarda sus capas y máscaras de luz para reutilizarlas en cada cuadro.
Los faroles iluminan un radio lógico de 285 y la luz temporal de Rumi alcanza
400 durante su intensidad plena.

## Ajuste posterior — claros cálidos y entrada legible

Cada `FuenteLuzNiebla` declara su color y fuerza de claro. El renderizador usa
esas propiedades para abrir más la niebla y añadir un resplandor cálido, sin
asumir que la fuente sea un farol o Rumi. La entrada de la Cueva queda libre de
enemigos; el primer encuentro comienza más adelante. Los enemigos de la Cueva
mantienen sus hitboxes para la colisión, pero sus marcadores de estado y trazos
de orientación permanecen ocultos.

## Ajuste posterior — halo suave y sprites sin cuadros

`FuenteLuzNiebla` calcula su intensidad según la distancia. El halo visual de
Rumi usa esa intensidad: sus anillos son de un píxel, se vuelven más suaves y
reducen su tamaño al alejarse de un farol; la luz temporal propia sigue dando
intensidad plena. Los sprites de enemigos oscuros se tintan conservando su
canal alfa en vez de recibir una capa rectangular negra.

## Ajuste posterior — criaturas alumbradas

`FuenteLuzNiebla` entrega una intensidad gradual según distancia. Cada
`EnemigoHostil` actualiza su atributo `alumbrado` e intensidad propia a partir
de las fuentes disponibles, sin depender de un nivel concreto. La Cueva pasa
esas fuentes después de actualizar los enemigos y la presentación dibuja un
resplandor cálido suave, encima de la niebla, solo para los que están
alumbrados. Los faroles y la luz temporal incrementaron su fuerza de claro.
