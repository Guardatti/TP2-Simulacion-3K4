import tkinter as tk
from tkinter import ttk

ventanas_tablas = []

def calcular_datos_cobro(D_inicial, T, C, h):
    """
    Calcula los valores t, D_i, D_i', y D_{i+1} utilizando el método de Euler.
    Retorna una lista con los resultados para cada paso de integración, hasta el tiempo límite calculado.

    Parámetros:
    - D_inicial: Valor inicial de D (180 o 130).
    - T: Constante ingresada como parámetro.
    - C: Cantidad de autos esperando el cobro al inicio.
    - h: Paso de integración en minutos (delta t).

    Retorna:
    - datos: Lista de tuplas con (t, D, derivada, D_siguiente).
    """
    datos = []
    D = D_inicial
    t = 0

    # Calculamos el tiempo límite usando obtener_t_cobro
    tiempo_limite = obtener_t_cobro(D_inicial, T, C, h)
    print(f"Tiempo límite calculado: {tiempo_limite} minutos")

    # Iteramos usando el método de Euler hasta alcanzar el tiempo límite
    while t < tiempo_limite:
        # Calculamos la derivada dD/dt
        derivada = T + 0.2 * (t ** 2) + C
        # Calculamos el nuevo valor D_{i+1}
        D_siguiente = D + h * derivada
        # Guardamos los datos actuales
        datos.append((t, D, derivada, D_siguiente))
        # Actualizamos D y t para el siguiente paso
        D = D_siguiente
        t += h

    # Aseguramos que la última fila se registre al tiempo límite exacto
    if t >= tiempo_limite:
        derivada = T + 0.2 * (tiempo_limite ** 2) + C
        D_siguiente = D + h * derivada
        datos.append((tiempo_limite, D, derivada, D_siguiente))

    return datos

def generar_tabla(Nro_auto, D_inicial, T, C, h):
    datos = calcular_datos_cobro(D_inicial, T, C, h)
    ventana = tk.Toplevel()  # Crear una nueva ventana para cada tabla
    ventana.title(f"Resultados de Cobro para el Auto Nro {Nro_auto}")

    tabla = ttk.Treeview(ventana, columns=("t", "Di", "Di'", "Di+1"), show="headings")
    tabla.heading("t", text="t (min)")
    tabla.heading("Di", text="D_i")
    tabla.heading("Di'", text="D_i'")
    tabla.heading("Di+1", text="D_{i+1}")

    for fila in datos:
        t, Di, derivada, Di_siguiente = fila
        tabla.insert("", tk.END, values=(t, round(Di, 2), round(derivada, 2), round(Di_siguiente, 2)))

    tabla.pack(expand=True, fill="both")
    ventana.state("normal")

    # Almacenar la ventana en la lista
    ventanas_tablas.append(ventana)

def mostrar_todas_las_tablas():
    # Mostrar todas las ventanas al finalizar la simulación
    for ventana in ventanas_tablas:
        ventana.deiconify()

def obtener_t_cobro(D_inicial, T, C, h):
    """
    Calcula el tiempo t en minutos necesario para completar el cobro utilizando el método de Euler.
    
    Parámetros:
    - D_inicial: Valor inicial de D (180 o 130 dependiendo del tipo de auto).
    - T: Constante ingresada como parámetro.
    - C: Cantidad de autos esperando el cobro al inicio.
    - h: Paso de integración en minutos (delta t).
    
    Retorna:
    - El tiempo t en minutos cuando se completa el cobro.
    """
    D = D_inicial
    t = 0

    # Umbral para finalizar el cobro
    umbral = 2 * D_inicial

    # Iteramos usando el método de Euler hasta que D alcance el umbral
    while D < umbral:
        # Calculamos la derivada dD/dt
        derivada = T + 0.2 * (t ** 2) + C
        # Calculamos el nuevo valor D_{i+1}
        D = D + h * derivada
        # Incrementamos el tiempo t
        t += h

    return t

# Ejemplo de uso
Nro_auto = 1
D_inicial = 180  # Por ejemplo, para autos grandes
T = 10
C = 5
h = 1  # Paso de integración en minutos

# generar_tabla(Nro_auto, D_inicial, T, C, h)
