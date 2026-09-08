"""Mensaje de interfaz que se desvanece sin afectar reglas del nivel."""


class MensajeTemporal:
    def __init__(self, duracionVisible=7.0, duracionFundido=1.0) -> None:
        self.duracionVisible = duracionVisible
        self.duracionFundido = duracionFundido
        self.texto = ""
        self.tiempo = 0.0

    def actualizar(self, texto, deltaTiempo) -> None:
        if texto != self.texto:
            self.texto = texto
            self.tiempo = 0.0
            return
        self.tiempo += max(0.0, deltaTiempo)

    @property
    def alfa(self):
        if self.tiempo <= self.duracionVisible:
            return 255
        progreso = (self.tiempo - self.duracionVisible) / self.duracionFundido
        return max(0, round(255 * (1.0 - progreso)))
