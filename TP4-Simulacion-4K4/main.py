import random
import tkinter as tk
from tkinter import ttk
import queue

contador_vehiculos = 0


def incrementar_contador():
    global contador_vehiculos
    contador_vehiculos += 1


# Cola para zona de cobro
cola = queue.Queue()


def encolar_elemento(vehiculo):
    global cola
    cola.put(vehiculo)
    print(
        f"{vehiculo} ha llegado. Cola actual: {[elemento for elemento in list(cola.queue)]}"
    )


def hay_elementos_en_cola():
    return not cola.empty()  # True si hay elementos, False si está vacía


def generar_encabezados():
    # 0 -> Pequeños ; 1 -> Grandes ; 2 -> Utilitarios
    encabezado = ["Evento", "Reloj (Min)"]
    encabezado += [
        "Tiempo Entre Llegadas",
        "Proxima Llegada",
        "RND Tipo Vehiculo",
        "Tipo Vehiculo",
    ]  # llegada_vehiculo
    encabezado += [
        "RND Tiempo Estacionamiento",
        "Tiempo Estacionamiento",
        "Hora Finalizacion",
    ]  # tiempo_estacionamiento
    encabezado += ["Tiempo de Cobro", "Tiempo Fin de Cobro"]  # llegada_tiempo_cobro
    encabezado += ["Estado", "Vehiculo en Zona de Cobro", "Cola"]  # zona_de_cobro
    encabezado += [
        "Sector 1",
        "Sector 2",
        "Sector 3",
        "Sector 4",
        "Sector 5",
        "Sector 6",
        "Sector 7",
        "Sector 8",
    ]  # sectores
    encabezado += [
        "Cantidad Cobrada",
        "Ac Recaudacion Playa",
        "Ac Tiempo de Utilizacion",
    ]  # contadores y acumuladores
    # encabezado += ["Vehiculo 1"] #Aca tengo que agregar cada vehiculo que vaya apareciendo en la simulacion
    # encabezado2 = agregar_vehiculo(encabezado)
    return encabezado


def generar_primera_fila():
    return [
        "Inicializacion",
        0.00,
        13.00,
        13.00,
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "Libre",
        "",
        0,
        ["Libre", "", ""],
        ["Libre", "", ""],
        ["Libre", "", ""],
        ["Libre", "", ""],
        ["Libre", "", ""],
        ["Libre", "", ""],
        ["Libre", "", ""],
        ["Libre", "", ""],
        0,
        0,
        0,
        [],
    ]


def agregar_vehiculos(encabezado):
    encabezado.append(["Vehiculo " + str(contador_vehiculos)])
    return encabezado


def obtener_proximo_evento(primera_fila):
    """
    Encuentra el menor valor entre proxima_llegada, t_fin_de_cobro y
    el valor de "hora finalización" en cada sector, y retorna el evento correspondiente.
    """
    # Diccionario para almacenar cada evento y su tiempo
    eventos = {}

    # Asegurarse de que "proxima_llegada" y "t_fin_de_cobro" sean floats
    if primera_fila[3] != "":
        eventos["proxima_llegada"] = float(primera_fila[3])
    if primera_fila[10] != "":
        eventos["t_fin_de_cobro"] = float(primera_fila[10])

    # Agregar cada sector al diccionario con su "hora finalización" (si existe)
    for i, sector in enumerate(primera_fila[14:22], start=1):
        partes = sector
        if (
            len(partes) >= 3 and partes[2]
        ):  # Verificar que exista una tercera parte y no esté vacía
            try:
                hora_finalizacion = float(partes[2])
                eventos[f"sector_{i}_fin"] = hora_finalizacion
            except ValueError:
                pass  # Ignorar valores no convertibles a float

    # Encontrar el evento con el menor valor
    evento_proximo = min(eventos, key=eventos.get)
    tiempo_proximo = eventos[evento_proximo]

    return evento_proximo, tiempo_proximo


def determinar_tipo_vehiculo(rnd_tipo_vehiculo, vec_tipos, vec_valores):
    for i, valor in enumerate(vec_valores):
        if rnd_tipo_vehiculo <= valor:
            return vec_tipos[i]
    return None


