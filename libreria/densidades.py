import math 

def pdf_exponencial(x: float, lamda: float) -> float:
    """Función de densidad de probabilidad de una Exponencial(lamda)."""
    if x < 0: 
        return 0.0
    return lamda * math.exp(-lamda * x)

def pdf_gamma(x: float, alfa: float, beta: float) -> float:
    """
    Función de densidad de probabilidad teórica de una Gamma(alfa, beta).
    alfa = parámetro de forma (k)
    beta = parámetro de escala (theta)
    """
    if x <= 0: 
        return 0.0
    # math.gamma(alfa) calcula exactamente la función Gamma teórica
    coeficiente = 1.0 / (math.gamma(alfa) * (beta ** alfa))
    return coeficiente * (x ** (alfa - 1)) * math.exp(-x / beta)