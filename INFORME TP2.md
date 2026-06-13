# Trabajo Práctico Especial: Problema de Reparación

**Materia:** Modelos y Simulación  
**Facultad:** FaMAF, U.N.C.  
**Integrantes:** 
* Lautaro Ezequiel Deco
* Juan Cruz Hermosilla Artico

---

## 1. Descripción del Problema y Análisis de Carga

El objetivo de este trabajo es simular y analizar la confiabilidad de un sistema de cobro de un supermercado. El sistema cuenta con $N = 7$ cajas registradoras operando en simultáneo y un banco de $S = 3$ máquinas de repuesto para reemplazarlas inmediatamente a medida que se descomponen. 

Contamos con un único técnico en el taller que repara las máquinas de a una por vez en orden de llegada (cola FIFO). Una vez arreglada, la máquina vuelve al banco de repuestos. El **fallo o colapso del sistema** ocurre en el instante exacto en que una caja se rompe y ya no quedan repuestos disponibles; es decir, cuando se acumulan $S + 1 = 4$ máquinas defectuosas en el taller.

Los datos e hipótesis estocásticas del problema son:
* Los tiempos de funcionamiento de las cajas hasta romperse siguen una distribución exponencial con media $T_F = 1$ mes.
* Los tiempos de reparación del técnico también son exponenciales, con media $T_R = 1/8$ de mes.
* Todos los tiempos son independientes entre sí.

### Análisis preliminar
Para entender el sistema antes de simular, podemos hacer un balance promedio de flujos. Como siempre hay 7 cajas andando, el taller recibe en promedio $N \cdot (1/T_F) = 7$ cajas rotas por mes. Por otro lado, el técnico repara a una tasa de $1/T_R = 8$ cajas por mes. 

La utilización teórica del taller es:
$$\rho = \frac{\text{Tasa de llegada}}{\text{Tasa de reparación}} = \frac{7}{8} = 0.875$$

Esto nos dice que el técnico trabaja al $87.5\%$ de su capacidad. Aunque en promedio "da abasto", el margen es muy chico. Debido a la variabilidad aleatoria de las exponenciales, cualquier racha de fallos cercanos o reparaciones largas va a acumular máquinas en el taller muy fácilmente, haciendo que el sistema colapse rápido (basta con juntar 4 rotas). El objetivo del programa es estimar justamente cuánto dura el sistema operativo ($T$) antes de este colapso.

---

## 2. Metodología de Simulación y Variables

Para modelar el problema utilizamos una **Simulación de Eventos Discretos (SED)** con avance de reloj variable. El estado del sistema cambia únicamente cuando ocurre uno de los dos eventos posibles: el fallo de una caja en servicio o el fin de una reparación.

### Variables de Estado y Reloj
* `t`: Reloj de simulación que mide el tiempo transcurrido en meses.
* `r`: Variable de estado contador que mide la cantidad de máquinas descompuestas en el taller en el instante `t`.
* `t_rep`: Instante futuro en el que el técnico terminará la reparación actual ($\infty$ si el taller está vacío).

### Lógica del Algoritmo (Eventos)

El motor de la simulación funciona evaluando constantemente qué evento va a ocurrir primero y actualizando el estado del sistema en consecuencia. El ciclo de vida de cada simulación sigue estos pasos:

1. **Inicialización:**
   Arrancamos en el tiempo $t = 0$ con el taller vacío ($r = 0$) y el técnico libre ($t\_rep = \infty$). Sorteamos los primeros tiempos de falla para las $N=7$ cajas que empiezan funcionando y los guardamos en el Min-Heap.

2. **Bucle Principal:**
   El programa compara el tiempo de la próxima falla (el tope del heap) contra el tiempo en que el técnico terminará su reparación actual ($t\_rep$). El menor de estos dos tiempos dicta cuál es el próximo evento.

3. **Evento A: Falla de una caja**
   * Se avanza el reloj $t$ hasta el instante de la falla y se suma una máquina al taller ($r = r + 1$).
   * **Condición de corte:** Si $r = S + 1 = 4$, significa que no nos quedan repuestos para reemplazar la caja que se acaba de romper. **El sistema colapsa** y la simulación termina devolviendo el tiempo $t$.
   * Si no colapsa, un repuesto entra a funcionar inmediatamente. Sorteamos su futuro tiempo de falla ($t + \mathcal{E}(1/T_F)$) y lo metemos al heap.
   * Si el técnico estaba tomando mate porque el taller estaba vacío ($r = 1$), se pone a trabajar de inmediato y sorteamos el tiempo de esta nueva reparación ($t + \mathcal{E}(1/T_R)$).

4. **Evento B: Fin de una reparación**
   * Se avanza el reloj $t$ hasta el instante en que el técnico termina.
   * La máquina arreglada vuelve al banco de repuestos, por lo que restamos uno a las máquinas rotas ($r = r - 1$).
   * Si todavía quedan máquinas rotas esperando en el taller ($r > 0$), el técnico no descansa e inicia inmediatamente la reparación de la siguiente, sorteando un nuevo tiempo de reparación. Si el taller quedó vacío, el técnico queda libre ($t\_rep = \infty$).
### Justificación del Calendario de Eventos (`heapq`)
A diferencia del enfoque del apunte que rastrea el número individual de cada máquina, en este código aprovechamos la **propiedad de falta de memoria de la distribución exponencial**. Como todas las cajas y repuestos son estadísticamente idénticos e indistinguibles, no hace falta identificar "cuál" máquina se rompió.

Para optimizar el calendario de eventos futuros de fallo, utilizamos una estructura de **Min-Heap** (mediante la librería `heapq` de Python). Esto nos permite mantener ordenados los tiempos de falla de las 7 cajas activas de manera sumamente eficiente. El próximo evento de fallo se encuentra instantáneamente en la posición `0` del heap, y las inserciones de nuevos tiempos cuando entra un repuesto se hacen en tiempo logarítmico ($O(\log N)$), acelerando la ejecución de las miles de simulaciones requeridas.

---

## 3. Diseño Estadístico

Cada corrida de simulación arranca en $t = 0$ con $r = 0$ (todas las cajas sanas) y termina de manera terminante cuando $r = S + 1 = 4$. Al ejecutar este experimento independiente $n = 10000$ veces, obtenemos una muestra de tiempos de colapso $T_1, T_2, \dots, T_n$.

Para describir el comportamiento del sistema, calculamos los siguientes estadísticos muestrales en papel y código:

1. **Tiempo Medio de Fallo ($\overline{T}$):** Estima el valor esperado del tiempo de colapso.
   $$\overline{T} = \frac{1}{n} \sum_{j=1}^{n} T_j$$

2. **Desviación Estándar Muestral ($S_T$):** Mide la dispersión y variabilidad intrínseca del tiempo de fallo del sistema.
   $$S_T = \sqrt{\frac{1}{n-1} \sum_{j=1}^{n} (T_j - \overline{T})^2}$$

3. **Intervalo de Confianza del 95% ($IC_{95\%}$):** Nos da un rango de certeza para el estimador de la media basado en el Teorema Central del Límite, utilizando el error estándar de la media ($S_T / \sqrt{n}$):
   $$IC_{95\%} = \left[ \overline{T} - 1.96 \frac{S_T}{\sqrt{n}} \ ; \ \overline{T} + 1.96 \frac{S_T}{\sqrt{n}} \right]$$