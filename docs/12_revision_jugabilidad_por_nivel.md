# Revisión crítica de jugabilidad por nivel

Las voces de criaturas siguen siendo ficción narrativa y no describen ni
evalúan al jugador. Esta revisión cambia mapa, comportamiento y presentación.

## Nivel 1 — Barranco (iteraciones 01–10)

| Iteración | Revisión | Criterio | Estado |
|---|---|---|---|
| 01 | Inicio | Mr. Fox y objetivo visibles en el guion | verificada |
| 02 | Niebla | El Barranco no incluye niebla | verificada |
| 03 | Enemigos | Perfil suave asignado a cada criatura | verificada |
| 04 | Avisos | Cada criatura activa su diálogo propio | verificada |
| 05 | Vida | Un contacto válido resta solo una vida | verificada |
| 06 | Saltos | F y segundo salto siguen desactivados | verificada |
| 07 | Encuentro | Mr. Fox inicia un único terremoto | verificada |
| 08 | Duración | Terremoto conserva cinco segundos | verificada |
| 09 | Sonido | Derrumbe reproduce y corta a los cinco segundos | verificada |
| 10 | Cámara | La cámara aplica desplazamiento oscilante durante temblor | verificada |

## Nivel 2 — Espejos (iteraciones 11–20)

| Iteración | Revisión | Criterio | Estado |
|---|---|---|---|
| 11 | Tramos | Cinco tramos conservan límites contiguos | verificada |
| 12 | Precipicios | Cada tramo contiene dos huecos de terreno | verificada |
| 13 | Plataformas | No hay plataformas elevadas junto a rocas | verificada |
| 14 | Rocas | Dos rocas altas por tramo crean rutas de salto | verificada |
| 15 | Segundo salto | Roca elevada activa el impulso solo en aire | verificada |
| 16 | Enemigos | Seis encuentros por tramo, treinta en total | verificada |
| 17 | Altura | Espejillas patrullan y atacan desde zonas altas | verificada |
| 18 | Perfil | El perfil Nivel 2 acelera el patrón base | verificada |
| 19 | Farol | El farol final completa el nivel sin terremoto | verificada |
| 20 | Recorrido | Ruta de saltos completa el mapa sin caer | verificada |

## Nivel 3 — Cueva (iteraciones 21–30)

| Iteración | Revisión | Criterio | Estado |
|---|---|---|---|
| 21 | Personajes | No se instancia Mr. Fox en la cueva | verificada |
| 22 | Niebla | Niebla reutilizable cubre toda la cueva | verificada |
| 23 | Nubes | Render usa grupos densos de nubes desplazables | verificada |
| 24 | Faroles | Cinco fuentes permanentes abren claros | verificada |
| 25 | Interacción | E junto a farol concede luz temporal | verificada |
| 26 | Luz | Luz dura dos segundos y reduce gradualmente su radio | verificada |
| 27 | Pilares | E junto a pilar conserva mensajes de aliento | verificada |
| 28 | Rocas | Diez rocas de salto tienen brillo visible | verificada |
| 29 | Enemigos | Perfil Nivel 3 acelera aviso, detección y embestida | verificada |
| 30 | Salida | Cruzar la salida completa el nivel | verificada |

## Decisiones de implementación

- `RocaImpulso` declara si brilla; `DibujadorEscenario` solo pinta ese brillo.
- `FarolNiebla` declara una fuente permanente; `NivelTres` añade la fuente
  temporal de Rumi tras la interacción. `DibujadorNiebla` consume ambas.
- La duración del terremoto pasó a cinco segundos y se propaga mediante el
  resultado del nivel hacia `SonidosJuego`; la cámara usa el estado de temblor
  sin incluir reglas de terremoto.
