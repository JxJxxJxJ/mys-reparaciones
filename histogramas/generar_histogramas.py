import matplotlib.pyplot as plt
from libreria.distribuciones import pdf_exponencial, pdf_gamma
from libreria.estadisticos import calcular_media_muestral, calcular_varianza_muestral

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