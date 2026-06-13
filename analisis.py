from simulaciones import simular_fallo_1_tecnico, simular_fallo_2_tecnicos
from libreria.estadisticos import calcular_estadisticos
from histogramas.generar_histogramas import graficar_histograma_y_ajuste

N_SIMULACIONES = 10_000

def imprimir_resultados_escenario(nombre_escenario: str, tiempos: list):
    """
    Calcula e imprime de forma tabulada todos los estadísticos 
    descriptivos para un escenario simulado.
    """
    # Desempaqueto la tupla con los 5 estadisticos que me interesan
    media, desvio, error_est, mediana, ic_95 = calcular_estadisticos(tiempos)
    
    print(f"\n{'-'*60}")
    print(f" {nombre_escenario}")
    print(f"{'-'*60}")
    print(f"   Media (T_barra)  : {media:.4f} meses")
    print(f"   Desvío Estándar  : {desvio:.4f} meses")
    print(f"   Error Estándar   : {error_est:.4f} meses")
    print(f"   Mediana          : {mediana:.4f} meses")
    print(f"   IC 95%           : [{ic_95[0]:.4f}; {ic_95[1]:.4f}]")

if __name__ == "__main__":
    N_SIM = 10000
    print(f"Iniciando simulación de {N_SIM} iteraciones por escenario...")
    
    # ---------------------------------------------------------
    # 1. ESCENARIO BASE: 1 Operario, S = 3
    # ---------------------------------------------------------
    # Llamamos a tu función original simulando 10000 veces
    tiempos_base = [simular_fallo_1_tecnico(n_cajas_repuesto=3) for _ in range(N_SIM)]
    imprimir_resultados_escenario("ESCENARIO BASE (1 Operario, S=3)", tiempos_base)
    graficar_histograma_y_ajuste(tiempos_base, "Escenario Base (1 Operario, S=3)", "histogramas/hist_base.png")
    
    # ---------------------------------------------------------
    # 2. ALTERNATIVA B: 1 Operario, S = 4 (Repuesto extra)
    # ---------------------------------------------------------
    # Usamos la misma función pero alterando tu parámetro n_cajas_repuesto
    tiempos_alt_b = [simular_fallo_1_tecnico(n_cajas_repuesto=4) for _ in range(N_SIM)]
    imprimir_resultados_escenario("ALTERNATIVA B (1 Operario, S=4)", tiempos_alt_b)
    graficar_histograma_y_ajuste(tiempos_alt_b, "Alternativa B (Repuesto extra, S=4)", "histogramas/hist_s4.png")
    
    # ---------------------------------------------------------
    # 3. ALTERNATIVA A: 2 Operarios, S = 3 (Segundo técnico)
    # ---------------------------------------------------------
    # Llamamos a tu función para dos técnicos
    tiempos_alt_a = [simular_fallo_2_tecnicos(n_cajas_repuesto=3) for _ in range(N_SIM)]
    imprimir_resultados_escenario("ALTERNATIVA A (2 Operarios, S=3)", tiempos_alt_a)
    graficar_histograma_y_ajuste(tiempos_alt_a, "Alternativa A (2 Operarios, S=3)", "histogramas/hist_2op.png")

    print(f"\n{'-'*60}")
    print("Simulación finalizada con éxito.")