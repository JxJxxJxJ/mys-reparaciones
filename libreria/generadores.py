from random import random, gammavariate
from math import log

# --------------------------------------------------------------------------------------

def gen_exponencial_lamda(lamda: float) -> float:
    """ 
    Genera un dato Exponencial mediante el método de la 
    Transformada Inversa usando la tasa (lamda): -ln(1-U)/lamda.
    """
    return -log(1.0 - random()) / lamda

def gen_exponencial_media(media: float) -> float:
    """ 
    Genera un dato Exponencial mediante el método de la 
    Transformada Inversa usando la media (E[X] = 1/lamda): -media * ln(1-U).
    """
    return -media * log(1.0 - random())

# def gen_n_exponenciales_parametros(n: int, lamda: float) -> list:
#     """ 
#     Genera 'n' datos Exponenciales mediante el método de la 
#     Transformada Inversa: -ln(1-U)/lamda.
#     """
#     return [gen_exponencial_lamda(lamda) for _ in range(n)]

# --------------------------------------------------------------------------------------

def gen_gamma_alfa_beta(alfa: float, beta: float) -> float:
    """ 
    Genera un único dato Gamma(alfa, beta).
    """
    return gammavariate(alfa, beta)

# def gen_n_gammas_parametros(n: int, parametros: tuple) -> list:
#     """ 
#     Genera 'n' datos Gamma desempaquetando la tupla (alfa, beta). 
#     """
#     alfa, beta = parametros
#     return [gammavariate(alfa, beta) for _ in range(n)]