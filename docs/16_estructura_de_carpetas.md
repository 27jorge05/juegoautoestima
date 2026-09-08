# Estructura de carpetas

El código se reorganizó por responsabilidad para que cada cambio tenga una
ubicación predecible.

| Carpeta | Responsabilidad |
|---|---|
| `src/aplicacion/` | Inicia el juego, administra el menú, la entrada, la configuración y la fábrica de escenas. |
| `src/audio/` | Reproduce efectos y música local. |
| `src/dominio/` | Conserva reglas que no dependen de Pygame: entidades, eventos, vida, luz y enemigos. |
| `src/mundo/` | Declara plataformas, elementos, recursos y constructores de los escenarios. |
| `src/niveles/` | Define reglas y narrativa específicas de los niveles 1, 2 y 3. |
| `src/presentacion/` | Contiene Pygame: dibujadores, cámara, animaciones y escenas. |

Las dependencias van desde aplicación y presentación hacia niveles, mundo y
dominio. El dominio no importa Pygame. Esta decisión facilita agregar otro
nivel o reemplazar la presentación sin trasladar reglas de juego a `main.py`.

Cada archivo de nivel importa únicamente el constructor de su propio mundo:
`NivelUno` usa el Barranco, `NivelDos` usa Espejos y `NivelTres` usa la Cueva.
El ciclo común de una partida (`jugando`, `derrotado`, `completado`) y los
catálogos reutilizables de frases viven en `dominio/`; así ningún nivel toma
reglas o datos desde otro nivel. Una prueba de integridad protege esa frontera.

La niebla sigue la misma regla: `NieblaNivel` conserva su área, activación y
`ConfiguracionNubesNiebla` (formas, densidad y desplazamiento). Un nivel elige
una configuración reutilizable, como `NUBES_NIEBLA_DENSA`; el dibujador solo
convierte esa información en píxeles y no contiene decisiones de un nivel.
