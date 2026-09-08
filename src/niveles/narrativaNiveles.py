"""Guion declarativo: separa relato y voz de cada personaje."""

from src.dominio.mensajes import Dialogo, Relato
from src.dominio.eventosNivel import EventoNivel, TipoEventoNivel


NIVEL_UNO_INICIO = Relato("Encuentra a Mr. Fox al final del camino.")
NIVEL_UNO_CAIDA = Relato("Rumi cayó del camino. Respira y vuelve a intentarlo.")
NIVEL_UNO_SIN_VIDAS = Relato("El Velo agotó las vidas de Rumi. Respira y vuelve a intentarlo.")
NIVEL_UNO_MR_FOX = Dialogo(
    "Rumi, por fin llegas. Las voces del Velo pueden sonar fuertes, pero no deciden quién eres. Mira el camino y da el siguiente paso.",
    hablante="Mr. Fox",
)
NIVEL_UNO_TERREMOTO_AVISO = Dialogo(
    "¡Un terremoto! Hay que apresurarnos.",
    hablante="Mr. Fox",
)
EVENTO_TERREMOTO_NIVEL_UNO = EventoNivel(
    TipoEventoNivel.TERREMOTO,
    NIVEL_UNO_TERREMOTO_AVISO,
    duracion=5.0,
)
NIVEL_UNO_TERREMOTO_FINAL = Relato("El terremoto terminó. Rumi y Mr. Fox buscarán el farol.")

NIVEL_DOS_INICIO = Dialogo(
    "Rumi, sigue adelante. Usa las rocas para dar un segundo salto. Yo revisaré si alguien más necesita ayuda; nos veremos junto al farol.",
    hablante="Mr. Fox",
)
NIVEL_DOS_LUZ = (
    Dialogo("Esas criaturas hacen ruido para distraerte. Respira y elige tu siguiente movimiento.", hablante="Mr. Fox"),
    Dialogo("Las voces del Velo no deciden quién eres. Tú eliges qué paso dar.", hablante="Mr. Fox"),
    Relato("La luz abre un camino breve entre las voces del Velo."),
)
NIVEL_DOS_CAIDA = Relato("Rumi cayó en la niebla.")
NIVEL_DOS_SIN_VIDAS = Relato("Rumi perdió sus tres vidas.")
NIVEL_DOS_FINAL = Dialogo("Qué miedo… mejor me escondo en la cueva.", hablante="Rumi")


def derrotaNivelDos(motivo: Relato) -> Relato:
    return Relato(f"{motivo.texto} Un intento no decide lo que puedes aprender. R: volver a intentarlo.")

NIVEL_TRES_INICIO = Relato("La niebla cubre la cueva. Presiona E junto a un farol para recibir luz durante tres segundos y junto a un pilar para escuchar aliento.")
NIVEL_TRES_LUZ = Dialogo("Mi luz te acompañará un momento. Avanza mientras el claro siga abierto.", hablante="Farol")
NIVEL_TRES_LUZ_AGOTADA = Dialogo("Tengo miedo y la oscuridad me hace dudar. Buscaré un pilar y avanzaré paso a paso.", hablante="Rumi")
NIVEL_TRES_CAIDA = Relato("Rumi cayó en la cueva.")
NIVEL_TRES_SIN_VIDAS = Relato("Rumi perdió sus tres vidas.")
NIVEL_TRES_DERROTA = Dialogo("¿Ves? Te dije que fallarías.", hablante="Velo")
NIVEL_TRES_SALIDA = Relato("Rumi encontró la salida. La cueva queda atrás y el camino vuelve a abrirse.")


def derrotaNivelTres(motivo: Relato) -> Relato:
    return Relato(f"{motivo.texto} R: volver a intentarlo.")
