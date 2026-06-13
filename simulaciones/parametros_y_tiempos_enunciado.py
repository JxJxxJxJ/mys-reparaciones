from math import log 
from random import random
from libreria.generadores import gen_exponencial_media

# Parametros del enunciado
N = 7          # Cajas en servicio
S = 3          # Repuestos
TF = 1.0       # Tiempo medio hasta fallar (meses)
TR = 1.0 / 8   # Tiempo medio de reparación (meses)
INF = float("inf")

def gen_tiempo_falla():
    """Simula un tiempo de falla ~ E(media=TF)"""
    return gen_exponencial_media(TF)

def gen_tiempo_reparacion():
    """Simula un tiempo de reparacion ~ E(media=TR)"""
    return gen_exponencial_media(TR)