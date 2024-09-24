import tkinter as tk
from tkinter import ttk
from tkinter import Frame, Entry, Label, Button, END
import random
from tkinter import messagebox

def truncate(number: float, max_decimals: int) -> float:
    int_part, dec_part = str(number).split(".")
    return float(".".join((int_part, dec_part[:max_decimals])))

# Función para agregar datos a la tabla en tiempo de ejecución
def agregar_datos(grilla, tabla, promedio):
    i = 0
    # Añadir datos desde la tabla
    while i != len(tabla):
        # Combinar los valores de los clientes en una sola cadena [RND; Demanda; PrecioVenta]
        fila = tabla[i][:4]  # Columnas básicas
        for cliente in tabla[i][4:4+30]:  # Para cada cliente
            fila.append(f"[{cliente[0]}; {cliente[1]}; {cliente[2]}]")  # Formatear los datos del cliente
        fila += tabla[i][4+30:]  # Columnas extra
        grilla.insert("", END, values=tuple(fila))
        i += 1

    # Mostrar el promedio en un label (si es necesario)
    nombrePromedio = Label(grilla.master, text="Ganancia promedio: $" + str(truncate(promedio, 2)))
    nombrePromedio.pack()

def crear_tabla(raiz):
    ventana = Frame(raiz)
    ventana.pack(fill="both", expand=True)

    # Columnas básicas (sin la columna de "Iteración")
    columnas_basicas = [
        "Día", "Stock Inicial", "RND Clientes", "Cantidad Clientes"
    ]
    
    # Generar las columnas para cada cliente (una sola columna por cliente con los 3 valores)
    columnas_clientes = []
    for cliente in range(1, 31):  # 30 Clientes
        columnas_clientes.append(f"Cliente {cliente}")

    # Columnas adicionales después de los clientes
    columnas_extra = [
        "Cantidad Vendida", "Stock Final", "Costo Producción", 
        "Ingresos", "Utilidad", "Promedio de Pastelitos Tirados"
    ]

    # Juntar todas las columnas
    columnas_totales = columnas_basicas + columnas_clientes + columnas_extra

    # Crear Treeview sin la columna de ID
    grilla = ttk.Treeview(ventana, columns=tuple(columnas_totales), show="headings")

    # Añadir barra de desplazamiento vertical
    barra_vertical = ttk.Scrollbar(raiz, orient="vertical", command=grilla.yview)
    barra_vertical.pack(side="right", fill="y")
    grilla.configure(yscrollcommand=barra_vertical.set)

    # Añadir barra de desplazamiento horizontal
    barra_horizontal = ttk.Scrollbar(raiz, orient="horizontal", command=grilla.xview)
    barra_horizontal.pack(side="bottom", fill="x")
    grilla.configure(xscrollcommand=barra_horizontal.set)

    # Ajustar el ancho de las columnas
    for col in columnas_totales:
        grilla.column(col, width=150)

    # Añadir encabezados para cada columna
    for col in columnas_totales:
        grilla.heading(col, text=col)

    grilla.pack(fill="both", expand=True)

    return grilla  # Devolvemos la tabla creada para usarla después


# Función para generar todas las filas de la simulación
def generar_simulacion_completa(prob_acumuladas, demandas, precios_unitarios, cantidad_dias):
    filas = []

    # Simulación de cada día
    for dia in range(1, cantidad_dias):
        # Stock inicial (puedes cambiarlo según la lógica de tu simulación)
        stock_inicial = 200

        # Número de clientes en el día
        rnd_clientes = round(random.random(), 2)  # Número aleatorio entre 0 y 1

        # Calcular la cantidad de clientes usando la fórmula
        cantidad_clientes = 10 + rnd_clientes * (20)
        cantidad_clientes = int(cantidad_clientes)  # Convertir a entero, si es necesario

        clientes_datos = []
        for _ in range(cantidad_clientes):
            rnd_demanda = round(random.random(), 2)  # Número aleatorio entre 0 y 1
            # Determinar la demanda y el precio basados en rnd_demanda
            for i, prob in enumerate(prob_acumuladas):
                if rnd_demanda < prob:
                    demanda_cliente = demandas[i]
                    precio_venta_cliente = precios_unitarios[i]
                    break
            # Agregar los datos a la lista de clientes
            clientes_datos.append([rnd_demanda, demanda_cliente, precio_venta_cliente])
        for _ in range (30 - cantidad_clientes):
            # Agregar los datos a la lista de clientes
            clientes_datos.append([0, 0, 0])

            
        # Inicializar cantidad_vendida
        cantidad_vendida = 0

        # Calcular la demanda total y asegurarse de no exceder el stock inicial
        for cliente in clientes_datos:
            demanda_cliente = cliente[1]  # La demanda del cliente es la segunda posición en la lista
            cantidad_vendida += demanda_cliente


        # Asegurarse de que cantidad_vendida no exceda el stock inicial
        cantidad_vendida = min(cantidad_vendida, stock_inicial)  # Asegura que no exceda el stock
        stock_final = stock_inicial - cantidad_vendida  # Stock después de la venta
        costo_produccion = 200 * 30  # Costo de producción (ajustar si es necesario)
        ingresos = cantidad_vendida * random.choice(precios_unitarios)  # Ingresos
        utilidad = ingresos - costo_produccion  # Utilidad
        promedio_pastelitos_tirados = round(stock_final / (cantidad_dias - 1), 3)  # Promedio de stock tirado

        # Armar fila con los datos del día
        fila = [dia, stock_inicial, rnd_clientes, cantidad_clientes]  # Datos iniciales
        fila += clientes_datos  # Añadir los datos de los clientes
        fila += [cantidad_vendida, stock_final, costo_produccion, ingresos, utilidad, promedio_pastelitos_tirados]  # Datos finales

        filas.append(fila)

    return filas


