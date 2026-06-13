import math
import matplotlib.pyplot as plt
import scipy.stats as stats
from simulaciones import simular_fallo_1_tecnico, simular_fallo_2_tecnicos
from libreria.densidades import pdf_exponencial, pdf_gamma
from libreria.estadisticos import calcular_media_muestral, calcular_varianza_muestral

N_SIMULACIONES = 10_000

def ejecutar_montecarlo(funcion_simuladora, n_repuestos) -> list:
    """Ejecuta N simulaciones y devuelve la lista de tiempos de colapso."""
    tiempos = []
    for _ in range(N_SIMULACIONES):
        t = funcion_simuladora(n_cajas_repuesto=n_repuestos)
        tiempos.append(t)
    return tiempos

def calcular_estadisticos(tiempos: list):
    """Calcula la media y la desviación estándar muestral de una lista de datos."""
    n = len(tiempos)
    media    = calcular_media_muestral(tiempos)
    varianza = calcular_varianza_muestral(tiempos, media)
    desvio   = math.sqrt(varianza)
    return media, desvio

def graficar_histograma_y_ajuste(tiempos: list, titulo: str, nombre_archivo: str):
    """
    Genera el histograma y superpone los ajustes Exponencial y Gamma 
    estimados y evaluados 100% analíticamente.
    """
    # Calculo estadisticos para estimar parametros
    media_est    = calcular_media_muestral(tiempos)
    varianza_est = calcular_varianza_muestral(tiempos, media_est)
    
    # Estimacion teorica de parametros (Metodo de los Momentos)
    lamda_est  = 1.0 / media_est
    forma_est  = (media_est ** 2) / varianza_est  # Alfa (forma)
    escala_est = varianza_est / media_est         # Beta (escala)
    
    # Preparo el grafico
    plt.figure(figsize=(8, 5))
    plt.hist(tiempos, bins=40, density=True, alpha=0.6, color='skyblue', edgecolor='white', label='Datos Simulados')
    
    # Genero el dominio x para evaluar las curvas exp y gamma
    x_vals = [i * 0.1 for i in range(int(max(tiempos) * 10) + 1)]
    
    # Evaluo las densidades
    y_expon = [pdf_exponencial(xi, lamda_est) for xi in x_vals]
    y_gamma = [pdf_gamma(xi, forma_est, escala_est) for xi in x_vals]
    
    plt.plot(x_vals, y_expon, 'r-',  lw=2, label=f'Ajuste Expon($\\lambda$={1/media_est:.2f})')
    plt.plot(x_vals, y_gamma, 'g--', lw=2, label=f'Ajuste Gamma($\\alpha$={forma_est:.2f}, $\\beta$={escala_est:.2f})')
    
    plt.title(titulo)
    plt.xlabel('Tiempo de fallo del sistema (meses)')
    plt.ylabel('Densidad')
    plt.legend()
    plt.grid(alpha=0.3)
    
    # Guardo las fotos
    plt.savefig(nombre_archivo)
    plt.close()
    print(f"[*] Gráfico guardado: {nombre_archivo}")

if __name__ == "__main__":
    print("="*60)
    print(f" CORRIENDO MONTE CARLO ({N_SIMULACIONES} simulaciones por escenario)")
    print("="*60)
    
    # ---------------------------------------------------------
    # ESCENARIO BASE: 1 TECNICO, S = 3
    # ---------------------------------------------------------
    tiempos_base = ejecutar_montecarlo(simular_fallo_1_tecnico, n_repuestos=3)
    media_base, desvio_base = calcular_estadisticos(tiempos_base)
    print(f"1. Escenario Base (1 Operario, S=3):")
    print(f"   Media: {media_base:.4f} meses  |  Desvío Estándar: {desvio_base:.4f} meses")
    graficar_histograma_y_ajuste(tiempos_base, "Histograma - Caso Base (1 Op, S=3)", "histogramas_generados/hist_base.png")
    
    # ---------------------------------------------------------
    # ALTERNATIVA A: 2 TECNICOS, S = 3
    # ---------------------------------------------------------
    tiempos_2op = ejecutar_montecarlo(simular_fallo_2_tecnicos, n_repuestos=3)
    media_2op, desvio_2op = calcular_estadisticos(tiempos_2op)
    print(f"\n2. Alternativa A (2 Operarios, S=3):")
    print(f"   Media: {media_2op:.4f} meses  |  Desvío Estándar: {desvio_2op:.4f} meses")
    graficar_histograma_y_ajuste(tiempos_2op, "Histograma - Dos Operarios (S=3)", "histogramas_generados/hist_2op.png")
    
    # ---------------------------------------------------------
    # ALTERNATIVA B: 1 TECNICO, S = 4 (Repuesto Extra)
    # ---------------------------------------------------------
    tiempos_s4 = ejecutar_montecarlo(simular_fallo_1_tecnico, n_repuestos=4)
    media_s4, desvio_s4 = calcular_estadisticos(tiempos_s4)
    print(f"\n3. Alternativa B (1 Operario, S=4 Repuestos):")
    print(f"   Media: {media_s4:.4f} meses  |  Desvío Estándar: {desvio_s4:.4f} meses")
    graficar_histograma_y_ajuste(tiempos_s4, "Histograma - Repuesto Extra (1 Op, S=4)", "histogramas_generados/hist_s4.png")
    
    print("="*60)
    print(" Análisis finalizado. Imágenes generadas (.png) para el informe.")