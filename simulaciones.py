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

def simular_fallo_1_tecnico(
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
            
            if cant_maquinas_rotas > 0:
                # El taller tiene aun maquinas para reparar, el tecnico sigue trabajando 
                t_fin_reparacion = reloj_actual + gen_exponencial(media_reparacion)
            elif cant_maquinas_rotas <= 0:
                # No hay maquinas en el pasillo. El tecnico pasa a estado ocioso.
                t_fin_reparacion = INF
                
    return reloj_actual

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
    n_cajas_servicio : int   = 7, 
    n_cajas_repuesto : int   = 3, 
    media_falla      : float = 1.0, 
    media_reparacion : float = 1.0 / 8
) -> float:
    # Variables de estado
    reloj_actual = 0.0
    cant_maquinas_rotas = 0
    
    # DOS TECNICOS: Dos relojes de fin de reparación independientes
    t_fin_reparacion = [INF, INF]
    
    # Sorteo de los tiempos de falla de las 7 CAJAS iniciales
    tiempos_proxima_falla = [gen_exponencial(media=media_falla) for _ in range(n_cajas_servicio)]

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
            tiempos_proxima_falla[id_puesto] = reloj_actual + gen_exponencial(media_falla)

            # Si el Tecnico 0 esta libre, se pone a trabajar
            if t_fin_reparacion[0] == INF:
                t_fin_reparacion[0] = reloj_actual + gen_exponencial(media_reparacion)
            # Si el Tecnico 0 esta ocupado pero el Tecnico 1 esta libre, se pone a trabajar el 1
            elif t_fin_reparacion[1] == INF:
                t_fin_reparacion[1] = reloj_actual + gen_exponencial(media_reparacion)

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
                t_fin_reparacion[id_operario_libre] = reloj_actual + gen_exponencial(media_reparacion)
            elif cant_maquinas_rotas <= 1:
                # No hay maquinas en el pasillo. El tecnico pasa a estado ocioso.
                t_fin_reparacion[id_operario_libre] = INF
                
    return reloj_actual