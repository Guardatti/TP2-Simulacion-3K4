import random
import math

def generar_dist_uniforme(tamaño_muestra, a, b):
    return [round(a + (b - a) * random.random(), 4) for _ in range(tamaño_muestra)] # A + (B - A) * RND

def generar_dist_normal(tamaño_muestra, media, desviacion):
    datos = []
    contador = 0
    for _ in range(tamaño_muestra):
        rnd1 = random.random()
        rnd2 = random.random()    
        if(contador <= tamaño_muestra-2):
            n1 = math.sqrt(-2 * math.log(1 - rnd1)) * math.cos(2 * math.pi * rnd2) * desviacion + media      # Raiz(-2 * ln(1-RND1)) * cos(2 * pi * RND2) * Desviación + Media 
            datos.append(round(n1, 4))
    
            n2 = math.sqrt(-2 * math.log(1 - rnd1)) * math.sin(2 * math.pi * rnd2) * desviacion + media      # Raiz(-2 * ln(1-RND1)) * sen(2 * pi * RND2) * Desviación + Media 
            datos.append(round(n2, 4))
            contador += 2
            if contador == tamaño_muestra:
                break
        else:
            n1 = math.sqrt(-2 * math.log(1 - rnd1)) * math.cos(2 * math.pi * rnd2) * desviacion + media      # Raiz(-2 * ln(1-RND1)) * cos(2 * pi * RND2) * Desviación + Media 
            datos.append(round(n1, 4))
            break
        
    return datos

def generar_dist_exponencial(muestra, lam_bda):
    return [round(- (1/lam_bda) * math.log(1 - random.random()), 4) for _ in range(muestra)]  # -(1 / lambda) * ln(1 - RND)