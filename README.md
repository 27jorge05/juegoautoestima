# Rumi: El Barranco del Velo

Prototipo jugable de exploración y plataformas en español. Rumi encuentra a Mr. Fox en el Barranco, cruza los Espejos de Niebla hasta un farol y busca la salida de la Cueva del Velo.

## Ejecutar

Objetivo del proyecto: Python 3.11+ y Pygame CE. Con las dependencias ya instaladas:

```bash
.venv/bin/python main.py
```

El entorno disponible durante este refactor tiene Python 3.10.12 y Pygame CE 2.5.8; las pruebas se ejecutaron ahí. No se instaló ni cambió ninguna dependencia. Falta comprobar la ejecución en Python 3.11+.

## Crear el ejecutable de Windows

Desde PowerShell, después de clonar el repositorio:

```powershell
py -m pip install -r requirements.txt pyinstaller
py -m PyInstaller --noconfirm main.spec
```

El resultado queda en `dist\\RumiAventura.exe`. La carpeta `dist/` no se
versiona porque es un producto de compilación; el código, los recursos y
`main.spec` sí se incluyen al clonar.

### Compilar sin una computadora Windows

El flujo [Compilar ejecutable de Windows](.github/workflows/build-windows.yml)
usa un runner Windows x64 de GitHub Actions. Después de subir el repositorio a
GitHub, abre **Actions**, elige ese flujo y pulsa **Run workflow**. Al terminar
sin errores, descarga el artefacto **RumiAventura-windows-x64**: contiene
`RumiAventura.exe` listo para Windows. El flujo instala Python 3.11, ejecuta
las pruebas y solo publica el ejecutable si el archivo existe. El flujo usa la
versión de Node 24 de la acción oficial de artefactos.

## Controles

- Flechas o A/D: moverse; W/S o flechas verticales: navegar el menú.
- Espacio: entrar al nivel o saltar. En el Nivel 2, una pulsación en el aire junto a una roca da el segundo salto.
- F: usar luz contra criaturas en el Nivel 2.
- E: activar un farol o escuchar un pilar de aliento cercano dentro de la Cueva del Velo. El farol da luz durante tres segundos.
- R: reiniciar el nivel completo.
- Escape: volver al menú. Al volver a entrar empieza una partida nueva.

## Arquitectura

`main.py` inicia `Juego`. El juego coordina escenas con un contrato común; la fábrica crea el nivel seleccionado. `EscenaNivelUno` coordina reglas, entrada, cámara, presentación y sonidos. `NivelUno` conserva las reglas sin importar Pygame.

```text
src/
├── aplicacion/   ciclo del juego, menú, entrada, fábrica y configuración
├── audio/        reproducción de efectos y música
├── dominio/      entidades, reglas, vida, eventos y tipos
├── mundo/        mapas, elementos, recursos y creadores de escenario
├── niveles/      reglas y narrativa de cada capítulo
└── presentacion/ escenas, cámara, animaciones y dibujadores Pygame
```

`CreadorBarrancoVelo` construye el mundo; `EscenarioNivel` contiene plataformas tipadas, decoración, elementos, enemigos y tramos. `DibujadorEscenario` interpreta esos datos. Los frames viven en `animaciones.py`; dibujar no avanza su tiempo.

## Verificación

```bash
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python3 -m unittest discover -s tests -p 'test*.py'
```

El modo dummy comprueba integración sin abrir una ventana; no sustituye una partida manual ni la escucha del audio.

## Documentación

- [Fundamento y límites del juego](docs/01_tres_raices_autoestima.md)
- [Personaje Rumi](docs/02_personaje_rumi.md)
- [Criaturas del Velo](docs/03_enemigos_del_velo.md)
- [Niveles y capítulos](docs/04_niveles_y_capitulos.md)
- [Plan técnico inicial](docs/05_plan_tecnico_nivel_01.md)
- [Tareas atómicas, criterios y revisiones del refactor](docs/07_refactor_iteraciones.md)
- [Terremoto, voces y pilares: tareas y validaciones](docs/11_iteraciones_terremoto_pilares.md)
- [Revisión crítica de jugabilidad por nivel](docs/12_revision_jugabilidad_por_nivel.md)
- [Dificultad, niebla densa y música de cueva](docs/13_dificultad_niebla_musica.md)
- [Auditoría de diálogos](docs/14_auditoria_dialogos.md)
- [Luz, niebla y diálogos de criaturas](docs/15_luz_niebla_y_dialogos.md)
- [Estructura de carpetas](docs/16_estructura_de_carpetas.md)

El juego no presenta sus mecánicas como terapia, diagnóstico ni medición clínica. No usa cuentas, telemetría ni almacenamiento de respuestas personales.