def determinar_tiempo_estacionamiento(rnd_tiempo, vec_tiempos, vec_valores):
    for i, valor in enumerate(vec_valores):
        if rnd_tiempo <= valor:
            return vec_tiempos[i]
    return None


def determinar_cobro(t_estacionamiento, tipo_vehiculo):
    if tipo_vehiculo == "Pequeño":
        return t_estacionamiento * 8.33
    elif tipo_vehiculo == "Grande":
        return t_estacionamiento * 25
    else:
        return t_estacionamiento * 50


def primer_sector_libre(sectores):
    for i, sector in enumerate(sectores):
        if sector[0] == "Libre":
            return i
    return None  # Si no hay sectores libres, devuelve None


def truncate(number, decimals=2):
    """
    Trunca un número a un número específico de decimales sin redondear.

    :param number: El número a truncar.
    :param decimals: Número de decimales a conservar.
    :return: El número truncado.
    """
    factor = 10.0**decimals
    return int(number * factor) / factor


def generar_segunda_fila(primera_fila, encabezados):
    """
    Indices que definen los eventos:
    primera_fila[3] -> Proxima Llegada
    primera_fila[10] -> Tiempo Fin de Cobro
    primera_fila[del 14 al 21 inclusive] -> Hora Finalizacion (Sectores)
    """
    # Asignaciones directas de valores individuales
    evento = primera_fila[0]
    reloj = primera_fila[1]
    t_entre_llegadas = primera_fila[2]
    proxima_llegada = primera_fila[3]
    rnd_tipo_vehiculo = primera_fila[4]
    tipo_vehiculo = primera_fila[5]
    rnd_t_estacionamiento = primera_fila[6]
    t_estacionamiento = primera_fila[7]
    hora_finalizacion = primera_fila[8]
    t_cobro = primera_fila[9]
    t_fin_de_cobro = primera_fila[10]
    estado_zcobro = primera_fila[11]
    vehiculo_zcobro = primera_fila[12]
    cola_zcobro = primera_fila[13]

    # Sectores (14 al 21) se dividen en estado, vehículo asociado y hora finalización
    """sector1 = primera_fila[14]
    sector2 = primera_fila[15]
    sector3 = primera_fila[16]
    sector4 = primera_fila[17]
    sector5 = primera_fila[18]
    sector6 = primera_fila[19]
    sector7 = primera_fila[20]
    sector8 = primera_fila[21]"""
    sectores = [
        primera_fila[14],
        primera_fila[15],
        primera_fila[16],
        primera_fila[17],
        primera_fila[18],
        primera_fila[19],
        primera_fila[20],
        primera_fila[21],
    ]

    # Resto de valores
    cantidad_cobrada = primera_fila[22]
    ac_recaudacion_playa = primera_fila[23]
    ac_tiempo_de_utilizacion = primera_fila[24]

    # Vehículo 1, con separación de atributos de "estado" y "hora de llegada"
    vehiculos = primera_fila[25]

    # Buscarmos el proximo evento
    proximo_evento = obtener_proximo_evento(primera_fila)
    # print(proximo_evento)

    if proximo_evento[0] == "proxima_llegada":
        # incrementar_contador()
        posicion_sector_libre = primer_sector_libre(sectores)

        if posicion_sector_libre is not None:
            incrementar_contador()
            siguiente_encabezado = agregar_vehiculos(encabezados)
            evento = "Llegada vehiculo " + str(contador_vehiculos)
            reloj = proximo_evento[1]
            t_entre_llegadas = 13.00
            proxima_llegada = reloj + t_entre_llegadas
            rnd_tipo_vehiculo = truncate(random.random(), 2)
            # rnd_tipo_vehiculo = 0.42
            tipo_vehiculo = determinar_tipo_vehiculo(
                rnd_tipo_vehiculo,
                ["Pequeño", "Grande", "Utilitario"],
                [0.44, 0.69, 0.99],
            )
            rnd_t_estacionamiento = truncate(random.random(), 2)
            # wrnd_t_estacionamiento = 0.33
            t_estacionamiento = determinar_tiempo_estacionamiento(
                rnd_t_estacionamiento, [60, 120, 180, 240], [0.49, 0.79, 0.94, 0.99]
            )
            # print(rnd_t_estacionamiento, t_estacionamiento)
            hora_finalizacion = reloj + t_estacionamiento
            t_cobro = ""
            t_fin_de_cobro = ""
            estado_zcobro = "Libre"
            vehiculo_zcobro = ""
            cola_zcobro = 0
            sectores[posicion_sector_libre] = [
                "Ocupado",
                contador_vehiculos,
                hora_finalizacion,
            ]
            cobro = determinar_cobro(t_estacionamiento, tipo_vehiculo)
            cantidad_cobrada += cobro  ### -> revisar este
            ac_recaudacion_playa += cantidad_cobrada
            vehiculos.append(["Estacionado", proximo_evento[1]])
        else:
            # print("NO HAY SECTORES LIBRES")
            # print(posicion_sector_libre)
            siguiente_encabezado = encabezados
            evento = "Llegada vehiculo " + str(contador_vehiculos)
            reloj = proximo_evento[1]
            t_entre_llegadas = 13
            proxima_llegada = reloj + t_entre_llegadas

    elif proximo_evento[0] == "t_fin_de_cobro":
        siguiente_encabezado = encabezados
        evento = "Fin Cobro " + (str(vehiculo_zcobro))
        reloj = proximo_evento[1]
        t_entre_llegadas = ""
        proxima_llegada = primera_fila[3]
        rnd_tipo_vehiculo = tipo_vehiculo = rnd_t_estacionamiento = (
            t_estacionamiento
        ) = hora_finalizacion = t_cobro = t_fin_de_cobro = ""
        if hay_elementos_en_cola == True:
            vechiculo = cola.get()
            estado_zcobro = "Ocupado"
            vehiculo_zcobro = vechiculo
            cola_zcobro -= 1
            vehiculos[vehiculo_zcobro - 1][0] = "En Cola Cobro"
            t_cobro = 2
            t_fin_de_cobro = reloj + t_cobro
        else:
            estado_zcobro = "Libre"
            # vehiculo_zcobro = ""
            cola_zcobro = 0
            # sectores = sectores
            cantidad_cobrada = 0
        ac_recaudacion_playa += cantidad_cobrada
        # ac_tiempo_de_utilizacion = ac_recaudacion_playa
        vehiculos[vehiculo_zcobro - 1] = ["", ""]
        vehiculo_zcobro = ""

    else:
        if estado_zcobro == "Ocupado":
            siguiente_encabezado = encabezados
            evento = "Fin Sector " + (str(proximo_evento[0].split("_")[1]))
            reloj = proximo_evento[1]
            t_entre_llegadas = ""
            rnd_tipo_vehiculo = tipo_vehiculo = rnd_t_estacionamiento = (
                t_estacionamiento
            ) = hora_finalizacion = ""
            id_vehiculo_cola_cobro = sectores[int(proximo_evento[0].split("_")[1]) - 1][
                1
            ]
            encolar_elemento(id_vehiculo_cola_cobro)
            cola_zcobro += 1
            sectores[int(proximo_evento[0].split("_")[1]) - 1] = ["Libre", "", ""]
            cobro = 0
            cantidad_cobrada = 0
            ac_recaudacion_playa += cantidad_cobrada
            ac_tiempo_de_utilizacion += reloj - int(vehiculos[vehiculo_zcobro - 1][1])
            vehiculos[vehiculo_zcobro - 1] = [
                "En Cola Cobro",
                int(vehiculos[vehiculo_zcobro - 1][1]),
            ]
        else:
            # print(f"Estado de cobro: {estado_zcobro}")
            siguiente_encabezado = encabezados
            evento = "Fin Sector " + (str(proximo_evento[0].split("_")[1]))
            reloj = proximo_evento[1]
            t_entre_llegadas = ""
            proxima_llegada = primera_fila[3]
            rnd_tipo_vehiculo = tipo_vehiculo = rnd_t_estacionamiento = (
                t_estacionamiento
            ) = hora_finalizacion = ""
            t_cobro = 2
            t_fin_de_cobro = reloj + t_cobro
            estado_zcobro = "Ocupado"
            vehiculo_zcobro = sectores[int(proximo_evento[0].split("_")[1]) - 1][1]
            cola_zcobro = 0
            sectores[int(proximo_evento[0].split("_")[1]) - 1] = ["Libre", "", ""]
            cobro = 0
            cantidad_cobrada = 0
            ac_recaudacion_playa += cantidad_cobrada
            # print(vehiculos[vehiculo_zcobro - 2][1])
            ac_tiempo_de_utilizacion += reloj - int(vehiculos[vehiculo_zcobro - 1][1])
            vehiculos[vehiculo_zcobro - 1] = [
                "En Cobro",
                int(vehiculos[vehiculo_zcobro - 1][1]),
            ]

    # Retornar valores o usarlos según el propósito de la función
    return [
        [
            evento,
            reloj,
            t_entre_llegadas,
            proxima_llegada,
            rnd_tipo_vehiculo,
            tipo_vehiculo,
            rnd_t_estacionamiento,
            t_estacionamiento,
            hora_finalizacion,
            t_cobro,
            t_fin_de_cobro,
            estado_zcobro,
            vehiculo_zcobro,
            cola_zcobro,
            sectores[0],
            sectores[1],
            sectores[2],
            sectores[3],
            sectores[4],
            sectores[5],
            sectores[6],
            sectores[7],
            cantidad_cobrada,
            ac_recaudacion_playa,
            ac_tiempo_de_utilizacion,
            vehiculos,
        ],
        proximo_evento[0],
        proximo_evento[1],
        siguiente_encabezado,
    ]


