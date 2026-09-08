# Auditoría de diálogos: Mr. Fox y las voces del Velo

## Alcance

La revisión cubre los textos visibles en `narrativaNiveles.py`,
`frasesVelo.py` y `mensajesPilares.py`. Los nombres técnicos históricos como
`Padre` se conservan por compatibilidad de código y sprites; el nombre que ve
el jugador es **Mr. Fox**.

## Criterios

1. Cada diálogo identifica a su hablante cuando es una voz de personaje.
2. Mr. Fox reconoce el miedo y propone una acción concreta sin minimizarlo.
3. Las criaturas son voces ficticias del Velo, no narradores fiables.
4. Ningún texto afirma que Rumi es incapaz, inútil o abandonado como un hecho.
5. Los pilares y Rumi usan frases breves, juveniles y serias: reconocen la
   dificultad y proponen un siguiente paso.

## Resultado

- Mr. Fox habla en el reencuentro y el prólogo del Nivel 2; no aparece como
  “papá” en los textos jugables.
- Las voces hostiles conservan tensión, pero evitan etiquetas personales.
- Los mensajes de Rumi y los pilares no prometen resultados ni presentan el
  juego como terapia, diagnóstico o medición de autoestima.
- Al final del Nivel 1, el diálogo de reencuentro de Mr. Fox termina por
  completo antes de mostrar “¡Un terremoto! Hay que apresurarnos.” e iniciar
  la sacudida. La secuencia pertenece a la regla del nivel, no al dibujador.
  `EventoNivel` declara el tipo `TERREMOTO`, el mensaje y sus cinco segundos;
  la escena solo reacciona reproduciendo su efecto de sonido.
