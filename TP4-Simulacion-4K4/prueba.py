import random
import tkinter as tk
from tkinter import ttk

#Función para generar todas las filas de la simulación
#def generar_primer_fila(cant_minutos, t_llegadas, t_cobro, i_inicial, i_final, v_tipo_auto, v_tipo_minutos, v_prob_acum_tipo_auto, v_prob_acum_minutos_estacionar):
def generar_primer_fila():
    # 0 -> Pequeños ; 1 -> Grandes ; 2 -> Utilitarios
    filas = []
    
    encabezado = ["Evento", "Reloj (Min)"]
    encabezado += ["Tiempo Entre Llegadas", "Proxima Llegada", "RND Tipo Vehiculo", "Tipo Vehiculo"] # llegada_vehiculo
    encabezado += ["RND Tiempo Estacionamiento", "Tiempo Estacionamiento", "Hora Finalizacion"] # tiempo_estacionamiento
    encabezado += ["Tiempo de Cobro", "Tiempo Fin de Cobro"] # llegada_tiempo_cobro
    encabezado += ["Estado", "Vehiculo en Zona de Cobro", "Cola"] # zona_de_cobro
    encabezado += ["Sector 1", "Sector 2", "Sector 3", "Sector 4", "Sector 5", "Sector 6", "Sector 7", "Sector 8"] # sectores
    encabezado += ["Cantidad Cobrada", "Ac Recaudacion Playa", "Ac Tiempo de Utilizacion"] # contadores y acumuladores
    encabezado += ["Vehiculo"] #Aca tengo que agregar cada vehiculo que vaya apareciendo en la simulacion
    #encabezado2 = agregar_vehiculo(encabezado)
    return encabezado

def agregar_vehiculo(encabezado):
    return encabezado + ["Vehiculo 2"]

# Función para mostrar la tabla en una ventana de Tkinter
def mostrar_tabla():
    # Crear ventana de Tkinter
    ventana = tk.Tk()
    ventana.title("Simulación - Tabla de Datos")
    ventana.geometry("1200x400")  # Tamaño de la ventana
    
     # Frame para contener el Treeview y las barras de desplazamiento
    frame = tk.Frame(ventana)
    frame.pack(expand=True, fill="both")

    # Generar encabezado
    encabezado = generar_primer_fila()

    # Configurar Treeview
    tree = ttk.Treeview(frame, columns=encabezado, show="headings")
    tree.pack(expand=True, fill="both")

    # Configurar columnas y encabezados
    for col in encabezado:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")

    # Insertar filas de datos de prueba (vacías por el momento)
    for _ in range(10):  # 10 filas de ejemplo
        tree.insert("", "end", values=[1] * len(encabezado))
        
    # Barra de desplazamiento vertical
    scrollbar_y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar_y.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar_y.set)

    # Barra de desplazamiento horizontal
    scrollbar_x = ttk.Scrollbar(ventana, orient="horizontal", command=tree.xview)
    scrollbar_x.pack(side="bottom", fill="x")
    tree.configure(xscrollcommand=scrollbar_x.set)

    # Ejecutar ventana
    ventana.mainloop()
    
def generar_primera_fila():
    return ["Inicializacion", "0.00", 13.00, 13.00, "", "", "", "", "", "", "", "Libre", "", 0, 
            "Libre||", "Libre||", "Libre||", "Libre||", "Libre||", "Libre||", "Libre||", "Libre||",
            0, 0, 0,
            "|"]
    

proximo_evento = ("Sector_1_fin", 13.2)
sectores = [['Ocupado', 1, 73.0], ['Ocupado', 2, 99.0], ['Ocupado', 3, 271.0], ['Libre', '', ''], ['Libre', '', ''], ['Libre', '', ''], ['Libre', '', ''], ['Libre', '', '']]
evento = "Fin Vehiculo " + (str(proximo_evento[0].split("_")[1]))
vehiculo_zcobro = sectores[int(proximo_evento[0].split("_")[1]) - 1][1]
vehiculos = [['Estacionado', 13.0], ['Estacionado', 26.0], ['Estacionado', 52.0], ['Estacionado', 104.0]]
reloj = 73
ac_tiempo_de_utilizacion = 0
ac_tiempo_de_utilizacion += (reloj - int(vehiculos[vehiculo_zcobro - 1][1]))

vehiculos[vehiculo_zcobro - 1] = ["En Cobro", int(vehiculos[vehiculo_zcobro - 1][1])]
print(evento)
print(vehiculo_zcobro)
print(vehiculos)
print(ac_tiempo_de_utilizacion)