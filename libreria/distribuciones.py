import math 
import scipy.stats as stats

def pdf_exponencial(x: float, lamda: float) -> float:
    """Función de densidad de probabilidad de una Exponencial(lamda)."""
    if x < 0: 
        return 0.0
    return lamda * math.exp(-lamda * x)

def cdf_exponencial(x: float, lamda: float) -> float:
    """ CDF teórica de la Exponencial F(x) = 1 - e^(-lamda * x) """
    if x < 0:
        return 0.0
    return 1.0 - math.exp(-lamda * x)

def pdf_gamma(x: float, alfa: float, beta: float) -> float:
    """
    Función de densidad de probabilidad teórica de una Gamma(alfa, beta).
    """
    if x <= 0: 
        return 0.0
    coeficiente = 1.0 / (math.gamma(alfa) * (beta ** alfa))
    return coeficiente * (x ** (alfa - 1)) * math.exp(-x / beta)

def cdf_gamma(x: float, alfa: float, beta: float) -> float:
    """ CDF teórica de la Gamma evaluada en x """
    return stats.gamma.cdf(x, a=alfa, scale=beta)