import queue

# Inicializar la cola
cola = queue.Queue()

# Función para simular la llegada de un vehículo
def llegada_vehiculo(vehiculo):
    cola.put(vehiculo)
    print(f"{vehiculo} ha llegado. Cola actual: {[elemento for elemento in list(cola.queue)]}")

# Simulación
llegada_vehiculo("Vehículo 1")
llegada_vehiculo("Vehículo 2")

# Desencolar un vehículo
vehiculo_atendido = cola.get()
print(f"{vehiculo_atendido} ha sido atendido. Cola actual: {[elemento for elemento in list(cola.queue)]}")
