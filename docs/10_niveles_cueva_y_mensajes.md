# Mensajes, terremoto y Cueva del Velo

## Categoría A — comunicación temporal

| Iteración | Tarea | Subtarea atómica | Criterio de aceptación | Estado |
|---|---|---|---|---|
| 01 | Mensajes | Crear reloj visual de mensaje | Mantiene el texto 7 s y después reduce su alfa | verificada |
| 02 | Mensajes | Integrar el panel de diálogo | Panel y texto se desvanecen juntos | verificada |
| 03 | Vida | Corazones y destello de daño | Un golpe válido enrojece corazón y pantalla | verificada |

## Categoría B — cambios en niveles existentes

| Iteración | Tarea | Subtarea atómica | Criterio de aceptación | Estado |
|---|---|---|---|---|
| 04 | Nivel 1 | Quitar F y segundo salto | El texto, entrada y reglas no activan esas habilidades | verificada |
| 05 | Nivel 1 | Hostilidad de insectos | Avisan, atacan y reducen vida como en nivel 2 | verificada |
| 06 | Nivel 2 | Crear prólogo del terremoto | Texto menciona separación, padre y voces | verificada |
| 07 | Nivel 2 | Padre y farol finales | Padre espera junto al farol | verificada |
| 08 | Nivel 2 | Terremoto terminal | Inicia una vez, congela juego y concluye a los 3 s | verificada |

## Categoría C — Nivel 3: Cueva del Velo

| Iteración | Tarea | Subtarea atómica | Criterio de aceptación | Estado |
|---|---|---|---|---|
| 09 | Mapa | Definir cinco tramos de cueva | Terreno, cristales y meta declarados | verificada |
| 10 | Mapa | Dibujar variante de cueva | Fondo, techo y cristales se desplazan con cámara | verificada |
| 11 | Reglas | Activar garras luminosas persistentes | Luz protege visibilidad en niebla | verificada |
| 12 | Reglas | Criaturas silenciosas | No muestran frases durante aviso o ataque | verificada |
| 13 | Reglas | Derrota con eco del Velo | Al caer dice una frase de derrota, no durante juego | verificada |
| 14 | Integración | Registrar nivel 3 | Menú y fábrica abren la escena correcta | verificada |

## Categoría D — 20 validaciones finales

| Iteración | Revisión | Criterio de aceptación | Estado |
|---|---|---|---|
| 15 | Mensaje inicial | Aparece y conserva legibilidad | verificada |
| 16 | Fundido | Alfa disminuye solo tras 7 s | verificada |
| 17 | Red de daño | Destello tiene duración limitada | verificada |
| 18 | Corazones | Valor y corazón afectado son rojos | verificada |
| 19 | Nivel 1 sin niebla | Sin elemento ni lentitud | verificada |
| 20 | Nivel 1 sin F | F y segundo salto no cambian movimiento | verificada |
| 21 | Nivel 1 hostil | Aviso/ataque/vida probados | verificada |
| 22 | Padre Nivel 1 | Intersección completa | verificada |
| 23 | Prólogo Nivel 2 | Texto y vida inicial correctos | verificada |
| 24 | Padre Nivel 2 | Visible junto al farol | verificada |
| 25 | Terremoto | Evento se emite una vez | verificada |
| 26 | Sonido | Derrumbe se limita a 3 s | verificada |
| 27 | Congelación | Nada se mueve durante terremoto | verificada |
| 28 | Final Nivel 2 | Se congela como pantalla final | verificada |
| 29 | Mapa Cueva | Cinco tramos contiguos | verificada |
| 30 | Luz Cueva | La niebla no reduce visibilidad | verificada |
| 31 | Insectos Cueva | Sin frases en el juego | verificada |
| 32 | Muerte Cueva | Una frase solo al perder | verificada |
| 33 | Navegación | Menú abre niveles 1–3 | verificada |
| 34 | Presentación | Capturas de inicio, golpe, final y cueva | verificada |

## Decisiones registradas

- Los mensajes y su fundido pertenecen a presentación. Los niveles solo exponen texto.
- El terremoto conserva su temporizador en el dominio del Nivel 2; el sonido lo reproduce la escena y `SonidosJuego` lo corta a tres segundos.
- La cueva será una composición visual por código con fondo nocturno existente, siluetas de roca y cristales. El generador de imágenes integrado no está disponible en esta sesión; por eso no se añadirá un PNG artificial ni se alterará el recurso adjunto.
- Las frases del Velo se reservan para avisos de Nivel 1/2 y la derrota de Nivel 3. No se presenta ninguna de ellas como una medición o verdad sobre el jugador.

## Resultado de las 20 validaciones

Las iteraciones 15–34 se ejecutaron contra la suite automatizada y capturas SDL dummy. La última corrida contiene 73 pruebas correctas y compilación de `src` correcta.

- 15–18: `testMensajesYVida` comprueba los siete segundos, fundido, reinicio con texto nuevo, destello y corazones.
- 19–22: `testNivelUno` comprueba ausencia de niebla, F y segundo salto inactivos, ataque hostil y encuentro con padre.
- 23–28: `testNivelDos` comprueba prólogo, padre, terremoto único, cuenta de tres segundos y congelación durante ese estado. `SonidosJuego` conserva el corte del derrumbe a los tres segundos.
- 29–32: `testNivelTres` comprueba cinco tramos, luz persistente sin pérdida de velocidad, criaturas sin frases y eco solo tras derrota.
- 33–34: fábrica y menú incluyen 1–3; se inspeccionaron capturas de inicio de los tres niveles, terremoto y derrota en la cueva. Se corrigió el título heredado del Nivel 2 y se redujo la opacidad del destello final para que el texto siga legible.
