"""Cámara lateral independiente de la biblioteca gráfica."""

def calcularCamara(x: float, anchoMapa: float, anchoVentana: float, margen: float = 360.0) -> float:
    return max(0.0, min(x - margen, max(0.0, anchoMapa - anchoVentana)))
