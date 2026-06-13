from simulaciones.parametros_y_tiempos_enunciado import S, N, INF, gen_tiempo_falla, gen_tiempo_reparacion

"""
Ejercicio 2 - Problema de reparación con dos operarios y alternativas.

El supermercado desea aumentar el tiempo medio hasta el fallo del sistema y 
para esto analiza y evalúa dos alternativas posibles:
1. Alternativa A: Contratar un segundo operario igualmente idóneo 
   (trabajan en paralelo, cada uno repara de a una caja por vez). 
   Se mantiene el stock de repuestos original (S = 3).
2. Alternativa B: Comprar una caja extra como repuesto (S = 4), 
   manteniendo un único operario (modelo del Ejercicio 1).

Las cajas en uso fallan tras tiempos Exp de media TF; cada operario 
emplea un tiempo de reparación Exp de media TR. El SISTEMA FALLA en el 
instante en que hay más de S cajas rotas.

El programa simula el modelo mediante eventos discretos, estima el
tiempo medio de fallo del sistema y su desviación estándar a partir de
n_sim simulaciones independientes, y compara los resultados para 
determinar la mejor alternativa.

Todos los tiempos se expresan en MESES.
"""

def simular_fallo_2_tecnicos(
    n_cajas_servicio : int = N, 
    n_cajas_repuesto : int = S, 
) -> float:
    # Variables de estado
    reloj_actual = 0.0
    cant_maquinas_rotas = 0
    
    # DOS TECNICOS: Dos relojes de fin de reparación independientes
    t_fin_reparacion = [INF, INF]
    
    # Sorteo de los tiempos de falla de las 7 CAJAS iniciales
    tiempos_proxima_falla = [gen_tiempo_falla() for _ in range(n_cajas_servicio)]

    while cant_maquinas_rotas <= n_cajas_repuesto:
        
        t_proxima_falla      = min(tiempos_proxima_falla)
        t_proxima_reparacion = min(t_fin_reparacion) # El tecnico que termine primero su reparacion
        t_proximo_evento     = min(t_proxima_falla, t_proxima_reparacion)

        # ---------------------------------------------------------
        # CASO 1: UNA MAQUINA EN SERVICIO FALLA
        # ---------------------------------------------------------
        if t_proximo_evento == t_proxima_falla:
            reloj_actual         = t_proxima_falla
            cant_maquinas_rotas += 1
            
            if cant_maquinas_rotas > n_cajas_repuesto:
                break # Colapso del sistema
            
            # El repuesto entra en servicio inmediatamente (swapeo en la línea de cajas)
            id_puesto = tiempos_proxima_falla.index(t_proxima_falla)
            tiempos_proxima_falla[id_puesto] = reloj_actual + gen_tiempo_falla()

            # Si el Tecnico 0 esta libre, se pone a trabajar
            if t_fin_reparacion[0] == INF:
                t_fin_reparacion[0] = reloj_actual + gen_tiempo_reparacion()
            # Si el Tecnico 0 esta ocupado pero el Tecnico 1 esta libre, se pone a trabajar el 1
            elif t_fin_reparacion[1] == INF:
                t_fin_reparacion[1] = reloj_actual + gen_tiempo_reparacion()

        # ---------------------------------------------------------
        # CASO 2: UNA MAQUINA FINALIZA SU REPARACION
        # ---------------------------------------------------------
        elif t_proximo_evento == t_proxima_reparacion:
            reloj_actual         = t_proxima_reparacion
            cant_maquinas_rotas -= 1
            
            # Identifico CUAL tecnico acaba de terminar su reparacion (el 0 o el 1)
            id_operario_libre = t_fin_reparacion.index(t_proxima_reparacion)
            
            # La maquina reparada va al banco de repuestos (APAGADA).
            # Como esta apagada, se decide NO SORTEAR su tiempo de falla.
            
            # Si hay 2 o mas maquinas rotas, significa que 1 la esta reparando el otro tenico 
            # y al menos 1 esta esperando en el pasillo. Este tecnico toma la que espera.
            if cant_maquinas_rotas >= 2:
                t_fin_reparacion[id_operario_libre] = reloj_actual + gen_tiempo_reparacion()
            elif cant_maquinas_rotas <= 1:
                # No hay maquinas en el pasillo. El tecnico pasa a estado ocioso.
                t_fin_reparacion[id_operario_libre] = INF
                
    return reloj_actual