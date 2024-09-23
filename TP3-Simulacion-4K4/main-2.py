import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random

# Función para calcular probabilidades acumuladas con redondeo
def calcular_probabilidades_acumuladas(probabilidades):
    acumulada = 0
    probabilidades_acumuladas = []
    
    for p in probabilidades:
        acumulada += p
        # Redondear a 2 decimales
        probabilidades_acumuladas.append(round(acumulada, 2))
    
    return probabilidades_acumuladas


def simular_dia(probabilidades, precios, num_clientes):
    demanda_total = 0
    for _ in range(num_clientes):
        rnd = random.random()
        demanda = calcular_demanda(probabilidades, rnd)
        demanda_total += demanda
    return demanda_total


def calcular_demanda(probabilidades, rnd):
    probabilidades_acumuladas = calcular_probabilidades_acumuladas(probabilidades)
    for i, prob in enumerate(probabilidades_acumuladas):
        if rnd <= prob:
            return [1, 2, 5, 6, 7, 8, 10][i]
    return 1  # Default, debería nunca llegar aquí.


def simular_dias(n_dias, min_clientes, max_clientes, probabilidades, precios):
    resultados = []
    costo_produccion = 200 * 30  # Costo fijo por día

    for _ in range(n_dias):
        num_clientes = random.randint(min_clientes, max_clientes)
        demanda_total = simular_dia(probabilidades, precios, num_clientes)

        vendidos = min(demanda_total, 200)  # No puede vender más de 200
        sobrantes = 200 - vendidos
        ingresos = sum([precios[i] * [1, 2, 5, 6, 7, 8, 10][i] for i in range(7)])
        utilidad = ingresos - costo_produccion

        resultados.append((vendidos, sobrantes, ingresos, utilidad))

    return resultados

# Función para agregar los datos a la tabla
def agregar_datos():
    try:
        cantidad_dias = int(entry_cantidad_dias.get())
        dia_minimo = int(entry_dia_minimo.get())
        dia_maximo = int(entry_dia_maximo.get())

        # Obtener y validar el vector de probabilidades
        probabilidades = list(map(float, entry_probabilidades.get().split()))
        if len(probabilidades) != 7 or abs(sum(probabilidades) - 1.0) > 1e-6:
            raise ValueError("El vector de probabilidades debe tener longitud 7 y sumar 1.")

        # Obtener el vector de precios de venta
        precios_venta = list(map(float, entry_precios_venta.get().split()))
        if len(precios_venta) != 7:
            raise ValueError("El vector de precios de venta debe tener longitud 7.")

            # Simular días
        resultados = simular_dias(cantidad_dias, dia_minimo, dia_maximo, probabilidades, precios_venta)

        # Agregar resultados a la tabla
        for dia, (vendidos, sobrantes, ingresos, utilidad) in enumerate(resultados, start=dia_minimo):
            tree.insert("", tk.END, values=(
                    dia,
                    *[f"{random.random():.2f} | {vendidos} | {precios_venta[i]}" for i in range(7)],
                    vendidos, sobrantes, 200 * 30, ingresos, utilidad, sobrantes
                ))

            limpiar_entradas()
        # Limpiar entradas
        limpiar_entradas()
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Función para limpiar la tabla y las entradas
def limpiar_todo():
    tree.delete(*tree.get_children())  # Limpiar la tabla
    limpiar_entradas()  # Limpiar las entradas

# Función para limpiar las entradas
def limpiar_entradas():
    entry_cantidad_dias.delete(0, tk.END)
    entry_dia_minimo.delete(0, tk.END)
    entry_dia_maximo.delete(0, tk.END)
    entry_probabilidades.delete(0, tk.END)
    entry_precios_venta.delete(0, tk.END)

# Crear la ventana principal
root = tk.Tk()
root.title("Tabla de Simulación de Pastelitos")

# Crear un Frame para el Treeview y la scrollbar
frame = tk.Frame(root)
frame.pack(expand=True, fill=tk.BOTH)

# Crear un estilo para el Treeview
style = ttk.Style()
style.configure("Treeview", rowheight=25)
style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
style.map("Treeview", background=[('selected', 'lightblue'), ('', 'white')])

# Crear el Treeview
tree = ttk.Treeview(frame, columns=("Día",
                                     *[f"Cliente {i} (RND, Demanda, Precio venta)" for i in range(1, 31)],
                                     "Cantidad vendida", "Stock final", "Costo producción",
                                     "Ingresos", "Utilidad", "Promedio pastelitos tirados"),
                    show='headings', height=15)

# Configurar encabezados
for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=100)

# Agregar scrollbar vertical
scrollbar_y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar_y.set)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

# Agregar scrollbar horizontal
scrollbar_x = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
tree.configure(xscroll=scrollbar_x.set)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

# Empaquetar el Treeview
tree.pack(expand=True, fill=tk.BOTH)

# Asignar el scrollbar horizontal al Treeview
tree.configure(xscrollcommand=scrollbar_x.set)

# Frame para entradas de datos
frame_entrada = tk.Frame(root)
frame_entrada.pack(pady=10)

# Entradas de datos
tk.Label(frame_entrada, text="Cantidad Días:").grid(row=0, column=0)
entry_cantidad_dias = tk.Entry(frame_entrada)
entry_cantidad_dias.grid(row=0, column=1)

tk.Label(frame_entrada, text="Día Mínimo:").grid(row=1, column=0)
entry_dia_minimo = tk.Entry(frame_entrada)
entry_dia_minimo.grid(row=1, column=1)

tk.Label(frame_entrada, text="Día Máximo:").grid(row=2, column=0)
entry_dia_maximo = tk.Entry(frame_entrada)
entry_dia_maximo.grid(row=2, column=1)

tk.Label(frame_entrada, text="Probabilidades (7 valores, suma=1):").grid(row=3, column=0)
entry_probabilidades = tk.Entry(frame_entrada)
entry_probabilidades.grid(row=3, column=1)

tk.Label(frame_entrada, text="Precios de Venta (7 valores):").grid(row=4, column=0)
entry_precios_venta = tk.Entry(frame_entrada)
entry_precios_venta.grid(row=4, column=1)

# Botón para agregar datos
btn_agregar = tk.Button(frame_entrada, text="Agregar Datos", command=agregar_datos)
btn_agregar.grid(row=5, column=0)

# Botón para limpiar todo
btn_limpiar = tk.Button(frame_entrada, text="Limpiar Todo", command=limpiar_todo)
btn_limpiar.grid(row=5, column=1)

# Iniciar el bucle principal
root.mainloop()