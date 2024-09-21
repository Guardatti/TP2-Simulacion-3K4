import tkinter as tk
from tkinter import messagebox
import random

# Configuración de la demanda y precios
demanda = [1, 2, 5, 6, 7, 8, 10]
probabilidades = [0.1, 0.2, 0.4, 0.1, 0.1, 0.05, 0.05]
precios_venta = [100, 100, 100, 80, 80, 80, 80]

def obtener_demanda(clientes):
    demanda_diaria = []
    for _ in range(clientes):
        r = random.random()
        acumulado = 0
        for i, prob in enumerate(probabilidades):
            acumulado += prob
            if r < acumulado:
                demanda_diaria.append(demanda[i])
                break
    return demanda_diaria

def simular_pastelitos(n_dias):
    pastelitos_producidos = 200
    costo_por_pastelito = 30
    resultados = []

    for _ in range(n_dias):
        clientes = random.randint(10, 30)
        demanda_diaria = obtener_demanda(clientes)
        total_demandado = sum(demanda_diaria)
        
        pastelitos_vendidos = min(total_demandado, pastelitos_producidos)
        pastelitos_sobrantes = pastelitos_producidos - pastelitos_vendidos

        # Calcular utilidad
        utilidad = 0
        for _ in range(pastelitos_vendidos):
            r = random.random()
            acumulado = 0
            for i, prob in enumerate(probabilidades):
                acumulado += prob
                if r < acumulado:
                    utilidad += precios_venta[i]
                    break
        utilidad -= pastelitos_producidos * costo_por_pastelito

        resultados.append((clientes, total_demandado, pastelitos_vendidos, pastelitos_sobrantes, utilidad))

    return resultados

def calcular():
    try:
        n_dias = int(entry_dias.get())
        if n_dias <= 0:
            raise ValueError("El número de días debe ser positivo.")

        resultados = simular_pastelitos(n_dias)
        mostrar_resultados(resultados)

    except ValueError as e:
        messagebox.showerror("Error", str(e))

def mostrar_resultados(resultados):
    for widget in tabla_frame.winfo_children():
        widget.destroy()  # Limpiar tabla anterior

    # Encabezados de la tabla
    headers = ["Clientes", "Demanda Total", "Pastelitos Vendidos", "Pastelitos Sobrantes", "Utilidad"]
    for col, header in enumerate(headers):
        tk.Label(tabla_frame, text=header, borderwidth=2, relief="groove").grid(row=0, column=col)

    # Filas de resultados
    for row, (clientes, demanda_total, vendidos, sobrantes, utilidad) in enumerate(resultados, start=1):
        tk.Label(tabla_frame, text=clientes, borderwidth=1, relief="groove").grid(row=row, column=0)
        tk.Label(tabla_frame, text=demanda_total, borderwidth=1, relief="groove").grid(row=row, column=1)
        tk.Label(tabla_frame, text=vendidos, borderwidth=1, relief="groove").grid(row=row, column=2)
        tk.Label(tabla_frame, text=sobrantes, borderwidth=1, relief="groove").grid(row=row, column=3)
        tk.Label(tabla_frame, text=f"${utilidad:.2f}", borderwidth=1, relief="groove").grid(row=row, column=4)

# Configuración de la interfaz
root = tk.Tk()
root.title("Simulación Vendedor de Pastelitos")

label_dias = tk.Label(root, text="Ingrese el número de días a simular (N):")
label_dias.pack()

entry_dias = tk.Entry(root)
entry_dias.pack()

button_calcular = tk.Button(root, text="Calcular", command=calcular)
button_calcular.pack()

tabla_frame = tk.Frame(root)
tabla_frame.pack()

root.mainloop()