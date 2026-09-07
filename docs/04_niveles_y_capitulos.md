# Lúmina: niveles y capítulos

## Forma del juego

Juego de plataformas 2D lateral con exploración corta, saltos, planeo, plataformas móviles, enemigos simbólicos y puntos de descanso. No es una novela visual: la reflexión aparece al inicio o cierre de niveles y dura pocos segundos.

## Prólogo: El Barranco del Velo

Rumi va con su padre por el Camino del Alba. La Niebla llega después del terremoto; el suelo se abre y el padre impulsa a Rumi al otro lado. Rumi aterriza, se asusta, sus alitas se congelan y la niebla tapa el camino de regreso.

Este nivel enseña únicamente caminar, saltar y seguir mariposas guía. Termina cuando Rumi encuentra el primer farol apagado.

## Capítulo 1: Espejos de Niebla

**Tema:** Seguridad interior.

| Nivel | Lugar | Reto principal | Recompensa |
|---|---|---|---|
| 1. Sendero de las Luces Tenues | Bosque oscuro con faroles apagados. | Seguir mariposas y no caer en rutas falsas. | Primer recuerdo de casa. |
| 2. Lago de los Reflejos | Agua espejo y cristales. | Distinguir plataformas reales de ilusiones. | Fragmento del Farol del Nombre. |
| 3. Torre de las Máscaras | Ruina vertical de espejos. | Saltos, clones falsos y jefe Espejo Rey. | Luz propia. |

## Capítulo 2: Puentes de Luz

**Tema:** Conexión segura.

| Nivel | Lugar | Reto principal | Recompensa |
|---|---|---|---|
| 4. Raíces Separadas | Árboles colgantes y grietas. | Liberar rutas atrapadas por Nudos de Niebla. | Señal de la familia. |
| 5. Nidos del Rumor | Ramas altas con cuervos de papel. | Recuperar mensajes verdaderos y evitar mensajes falsos. | Fragmento del Farol del Vínculo. |
| 6. Plaza de los Faroles | Pequeña ciudad-bosque abandonada. | Activar luces junto a criaturas rescatadas. | Llamado de mariposas. |

## Capítulo 3: Jardines de Lluvia

**Tema:** Paz interior.

| Nivel | Lugar | Reto principal | Recompensa |
|---|---|---|---|
| 7. Río del Impulso | Corriente rápida y puentes débiles. | Saber cuándo correr, saltar o esperar. | Piedra de pausa. |
| 8. Jardín de las Espinas | Flores cerradas, espinas y caracoles de piedra. | Quitar Pesos Grises y reparar un puente. | Fragmento del Farol Sereno. |
| 9. Santuario de la Tormenta | Templo abierto bajo lluvia. | Usar calma para atravesar viento y jefe Tormenta Viva. | Aleteo sereno. |

## Capítulo 4: Faro del Alba

**Tema:** Esperanza valiente.

| Nivel | Lugar | Reto principal | Recompensa |
|---|---|---|---|
| 10. Camino sin Estrellas | Sendero mezclado de los tres mundos. | Usar Luz propia, Llamado y Aleteo juntos. | Brújula del Amanecer. |
| 11. El Faro | Torre central de Lúmina. | Activar los tres faroles bajo ataque de Umbra. | Camino hacia casa. |
| 12. Regreso al Árbol Faro | Lúmina iluminada. | Cruzar el último trayecto y reunirse con la familia. | Final: Rumi vuelve, más capaz y acompañado. |

## Mariposas guía

Las **Mariposas de Luz** son criaturas luminiscentes que aparecen cuando Rumi está perdido o su luz está baja. Al inicio guían a Rumi porque él todavía no ve rutas con claridad. Después de obtener la Luz propia, dejan de resolver todo: señalan secretos, aliados atrapados o una dirección posible, pero el jugador sigue eligiendo el camino.

## Prototipo realista

Para el primer prototipo en Pygame se construirá solo:

1. El prólogo del Barranco del Velo.
2. Una sección corta del Sendero de las Luces Tenues.
3. Rumi caminando, saltando, con luz variable y mariposas guía.
4. Un Susurro y una Espejilla.

Eso permite probar si el movimiento es divertido antes de crear los 12 niveles.
# Ajuste de niebla y rocas — Nivel 1

- La niebla es un overlay oscuro azul-violeta de varias capas móviles. Afecta visualmente al mapa y a Rumi, no solo al fondo.
- La luz naranja del padre y sus garras abren un claro parcial: disminuyen la opacidad sin eliminar la atmósfera.
- Las rocas de impulso son grandes, no son plataformas y se pueden reutilizar. Solo habilitan un segundo salto si Rumi está en el aire, pasa cerca y el jugador vuelve a pulsar Espacio.
- `NivelUno` compone una lista de elementos: hoy contiene niebla y rocas. Cada objeto posee sus medidas y comportamiento; el render recibe el objeto, no el nivel completo. Esto permite añadir o quitar elementos sin convertir `NivelUno` en un bloque de condiciones.
