import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

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

        # Agregar datos para cada día
        for dia in range(dia_minimo, dia_maximo + 1):
            # Crear un string de datos de clientes, todos en 0
            datos_clientes = ["0 | 0 | 0" for _ in range(30)]  # 30 clientes con 0 en RND, Demanda y Precio venta

            # Agregar datos a la tabla para el día actual, todos los valores hardcodeados a 0
            tree.insert("", tk.END, values=(
                dia,
                *datos_clientes,
                0,  # Cantidad vendida
                0,  # Stock final
                0,  # Costo producción
                0,  # Ingresos
                0,  # Utilidad
                0   # Promedio pastelitos tirados
            ))

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
