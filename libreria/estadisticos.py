import math 

def calcular_media_muestral(datos: list) -> float:
    """Calcula el promedio empírico de la muestra (X_barra)."""
    return sum(datos) / len(datos)

def calcular_varianza_muestral(datos: list, media: float) -> float:
    """Calcula la varianza muestral S^2(n) de la muestra."""
    n = len(datos)
    return sum((x - media) ** 2 for x in datos) / (n - 1)

def calcular_error_estandar(desvio: float, n: int) -> float:
    """Calcula el error estándar de la media poblacional."""
    return desvio / math.sqrt(n)

def calcular_mediana(datos: list) -> float:
    """Calcula la mediana de una lista de datos (sin alterar el orden original)."""
    datos_ordenados = sorted(datos)
    n = len(datos_ordenados)
    mitad = n // 2
    
    if n % 2 == 0:
        return (datos_ordenados[mitad - 1] + datos_ordenados[mitad]) / 2.0
    else:
        return datos_ordenados[mitad]

def calcular_intervalo_confianza_95(media: float, error_estandar: float) -> tuple[float, float]:
    """
    Calcula el IC del 95% aproximado por la Normal (Teorema Central del Límite).
    Utiliza z_alfa/2 = 1.96.
    """
    margen_error = 1.96 * error_estandar
    limite_inf = media - margen_error
    limite_sup = media + margen_error
    return limite_inf, limite_sup

def calcular_estadisticos(tiempos: list):
    """
    Calcula la media, desviación estándar, error estándar, mediana
    y el intervalo de confianza (95%) de una muestra.
    """
    n = len(tiempos)

    media      = calcular_media_muestral(tiempos)
    varianza   = calcular_varianza_muestral(tiempos, media)
    desvio     = math.sqrt(varianza)
    error_est  = calcular_error_estandar(desvio, n)
    mediana    = calcular_mediana(tiempos)
    ic_95      = calcular_intervalo_confianza_95(media, error_est)

    return media, desvio, error_est, mediana, ic_95
