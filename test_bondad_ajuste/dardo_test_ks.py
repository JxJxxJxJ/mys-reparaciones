def calcular_estadistico_D(datos: list[float], funcion_cdf) -> float:
    """
    Calcula el estadístico D de Kolmogorov-Smirnov para datos continuos.
    
    Args:
        datos: Lista de datos crudos observados.
        funcion_cdf: La Función de Distribución Acumulada (CDF) a evaluar. 
                     Debe recibir un solo parámetro 'x'. (Si tiene más, pásala con un lambda).
                     
    Returns:
        El valor del estadístico D_obs (la máxima deformación).
    """
    n_total = len(datos)
    
    # Es obligatorio ordenar los datos de menor a mayor
    datos_ordenados = sorted(datos)
    
    d_obs = 0.0
    # Recorro los datos y^(1), ..., y^(n_total-1) evaluando las distancias entre Fe(Y^(j)) 
    # a la acumulada F(y^(j))
    for j in range(n_total):
        x = datos_ordenados[j]
        F_teorica_en_x = funcion_cdf(x)

        # Como en Python los indices 'j' van de 0 a n-1, las proporciones son:
        Fe_techo = (j + 1) / n_total
        Fe_piso = j / n_total
        
        distancia_arriba_curva = Fe_techo - F_teorica_en_x
        distancia_abajo_curva = F_teorica_en_x - Fe_piso       

        # Actualizo max
        d_obs = max(d_obs, distancia_arriba_curva, distancia_abajo_curva)
        
    return d_obs

def crear_dardo_ks_estimando_parametros(
    muestra_real_observada: list[float],
    funcion_estimar_parametro_H0: callable,
    generar_dato_simulado_H0: callable,
    evaluar_cdf_H0: callable,
    shh=None
):
    """
    Fábrica de Kolmogorov-Smirnov para distribuciones continuas ESTIMANDO parámetros.
    (Bootstrap Paramétrico). 
    
    Como estimamos un parámetro, "forzamos" a la curva teórica a acercarse a nuestros 
    datos reales (achicando el error). Para que la comparación sea justa, el universo 
    simulado está obligado a estimar su propio parámetro falso a partir de sus 
    propios datos falsos.
    
    ----------------------------------------------------------------------
    EJEMPLO DE INYECCIÓN (Ej. 9 Práctico 7: Probar si es Exponencial desconocida):
    ----------------------------------------------------------------------
    ATENCIÓN: A diferencia de K-S sin estimar, aquí el generador y la evaluar_cdf deben 
    estar preparados para recibir el parámetro que la estimadora adivine.
    
    - funcion_estimar_parametro_H0 = lambda muestra: len(muestra) / sum(muestra)        # Para estimar thetavec_real y thetavec_sim
    - generar_dato_simulado_H0     = lambda lamda_est: gen_exponencial(lamda=lamda_est) # Para generar datos_sim mediante gen(Thetavec_real)
    - evaluar_cdf_H0               = lambda x, lamda_est: 1 - exp(-lamda_est * x)       # Para calcular estadistico D
    """

    n_total = len(muestra_real_observada)

    # ---------------------------------------------------------
    # MUNDO REAL: Se ajusta la curva a los datos
    # ---------------------------------------------------------
    # Se estima mediante los datos reales al parametro real
    param_real_estimado = funcion_estimar_parametro_H0(muestra_real_observada)
    
    # Calculo el estadistico respecto a los datos y esta curva teorica (H0) con parametro estimado
    d_obs = calcular_estadistico_D(
        muestra_real_observada, 
        lambda x: evaluar_cdf_H0(x, param_real_estimado)
    )

    if shh is None:
        print(f"[Factory K-S Bootstrap] Parámetro real estimado: {param_real_estimado:.4f}")
        print(f"[Factory K-S Bootstrap] Deformación real (d_obs): {d_obs:.4f}")

    # ---------------------------------------------------------
    # SIMULACION: El Dardo de Monte Carlo
    # ---------------------------------------------------------
    def dardo_montecarlo():
        # Muestreo datos_sim asumiendo que el parametro_real_estimado desde la muestra real es cierto
        datos_sim = [generar_dato_simulado_H0(param_real_estimado) for _ in range(n_total)]
        
        # Estimo thetavec_sim mediante los datos simulados
        param_falso_estimado = funcion_estimar_parametro_H0(datos_sim)
        
        # Calculo D_sim entre los datos_sim y la curva F_sim(Thetavec_sim)
        D_sim = calcular_estadistico_D(
            datos_sim, 
            lambda x_sim: evaluar_cdf_H0(x_sim, param_falso_estimado)
        )

        # Output de la indicadora I(D_sim >= d_obs)
        return D_sim >= d_obs 

    return dardo_montecarlo, d_obs