from test_bondad_ajuste.dardo_test_ks import crear_dardo_ks_estimando_parametros
from libreria.estadisticos import estimar_exp_momentos, estimar_gamma_momentos
from libreria.generadores import gen_exponencial_lamda, gen_gamma_alfa_beta
from libreria.distribuciones import cdf_exponencial, cdf_gamma

def imprimir_resultados_ks(nombre_escenario: str, tiempos: list, n_sim_ks: int = 1000):
    """
    Ejecuta el test K-S utilizando la fábrica de dardos con Bootstrap Paramétrico 
    para distribuciones continuas, estimando los parámetros desde la muestra.
    """
    print(f"\n--- Tests Kolmogorov-Smirnov (Bootstrap Paramétrico) para {nombre_escenario} ---")

    # ---------------- 1. TEST EXPONENCIAL ----------------
    lamda_exp = estimar_exp_momentos(tiempos) # devuelve parametro exp: lambda
    
    dardo_exp, d_obs_exp = crear_dardo_ks_estimando_parametros(
        muestra_real_observada=tiempos,
        funcion_estimar_parametro_H0 = lambda datos : estimar_exp_momentos(datos),
        generar_dato_simulado_H0     = lambda p     : gen_exponencial_lamda(lamda=p),
        evaluar_cdf_H0               = lambda x, p  : cdf_exponencial(x, lamda=p),
        shh=True # Silencio debugeo para no ensuciar stdout
    )
    
    # Tiro el dardo n_sim_ks veces para estimar el p-valor (montecarlo)
    p_valor_exp = sum(dardo_exp() for _ in range(n_sim_ks)) / n_sim_ks

    # ---------------- 2. TEST GAMMA ----------------
    params_gamma = estimar_gamma_momentos(tiempos) # devuelve parametros gamma: (alfa, beta)
    
    dardo_gamma, d_obs_gamma = crear_dardo_ks_estimando_parametros(
        muestra_real_observada=tiempos,
        funcion_estimar_parametro_H0 = lambda datos : estimar_gamma_momentos(datos),
        generar_dato_simulado_H0     = lambda p     : gen_gamma_alfa_beta(alfa=p[0], beta=p[1]),
        evaluar_cdf_H0               = lambda x, p  : cdf_gamma(x=x, alfa=p[0], beta=p[1]),
        shh=True
    )
    
    p_valor_gamma = sum(dardo_gamma() for _ in range(n_sim_ks)) / n_sim_ks

    # ---------------- IMPRESIÓN ----------------
    print(f"   [Exponencial (λ={lamda_exp:.4f})] D_obs = {d_obs_exp:.4f} | p-valor = {p_valor_exp:.4f}")
    print(f"   [Gamma (α={params_gamma[0]:.4f}, β={params_gamma[1]:.4f})] D_obs = {d_obs_gamma:.4f} | p-valor = {p_valor_gamma:.4f}")
    print(f"   Decisión (nivel=0.05):")
    print(f"    - Exponencial: {'RECHAZAR H0' if p_valor_exp < 0.05 else 'NO RECHAZAR H0'}")
    print(f"    - Gamma:       {'RECHAZAR H0' if p_valor_gamma < 0.05 else 'NO RECHAZAR H0'}\n")