# def iniciar_simulacion(minutos_a_simular, tiempo_entre_llegadas, tiempo_cobro, intervalo_inicial, intervalo_final, valores_tipo_auto, valores_tipo_minutos, prob_acumuladas_tipo_auto, prob_acumuladas_minutos_estacionar):
def iniciar_simulacion():
    grilla = []
    encabezados = generar_encabezados()
    # print('encabezados F1> ', encabezados, end="\n")

    primera_fila = generar_primera_fila()
    # print('primera_fila> ', primera_fila, end="\n")
    grilla.append(primera_fila)

    segunda_fila = generar_segunda_fila(primera_fila, encabezados)
    # print('encabezados F2> ', segunda_fila[3], end="\n")
    # print('segunda_fila> ', segunda_fila[0], end="\n")
    grilla.append(segunda_fila[0])

    minutos_a_simular = 1000
    reloj = segunda_fila[0][1]
    contador_fila = 3
    while reloj <= minutos_a_simular:
        segunda_fila = generar_segunda_fila(segunda_fila[0], segunda_fila[3])
        # print('\nencabezados F', contador_fila, '> ', segunda_fila[3], end="\n")
        # print('Fila ', contador_fila, '> ', segunda_fila[0], end="\n")
        reloj = segunda_fila[0][1]
        contador_fila += 1
        vector_vehiculos = segunda_fila[0][-1]
        fila_vehiculos_aplanada = [sublista for sublista in vector_vehiculos]
        fila_final = segunda_fila[0][:-1] + fila_vehiculos_aplanada
        # Agrega fila_final a la grilla
        grilla.append(fila_final)

    # print(grilla)

    return segunda_fila[3], grilla


def main():
    print("Simulacion Comenzada")

    # Crear ventana de Tkinter
    ventana = tk.Tk()
    ventana.title("Simulación - Sistema de Colas")
    ventana.state("zoomed")

    # Frame para contener el Treeview y las barras de desplazamiento
    frame = tk.Frame(ventana)
    frame.pack(expand=True, fill="both")

    # Generar encabezado
    encabezados, grilla = iniciar_simulacion()

    # Configurar Treeview
    tree = ttk.Treeview(frame, columns=encabezados, show="headings")
    tree.pack(expand=True, fill="both")

    # Configurar columnas y encabezados
    for col in encabezados:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")

    # Barra de desplazamiento vertical
    scrollbar_y = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
    scrollbar_y.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar_y.set)

    # Barra de desplazamiento horizontal
    scrollbar_x = ttk.Scrollbar(tree, orient="horizontal", command=tree.xview)
    scrollbar_x.pack(side="bottom", fill="x")
    tree.configure(xscrollcommand=scrollbar_x.set)

    # Insertar datos de la grilla en el Treeview
    for fila in grilla:
        tree.insert("", "end", values=fila)

    # Ejecutar ventana
    ventana.mainloop()


if __name__ == "__main__":
    main()
