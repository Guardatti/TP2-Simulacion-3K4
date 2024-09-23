import tkinter as tk
from tkinter import Frame, Entry, Label, Button

"""
    prueba.py es un archivo .py que se encarga de la carga de datos en la interfaz y 
    calcula las probabilidades acumuladas de acuerdo con las probabilidades que se carguen en la interfaz
    
    Me falta integrarlo con la tabla que esta en main.py
    Todavia no genera ninguna tabla, pero la idea que a partir de la funcion llamar_TP(), se tomen los datos y se 
    envíen a la funcion encargada de armar la tabla (mañana lo hago)
"""

# Función para calcular probabilidades acumuladas con redondeo
def calcular_probabilidades_acumuladas(probabilidades):
    acumulada = 0
    probabilidades_acumuladas = []
    
    for p in probabilidades:
        acumulada += p
        # Redondear a 2 decimales
        probabilidades_acumuladas.append(round(acumulada, 2))
    
    return probabilidades_acumuladas

# Función que se ejecutará al hacer clic en "Aceptar"
def llamar_TP():
    probabilidades = []  # Lista de probabilidades
    for i, demanda in enumerate(valores_demanda):
        probabilidad = float(entry_probabilidad[i].get())# Convertir a float
        precio = entry_precio[i].get()
        print(f"Demanda: {demanda}, Probabilidad: {probabilidad}, Precio: {precio}")
        probabilidades.append(probabilidad)  # Añadir cada probabilidad a la lista
    
    # Calcular las probabilidades acumuladas
    prob_acumuladas = calcular_probabilidades_acumuladas(probabilidades)
    print("Probabilidades Acumuladas:", prob_acumuladas)

# Ventana principal
raiz = tk.Tk()
raiz.title("Grupo 6 - Venta Callejera")
raiz.geometry("800x500")
ventana = Frame(raiz)
ventana.pack()
raiz.configure(background="#dedede")
back = "#c1c1c1"
ventana.configure(background=back)

nombreTitulo = Label(ventana, text="Carga de Datos:", font=("Arial bold", 20), background=back)
nombreTitulo.grid(row=0, column=0)

# Entrada de "Cantidad de Días a Simular (X)"
cuadroReposicion = Entry(ventana, font=("Arial bold", 13))
cuadroReposicion.grid(row=1, column=1)
nombreReposicion = Label(ventana, text="Cantidad de Días a Simular (X):", font=("Arial bold", 13), background=back)
nombreReposicion.grid(row=1, column=0)

# Entrada de "Cantidad de Filas a Mostrar (N)"
cuadroPedido = Entry(ventana, font=("Arial bold", 13))
cuadroPedido.grid(row=2, column=1)
nombrePedido = Label(ventana, text="Cantidad de Filas a Mostrar (N):", font=("Arial bold", 13), background=back)
nombrePedido.grid(row=2, column=0)

# Entrada de "Intervalo Inicial a Mostrar (i)"
cuadroSimulacion = Entry(ventana, font=("Arial bold", 13))
cuadroSimulacion.grid(row=3, column=1)
nombreSimulacion = Label(ventana, text="Intervalo Inicial a Mostrar (i):", font=("Arial bold", 13), background=back)
nombreSimulacion.grid(row=3, column=0)

# Entrada de "Intervalo Final a Mostrar (j)"
cuadroVto = Entry(ventana, font=("Arial bold", 13))
cuadroVto.grid(row=4, column=1)
nombreVto = Label(ventana, text="Intervalo Final a Mostrar (j):", font=("Arial bold", 13), background=back)
nombreVto.grid(row=4, column=0)

# Valores de demanda, probabilidad y precio por defecto
valores_demanda = [1, 2, 5, 6, 7, 8, 10]
valores_probabilidad = [0.10, 0.20, 0.40, 0.10, 0.10, 0.05, 0.05]
valores_precio = [100, 100, 100, 80, 80, 80, 80]

# Etiquetas para las columnas
Label(ventana, text="Demanda", font=("Arial", 12), background=back).grid(row=5, column=0, padx=10, pady=5)
Label(ventana, text="Probabilidad", font=("Arial", 12), background=back).grid(row=5, column=1, padx=10, pady=5)
Label(ventana, text="Precio por Unidad", font=("Arial", 12), background=back).grid(row=5, column=2, padx=10, pady=5)

# Crear listas para almacenar los campos de probabilidad y precio
entry_probabilidad = []
entry_precio = []

# Crear filas de inputs para cada valor de demanda predefinido
for i, demanda in enumerate(valores_demanda):
    # Mostrar la demanda predefinida en un Label
    label_demanda = Label(ventana, text=str(demanda), font=("Arial", 12), background=back)
    label_demanda.grid(row=i+6, column=0, padx=10, pady=5)
    
    # Crear un Entry para la probabilidad con un valor por defecto
    prob_entry = Entry(ventana, font=("Arial", 12))
    prob_entry.grid(row=i+6, column=1, padx=10, pady=5)
    prob_entry.insert(0, str(valores_probabilidad[i]))  # Valor por defecto
    entry_probabilidad.append(prob_entry)
    
    # Crear un Entry para el precio por unidad con un valor por defecto
    precio_entry = Entry(ventana, font=("Arial", 12))
    precio_entry.grid(row=i+6, column=2, padx=10, pady=5)
    precio_entry.insert(0, str(valores_precio[i]))  # Valor por defecto
    entry_precio.append(precio_entry)

# Botón "Aceptar"
boton = Button(ventana, text="Aceptar", font=6, command=llamar_TP, width=8, background="#b0b0b0")
boton.grid(row=14, column=1, pady=20)

raiz.mainloop()
