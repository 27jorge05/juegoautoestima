# Rumi: especificación inicial de sprites

Rumi es un cachorro de zorro joven. Su diseño debe ser tierno y con actitud, no humanoide.

## Apariencia

- Pelaje naranja rojizo, pecho y punta de cola crema.
- Orejas grandes, ojos expresivos y cola voluminosa.
- Pañuelo azul petróleo: recuerdo de casa y elemento visual reconocible.
- Pequeña luz cálida en la punta de la cola; no debe parecer un arma.

## Sprites necesarios para el primer prototipo

- `rumi_idle.png`: reposo, mirando a la derecha.
- `rumi_run.png`: tira de 4 fotogramas de carrera, mirando a la derecha.
- `rumi_hurt.png`: reacción breve al recibir daño.
- `rumi_claw_grip.png`: agarre con garras luminosas.
- `rumi_light_pulse.png`: habilidad de calma/luz.

Los archivos deberán tener fondo transparente, estilo pixel art 2D, cuadrícula consistente y sin texto.

## Assets generados — versión 1

- `rumi_sprite_sheet_v1.png`: primer borrador de Rumi con reposo, carrera, salto, agarre de garras, daño y pulso de luz.
- `rumi_sprite_sheet_v2.png`: borrador de poses y luz.
- `../../enemies/enemigos_nivel_01_v1.png`: hoja para Susurros, Espejillas, pajarito guía y padre de Rumi.
- `../../backgrounds/barranco_del_velo_v1.png`: fondo pixel art del primer nivel.

Los borradores se conservan como referencia. La versión activa se describe al final de este archivo y se carga desde `src/dibujadorNivelUno.py`.
# Hojas de sprites activas

- `rumi_sprite_sheet_v3.png`: Rumi, 12 poses para reposo, carrera, salto, garras y cansancio.
- `padre_sprite_sheet_v1.png`: padre de Rumi, 12 poses para guía, caminata, protección y reencuentro.

Las hojas se dividen en una cuadrícula de 4 columnas por 3 filas y se consumen desde `src/animaciones.py`.
