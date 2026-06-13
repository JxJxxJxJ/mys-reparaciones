def calcular_media_muestral(datos: list) -> float:
    """Calcula el promedio empírico de la muestra (X_barra)."""
    return sum(datos) / len(datos)

def calcular_varianza_muestral(datos: list, media: float) -> float:
    """Calcula la varianza muestral S^2(n) de la muestra."""
    n = len(datos)
    return sum((x - media) ** 2 for x in datos) / (n - 1)