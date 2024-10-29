import tkinter as tk
from tkinter import ttk
from tkinter import Frame, Entry, Label, Button, END
import random
from tkinter import messagebox

# Función para calcular probabilidades acumuladas con redondeo
def calcular_probabilidades_acumuladas(probabilidades):
    acumulada = 0
    probabilidades_acumuladas = []
    
    for p in probabilidades:
        acumulada += p
        # Redondear a 2 decimales
        probabilidades_acumuladas.append(round(acumulada, 2))
    
    return probabilidades_acumuladas

def llamar_TP():
    prob_tipo_auto = []  # Lista de probabilidades del tipo de auto
    prob_minutos_estacionar = [] #Lista de probabilidades de minutos a estacionar

    #Recoger los datos de las entradas
    for i, tipo_auto in enumerate(valores_tipo_auto):
        probabilidad = float(entry_probabilidad_tipo[i].get())
        prob_tipo_auto.append(probabilidad)

    print(prob_tipo_auto)
    print(valores_tipo_auto)
    
    for i,min_a_estacionar in enumerate(valores_tipo_minutos):
        probabilidad = float(entry_probabilidad_minutos[i].get())
        prob_minutos_estacionar.append(probabilidad)

    print(prob_minutos_estacionar)
    print(valores_tipo_minutos)

    # Validar que la suma de las probabilidades sea igual a 1
    if (round(sum(prob_tipo_auto), 2) != 1.00) or (round(sum(prob_minutos_estacionar), 2) != 1.00):
        messagebox.showerror("Error", "La suma de las probabilidades debe ser igual a 1")
        return
    
    cantidad_minutos = float(cuadroCantDias.get())
    if cantidad_minutos > 100000:
        messagebox.showerror("Error", "La cantidad de minutos no puede superar los 100.000")
        return

    intervalo_inicial = int(cuadroIntInicial.get())
    if intervalo_inicial < 0 or intervalo_inicial >= cantidad_minutos: ##Revisar
        messagebox.showerror("Error", "El intervalo inicial tiene que ser mayor a 0 y no puede superar a X")
        return
    
    intervalo_final = int(cuadroIntFinal.get())
    if intervalo_final <= intervalo_inicial or intervalo_final > cantidad_minutos: ##Revisar
        messagebox.showerror("Error", "El intervalo final tiene que ser mayor al intervalo incial y no puede superar a X")
        return

    prob_acumuladas_tipo_auto = calcular_probabilidades_acumuladas(prob_tipo_auto)
    prob_acumuladas_minutos_estacionar = calcular_probabilidades_acumuladas(prob_minutos_estacionar)

    print(prob_acumuladas_tipo_auto)
    print(prob_acumuladas_minutos_estacionar)


# Ventana principal
raiz = tk.Tk()
raiz.title("Grupo 6 - Playa de Estacionamiento")
raiz.geometry("800x630")
ventana = Frame(raiz)
ventana.pack()
raiz.configure(background="#dedede")
back = "#c1c1c1"
ventana.configure(background=back)

nombreTitulo = Label(ventana, text="Carga de Datos:", font=("Arial bold", 20), background=back)
nombreTitulo.grid(row=0, column=0)

# Entrada de "Cantidad de Minutos a Simular (X)"
cuadroCantDias = Entry(ventana, font=("Arial bold", 13))
cuadroCantDias.grid(row=1, column=1)
nombreCantDias = Label(ventana, text="Cantidad de Minutos a Simular (X):", font=("Arial bold", 13), background=back)
nombreCantDias.grid(row=1, column=0)

# Entrada de "Intervalo Inicial a Mostrar (i)"
cuadroIntInicial = Entry(ventana, font=("Arial bold", 13))
cuadroIntInicial.grid(row=2, column=1)
nombreIntInicial = Label(ventana, text="Intervalo Inicial a Mostrar (i):", font=("Arial bold", 13), background=back)
nombreIntInicial.grid(row=2, column=0)

