import math
import matplotlib.pyplot as plt
import scipy.stats as stats
from simulaciones import simular_fallo_1_tecnico, simular_fallo_2_tecnicos

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
    media = sum(tiempos) / n
    varianza = sum((x - media) ** 2 for x in tiempos) / (n - 1)
    desvio = math.sqrt(varianza)
    return media, desvio

def graficar_histograma_y_ajuste(tiempos: list, titulo: str, nombre_archivo: str):
    """Genera el histograma y superpone los ajustes Exponencial y Gamma."""
    media, _ = calcular_estadisticos(tiempos)
    
    # Preparamos el gráfico
    plt.figure(figsize=(8, 5))
    plt.hist(tiempos, bins=40, density=True, alpha=0.6, color='skyblue', edgecolor='white', label='Datos Simulados')
    
    # Ajuste Exponencial (Teorico: lambda = 1 / media)
    x = [i * 0.1 for i in range(int(max(tiempos) * 10) + 1)]
    lamda_est = 1.0 / media
    y_expon = [lamda_est * math.exp(-lamda_est * xi) for xi in x]
    plt.plot(x, y_expon, 'r-', lw=2, label=f'Ajuste Expon(media={media:.2f})')
    
    # Ajuste Gamma usando Scipy
    forma, loc, escala = stats.gamma.fit(tiempos, floc=0)
    y_gamma = stats.gamma.pdf(x, a=forma, loc=loc, scale=escala)
    plt.plot(x, y_gamma, 'g--', lw=2, label=f'Ajuste Gamma(k={forma:.2f})')
    
    plt.title(titulo)
    plt.xlabel('Tiempo de fallo del sistema (meses)')
    plt.ylabel('Densidad')
    plt.legend()
    plt.grid(alpha=0.3)
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