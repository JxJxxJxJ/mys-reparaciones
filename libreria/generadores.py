from math import log
from random import random

def gen_exponencial(media):
    """
    Genera una variable aleatoria exponencial por el Método de la Transformada Inversa.
    E[X] = media.
    """
    # Usamos random() nativo que distribuye U(0,1)
    return -media * log(random())