import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
from distribuciones import generar_dist_uniforme, generar_dist_normal, generar_dist_exponencial
from histograma import generar_histograma
from tabla import generar_tabla

# Función para validar la muestra
def validar_muestra(muestra):
    try:
        muestra = int(muestra)
        if muestra < 1 or muestra > 1000000:
            raise ValueError
        return muestra
    except ValueError:
        messagebox.showerror("Error", "La muestra debe ser un número entero entre 1 y 1,000,000")
        return None

# Función para validar los intervalos
def validar_intervalos(intervalo):
    try:
        intervalo = int(intervalo)
        if intervalo not in [5, 10, 15, 20]:
            raise ValueError
        return intervalo
    except ValueError:
        messagebox.showerror("Error", "El intervalo debe ser uno de los siguientes valores: 5, 10, 15 o 20")
        return None

# Función para validar los parámetros de la distribución
def validar_parametros(tipo):
    if tipo == "Uniforme":
        try:
            a = float(entry_a.get())
            b = float(entry_b.get())
            if b <= a or a <= 0:
                raise ValueError
            return a, b
        except ValueError:
            messagebox.showerror("Error", "a debe ser mayor a 0 y b debe ser mayor que a")
            return None
    elif tipo == "Normal":
        try:
            media = float(entry_media.get())
            desviacion = float(entry_desviacion.get())
            if desviacion <= 0:
                raise ValueError
            return media, desviacion
        except ValueError:
            messagebox.showerror("Error", "La desviación estándar debe ser mayor a 0")
            return None
    elif tipo == "Exponencial":
        try:
            lam = float(entry_lambda.get())
            if lam <= 0:
                raise ValueError
            return lam
        except ValueError:
            messagebox.showerror("Error", "Lambda debe ser mayor a 0")
            return None
    return None

# Función que se ejecuta cuando se presiona el botón "Generar"
def generar():
    muestra = validar_muestra(entry_muestra.get())
    cant_intervalos = validar_intervalos(entry_intervalos.get())

    if muestra and cant_intervalos:
        distribucion = combo_distribucion.get()
        parametros = validar_parametros(distribucion)
        
        if parametros is not None:
            if distribucion == "Uniforme":
                a, b = parametros
                serie = generar_dist_uniforme(muestra, a, b)
                titulo = "Distribucion Uniforme [a, b]"
            
            elif distribucion == "Normal":
                media, desviacion = parametros
                serie = generar_dist_normal(muestra, media, desviacion)
                titulo = "Distribucion Normal"
            
            elif distribucion == "Exponencial":
                lam = parametros
                serie = generar_dist_exponencial(muestra, lam)
                titulo = "Distribucion Exponencial"
            
            # Aquí es donde puedes llamar a funciones adicionales para mostrar la tabla o gráfico
            intervalos, frecObservada = generar_tabla(serie, cant_intervalos)
            #print(serie)
            print(len(serie))
            generar_histograma(serie, titulo, frecObservada, intervalos)
        else:
            messagebox.showerror("Error", "Faltan o son incorrectos los parámetros de la distribución")
    else:
        messagebox.showerror("Error", "Revise los valores de la muestra o los intervalos")


# Crear la ventana principal
root = tk.Tk()
root.title("Generador de Distribuciones")
root.geometry("400x400")

# Crear los widgets de la interfaz
label_muestra = tk.Label(root, text="Tamaño de la muestra (<= 1.000.000):")
label_muestra.pack(pady=5)
entry_muestra = tk.Entry(root)
entry_muestra.pack(pady=5)

label_intervalos = tk.Label(root, text="Intervalos (5, 10, 15, 20):")
label_intervalos.pack(pady=5)
entry_intervalos = tk.Entry(root)
entry_intervalos.pack(pady=5)

label_distribucion = tk.Label(root, text="Selecciona el tipo de distribución:")
label_distribucion.pack(pady=5)

# Crear un combobox para seleccionar la distribución
combo_distribucion = ttk.Combobox(root, values=["Uniforme", "Normal", "Exponencial"], state="readonly")
combo_distribucion.pack(pady=5)

# Contenedor para los parámetros adicionales
frame_parametros = tk.Frame(root)
frame_parametros.pack(pady=10)

# Parámetros para la distribución Uniforme (a y b)
label_a = tk.Label(frame_parametros, text="a (mínimo):")
entry_a = tk.Entry(frame_parametros)

label_b = tk.Label(frame_parametros, text="b (máximo):")
entry_b = tk.Entry(frame_parametros)

# Parámetros para la distribución Normal (media y desviación)
label_media = tk.Label(frame_parametros, text="Media:")
entry_media = tk.Entry(frame_parametros)

label_desviacion = tk.Label(frame_parametros, text="Desviación estándar:")
entry_desviacion = tk.Entry(frame_parametros)

# Parámetro para la distribución Exponencial (lambda)
label_lambda = tk.Label(frame_parametros, text="Lambda:")
entry_lambda = tk.Entry(frame_parametros)

# Función que cambia los campos según la distribución seleccionada
def actualizar_parametros(event):
    for widget in frame_parametros.winfo_children():
        widget.pack_forget()

    tipo = combo_distribucion.get()
    if tipo == "Uniforme":
        label_a.pack(pady=5)
        entry_a.pack(pady=5)
        label_b.pack(pady=5)
        entry_b.pack(pady=5)
    elif tipo == "Normal":
        label_media.pack(pady=5)
        entry_media.pack(pady=5)
        label_desviacion.pack(pady=5)
        entry_desviacion.pack(pady=5)
    elif tipo == "Exponencial":
        label_lambda.pack(pady=5)
        entry_lambda.pack(pady=5)

# Asociar el evento de selección de distribución
combo_distribucion.bind("<<ComboboxSelected>>", actualizar_parametros)

# Botón para generar la distribución
btn_generar = tk.Button(root, text="Generar", command=generar)
btn_generar.pack(pady=10)

# Iniciar el bucle de la interfaz
root.mainloop()