# Entrada de "Intervalo Final a Mostrar (j)"
cuadroIntFinal = Entry(ventana, font=("Arial bold", 13))
cuadroIntFinal.grid(row=3, column=1)
nombreIntFinal = Label(ventana, text="Intervalo Final a Mostrar (j):", font=("Arial bold", 13), background=back)
nombreIntFinal.grid(row=3, column=0)

# Valores de demanda, probabilidad y precio por defecto
valores_tipo_auto = ["Pequeños","Grandes","Utilitarios"]
valores_probabilidad_tipo = [0.45, 0.25,0.30]
valores_tipo_minutos = [60,120,180,240]
valores_probabilidad_minutos = [0.50,0.30,0.15,0.05]

# Primer conjunto de etiquetas
Label(ventana, text="Tipo de Auto", font=("Arial", 12), background=back).grid(row=5, column=0, padx=10, pady=5)
Label(ventana, text="Probabilidad", font=("Arial", 12), background=back).grid(row=5, column=1, padx=10, pady=5)

# Segundo conjunto de etiquetas en una fila diferente
Label(ventana, text="Cant minutos a estacionar", font=("Arial", 12), background=back).grid(row=10, column=0, padx=20, pady=5)
Label(ventana, text="Probabilidad", font=("Arial", 12), background=back).grid(row=10, column=1, padx=20, pady=5)

# Tiempo entre llegada de autos
Label(ventana, text="Tiempo entre llegada de autos (en minutos): ", font=("Arial", 12), background=back).grid(row=17, column=0, padx=20, pady=5)
prob_entry_llegada = Entry(ventana, font=("Arial", 12))
prob_entry_llegada.grid(row=17, column=1, padx=10, pady=5)
prob_entry_llegada.insert(0, str(13))  # Valor por defecto

# Tiempo de cobro
Label(ventana, text="Tiempo de cobro (en minutos): ", font=("Arial", 12), background=back).grid(row=18, column=0, padx=20, pady=5)
prob_entry_cobro = Entry(ventana, font=("Arial", 12))
prob_entry_cobro.grid(row=18, column=1, padx=10, pady=5)
prob_entry_cobro.insert(0, str(2))  # Valor por defecto

# Crear listas para almacenar los campos de probabilidad y precio
entry_probabilidad_tipo = []
entry_probabilidad_minutos = []

# Crear filas de inputs para cada valor de demanda predefinido
for i, demanda in enumerate(valores_tipo_auto):
    # Mostrar la demanda predefinida en un Label
    label_demanda = Label(ventana, text=str(demanda), font=("Arial", 12), background=back)
    label_demanda.grid(row=i+6, column=0, padx=10, pady=5)
    
    # Crear un Entry para la probabilidad con un valor por defecto
    prob_entry = Entry(ventana, font=("Arial", 12))
    prob_entry.grid(row=i+6, column=1, padx=10, pady=5)
    prob_entry.insert(0, str(valores_probabilidad_tipo[i]))  # Valor por defecto
    entry_probabilidad_tipo.append(prob_entry)

for i, demanda in enumerate(valores_tipo_minutos):
    # Mostrar la demanda predefinida en un Label
    label_demanda = Label(ventana, text=str(demanda), font=("Arial", 12), background=back)
    label_demanda.grid(row=i+11, column=0, padx=10, pady=5)
    
    # Crear un Entry para la probabilidad con un valor por defecto
    prob_entry = Entry(ventana, font=("Arial", 12))
    prob_entry.grid(row=i+11, column=1, padx=10, pady=5)
    prob_entry.insert(0, str(valores_probabilidad_minutos[i]))  # Valor por defecto
    entry_probabilidad_minutos.append(prob_entry)

# Botón "Aceptar"
boton = Button(ventana, text="Agregar Datos", font=6, command=llamar_TP, width=15, background="#b0b0b0")
boton.grid(row=20, column=1, pady=20)

raiz.mainloop()
