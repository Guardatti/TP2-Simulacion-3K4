import matplotlib.pyplot as plot

def generar_histograma(serie, distrib, frecuencia, intervalos):
    
    # Esto es para que se siga ejecutando el código mientras está la ventana del histograma abierta
    # plot.ion()
    
    # Extraer los límites de los intervalos
    rango = [intervalo[0] for intervalo in intervalos] + [intervalos[-1][1]]
    rangoLabel = [f"[{intervalo[0]}, {intervalo[1]}]" for intervalo in intervalos]
    
    # Generar el histograma
    n, bins, patches = plot.hist(serie, bins=rango, color="orange", edgecolor="white")
    
    # Añadir las etiquetas de frecuencia en cada barra
    for i in range(len(n)):
        plot.text(bins[i], n[i], str(int(n[i])), ha='left', va='bottom')
    
    # Configuración de etiquetas de los intervalos en el eje X
    plot.xticks(bins, rotation=45)
    plot.title(distrib)
    plot.ylabel("Frecuencia observada")
    plot.xlabel("Intervalos")
    
    plot.show()
