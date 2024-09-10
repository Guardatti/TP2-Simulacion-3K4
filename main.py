import matplotlib.pyplot as plt
import random
import math


def validar_opcion():
    op = int(input('Ingrese una opción: 1- Uniforme | 2- Normal | 3- Exponencial | 4- Salír : '))
    print()
    while op < 1 or op > 4:
        print('Ingresó una opción incorrecta \n')
        op = int(input('Ingrese una opción: 1- Uniforme | 2- Normal | 3- Exponencial | 4- Salír: '))
        print()
    return op


def validar_muestra():
    tamaño = int(input('Ingrese un tamaño para la muestra que sea hasta a 1.000.000: '))
    print()
    while tamaño < 1 or tamaño > 1000000:
        print('Ingresó un tamaño no válido \n')
        tamaño = int(input('Ingrese un tamaño para la muestra que sea hasta a 1.000.000: '))
    return tamaño


def validar_intervalos():
    print('Intervalos válidos: 5, 10, 15 o 20')
    intervalo = int(input('Ingrese un intervalo válido: '))
    print()
    while intervalo != 5 and intervalo != 10 and intervalo != 15 and intervalo != 20:
        print('Ingresó un intervalo no válido \n')
        print('Intervalos válidos: 5, 10, 15 o 20')
        intervalo = int(input('Ingrese un intervalo válido: '))
    return intervalo


def validar_b(a):
    b = float(input("Ingresa el valor máximo b: "))
    print()
    while b <= a:
        print('ERROR: b debe ser siempre mayor que a \n')
        b = float(input("Ingresa el valor máximo b: "))
    return b


def validar_desviacion():
    desviacion = float(input("Ingresa el valor de la desviación estándar: "))
    print()
    while desviacion <= 0:
        print('ERROR: la desviacion estandar debe ser mayor a 0 \n')
        desviacion = float(input("Ingresa el valor de la desviación estándar: "))
    return desviacion


def validar_lambda():
    lam_bda = float(input('Ingrese el valor de lambda: '))
    print()
    while lam_bda <= 0:
        print('ERROR: lambda debe ser mayor a 0 \n')
        lam_bda = float(input('Ingrese el valor de lambda: '))
    return lam_bda
         

def generar_uniforme(tamaño_muestra, a, b):
    return [round(a + (b - a) * random.random(), 4) for _ in range(tamaño_muestra)]     # A + (B - A) * RND


def generar_normal(tamaño_muestra, media, desviacion):
    datos = []
    for _ in range(tamaño_muestra):
        rnd1 = random.random()
        rnd2 = random.random()
        n1 = math.sqrt(-2 * math.log(1 - rnd1)) * math.cos(2 * math.pi * rnd2) * desviacion + media      # Raiz(-2 * ln(1-RND1)) * cos(2 * pi * RND2) * Desviación + Media 
        n2 = math.sqrt(-2 * math.log(1 - rnd1)) * math.sin(2 * math.pi * rnd2) * desviacion + media      # Raiz(-2 * ln(1-RND1)) * sen(2 * pi * RND2) * Desviación + Media 
        datos.append(round(n1, 4))
        datos.append(round(n2, 4))
    return datos


def generar_exponencial(tamaño_muestra, lam_bda):
    return [round(- (1/lam_bda) * math.log(1 - random.random()), 4) for _ in range(tamaño_muestra)]     # -(1 / lambda) * ln(1 - RND)


def plot_histograma(datos, intervalos):
    plt.hist(datos, bins=intervalos, edgecolor='black', alpha=0.7)
    plt.xlabel('Valor')
    plt.ylabel('Frecuencia')
    plt.title(f'Histograma con {intervalos} intervalos')
    plt.grid(True)
    plt.show()


def mostrar_frecuencias(datos, intervalos):
    frecuencias, bins, _ = plt.hist(datos, bins=intervalos, edgecolor='black', alpha=0.7)
    plt.close()
    
    print(f'Intervalos con límites inferior y superior: {bins}')
    print()
    print(f'Frecuencias: {frecuencias}')


def main():

    op = -1

    while op != 4:
        
        op = validar_opcion()

        if op == 1:
            tamaño_muestra = validar_muestra()
            print()
            num_intervalos = validar_intervalos()
            print()
            a = float(input("Ingresa el valor mínimo a: "))
            b = validar_b(a)
            datos = generar_uniforme(tamaño_muestra, a, b)
            print()

        elif op == 2:
            tamaño_muestra = validar_muestra()
            print()
            num_intervalos = validar_intervalos()
            print()
            media = float(input("Ingresa la media: "))
            desviacion = validar_desviacion()
            datos = generar_normal(tamaño_muestra, media, desviacion)
            print()

        elif op == 3:
            tamaño_muestra = validar_muestra()
            print()
            num_intervalos = validar_intervalos()
            print()
            lam = validar_lambda()
            datos = generar_exponencial(tamaño_muestra, lam)
            print()
        
        elif op == 4:
            print('Programa finalizado \n')
            break


        plot_histograma(datos, num_intervalos)
        mostrar_frecuencias(datos, num_intervalos)
        print()

if __name__ == "__main__":
    main()