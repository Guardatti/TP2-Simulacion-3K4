import math
import tkinter as tk
from tkinter import ttk


def generar_tabla(serie, cant_intervalos):
    archivo = "resultados.txt"
    # Generar intervalos, frecuencias observadas y esperadas
    intervalos = generar_intervalos(serie, cant_intervalos)
    print(intervalos)
    frecObservada = frecuencia_observada(serie, intervalos)
    print(frecObservada)
    
    # Guardar en archivo de texto
    with open(archivo, "w") as f:
        f.write("Serie:\n")
        for i in range(0, len(serie)):
            f.write(f"{serie[i]}\n")
    
    # Mostrar tabla en la interfaz
    mostrar_tabla(intervalos, frecObservada) 

    return intervalos, frecObservada


def mostrar_tabla(intervalos, frec_observada):
    # Crear ventana de la tabla
    tabla_window = tk.Toplevel()
    tabla_window.title("Tabla de Frecuencias")

    # Estilo para la fila de Total
    style = ttk.Style()
    style.configure("Treeview", rowheight=25)
    style.configure("mystyle.Treeview", font=('Helvetica', 10)) 
    style.configure("mystyle.Treeview.Heading", font=('Helvetica', 12, 'bold')) 
    style.configure("Total.Treeview", background="#D3D3D3", font=('Helvetica', 10, 'bold'))  

    # Crear Treeview para mostrar la tabla
    tabla = ttk.Treeview(tabla_window, columns=("Intervalo", "Lim Inf", "Lim Sup", "Frec. Observada"), show="headings", style="mystyle.Treeview")
    tabla.heading("Intervalo", text="Intervalo")
    tabla.heading("Lim Inf", text="Límite Inferior")
    tabla.heading("Lim Sup", text="Límite Superior")
    tabla.heading("Frec. Observada", text="Frecuencia Observada")

    # Ajustar el tamaño de las columnas
    tabla.column("Intervalo", width=100, anchor='center')
    tabla.column("Lim Inf", width=100, anchor='center')
    tabla.column("Lim Sup", width=100, anchor='center')
    tabla.column("Frec. Observada", width=150, anchor='center')

    # Insertar los datos en la tabla
    for i in range(len(intervalos)):
        tabla.insert("", "end", values=(i+1, intervalos[i][0], intervalos[i][1], frec_observada[i]))

    # Calcular el total de la frecuencia observada
    total_frec_observada = sum(frec_observada)

    # Insertar fila de total con un estilo específico
    tabla.insert("", "end", values=("Total", "", "", total_frec_observada), tags=('total',))

    # Aplicar el estilo a la fila "Total"
    tabla.tag_configure('total', background="#D3D3D3")  # Color de fondo más oscuro para la fila "Total"

    # Empaquetar la tabla en la ventana
    tabla.pack(expand=True, fill="both")

    # Agregar un botón para cerrar la ventana
    cerrar_btn = tk.Button(tabla_window, text="Cerrar", command=tabla_window.destroy)
    cerrar_btn.pack(pady=10)


def generar_intervalos(serie, cantidad_intervalos):
    # Evitar sobrescribir las funciones integradas 'min' y 'max'
    max_val = max(serie)
    min_val = min(serie)

    rango = max_val - min_val
    amplitud = rango / cantidad_intervalos

    # Definir los primeros límites
    lim_inf = min_val
    lim_sup = min_val + amplitud
    intervalos = [[round(lim_inf, 4), round(lim_sup, 4)]]

    for i in range(cantidad_intervalos - 1):
        lim_inf += amplitud
        lim_sup += amplitud
        intervalos.append([round(lim_inf, 4), round(lim_sup, 4)])

    # Asegurarse de que el último intervalo incluye el valor máximo de la serie
    intervalos[-1][1] = round(max_val, 4)

    return intervalos


def frecuencia_observada(serie, intervalos):
    v = [0] * len(intervalos)
    for n in serie:
        for j in range(0, len(intervalos)):
            # Para el último intervalo, incluir el valor máximo con <=
            if j == len(intervalos) - 1:
                if n <= intervalos[j][1] and n >= intervalos[j][0]:
                    v[j] += 1
            # Para los otros intervalos, mantener la condición original
            elif n < intervalos[j][1] and n >= intervalos[j][0]:
                v[j] += 1
    return v