# Función para mostrar solo un rango de la simulación completa
def mostrar_filas_simulacion(tabla_completa, intervalo_inicial, cantidad_filas, intervalo_final):
    # Convertir a enteros los valores de los cuadros de entrada
    intervalo_inicial = int(intervalo_inicial)
    cantidad_filas = int(cantidad_filas)
    intervalo_final = int(intervalo_final)
    
    # Filtrar las filas dentro del intervalo
    filas_a_mostrar = tabla_completa[intervalo_inicial - 1 : intervalo_final -1]

    if intervalo_final <= len(tabla_completa):
        filas_a_mostrar.append(tabla_completa[-1])

    return filas_a_mostrar


# Función principal para ejecutar y mostrar la simulación
def llamar_TP():
    probabilidades = []  # Lista de probabilidades
    demandas = []  # Lista de demandas
    precios_unitarios = []  # Lista de precios

    # Recoger los datos de las entradas
    for i, demanda in enumerate(valores_demanda):
        probabilidad = float(entry_probabilidad[i].get())  # Convertir a float
        precio = int(entry_precio[i].get())
        probabilidades.append(probabilidad)
        precios_unitarios.append(precio)
        demandas.append(demanda)

    # Calcular las probabilidades acumuladas
    prob_acumuladas = calcular_probabilidades_acumuladas(probabilidades)
    
    # Obtener valores de los cuadros de entrada
    cantidad_dias = int(cuadroCantDias.get()) + 1# Simular por todos los días
    if cantidad_dias <= 1:
        messagebox.showerror("Error", "La cantidad de días debe ser mayor a 0")
        return
    
    cantidad_filas = int(cuadroCantFilas.get())  # Cantidad de filas a mostrar
    if cantidad_filas > (cantidad_dias - 1):
        messagebox.showerror("Error", "La cantidad de filas debe ser igual o menor a la cantidad de días")
        return
    
    # Simular todos los días (esto es el proceso completo)
    tabla_completa = generar_simulacion_completa(prob_acumuladas, demandas, precios_unitarios, cantidad_dias)

    intervalo_inicial = int(cuadroIntInicial.get())  # Desde qué fila mostrar
    if intervalo_inicial <= 0 or intervalo_inicial > cantidad_dias:
        messagebox.showerror("Error", "El intervalo inicial debe ser al menos 1 y menor a la cantidad de dias")
        return
    
    intervalo_final = int(cuadroIntFinal.get())
    if intervalo_final < intervalo_inicial:
        messagebox.showerror("Error", "El intervalo final debe ser mayor que el intervalo inicial")
        return
    
    if intervalo_final > cantidad_dias:
        messagebox.showerror("Error", "El intervalo final excede la cantidad de días disponibles")
        return
    
    # Validar que la cantidad de filas a mostrar coincida con el rango
    if (intervalo_final - intervalo_inicial + 1) != cantidad_filas:
        messagebox.showerror("Error", "El intervalo no coincide con la cantidad de filas a mostrar")
        return

    raiz_tabla = tk.Tk()
    raiz_tabla.title("Grupo 6 - Venta Callejera")
    
    # Crear la tabla e inicializar las columnas
    tabla = crear_tabla(raiz_tabla)

    
    # Obtener las filas a mostrar según el intervalo
    filas_a_mostrar = mostrar_filas_simulacion(tabla_completa, intervalo_inicial, cantidad_filas, intervalo_final)
    
    # Agregar las filas filtradas a la tabla en la interfaz
    agregar_datos(tabla, filas_a_mostrar, promedio=0.1)


# Función para calcular probabilidades acumuladas con redondeo
def calcular_probabilidades_acumuladas(probabilidades):
    acumulada = 0
    probabilidades_acumuladas = []
    
    for p in probabilidades:
        acumulada += p
        # Redondear a 2 decimales
        probabilidades_acumuladas.append(round(acumulada, 2))
    
    return probabilidades_acumuladas

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
cuadroCantDias = Entry(ventana, font=("Arial bold", 13))
cuadroCantDias.grid(row=1, column=1)
nombreCantDias = Label(ventana, text="Cantidad de Días a Simular (X):", font=("Arial bold", 13), background=back)
nombreCantDias.grid(row=1, column=0)

# Entrada de "Cantidad de Filas a Mostrar (N)"
cuadroCantFilas = Entry(ventana, font=("Arial bold", 13))
cuadroCantFilas.grid(row=2, column=1)
nombreCantFilas = Label(ventana, text="Cantidad de Filas a Mostrar (N):", font=("Arial bold", 13), background=back)
nombreCantFilas.grid(row=2, column=0)

# Entrada de "Intervalo Inicial a Mostrar (i)"
cuadroIntInicial = Entry(ventana, font=("Arial bold", 13))
cuadroIntInicial.grid(row=3, column=1)
nombreIntInicial = Label(ventana, text="Intervalo Inicial a Mostrar (i):", font=("Arial bold", 13), background=back)
nombreIntInicial.grid(row=3, column=0)

# Entrada de "Intervalo Final a Mostrar (j)"
cuadroIntFinal = Entry(ventana, font=("Arial bold", 13))
cuadroIntFinal.grid(row=4, column=1)
nombreIntFinal = Label(ventana, text="Intervalo Final a Mostrar (j):", font=("Arial bold", 13), background=back)
nombreIntFinal.grid(row=4, column=0)

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
boton = Button(ventana, text="Agregar Datos", font=6, command=llamar_TP, width=15, background="#b0b0b0")
boton.grid(row=14, column=1, pady=20)

raiz.mainloop()
