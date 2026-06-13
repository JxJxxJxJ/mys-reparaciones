"""
Ejercicio 1 - Problema de reparación con un operario.

Un supermercado tiene N cajas registradoras en servicio y S de repuesto.
Las cajas en uso fallan tras tiempos Exp de media TF; un único técnico
repara de a una caja por vez, con tiempos de reparación Exp de media TR.
Una caja reparada vuelve al banco de repuestos. El SISTEMA FALLA en el
instante en que hay más de S cajas rotas (equivalentemente, quedan menos
de N cajas en condiciones de estar en servicio).

El programa simula el modelo mediante eventos discretos y estima el
tiempo medio de fallo del sistema y su desviación estándar a partir de
n_sim simulaciones independientes.

Todos los tiempos se expresan en MESES.
"""

from libreria.generadores import gen_exponencial

# Parametros del enunciado
N = 7          # Cajas en servicio
S = 3          # Repuestos
TF = 1.0       # Tiempo medio hasta fallar (meses)
TR = 1.0 / 8   # Tiempo medio de reparación (meses)
INF = float("inf")

def simular_fallo_1_operario(
    n_cajas_servicio : int   = N, 
    n_cajas_repuesto : int   = S, 
    media_falla      : float = TF, 
    media_reparacion : float = TR
) -> float:
    # Variables de estado
    reloj_actual = 0.0
    cant_maquinas_rotas = 0
    t_fin_reparacion = INF
    
    # Sorteo de los tiempos de falla de las 7 CAJAS iniciales
    tiempos_proxima_falla = [gen_exponencial(media=media_falla) for _ in range(n_cajas_servicio)]

    while cant_maquinas_rotas <= n_cajas_repuesto:
        
        t_proxima_falla = min(tiempos_proxima_falla)
        t_proximo_evento = min(t_proxima_falla, t_fin_reparacion)

        # ---------------------------------------------------------
        # CASO 1: UNA MAQUINA EN SERVICIO FALLA
        # ---------------------------------------------------------
        if t_proximo_evento == t_proxima_falla:
            reloj_actual         = t_proxima_falla
            cant_maquinas_rotas += 1
            
            # Condicion de colapso: Se rompió una máquina y el banco de repuestos estaba vacío
            if cant_maquinas_rotas > n_cajas_repuesto:
                break 
            
            # Se continua la simulacion, existen cajas de repuesto listas para ser swapeadas
            elif cant_maquinas_rotas <= n_cajas_repuesto:
                # Identifico CUAL caja fallo (por ID 0...6)
                id_puesto = tiempos_proxima_falla.index(t_proxima_falla)
                    
                # El repuesto entra en servicio inmediatamente, se sortea su tiempo de falla
                tiempos_proxima_falla[id_puesto] = reloj_actual + gen_exponencial(media_falla)

                # Si el tecnico estaba libre, se pone a trabajar de inmediato en la maquina rota
                if cant_maquinas_rotas == 1:
                    t_fin_reparacion = reloj_actual + gen_exponencial(media_reparacion)

        # ---------------------------------------------------------
        # CASO 2: UNA MAQUINA SE HA TERMINADO DE REPARAR
        # ---------------------------------------------------------
        elif t_proximo_evento == t_fin_reparacion:
            reloj_actual         = t_fin_reparacion
            cant_maquinas_rotas -= 1
            
            # La maquina reparada va al banco de repuestos (APAGADA).
            # Como esta apagada, se decide NO SORTEAR su tiempo de falla.
            
            # El taller tiene aun maquinas para reparar, el técnico sigue trabajando 
            if cant_maquinas_rotas > 0:
                t_fin_reparacion = reloj_actual + gen_exponencial(media_reparacion)
            elif cant_maquinas_rotas <= 0:
                t_fin_reparacion = INF
                
    return reloj_actual