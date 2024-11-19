import tkinter as tk
from tkinter import ttk
from tkinter import Frame, Entry, Label, Button, END
from tkinter import messagebox
from main import *
from euler import *


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

    #print(prob_tipo_auto)
    #print(valores_tipo_auto)
    
    for i,min_a_estacionar in enumerate(valores_tipo_minutos):
        probabilidad = float(entry_probabilidad_minutos[i].get())
        prob_minutos_estacionar.append(probabilidad)

    #print(prob_minutos_estacionar)
    #print(valores_tipo_minutos)

    # Validar que la suma de las probabilidades sea igual a 1
    if (round(sum(prob_tipo_auto), 2) != 1.00) or (round(sum(prob_minutos_estacionar), 2) != 1.00):
        messagebox.showerror("Error", "La suma de las probabilidades debe ser igual a 1")
        return
    
    cantidad_minutos = int(cuadroCantDias.get())
    if cantidad_minutos > 100000:
        messagebox.showerror("Error", "La cantidad de minutos no puede superar los 100.000")
        return
    
    intervalo_final = int(cuadroIntFinal.get())
    if intervalo_final < 0 or intervalo_final > cantidad_minutos:
        messagebox.showerror("Error", "La cantidad de minutos no puede ser menor a 0 y no puede superar a X")
        return

    intervalo_inicial = int(cuadroIntInicial.get())
    if intervalo_inicial > (cantidad_minutos - intervalo_final) or intervalo_final < 0: ##Revisar
        messagebox.showerror("Error", "La cantidad de iteraciones no puede ser mayor a la diferencia entre X y j y mayor a 0")
        return

    #["Pequeños","Grandes","Utilitarios"]
    prob_acumuladas_tipo_auto = calcular_probabilidades_acumuladas(prob_tipo_auto)
    prob_acumuladas_minutos_estacionar = calcular_probabilidades_acumuladas(prob_minutos_estacionar)
    
    #Resto de parametros
    tiempo_entre_llegadas = float(prob_entry_llegada.get()) # 13 minutos
    tiempo_cobro = float(prob_entry_cobro.get()) # 2 minutos
    valor_T = float(parametro_T.get())
    valor_h = float(parametro_h.get())

    '''print(prob_acumuladas_tipo_auto)
    print(prob_acumuladas_minutos_estacionar)
    print(minutos_a_simular)
    print(tiempo_entre_llegadas)
    print(tiempo_cobro)
    print(intervalo_inicial)
    print(intervalo_final)'''
    
    encabezados, grilla = iniciar_simulacion(cantidad_minutos, tiempo_entre_llegadas, tiempo_cobro, valores_tipo_auto, valores_tipo_minutos, prob_acumuladas_tipo_auto, prob_acumuladas_minutos_estacionar, valor_T, valor_h)
    dibujar_grafico(encabezados, grilla, intervalo_final, intervalo_inicial)


# Ventana principal
raiz = tk.Tk()
raiz.title("Grupo 6 - Playa de Estacionamiento")
raiz.geometry("800x700")
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

# Entrada de "Intervalo Final a Mostrar (j)"
cuadroIntFinal = Entry(ventana, font=("Arial bold", 13))
cuadroIntFinal.grid(row=2, column=1)
nombreIntFinal = Label(ventana, text="Minuto Inicial a Mostrar (j):", font=("Arial bold", 13), background=back)
nombreIntFinal.grid(row=2, column=0)

# Entrada de "Intervalo Inicial a Mostrar (i)"
cuadroIntInicial = Entry(ventana, font=("Arial bold", 13))
cuadroIntInicial.grid(row=3, column=1)
nombreIntInicial = Label(ventana, text="Cantidad de Iteraciones (i):", font=("Arial bold", 13), background=back)
nombreIntInicial.grid(row=3, column=0)

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

# Parametros para Euler
nombreEuler = Label(ventana, text="Parámetros para Euler:", font=("Arial bold", 16), background=back)
nombreEuler.grid(row=19, column=0)

# Parametro T
Label(ventana, text="Valor de T: ", font=("Arial", 12), background=back).grid(row=20, column=0, padx=20, pady=5)
parametro_T = Entry(ventana, font=("Arial", 12))
parametro_T.grid(row=20, column=1, padx=10, pady=5)
#parametro_T.insert(0, str(2))  # Valor por defecto

# Parametro h
Label(ventana, text="Valor de h: ", font=("Arial", 12), background=back).grid(row=21, column=0, padx=20, pady=5)
parametro_h = Entry(ventana, font=("Arial", 12))
parametro_h.grid(row=21, column=1, padx=10, pady=5)

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
boton.grid(row=30, column=1, pady=20)

raiz.mainloop()