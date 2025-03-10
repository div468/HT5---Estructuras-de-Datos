#Universidad del Valle de Guatemala
#Algoritmos y Estructuras de Datos
#Ing. Douglas Barrios
#@author: Julián Divas, Arodi Chávez, Ronald Catún
#Creación: 25/02/2025
#última modificación: 28/02/2025
#File Name: Simulacion.py
#Descripción: Simulacion DES de un sistema operativo utilizando la clase Resources y Container de SimPy

import simpy
import random
import math

# Función para calcular el promedio manualmente
def calcular_promedio(tiempos):
    if len(tiempos) == 0:
        return 0
    return sum(tiempos) / len(tiempos)

# Función para calcular la desviación estándar manualmente
def calcular_desviacion_estandar(tiempos, promedio):
    if len(tiempos) == 0:
        return 0
    suma_cuadrados = sum((x - promedio) ** 2 for x in tiempos)
    varianza = suma_cuadrados / len(tiempos)
    return math.sqrt(varianza)

# Función para solicitar memoria
def solicitar_memoria(env, nombre, memoria, ram):
    print(f"{nombre} está en NEW, solicitando {memoria} de RAM")
    yield ram.get(memoria)
    print(f"{nombre} obtuvo memoria y está en READY")

# Función para ejecutar instrucciones
def ejecutar_instrucciones(env, nombre, instrucciones, cpu):
    while instrucciones > 0:
        with cpu.request() as req:
            yield req
            print(f"{nombre} está en RUNNING")
            ejecutar = min(3, instrucciones)
            instrucciones -= ejecutar
            yield env.timeout(1)
            print(f"{nombre} ejecutó {ejecutar} instrucciones. Restantes: {instrucciones}")
            
            if instrucciones == 0:
                print(f"{nombre} ha finalizado y pasa a TERMINATED")
                return True
            
            if random.choice([True, False]):
                print(f"{nombre} entra en WAITING (I/O)")
                yield env.timeout(random.randint(1, 3))
                print(f"{nombre} terminó I/O y vuelve a READY")
    return False

# Función para liberar memoria
def liberar_memoria(env, nombre, memoria, ram):
    print(f"{nombre} libera {memoria} de RAM")
    yield ram.put(memoria)

# Función para el proceso completo
def proceso(env, nombre, memoria, instrucciones, ram, cpu, tiempos):
    inicio = env.now
    yield from solicitar_memoria(env, nombre, memoria, ram)
    finalizado = yield from ejecutar_instrucciones(env, nombre, instrucciones, cpu)
    if finalizado:
        yield from liberar_memoria(env, nombre, memoria, ram)
    fin = env.now
    tiempos.append(fin - inicio)

# Función para crear procesos
def crear_procesos(env, total_procesos, ram, cpu, tiempos):
    for i in range(total_procesos):
        yield env.timeout(random.expovariate(1.0 / 10))
        mem_necesaria = random.randint(1, 10)
        instrucciones = random.randint(1, 10)
        env.process(proceso(env, f"Proceso {i + 1}", mem_necesaria, instrucciones, ram, cpu, tiempos))

# Función principal para ejecutar la simulación
def ejecutar_simulacion(total_procesos):
    random.seed(0)
    capacidad_ram = 100 
    cantidad_cpu = 1

    env = simpy.Environment()
    ram = simpy.Container(env, init=capacidad_ram, capacity=capacidad_ram)
    cpu = simpy.Resource(env, capacity=cantidad_cpu)

    tiempos = []
    env.process(crear_procesos(env, total_procesos, ram, cpu, tiempos))
    env.run()

    promedio = calcular_promedio(tiempos)
    desviacion = calcular_desviacion_estandar(tiempos, promedio)
    print(f"\nProcesos: {total_procesos}")
    print(f"Tiempo promedio de los procesos: {promedio:.2f}, Desviación estándar de los procesos: {desviacion:.2f}\n")

ejecutar_simulacion(200)