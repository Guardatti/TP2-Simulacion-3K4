import random
import tkinter as tk
from tkinter import *
from tkinter import ttk

def truncate(number: float, max_decimals: int) -> float:
    int_part, dec_part = str(number).split(".")
    return float(".".join((int_part, dec_part[:max_decimals])))


def crear_lista_aleatorios(n):
    i = 0
    lista = []
    while i != n:
        lista.append(truncate(random.random(), 2))
        i = i + 1
    return lista


def mostrar_datos(tabla, promedio):
    i = 0
    raiz = Tk()
    raiz.title("Grupo F - Ejercicio 4 - Montecarlo")

    ventana = Frame(raiz)
    ventana.pack()

    grilla = ttk.Treeview(ventana, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8", "col9"))
    barra = ttk.Scrollbar(raiz, orient="vertical", command=grilla.yview)
    barra.pack(side="right", fill="x")
    raiz.resizable(width=False, height=False)
    grilla.configure(xscrollcommand = barra.set)

    grilla.column("#0", width=150)
    grilla.column("col1", width=150)
    grilla.column("col2", width=150)
    grilla.column("col3", width=150)
    grilla.column("col4", width=150)
    grilla.column("col5", width=150)
    grilla.column("col6", width=150)
    grilla.column("col7", width=150)
    grilla.column("col8", width=150)

    grilla.heading("#0", text="Dias")
    grilla.heading("col1", text="RND Demanda")
    grilla.heading("col2", text="Demanda")
    grilla.heading("col3", text="Q(Stock)")
    grilla.heading("col4", text="Q Resultante")
    grilla.heading("col5", text="Q Recuperado")
    grilla.heading("col6", text="Venta")
    grilla.heading("col7", text="Costo Pedido")
    grilla.heading("col8", text="Total Dia")
    grilla.heading("col9", text="Acumulado")

    grilla.insert("", END, text="0", values=("N/A", "N/A", "0", "0", "0", "N/A", "N/A", "N/A", "N/A"))

    while i != len(tabla):
        grilla.insert("", END, text=str(tabla[i][0]), values=(tabla[i][1], tabla[i][2], tabla[i][3], tabla[i][4], tabla[i][5], tabla[i][6], tabla[i][7], tabla[i][8], tabla[i][9]))
        i = i + 1

    scroll_y = Scrollbar(ventana, orient = "vertical", command=grilla.yview)
    scroll_y.pack(side="right", fill="y")
    grilla.configure(yscrollcommand=scroll_y.set)

    nombrePromedio = Label(ventana, text="Ganancia promedio: $" + str(truncate(promedio, 2)))
    
    grilla.pack(fill="both", expand=True)
    nombrePromedio.pack()
    
    raiz.mainloop()
    return


def tp_tkinter(dias):
    
    if dias == 0:
        mostrar_datos([], 0)
    else:
        tabla = armado_tabla_1(crear_lista_aleatorios(dias), dias) #FUNCIONA
        tabla = armado_tabla_2(tabla, reposicion, vto_, pedido, stock_, costo_, recupero_) #FUNCIONA
        tabla = armado_tabla_3(tabla, precio_, recupero_) #FUNCIONA
        promedio = calcular_ganancia_promedio(tabla)
        mostrar_datos(tabla, promedio)


def armado_tabla_1(aleatorios, simulacion): #ARMADO DE LA TABLA CON LAS COLUMNAS: DIAS, RND, DEMANDA
    i = 0
    demanda = [1, 2, 5, 6, 7, 8, 10]
    probabilidades = [0.1, 0.2, 0.4, 0.1, 0.1, 0.05, 0.05]
    prob_acumuladas = [0.1, 0.3, 0.7, 0.8, 0.9, 0.95, 1]
    fila = []
    tabla = []
    cantidad_demanda = 0
    while i != simulacion:
        for j in prob_acumuladas:
            if j > aleatorios[i]:
                cantidad_demanda = demanda[prob_acumuladas.index(j)]
                break
        fila = [i+1, aleatorios[i], cantidad_demanda, 0, 0, 0, 0, 0, 0, 0]
        tabla.append(fila)
        i += 1
    return tabla


def armado_tabla_2(tabla, reposicion, vto_, pedido, stock_inicial, costo_producto, recupero_): #AGREGA COLUMNAS DE STOCK, STOCK RESULTANTE Y COSTO DE PEDIDO
    reponer_stock = 0
    vto_stock = 0
    i = 0
    qvencida = 0
    while i != len(tabla):
        if i == 0:
            if vto_ != reposicion:
                if vto_/reposicion >= 2:
                    vto_stock = 0
                else:
                    if vto_ == reposicion:
                        vto_stock = 0
                    else:
                        vto_stock += vto_ + i
            tabla[i][3] = stock_inicial
            if (tabla[i][3] - tabla[i][2]) <= 0:
                tabla[i][4] = 0
            else:
                tabla[i][4] = tabla[i][3] - tabla[i][2]
            tabla[i][7] = costo_producto * pedido
            reponer_stock = i + reposicion
        else:
            if i != reponer_stock and i != vto_stock:
                tabla[i][3] = tabla[i - 1][4]
                if (tabla[i][3] - tabla[i][2]) <= 0:
                    tabla[i][4] = 0
                else:
                    tabla[i][4] = tabla[i][3] - tabla[i][2]
                if i % 15 == 0 and recupero_ != 0:
                    tabla[i][5] = tabla[i][4]
                    tabla[i][4] = 0
            else:
                if i == reponer_stock:
                    tabla[i][3] = tabla[i - 1][4] + pedido
                    if (tabla[i][3] - tabla[i][2]) <= 0:
                        tabla[i][4] = 0
                    else:
                        tabla[i][4] = tabla[i][3] - tabla[i][2]
                    tabla[i][7] = costo_producto * pedido
                    reponer_stock = i + reposicion
                    if 1 < vto_/reposicion < 2:
                        qvencida = tabla[i - 1][4]
                    elif 0 < vto_/reposicion < 1:
                        vto_stock = i + vto_
                    if i % 15 == 0 and recupero_ != 0:
                        tabla[i][5] = tabla[i][4]
                        tabla[i][4] = 0
                else:
                    if vto_stock != 0 and i == vto_stock:
                        tabla[i][3] = tabla[i - 1][4]

                        if 0 < vto_/reposicion < 1:
                            if i % 15 == 0 and recupero_ != 0:
                                tabla[i][5] = tabla[i][4]
                            tabla[i][4] = 0

                        else:
                            if qvencida >= tabla[i][3] - tabla[i][2]:
                                if i % 15 == 0 and recupero_ != 0:
                                    tabla[i][5] = tabla[i][4]
                                tabla[i][4] = 0
                            else:
                                tabla[i][4] = tabla[i][3] - qvencida - tabla[i][2]
                                vto_stock = i + reposicion
                                if i % 15 == 0 and recupero_ != 0:
                                    tabla[i][5] = tabla[i][4]
                                    tabla[i][4] = 0

        i = i + 1
    return tabla


def armado_tabla_3(tabla, precio, recupero): #AGREGA COLUMNAS: VENTAS, TOTAL, ACUMULADO, RECUPERO
    i = 0
    while i != len(tabla):

        if (tabla[i][3] - tabla[i][2]) <= 0:
            tabla[i][6] = tabla[i][3] * precio
        else:
            tabla[i][6] = tabla[i][2] * precio

        if i % 15 == 0:
           tabla[i][6] = tabla[i][6] + tabla[i][5] * recupero

        tabla[i][8] = tabla[i][6] - tabla[i][7]

        if i == 0:
            tabla[i][9] = tabla[i][8]
        else:
            tabla[i][9] = tabla[i][8] + tabla[i-1][9]

        i = i + 1

    return tabla


def calcular_ganancia_promedio(tabla):
    i = 0
    promedio = 0
    promedio = tabla[len(tabla)-1][9] / len(tabla)
    return promedio


if __name__ == "__main__":
    tabla = armado_tabla_1(crear_lista_aleatorios(10), 10)
    for fila in tabla:
        print(fila)
    